from __future__ import annotations

import argparse
import cmath
import csv
import hashlib
import importlib.util
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
from scipy.interpolate import AAA


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5266"
WORKERS = SOURCE / "workers"

SCRIPT_5034 = (
    SCRIPTS / "Y5_R2FR_5034_bounded_adaptive_outer_phase_space_smoke.py"
)
SCRIPT_5028 = (
    SCRIPTS / "Y5_R2FR_5028_finite_x_relative_chamber_transport_event.py"
)
SCRIPT_5232 = (
    SCRIPTS
    / "Y5_R2FR_5232_outer_factorization_pole_moment_theorem_and_subtraction_contract.py"
)
SCRIPT_5265 = (
    SCRIPTS / "Y5_R2FR_5265_piecewise_outer_coefficient_reassembly.py"
)
CONFIG_5224 = FUNCTIONAL_RG / "5224" / "frozen_replacement_config.json"
MANIFEST_5239 = (
    FUNCTIONAL_RG / "5239" / "matched_event_A00_job_manifest.json"
)
RESULT_5265 = FUNCTIONAL_RG / "5265" / "piecewise_outer_result.json"
COEFFICIENT_5265 = (
    FUNCTIONAL_RG / "5265" / "piecewise_outer_coefficient.csv"
)
FORMAL_INVENTORY_5252 = (
    FUNCTIONAL_RG
    / "5252"
    / "formalization_workbench_start_inventory.csv"
)

MANIFEST = SOURCE / "soft_energy_pilot_manifest.json"
DRY_RUN = SOURCE / "soft_energy_pilot_dry_run.json"
MEASURE_AUDIT = SOURCE / "soft_energy_measure_audit.csv"
FACTORIZATION = SOURCE / "soft_energy_factorization_witnesses.csv"
ENDPOINTS = SOURCE / "soft_energy_endpoint_scaling.csv"
POLES = SOURCE / "soft_energy_AAA_poles.csv"
QUADRATURE = SOURCE / "soft_energy_subtracted_quadrature.csv"
ORDER_ARTIFACT = SOURCE / "soft_energy_inner_order_artifact.csv"
VALIDATION = SOURCE / "soft_energy_pilot_validation.csv"
RESULT = SOURCE / "soft_energy_pilot_result.json"
STATUS = SOURCE / "status.json"
DOC = POST / "5266-Y5-R2FR-soft-energy-measure-and-energy-first-pilot.md"

CHECKPOINT = 5266
PARENT_CHECKPOINT = 5265
MARKER = "MTS_5266_SOFT_ENERGY_MEASURE_AND_ENERGY_FIRST_PILOT"
REVISION = "soft-energy-measure-energy-first-route-falsification-v2"
EPSILON_VALUES = {"E040": 0.04, "E020": 0.02}
TARGET_REAL = -9.0
ENERGY_SCAN_COUNT = 128
ENERGY_VALIDATION_COUNT = 64
ENERGY_GAUSS_ORDERS = (32, 64)
INNER_RELATIVE_ORDER = 24
INNER_GLOBAL_NODES = 24
INNER_RESIDUE_NODES = 24
INNER_TRACKING_STEPS = 64
AAA_RELATIVE_TOLERANCE = 1.0e-9
AAA_MAXIMUM_TERMS = 60
AAA_VALIDATION_RELATIVE_LIMIT = 0.15
ENERGY_SUBTRACTED_RELATIVE_LIMIT = 0.15
ENDPOINT_POWER_ABSOLUTE_LIMIT = 0.25
FACTORIZATION_SPREAD_MINIMUM = 0.10
MAXIMUM_SELECTED_POLES = 24
ORDER_ARTIFACT_ORDERS = (16, 24, 32)
ORDER_ARTIFACT_ENERGIES = (
    0.49386423085714004,
    0.50613576914286,
    0.5184036114706795,
    0.5306603681511043,
    0.5794290716669306,
)
ORDER_ARTIFACT_RELATIVE_MINIMUM = 0.50
ENDPOINT_DELTAS = (
    1.0e-4,
    2.0e-4,
    4.0e-4,
    8.0e-4,
    1.6e-3,
    3.2e-3,
    6.4e-3,
)
FACTORIZATION_ENERGIES = (0.1, 0.2630569525063038, 0.5, 0.8)
FACTORIZATION_ANGLES = (
    (-0.75, -0.75),
    (-0.4, 0.2),
    (0.0, 0.0),
    (0.35, -0.45),
    (0.75, 0.65),
)


def set_resource_policy() -> None:
    for name in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "BLIS_NUM_THREADS",
    ):
        os.environ[name] = "1"
    try:
        import psutil

        psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    except Exception:
        pass


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
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
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def formal_inventory_digest() -> str:
    rows: list[dict[str, str]] = []
    for path in sorted(
        (item for item in FORMAL.rglob("*") if item.is_file()),
        key=lambda item: str(item).lower(),
    ):
        rows.append(
            {
                "relative_path": str(path.relative_to(FORMAL)),
                "size": str(path.stat().st_size),
                "sha256": digest(path),
            }
        )
    return serialized_hash(rows)


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5034,
        SCRIPT_5028,
        SCRIPT_5232,
        SCRIPT_5265,
        CONFIG_5224,
        MANIFEST_5239,
        RESULT_5265,
        COEFFICIENT_5265,
        FORMAL_INVENTORY_5252,
    )


def target_event() -> dict[str, Any]:
    return dict(read_json(MANIFEST_5239)["target_event"])


def measure_audit_rows() -> list[dict[str, Any]]:
    configuration = read_json(CONFIG_5224)
    rows: list[dict[str, Any]] = []
    for event in configuration["events"]:
        point = [float(value) for value in event["unit_cube_point"]]
        checks = {
            "soft_energy_equals_u0": math.isclose(
                float(event["soft_energy"]),
                point[0],
                rel_tol=0.0,
                abs_tol=2.0e-15,
            ),
            "soft_cosine_equals_2u1_minus_1": math.isclose(
                float(event["soft_cosine"]),
                2.0 * point[1] - 1.0,
                rel_tol=0.0,
                abs_tol=2.0e-15,
            ),
            "decay_cosine_equals_2u2_minus_1": math.isclose(
                float(event["decay_cosine"]),
                2.0 * point[2] - 1.0,
                rel_tol=0.0,
                abs_tol=2.0e-15,
            ),
        }
        rows.append(
            {
                "event_id": event["event_id"],
                "u_energy": point[0],
                "u_soft_angle": point[1],
                "u_decay_angle": point[2],
                "soft_energy": float(event["soft_energy"]),
                "soft_cosine": float(event["soft_cosine"]),
                "decay_cosine": float(event["decay_cosine"]),
                **checks,
                "event_map_passed": all(checks.values()),
                "dx_du_energy": 1.0,
                "dcos_soft_du_soft": 2.0,
                "dcos_decay_du_decay": 2.0,
                "normalized_measure_jacobian": 0.25,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def build_manifest() -> dict[str, Any]:
    parent = read_json(RESULT_5265)
    event = target_event()
    manifest = {
        "marker": f"{MARKER}_MANIFEST",
        "revision": REVISION,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "parent_decision": parent["decision"],
        "parent_fixed_soft_energy": float(event["soft_energy"]),
        "target_event": event,
        "target_argument_real": TARGET_REAL,
        "epsilon_values": EPSILON_VALUES,
        "energy_domain": [0.0, 1.0],
        "measure_contract": {
            "unit_cube_map": (
                "x=u_E, c_soft=2u_soft-1, c_decay=2u_decay-1"
            ),
            "normalized_measure": (
                "du_E du_soft du_decay = "
                "dx (dc_soft/2) (dc_decay/2)"
            ),
            "soft_energy_jacobian": 1.0,
            "angular_jacobian": 0.25,
            "new_fitted_measure_factor": False,
        },
        "energy_first_contract": {
            "regulated_identity": (
                "I_epsilon=(1/4) integral dc_soft dc_decay "
                "integral_0^1 dx F_epsilon"
            ),
            "pole_subtraction": (
                "F=F_reg+sum_j R_j/(x-p_j); "
                "integral pole=R_j[Log(1-p_j)-Log(-p_j)]"
            ),
            "order_exchange_condition": (
                "fixed nonzero Feynman regulator plus bounded endpoint "
                "limits and explicit subtraction of isolated interior poles"
            ),
            "physical_regulator_extrapolation": "2*E020-E040",
            "route_falsification_clause": (
                "If the apparent energy poles or values move materially "
                "with the finite inner contour order, the post-quadrature "
                "energy rule is rejected and energy subtraction moves "
                "inside both contour quadratures."
            ),
        },
        "factorization_witness_energies": list(
            FACTORIZATION_ENERGIES
        ),
        "factorization_witness_angles": [
            {
                "soft_cosine": soft_cosine,
                "decay_cosine": decay_cosine,
            }
            for soft_cosine, decay_cosine in FACTORIZATION_ANGLES
        ],
        "scan_count": ENERGY_SCAN_COUNT,
        "validation_count": ENERGY_VALIDATION_COUNT,
        "gauss_orders": list(ENERGY_GAUSS_ORDERS),
        "inner_order_artifact_orders": list(ORDER_ARTIFACT_ORDERS),
        "inner_order_artifact_energies": list(
            ORDER_ARTIFACT_ENERGIES
        ),
        "inner_settings": {
            "relative_order": INNER_RELATIVE_ORDER,
            "global_nodes": INNER_GLOBAL_NODES,
            "residue_nodes": INNER_RESIDUE_NODES,
            "tracking_steps": INNER_TRACKING_STEPS,
        },
        "resource_contract": {
            "maximum_owned_python_processes": 2,
            "maximum_concurrent_workers": 2,
            "threads_per_worker": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "formalization_workbench_start_digest": (
            formal_inventory_digest()
        ),
        "source_files": [
            {"path": str(path), "sha256": digest(path)}
            for path in source_paths()
        ],
        "claim_boundary": {
            "valid_for_route_falsification": False,
            "valid_for_fixed_angle_energy_pilot": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The pilot tests and may falsify energy integration after "
                "a finite inner contour rule. It does not yet integrate "
                "energy inside the exact contour construction or cover "
                "the complete two-angular domain."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    return manifest


def prepare() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    WORKERS.mkdir(parents=True, exist_ok=True)
    rows = measure_audit_rows()
    manifest = build_manifest()
    checks = {
        "all_sources_exist": all(path.exists() for path in source_paths()),
        "all_source_hashes_present": all(
            len(row["sha256"]) == 64 for row in manifest["source_files"]
        ),
        "parent_5265_accepted": bool(
            read_json(RESULT_5265)["validation_passed"]
        ),
        "unit_cube_event_map_exact": all(
            bool(row["event_map_passed"]) for row in rows
        ),
        "soft_energy_jacobian_is_one": (
            manifest["measure_contract"]["soft_energy_jacobian"] == 1.0
        ),
        "angular_jacobian_is_one_quarter": (
            manifest["measure_contract"]["angular_jacobian"] == 0.25
        ),
        "resource_contract_bounded": (
            manifest["resource_contract"][
                "maximum_owned_python_processes"
            ]
            == 2
            and manifest["resource_contract"]["threads_per_worker"] == 1
        ),
        "higher_claims_locked_false": all(
            not bool(manifest["claim_boundary"][field])
            for field in (
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
    }
    dry = {
        "marker": f"{MARKER}_DRY_RUN",
        "revision": REVISION,
        "dry_run_passed": all(checks.values()),
        "checks": checks,
        "manifest_hash": manifest["manifest_hash"],
        "writes_performed": True,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    if not dry["dry_run_passed"]:
        failed = [key for key, value in checks.items() if not value]
        raise RuntimeError(f"5266 prepare failed: {failed}")
    write_csv(MEASURE_AUDIT, rows)
    atomic_json(MANIFEST, manifest)
    atomic_json(DRY_RUN, dry)
    atomic_json(
        STATUS,
        {
            "marker": MARKER,
            "state": "prepared",
            "completed_workers": 0,
            "total_workers": 2,
            "manifest_hash": manifest["manifest_hash"],
        },
    )
    return dry


def worker_directory(epsilon_id: str) -> Path:
    return WORKERS / epsilon_id


def chebyshev_points(count: int) -> np.ndarray:
    indices = np.arange(count, dtype=float)
    return 0.5 * (
        1.0
        - np.cos(math.pi * (indices + 0.5) / float(count))
    )


def validation_points(count: int) -> np.ndarray:
    golden = (math.sqrt(5.0) - 1.0) / 2.0
    return np.asarray(
        [
            ((index + 0.5) * golden) % 1.0
            for index in range(count)
        ],
        dtype=float,
    )


def endpoint_power(rows: list[dict[str, Any]]) -> float:
    deltas = np.asarray(
        [float(row["endpoint_delta"]) for row in rows],
        dtype=float,
    )
    magnitudes = np.asarray(
        [
            max(
                math.hypot(
                    float(row["value_real"]),
                    float(row["value_imaginary"]),
                ),
                1.0e-300,
            )
            for row in rows
        ],
        dtype=float,
    )
    return float(
        np.polyfit(np.log(deltas), np.log(magnitudes), 1)[0]
    )


def selected_aaa_poles(
    approximant: AAA,
    scale: float,
) -> list[tuple[complex, complex]]:
    poles = np.asarray(approximant.poles(), dtype=np.complex128)
    residues = (
        np.asarray(approximant.residues(), dtype=np.complex128) * scale
    )
    rows: list[tuple[complex, complex]] = []
    for pole, residue in zip(poles, residues):
        if not (
            -0.03 <= pole.real <= 1.03
            and abs(pole.imag) <= 0.20
            and abs(residue) >= 1.0e-10
        ):
            continue
        rows.append((complex(pole), complex(residue)))
    rows.sort(
        key=lambda item: (
            abs(item[0].imag),
            min(abs(item[0].real), abs(1.0 - item[0].real)),
            -abs(item[1]),
        )
    )
    return rows[:MAXIMUM_SELECTED_POLES]


def worker(epsilon_id: str) -> dict[str, Any]:
    set_resource_policy()
    if epsilon_id not in EPSILON_VALUES:
        raise ValueError(f"unsupported regulator {epsilon_id}")
    manifest = read_json(MANIFEST)
    if manifest["manifest_hash"] != serialized_hash(
        {
            key: value
            for key, value in manifest.items()
            if key != "manifest_hash"
        }
    ):
        raise RuntimeError("manifest hash mismatch")
    for row in manifest["source_files"]:
        path = Path(row["path"])
        if not path.exists() or digest(path) != row["sha256"]:
            raise RuntimeError(f"source changed after prepare: {path}")

    output = worker_directory(epsilon_id)
    output.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    module = load_module(
        f"mts_5028_for_5266_{epsilon_id.lower()}",
        SCRIPT_5028,
    )
    epsilon = EPSILON_VALUES[epsilon_id]
    target = complex(TARGET_REAL, epsilon)
    event = manifest["target_event"]
    witness_soft_cosine = float(event["soft_cosine"])
    witness_decay_cosine = float(event["decay_cosine"])
    cache: dict[tuple[float, float, float], complex] = {}
    diagnostic_cache: dict[
        tuple[float, float, float], dict[str, float]
    ] = {}

    def evaluate(
        energy: float,
        soft_cosine: float = witness_soft_cosine,
        decay_cosine: float = witness_decay_cosine,
    ) -> complex:
        key = (
            float(energy),
            float(soft_cosine),
            float(decay_cosine),
        )
        if key not in cache:
            local = module.transported_relative_chambers(
                float(energy),
                float(soft_cosine),
                float(decay_cosine),
                target,
                INNER_RELATIVE_ORDER,
                INNER_GLOBAL_NODES,
                INNER_RESIDUE_NODES,
                INNER_TRACKING_STEPS,
            )
            cache[key] = complex(local["value"])
            diagnostic_cache[key] = {
                "boundary_count": float(local["boundary_count"]),
                "global_correction_evaluations": float(
                    local["global_correction_evaluations"]
                ),
            }
        return cache[key]

    factorization_rows: list[dict[str, Any]] = []
    for angle_index, (
        soft_cosine,
        decay_cosine,
    ) in enumerate(FACTORIZATION_ANGLES):
        for energy in FACTORIZATION_ENERGIES:
            value = evaluate(
                energy,
                soft_cosine,
                decay_cosine,
            )
            factorization_rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "angle_id": f"W{angle_index:02d}",
                    "soft_cosine": soft_cosine,
                    "decay_cosine": decay_cosine,
                    "soft_energy": energy,
                    "value_real": value.real,
                    "value_imaginary": value.imag,
                    "value_magnitude": abs(value),
                    **diagnostic_cache[
                        (energy, soft_cosine, decay_cosine)
                    ],
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )

    order_artifact_rows: list[dict[str, Any]] = []
    maximum_order_artifact_relative_difference = 0.0
    if epsilon_id == "E040":
        values_by_energy: dict[float, dict[int, complex]] = {}
        for energy in ORDER_ARTIFACT_ENERGIES:
            values_by_energy[energy] = {}
            for inner_order in ORDER_ARTIFACT_ORDERS:
                if inner_order == INNER_RELATIVE_ORDER:
                    value = evaluate(energy)
                    diagnostics = diagnostic_cache[
                        (
                            energy,
                            witness_soft_cosine,
                            witness_decay_cosine,
                        )
                    ]
                else:
                    local = module.transported_relative_chambers(
                        energy,
                        witness_soft_cosine,
                        witness_decay_cosine,
                        target,
                        inner_order,
                        inner_order,
                        inner_order,
                        INNER_TRACKING_STEPS,
                    )
                    value = complex(local["value"])
                    diagnostics = {
                        "boundary_count": float(
                            local["boundary_count"]
                        ),
                        "global_correction_evaluations": float(
                            local["global_correction_evaluations"]
                        ),
                    }
                values_by_energy[energy][inner_order] = value
                order_artifact_rows.append(
                    {
                        "epsilon_id": epsilon_id,
                        "soft_energy": energy,
                        "inner_order": inner_order,
                        "value_real": value.real,
                        "value_imaginary": value.imag,
                        "value_magnitude": abs(value),
                        **diagnostics,
                        "valid_for_post_quadrature_energy_rule": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
        for values in values_by_energy.values():
            reference = values[max(ORDER_ARTIFACT_ORDERS)]
            local = max(
                abs(value - reference)
                / max(abs(reference), 1.0e-30)
                for value in values.values()
            )
            maximum_order_artifact_relative_difference = max(
                maximum_order_artifact_relative_difference,
                local,
            )
    else:
        order_artifact_rows.append(
            {
                "epsilon_id": epsilon_id,
                "soft_energy": "",
                "inner_order": "",
                "value_real": "",
                "value_imaginary": "",
                "value_magnitude": "",
                "boundary_count": "",
                "global_correction_evaluations": "",
                "note": "E040-only route-discrimination audit",
                "valid_for_post_quadrature_energy_rule": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )

    endpoint_rows: list[dict[str, Any]] = []
    for endpoint_side in ("ZERO", "ONE"):
        for delta in ENDPOINT_DELTAS:
            energy = delta if endpoint_side == "ZERO" else 1.0 - delta
            value = evaluate(energy)
            endpoint_rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "endpoint_side": endpoint_side,
                    "endpoint_delta": delta,
                    "soft_energy": energy,
                    "value_real": value.real,
                    "value_imaginary": value.imag,
                    "value_magnitude": abs(value),
                    **diagnostic_cache[
                        (
                            energy,
                            witness_soft_cosine,
                            witness_decay_cosine,
                        )
                    ],
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )

    training_coordinates = chebyshev_points(ENERGY_SCAN_COUNT)
    training_values = np.asarray(
        [evaluate(float(value)) for value in training_coordinates],
        dtype=np.complex128,
    )
    scale = max(float(np.max(np.abs(training_values))), 1.0)
    approximant = AAA(
        training_coordinates,
        training_values / scale,
        rtol=AAA_RELATIVE_TOLERANCE,
        max_terms=AAA_MAXIMUM_TERMS,
        clean_up=True,
    )
    independent_coordinates = validation_points(
        ENERGY_VALIDATION_COUNT
    )
    independent_values = np.asarray(
        [evaluate(float(value)) for value in independent_coordinates],
        dtype=np.complex128,
    )
    predictions = np.asarray(
        approximant(independent_coordinates),
        dtype=np.complex128,
    ) * scale
    aaa_relative_error = float(
        np.linalg.norm(predictions - independent_values)
        / max(np.linalg.norm(independent_values), 1.0e-30)
    )
    selected = selected_aaa_poles(approximant, scale)

    scan_rows: list[dict[str, Any]] = []
    for row_type, coordinates, values in (
        ("AAA_TRAINING", training_coordinates, training_values),
        (
            "AAA_INDEPENDENT_VALIDATION",
            independent_coordinates,
            independent_values,
        ),
    ):
        for coordinate, value in zip(coordinates, values):
            prediction = complex(approximant(float(coordinate)) * scale)
            scan_rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "row_type": row_type,
                    "soft_energy": float(coordinate),
                    "value_real": value.real,
                    "value_imaginary": value.imag,
                    "prediction_real": prediction.real,
                    "prediction_imaginary": prediction.imag,
                    "absolute_residual": abs(prediction - value),
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )

    pole_rows: list[dict[str, Any]] = []
    for pole_index, (pole, residue) in enumerate(selected):
        pole_rows.append(
            {
                "epsilon_id": epsilon_id,
                "pole_id": f"{epsilon_id}_P{pole_index:02d}",
                "pole_real": pole.real,
                "pole_imaginary": pole.imag,
                "residue_real": residue.real,
                "residue_imaginary": residue.imag,
                "residue_magnitude": abs(residue),
                "distance_to_real_energy_domain": (
                    abs(pole.imag)
                    if 0.0 <= pole.real <= 1.0
                    else min(abs(pole), abs(pole - 1.0))
                ),
                "extraction_method": "scipy_AAA_regulated_full_cycle",
                "valid_for_fixed_angle_energy_pilot": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )

    quadrature_rows: list[dict[str, Any]] = []
    totals: dict[int, dict[str, complex]] = {}
    analytic_singular = sum(
        (
            residue
            * (cmath.log(1.0 - pole) - cmath.log(-pole))
            for pole, residue in selected
        ),
        0.0j,
    )
    for order in ENERGY_GAUSS_ORDERS:
        nodes, weights = np.polynomial.legendre.leggauss(order)
        coordinates = 0.5 * (nodes + 1.0)
        normalized_weights = 0.5 * weights
        raw_total = 0.0j
        regular_total = 0.0j
        for coordinate, weight in zip(
            coordinates, normalized_weights
        ):
            value = evaluate(float(coordinate))
            singular = sum(
                (
                    residue / (float(coordinate) - pole)
                    for pole, residue in selected
                ),
                0.0j,
            )
            raw_total += float(weight) * value
            regular_total += float(weight) * (value - singular)
        subtracted_total = regular_total + analytic_singular
        totals[order] = {
            "raw": raw_total,
            "regular": regular_total,
            "analytic": analytic_singular,
            "subtracted": subtracted_total,
        }
        quadrature_rows.append(
            {
                "epsilon_id": epsilon_id,
                "gauss_order": order,
                "selected_pole_count": len(selected),
                "raw_integral_real": raw_total.real,
                "raw_integral_imaginary": raw_total.imag,
                "regular_remainder_real": regular_total.real,
                "regular_remainder_imaginary": regular_total.imag,
                "analytic_singular_real": analytic_singular.real,
                "analytic_singular_imaginary": analytic_singular.imag,
                "subtracted_integral_real": subtracted_total.real,
                "subtracted_integral_imaginary": (
                    subtracted_total.imag
                ),
                "valid_for_fixed_angle_energy_pilot": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )

    low = totals[ENERGY_GAUSS_ORDERS[0]]
    high = totals[ENERGY_GAUSS_ORDERS[1]]
    raw_relative = abs(low["raw"] - high["raw"]) / max(
        abs(high["raw"]), 1.0e-30
    )
    subtracted_relative = abs(
        low["subtracted"] - high["subtracted"]
    ) / max(abs(high["subtracted"]), 1.0e-30)
    zero_rows = [
        row for row in endpoint_rows if row["endpoint_side"] == "ZERO"
    ]
    one_rows = [
        row for row in endpoint_rows if row["endpoint_side"] == "ONE"
    ]
    zero_power = endpoint_power(zero_rows)
    one_power = endpoint_power(one_rows)
    worker_passed = (
        math.isfinite(aaa_relative_error)
        and aaa_relative_error <= AAA_VALIDATION_RELATIVE_LIMIT
        and len(selected) > 0
        and subtracted_relative <= ENERGY_SUBTRACTED_RELATIVE_LIMIT
        and abs(zero_power) <= ENDPOINT_POWER_ABSOLUTE_LIMIT
        and abs(one_power) <= ENDPOINT_POWER_ABSOLUTE_LIMIT
    )
    result = {
        "marker": f"{MARKER}_{epsilon_id}",
        "revision": REVISION,
        "epsilon_id": epsilon_id,
        "epsilon_value": epsilon,
        "manifest_hash": manifest["manifest_hash"],
        "worker_passed": worker_passed,
        "aaa_support_count": len(approximant.support_points),
        "aaa_validation_relative_error": aaa_relative_error,
        "selected_pole_count": len(selected),
        "zero_endpoint_power": zero_power,
        "one_endpoint_power": one_power,
        "raw_order32_to64_relative_difference": raw_relative,
        "subtracted_order32_to64_relative_difference": (
            subtracted_relative
        ),
        "maximum_inner_order_artifact_relative_difference": (
            maximum_order_artifact_relative_difference
        ),
        "post_quadrature_order_artifact_detected": (
            epsilon_id == "E040"
            and maximum_order_artifact_relative_difference
            >= ORDER_ARTIFACT_RELATIVE_MINIMUM
        ),
        "order64_raw_integral": complex_row(high["raw"]),
        "order64_subtracted_integral": complex_row(
            high["subtracted"]
        ),
        "function_evaluation_count": len(cache),
        "maximum_boundary_count": max(
            value["boundary_count"]
            for value in diagnostic_cache.values()
        ),
        "maximum_global_correction_evaluations": max(
            value["global_correction_evaluations"]
            for value in diagnostic_cache.values()
        ),
        "elapsed_seconds": time.perf_counter() - started,
        "valid_for_fixed_angle_energy_pilot": worker_passed,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_csv(output / "factorization_witnesses.csv", factorization_rows)
    write_csv(output / "endpoint_scaling.csv", endpoint_rows)
    write_csv(output / "energy_scan.csv", scan_rows)
    write_csv(output / "AAA_poles.csv", pole_rows or [{
        "epsilon_id": epsilon_id,
        "pole_id": "NONE",
        "extraction_method": "scipy_AAA_regulated_full_cycle",
        "valid_for_fixed_angle_energy_pilot": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }])
    write_csv(output / "subtracted_quadrature.csv", quadrature_rows)
    write_csv(
        output / "inner_order_artifact.csv",
        order_artifact_rows,
    )
    atomic_json(output / "worker_result.json", result)
    return result


def worker_result(epsilon_id: str) -> dict[str, Any]:
    path = worker_directory(epsilon_id) / "worker_result.json"
    if not path.exists():
        raise RuntimeError(f"missing worker result: {epsilon_id}")
    return read_json(path)


def aggregate_factorization_rows() -> tuple[
    list[dict[str, Any]], float
]:
    by_regulator = {
        epsilon_id: read_csv(
            worker_directory(epsilon_id)
            / "factorization_witnesses.csv"
        )
        for epsilon_id in EPSILON_VALUES
    }
    lookup: dict[
        tuple[str, str, float], dict[str, str]
    ] = {}
    for epsilon_id, rows in by_regulator.items():
        for row in rows:
            lookup[
                (
                    epsilon_id,
                    row["angle_id"],
                    float(row["soft_energy"]),
                )
            ] = row
    result: list[dict[str, Any]] = []
    ratios_by_energy: dict[float, list[complex]] = {
        energy: [] for energy in FACTORIZATION_ENERGIES
    }
    reference_energy = FACTORIZATION_ENERGIES[1]
    for angle_index, (
        soft_cosine,
        decay_cosine,
    ) in enumerate(FACTORIZATION_ANGLES):
        angle_id = f"W{angle_index:02d}"
        physical: dict[float, complex] = {}
        for energy in FACTORIZATION_ENERGIES:
            e40 = lookup[("E040", angle_id, energy)]
            e20 = lookup[("E020", angle_id, energy)]
            value40 = complex(
                float(e40["value_real"]),
                float(e40["value_imaginary"]),
            )
            value20 = complex(
                float(e20["value_real"]),
                float(e20["value_imaginary"]),
            )
            physical[energy] = 2.0 * value20 - value40
        reference = physical[reference_energy]
        for energy, value in physical.items():
            ratio = value / reference if abs(reference) > 1.0e-30 else 0.0j
            ratios_by_energy[energy].append(ratio)
            result.append(
                {
                    "angle_id": angle_id,
                    "soft_cosine": soft_cosine,
                    "decay_cosine": decay_cosine,
                    "soft_energy": energy,
                    "physical_value_real": value.real,
                    "physical_value_imaginary": value.imag,
                    "ratio_to_parent_energy_real": ratio.real,
                    "ratio_to_parent_energy_imaginary": ratio.imag,
                    "valid_for_common_energy_factorization": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    spreads = []
    for energy, ratios in ratios_by_energy.items():
        if energy == reference_energy:
            continue
        center = sum(ratios, 0.0j) / len(ratios)
        spreads.append(
            max(abs(value - center) for value in ratios)
            / max(abs(center), 1.0e-30)
        )
    return result, max(spreads)


def aggregate_worker_csv(filename: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for epsilon_id in EPSILON_VALUES:
        rows.extend(read_csv(worker_directory(epsilon_id) / filename))
    return rows


def write_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5266 — Soft-energy measure and energy-first pilot",
        "",
        "## Derived measure",
        "",
        (
            "The parent Sobol generator owns the exact map "
            "`x=u_E`, `c_s=2u_s-1`, `c_d=2u_d-1`. Therefore"
        ),
        "",
        "`du_E du_s du_d = dx (dc_s/2) (dc_d/2)`,",
        "",
        (
            "so the soft-energy Jacobian is exactly one and the only "
            "remaining coordinate factor is the already used angular "
            "Jacobian `1/4`. No energy weight has been fitted."
        ),
        "",
        "## Route tested",
        "",
        (
            "At fixed nonzero Feynman regulator the pilot changes the "
            "order of integration: it integrates the finite-plus kernel "
            "over `x` first at one angular witness. Every AAA-extracted "
            "interior pole is removed as `R/(x-p)` and restored with "
            "`R[Log(1-p)-Log(-p)]`."
        ),
        "",
        "## Results",
        "",
        (
            f"- E040 post-quadrature integral gate passed: "
            f"`{result['workers']['E040']['worker_passed']}`."
        ),
        (
            f"- E020 post-quadrature integral gate passed: "
            f"`{result['workers']['E020']['worker_passed']}`."
        ),
        (
            f"- Common energy factorization rejected: "
            f"`{result['common_energy_factorization_rejected']}`."
        ),
        (
            f"- Maximum normalized ratio spread: "
            f"`{result['maximum_factorization_ratio_spread']}`."
        ),
        (
            f"- Maximum inner-order artifact: "
            f"`{result['maximum_inner_order_artifact_relative_difference']}`."
        ),
        (
            f"- Post-quadrature energy route rejected: "
            f"`{result['post_quadrature_energy_route_rejected']}`."
        ),
        "",
        "## Claim boundary",
        "",
        (
            "The candidate fixed-angle integral is explicitly invalid: "
            "its global AAA continuation and 32/64 Gauss values do not "
            "converge, and the apparent pole ladder moves with finite "
            "inner contour order. Numeric UV, local GR and full-MTS "
            "claim flags remain false."
        ),
        "",
        "## Next target",
        "",
        (
            "Move the energy integration and pole subtraction inside "
            "the relative/global contour quadratures. Derive the local "
            "energy-pole residue before applying any finite contour-node "
            "rule, then test convergence under simultaneous energy and "
            "contour refinement."
        ),
        "",
    ]
    atomic_text(DOC, "\n".join(lines))


def aggregate() -> dict[str, Any]:
    manifest = read_json(MANIFEST)
    workers = {
        epsilon_id: worker_result(epsilon_id)
        for epsilon_id in EPSILON_VALUES
    }
    factorization_rows, maximum_spread = (
        aggregate_factorization_rows()
    )
    endpoint_rows = aggregate_worker_csv("endpoint_scaling.csv")
    pole_rows = aggregate_worker_csv("AAA_poles.csv")
    quadrature_rows = aggregate_worker_csv("subtracted_quadrature.csv")
    common_factorization_rejected = (
        maximum_spread >= FACTORIZATION_SPREAD_MINIMUM
    )
    e40 = workers["E040"]["order64_subtracted_integral"]
    e20 = workers["E020"]["order64_subtracted_integral"]
    integral40 = complex(
        float(e40["real"]), float(e40["imaginary"])
    )
    integral20 = complex(
        float(e20["real"]), float(e20["imaginary"])
    )
    physical_integral = 2.0 * integral20 - integral40
    maximum_order_artifact = float(
        workers["E040"][
            "maximum_inner_order_artifact_relative_difference"
        ]
    )
    order_artifact_detected = (
        maximum_order_artifact
        >= ORDER_ARTIFACT_RELATIVE_MINIMUM
    )
    formal_end = formal_inventory_digest()
    formal_unchanged = (
        formal_end
        == manifest["formalization_workbench_start_digest"]
    )
    workers_completed = all(
        int(value["function_evaluation_count"]) > 0
        and math.isfinite(
            float(value["aaa_validation_relative_error"])
        )
        and int(value["selected_pole_count"]) > 0
        for value in workers.values()
    )
    candidate_integral_failed = not all(
        bool(value["worker_passed"]) for value in workers.values()
    )
    route_rejected = (
        workers_completed
        and common_factorization_rejected
        and order_artifact_detected
        and candidate_integral_failed
        and formal_unchanged
    )
    validation_definitions = [
        (
            "SOURCE_PATHS_EXIST_AND_MATCH",
            all(
                Path(row["path"]).exists()
                and digest(Path(row["path"])) == row["sha256"]
                for row in manifest["source_files"]
            ),
            len(manifest["source_files"]),
            "all manifest sources and hashes",
        ),
        (
            "SOFT_ENERGY_MEASURE_IS_PARENT_OWNED",
            all(
                parse_bool(row["event_map_passed"])
                for row in read_csv(MEASURE_AUDIT)
            ),
            "x=u_E; energy Jacobian=1",
            "all source events satisfy the exact map",
        ),
        (
            "BOTH_REGULATOR_WORKERS_COMPLETE",
            workers_completed,
            {
                key: value["function_evaluation_count"]
                for key, value in workers.items()
            },
            "both positive and finite",
        ),
        (
            "COMMON_ENERGY_FACTORIZATION_REJECTED",
            common_factorization_rejected,
            maximum_spread,
            f">={FACTORIZATION_SPREAD_MINIMUM}",
        ),
        (
            "FINITE_INNER_ORDER_ARTIFACT_DETECTED",
            order_artifact_detected,
            maximum_order_artifact,
            f">={ORDER_ARTIFACT_RELATIVE_MINIMUM}",
        ),
        (
            "NONCONVERGED_CANDIDATE_INTEGRAL_NOT_CLAIMED",
            candidate_integral_failed,
            {
                key: value["worker_passed"]
                for key, value in workers.items()
            },
            "at least one false; fixed-angle integral flag false",
        ),
        (
            "ENDPOINTS_FINITE_AT_FIXED_WITNESS",
            all(
                abs(float(worker["zero_endpoint_power"]))
                <= ENDPOINT_POWER_ABSOLUTE_LIMIT
                and abs(float(worker["one_endpoint_power"]))
                <= ENDPOINT_POWER_ABSOLUTE_LIMIT
                for worker in workers.values()
            ),
            {
                key: [
                    value["zero_endpoint_power"],
                    value["one_endpoint_power"],
                ]
                for key, value in workers.items()
            },
            f"absolute power <= {ENDPOINT_POWER_ABSOLUTE_LIMIT}",
        ),
        (
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            formal_unchanged,
            formal_end,
            manifest["formalization_workbench_start_digest"],
        ),
        (
            "HIGHER_CLAIMS_REMAIN_FALSE",
            route_rejected,
            {
                "fixed_angle_energy_pilot": False,
                "numeric_UV": False,
                "local_GR": False,
                "full_MTS": False,
            },
            "all false",
        ),
    ]
    validation_rows = [
        {
            "gate": gate,
            "passed": passed,
            "observed": json.dumps(observed, sort_keys=True),
            "required": json.dumps(required, sort_keys=True),
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for gate, passed, observed, required in validation_definitions
    ]
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "manifest_hash": manifest["manifest_hash"],
        "integrity_passed": all(
            bool(row["passed"]) for row in validation_rows
        ),
        "acceptance_passed": route_rejected,
        "decision": (
            "REJECT_POST_QUADRATURE_ENERGY_RULE__"
            "MOVE_ENERGY_SUBTRACTION_INSIDE_BOTH_CONTOURS"
            if route_rejected
            else "HOLD_ROUTE_FALSIFICATION__REPAIR_FAILED_GATES"
        ),
        "measure_contract": manifest["measure_contract"],
        "workers": workers,
        "common_energy_factorization_rejected": (
            common_factorization_rejected
        ),
        "maximum_factorization_ratio_spread": maximum_spread,
        "invalid_candidate_fixed_angle_energy_integral_real": (
            physical_integral.real
        ),
        "invalid_candidate_fixed_angle_energy_integral_imaginary": (
            physical_integral.imag
        ),
        "candidate_fixed_angle_energy_integral_valid": False,
        "maximum_inner_order_artifact_relative_difference": (
            maximum_order_artifact
        ),
        "post_quadrature_energy_route_rejected": route_rejected,
        "formalization_workbench_start_digest": manifest[
            "formalization_workbench_start_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0 if formal_unchanged else -1
        ),
        "valid_for_route_falsification": route_rejected,
        "valid_for_fixed_angle_energy_pilot": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            "derive energy-pole subtraction inside the relative and "
            "global contour quadratures"
        ),
    }
    write_csv(FACTORIZATION, factorization_rows)
    write_csv(ENDPOINTS, endpoint_rows)
    write_csv(POLES, pole_rows)
    write_csv(QUADRATURE, quadrature_rows)
    write_csv(
        ORDER_ARTIFACT,
        aggregate_worker_csv("inner_order_artifact.csv"),
    )
    write_csv(VALIDATION, validation_rows)
    atomic_json(RESULT, result)
    write_document(result)
    atomic_json(
        STATUS,
        {
            "marker": MARKER,
            "state": "completed",
            "completed_workers": 2,
            "total_workers": 2,
            "acceptance_passed": route_rejected,
            "decision": result["decision"],
        },
    )
    return result


def execute() -> dict[str, Any]:
    set_resource_policy()
    prepare()
    environment = dict(os.environ)
    environment["PYTHONNOUSERSITE"] = "1"
    for name in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "BLIS_NUM_THREADS",
    ):
        environment[name] = "1"
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker",
        "E020",
    ]
    creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    child = subprocess.Popen(
        command,
        env=environment,
        creationflags=creation_flags,
    )
    try:
        try:
            import psutil

            psutil.Process(child.pid).nice(
                psutil.BELOW_NORMAL_PRIORITY_CLASS
            )
        except Exception:
            pass
        worker("E040")
        return_code = child.wait()
        if return_code != 0:
            raise RuntimeError(
                f"E020 worker exited with code {return_code}"
            )
    except BaseException:
        if child.poll() is None:
            child.terminate()
            child.wait(timeout=30)
        raise
    return aggregate()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--worker", choices=tuple(EPSILON_VALUES))
    parser.add_argument("--aggregate", action="store_true")
    parser.add_argument("--execute", action="store_true")
    arguments = parser.parse_args()
    selected = sum(
        bool(value)
        for value in (
            arguments.prepare,
            arguments.worker,
            arguments.aggregate,
            arguments.execute,
        )
    )
    if selected != 1:
        raise SystemExit(
            "select exactly one of --prepare, --worker, "
            "--aggregate, --execute"
        )
    if arguments.prepare:
        value = prepare()
    elif arguments.worker:
        value = worker(arguments.worker)
    elif arguments.aggregate:
        value = aggregate()
    else:
        value = execute()
    print(json.dumps(value, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
