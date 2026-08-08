from __future__ import annotations

import argparse
import cmath
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5311"

SCRIPT_5310 = SCRIPTS / "Y5_R2FR_5310_anisotropic_topology_cell_refinement.py"
RESULT_5310 = FUNCTIONAL_RG / "5310" / "anisotropic_refinement_result.json"
LEAVES_5310 = FUNCTIONAL_RG / "5310" / "E0025_adaptive_leaf_plan.csv"
CONTRACT_5308 = FUNCTIONAL_RG / "5308" / "fixed_decay_energy_soft_cubature_contract.csv"

DRY_RUN = SOURCE / "material_pole_aligned_energy_preflight_dry_run.json"
WITNESSES = SOURCE / "failed_leaf_material_pole_witnesses.csv"
GEOMETRIC_POLES = SOURCE / "E0025_witness_geometric_poles.csv"
POLE_FITS = SOURCE / "E0025_witness_pole_residue_fits.csv"
POLE_CLASSIFICATION = SOURCE / "E0025_witness_pole_classification.csv"
PANELS = SOURCE / "E0025_pole_aligned_energy_panels.csv"
INTEGRALS = SOURCE / "E0025_pole_aligned_energy_integrals.csv"
RESULT = SOURCE / "material_pole_aligned_energy_preflight_result.json"
VALIDATION = SOURCE / "material_pole_aligned_energy_preflight_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5311_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5311-Y5-R2FR-material-pole-aligned-energy-preflight.md"

CHECKPOINT = 5311
PARENT_CHECKPOINT = 5310
MARKER = "MTS_5311_MATERIAL_POLE_ALIGNED_ENERGY_PREFLIGHT"
REVISION = "material-pole-aligned-energy-preflight-v1"
EPSILON_ID = "E0025"
EPSILON = 0.0025
WITNESS_CONTRACTS = (3, 8, 29)
FIT_BACKGROUND_DEGREE = 4
FIT_RELATIVE_RESIDUAL_LIMIT = 1.0e-4
FIT_RESIDUE_CHANGE_LIMIT = 5.0e-4
MATERIAL_RESIDUE_FLOOR = 1.0e-6
REMOVABLE_RESIDUE_CEILING = 1.0e-8
CORRECTED_ORDER_CHANGE_LIMIT = 5.0e-3
ENERGY_ORDERS = (4, 8, 12)
CLAIM_FIELDS = (
    "valid_for_full_angular_convergence",
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


M5310 = load_module("mts_5310_for_5311", SCRIPT_5310)
M5309 = M5310.M5309
M5308 = M5310.M5308
M5305 = M5310.M5305
M5303 = M5310.M5303
M5301 = M5310.M5301
M5283 = M5310.M5283
M5280 = M5310.M5280
M5291 = M5301.M5300.M5295.M5291
np = M5310.np
mp = M5310.mp


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetCurrentProcess.restype = ctypes.c_void_p
    kernel32.SetPriorityClass.argtypes = (ctypes.c_void_p, ctypes.c_uint32)
    kernel32.SetPriorityClass.restype = ctypes.c_int
    process = kernel32.GetCurrentProcess()
    if not kernel32.SetPriorityClass(process, 0x00004000):
        raise ctypes.WinError()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def parse_bool(value: Any) -> bool:
    return M5310.parse_bool(value)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return M5310.complex_fields(prefix, value)


def relative_complex_change(first: complex, second: complex) -> float:
    return M5310.relative_complex_change(first, second)


def contract_lookup() -> dict[int, dict[str, str]]:
    return {
        int(row["contract_index"]): row for row in read_csv(CONTRACT_5308)
    }


def failed_witness_rows() -> list[dict[str, Any]]:
    contracts = contract_lookup()
    failed = [
        row for row in read_csv(LEAVES_5310)
        if not parse_bool(row["leaf_local_gate_passes"])
    ]
    rows: list[dict[str, Any]] = []
    for contract_index in WITNESS_CONTRACTS:
        source = max(
            (
                row for row in failed
                if int(row["contract_index"]) == contract_index
            ),
            key=lambda row: float(row["E0025_local_relative_change"]),
        )
        contract = contracts[contract_index]
        row = {
            "witness_id": f"C{contract_index:02d}",
            "contract_index": contract_index,
            "failed_region_id": source["region_id"],
            "failed_depth": source["depth"],
            "parent_local_relative_change": source[
                "E0025_local_relative_change"
            ],
            "failed_u_lower": source["u_lower"],
            "failed_u_upper": source["u_upper"],
            "failed_v_lower": source["v_lower"],
            "failed_v_upper": source["v_upper"],
            "evaluation_term_ids": contract["evaluation_term_ids"],
            "valid_for_material_pole_witness_selection": True,
            **{field: False for field in CLAIM_FIELDS},
        }
        update_witness_coordinate(row, 0.5)
        rows.append(row)
    return rows


def update_witness_coordinate(
    witness: dict[str, Any], probe_fraction: float
) -> None:
    contract = contract_lookup()[int(witness["contract_index"])]
    u_lower = float(witness["failed_u_lower"])
    u_upper = float(witness["failed_u_upper"])
    u_value = u_lower + probe_fraction * (u_upper - u_lower)
    x_lower = float(contract["lower_absolute_soft_cosine"])
    x_upper = float(contract["upper_absolute_soft_cosine"])
    coordinate = x_lower + (x_upper - x_lower) * u_value
    energy_lower = M5308.boundary_energy(
        contract["lower_energy_boundary"], coordinate
    )
    energy_upper = M5308.boundary_energy(
        contract["upper_energy_boundary"], coordinate
    )
    witness.update(
        {
            "selected_u_probe_fraction": probe_fraction,
            "selected_u_value": u_value,
            "absolute_soft_cosine": coordinate,
            "full_energy_lower": energy_lower,
            "full_energy_upper": energy_upper,
            "failed_leaf_energy_lower": energy_lower
            + (energy_upper - energy_lower) * float(witness["failed_v_lower"]),
            "failed_leaf_energy_upper": energy_lower
            + (energy_upper - energy_lower) * float(witness["failed_v_upper"]),
        }
    )


def synthetic_energy_problem(
    component_id: str,
    signed_soft_cosine: float,
    signed_decay_cosine: float,
) -> dict[str, Any]:
    source_job = M5291.manifest_job("E020", component_id)
    problem = M5291.M5286.angular_problem(
        source_job,
        signed_soft_cosine,
        signed_decay_cosine,
    )
    problem["target"] = complex(-9.0, EPSILON)
    M5291.M5267.install_paired_track(problem)
    return problem


def derive_geometric_poles(
    witnesses: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for witness_counter, witness in enumerate(witnesses, start=1):
        selected_rows: list[dict[str, Any]] = []
        for probe_fraction in (0.5, 0.25, 0.75, 0.125, 0.875):
            update_witness_coordinate(witness, probe_fraction)
            coordinate = float(witness["absolute_soft_cosine"])
            local_rows: list[dict[str, Any]] = []
            for term_id in M5309.term_ids(witness["evaluation_term_ids"]):
                specification = M5308.SURFACE_LOOKUP[term_id]
                component_id = str(specification["component_id"])
                soft_sign = int(specification["soft_sign"])
                decay_sign = int(specification["decay_sign"])
                problem = synthetic_energy_problem(
                    component_id,
                    soft_sign * coordinate,
                    decay_sign * M5308.M5302.EDGE_DECAY_ABSOLUTE,
                )
                _, _, poles, _ = M5291.M5267.M5239.scan_problem(problem)
                for pole in poles:
                    pole_real = float(pole["pole_real"])
                    local_rows.append(
                        {
                            "witness_id": witness["witness_id"],
                            "contract_index": witness["contract_index"],
                            "selected_u_probe_fraction": probe_fraction,
                            "term_id": term_id,
                            "component_id": component_id,
                            "soft_sign": soft_sign,
                            "decay_sign": decay_sign,
                            "epsilon_id": EPSILON_ID,
                            "epsilon": EPSILON,
                            "pole_id": pole["pole_id"],
                            "primary_surface_id": pole["primary_surface_id"],
                            "real_axis_center": pole["real_axis_center"],
                            "pole_real": pole_real,
                            "pole_imaginary": pole["pole_imaginary"],
                            "inside_full_energy_interval": (
                                float(witness["full_energy_lower"])
                                < pole_real
                                < float(witness["full_energy_upper"])
                            ),
                            "inside_failed_leaf_energy_interval": (
                                float(witness["failed_leaf_energy_lower"])
                                < pole_real
                                < float(witness["failed_leaf_energy_upper"])
                            ),
                            "valid_for_E0025_geometric_pole_witness": True,
                            **{field: False for field in CLAIM_FIELDS},
                        }
                    )
            selected_rows = local_rows
            if any(
                bool(row["inside_failed_leaf_energy_interval"])
                for row in local_rows
            ):
                break
        rows.extend(selected_rows)
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "GEOMETRIC_POLE_DERIVATION",
                "completed_witness_count": witness_counter,
                "planned_witness_count": len(witnesses),
            },
        )
    return rows


def fit_pole_residues(
    witnesses: list[dict[str, Any]],
    poles: list[dict[str, Any]],
    evaluate: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    witness_lookup = {row["witness_id"]: row for row in witnesses}
    fit_rows: list[dict[str, Any]] = []
    classification: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in poles:
        grouped.setdefault((row["witness_id"], row["term_id"]), []).append(row)
    for row in poles:
        if not bool(row["inside_full_energy_interval"]):
            continue
        witness = witness_lookup[row["witness_id"]]
        coordinate = float(witness["absolute_soft_cosine"])
        center = float(row["real_axis_center"])
        pole = complex(float(row["pole_real"]), float(row["pole_imaginary"]))
        local_poles = grouped[(row["witness_id"], row["term_id"])]
        separations = [
            abs(center - float(other["real_axis_center"]))
            for other in local_poles
            if other is not row
        ]
        margin = min(
            center - float(witness["full_energy_lower"]),
            float(witness["full_energy_upper"]) - center,
            *(separations or [1.0]),
        )
        base_radius = min(
            max(8.0 * abs(pole.imag), 2.0e-6),
            margin / 10.0,
        )
        if base_radius <= 0.0:
            raise RuntimeError(f"nonpositive fit radius for {row}")
        residues: list[complex] = []
        residuals: list[float] = []
        for fit_scale in (1.0, 2.0):
            radius = fit_scale * base_radius
            offsets = (
                -4.0 * radius,
                -2.0 * radius,
                -radius,
                -0.5 * radius,
                0.5 * radius,
                radius,
                2.0 * radius,
                4.0 * radius,
            )
            matrix_rows: list[list[complex]] = []
            values: list[complex] = []
            all_active = True
            for offset in offsets:
                energy = center + offset
                value, active = evaluate(
                    EPSILON_ID,
                    energy,
                    coordinate,
                    row["component_id"],
                    int(row["soft_sign"]),
                    int(row["decay_sign"]),
                )
                all_active = all_active and active
                delta = energy - center
                matrix_rows.append(
                    [
                        1.0 / (energy - pole),
                        *[
                            complex(delta**power)
                            for power in range(FIT_BACKGROUND_DEGREE + 1)
                        ],
                    ]
                )
                values.append(value)
            matrix = np.asarray(matrix_rows, dtype=np.complex128)
            vector = np.asarray(values, dtype=np.complex128)
            coefficients, _, _, _ = np.linalg.lstsq(
                matrix, vector, rcond=None
            )
            predicted = matrix @ coefficients
            residual = float(
                np.linalg.norm(predicted - vector)
                / max(np.linalg.norm(vector), 1.0)
            )
            residue = complex(coefficients[0])
            residues.append(residue)
            residuals.append(residual)
            fit_rows.append(
                {
                    "witness_id": row["witness_id"],
                    "contract_index": row["contract_index"],
                    "term_id": row["term_id"],
                    "component_id": row["component_id"],
                    "soft_sign": row["soft_sign"],
                    "decay_sign": row["decay_sign"],
                    "pole_id": row["pole_id"],
                    "fit_scale": fit_scale,
                    "fit_radius": radius,
                    "fit_sample_count": len(offsets),
                    "background_polynomial_degree": FIT_BACKGROUND_DEGREE,
                    **complex_fields("fitted_residue", residue),
                    "fit_relative_residual": residual,
                    "all_fit_samples_mask_active": all_active,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
        residue_change = relative_complex_change(residues[0], residues[1])
        material = (
            min(abs(value) for value in residues) >= MATERIAL_RESIDUE_FLOOR
            and max(residuals) <= FIT_RELATIVE_RESIDUAL_LIMIT
            and residue_change <= FIT_RESIDUE_CHANGE_LIMIT
        )
        removable = max(abs(value) for value in residues) <= REMOVABLE_RESIDUE_CEILING
        classification.append(
            {
                "witness_id": row["witness_id"],
                "contract_index": row["contract_index"],
                "term_id": row["term_id"],
                "component_id": row["component_id"],
                "soft_sign": row["soft_sign"],
                "decay_sign": row["decay_sign"],
                "pole_id": row["pole_id"],
                "pole_real": row["pole_real"],
                "pole_imaginary": row["pole_imaginary"],
                **complex_fields("selected_residue", residues[-1]),
                "maximum_fit_relative_residual": max(residuals),
                "fit_residue_relative_change": residue_change,
                "material_simple_pole": material,
                "removable_zero_residue_pole": removable,
                "pole_classification_resolved": material or removable,
                "inside_failed_leaf_energy_interval": row[
                    "inside_failed_leaf_energy_interval"
                ],
                "valid_for_pole_aligned_energy_preflight": material or removable,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return fit_rows, classification


def panel_rows(
    witness: dict[str, Any],
    local_poles: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    lower = float(witness["full_energy_lower"])
    upper = float(witness["full_energy_upper"])
    points = {lower, upper}
    points.update(
        lower + index * (upper - lower) / 16.0 for index in range(17)
    )
    for row in local_poles:
        center = float(row["pole_real"])
        core = max(abs(float(row["pole_imaginary"])), 1.0e-7)
        for scale in (0.0, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0):
            points.add(max(lower, min(upper, center - scale * core)))
            points.add(max(lower, min(upper, center + scale * core)))
    coordinates = sorted(points)
    rows: list[dict[str, Any]] = []
    for panel_index, (left, right) in enumerate(
        zip(coordinates[:-1], coordinates[1:]), start=1
    ):
        if right - left <= 1.0e-15:
            continue
        rows.append(
            {
                "witness_id": witness["witness_id"],
                "contract_index": witness["contract_index"],
                "panel_index": panel_index,
                "energy_lower": left,
                "energy_upper": right,
                "panel_width": right - left,
                "valid_for_pole_aligned_energy_panel": True,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def integrate_witness(
    witness: dict[str, Any],
    classifications: list[dict[str, Any]],
    evaluate: Any,
    multiplier: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    coordinate = float(witness["absolute_soft_cosine"])
    selected_ids = M5309.term_ids(witness["evaluation_term_ids"])
    local = [
        row for row in classifications
        if row["witness_id"] == witness["witness_id"]
    ]
    panels = panel_rows(witness, local)
    material = [row for row in local if bool(row["material_simple_pole"])]
    analytic = sum(
        (
            complex(
                float(row["selected_residue_real"]),
                float(row["selected_residue_imaginary"]),
            )
            * (
                cmath.log(
                    float(witness["full_energy_upper"])
                    - complex(float(row["pole_real"]), float(row["pole_imaginary"]))
                )
                - cmath.log(
                    float(witness["full_energy_lower"])
                    - complex(float(row["pole_real"]), float(row["pole_imaginary"]))
                )
            )
            for row in material
        ),
        0.0j,
    )

    def raw_value(energy: float) -> complex:
        value, inactive = M5309.evaluate_selected_terms(
            evaluate,
            EPSILON_ID,
            energy,
            coordinate,
            selected_ids,
        )
        if inactive:
            raise RuntimeError(
                f"witness {witness['witness_id']} left selected mask"
            )
        return value

    def singular_value(energy: float) -> complex:
        total = 0.0j
        for row in material:
            pole = complex(float(row["pole_real"]), float(row["pole_imaginary"]))
            residue = complex(
                float(row["selected_residue_real"]),
                float(row["selected_residue_imaginary"]),
            )
            total += residue / (energy - pole)
        return total

    rows: list[dict[str, Any]] = []
    lower = float(witness["full_energy_lower"])
    upper = float(witness["full_energy_upper"])
    for order in ENERGY_ORDERS:
        nodes, weights = np.polynomial.legendre.leggauss(order)
        direct = 0.0j
        half = 0.5 * (upper - lower)
        midpoint = 0.5 * (upper + lower)
        for node, weight in zip(nodes, weights):
            energy = midpoint + half * float(node)
            direct += half * float(weight) * raw_value(energy)
        regular = 0.0j
        for panel in panels:
            left = float(panel["energy_lower"])
            right = float(panel["energy_upper"])
            local_half = 0.5 * (right - left)
            local_midpoint = 0.5 * (right + left)
            for node, weight in zip(nodes, weights):
                energy = local_midpoint + local_half * float(node)
                regular += (
                    local_half
                    * float(weight)
                    * (raw_value(energy) - singular_value(energy))
                )
        corrected = multiplier * (regular + analytic)
        rows.append(
            {
                "witness_id": witness["witness_id"],
                "contract_index": witness["contract_index"],
                "energy_order": order,
                "panel_count": len(panels),
                "material_pole_count": len(material),
                **complex_fields("unpanelled_direct_integral", multiplier * direct),
                **complex_fields("regularized_numeric_integral", multiplier * regular),
                **complex_fields("analytic_pole_integral", multiplier * analytic),
                **complex_fields("pole_corrected_integral", corrected),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    order_lookup = {
        int(row["energy_order"]): complex(
            float(row["pole_corrected_integral_real"]),
            float(row["pole_corrected_integral_imaginary"]),
        )
        for row in rows
    }
    direct_lookup = {
        int(row["energy_order"]): complex(
            float(row["unpanelled_direct_integral_real"]),
            float(row["unpanelled_direct_integral_imaginary"]),
        )
        for row in rows
    }
    for row in rows:
        row["corrected_order4_order8_relative_change"] = (
            relative_complex_change(order_lookup[4], order_lookup[8])
        )
        row["corrected_order8_order12_relative_change"] = (
            relative_complex_change(order_lookup[8], order_lookup[12])
        )
        row["direct_order4_order8_relative_change"] = (
            relative_complex_change(direct_lookup[4], direct_lookup[8])
        )
        row["direct_order8_order12_relative_change"] = (
            relative_complex_change(direct_lookup[8], direct_lookup[12])
        )
        row["passes_pole_aligned_energy_gate"] = (
            row["corrected_order4_order8_relative_change"]
            <= CORRECTED_ORDER_CHANGE_LIMIT
            and row["corrected_order8_order12_relative_change"]
            <= CORRECTED_ORDER_CHANGE_LIMIT
        )
    return panels, rows


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5310,
        RESULT_5310,
        LEAVES_5310,
        CONTRACT_5308,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5310)
    witnesses = failed_witness_rows()
    failed = [
        row for row in read_csv(LEAVES_5310)
        if not parse_bool(row["leaf_local_gate_passes"])
    ]
    checks = {
        "parent_5310_rejected_rectangular_depth_extension": (
            not bool(parent["acceptance_passed"])
            and parent["decision"]
            == "ADAPTIVE_PLAN_REACHES_DEPTH_BOUND__REFINE_POLE_COORDINATES"
        ),
        "failed_leaves_are_real_and_localized": (
            len(failed) > 0
            and {int(row["contract_index"]) for row in failed}
            == set(WITNESS_CONTRACTS)
        ),
        "one_worst_witness_selected_per_failed_contract": (
            len(witnesses) == len(WITNESS_CONTRACTS)
            and {int(row["contract_index"]) for row in witnesses}
            == set(WITNESS_CONTRACTS)
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == parent["formalization_workbench_end_digest"]
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "witness_count": len(witnesses),
        "decision": (
            "DRY_RUN_ACCEPTED__DERIVE_AND_SUBTRACT_WITNESS_MATERIAL_POLES"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    set_below_normal_priority()
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    M5301.configure_reused_pipeline()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5311 dry run did not pass")
    witnesses = failed_witness_rows()
    poles = derive_geometric_poles(witnesses)
    write_csv(WITNESSES, witnesses)
    write_csv(GEOMETRIC_POLES, poles)
    base_context = M5303.synthetic_context()
    evaluate = M5305.component_evaluator(base_context)
    fits, classifications = fit_pole_residues(witnesses, poles, evaluate)
    write_csv(POLE_FITS, fits)
    write_csv(POLE_CLASSIFICATION, classifications)
    all_panels: list[dict[str, Any]] = []
    integrals: list[dict[str, Any]] = []
    multiplier = M5309.physical_multiplier()
    for witness_counter, witness in enumerate(witnesses, start=1):
        local_panels, local_integrals = integrate_witness(
            witness,
            classifications,
            evaluate,
            multiplier,
        )
        all_panels.extend(local_panels)
        integrals.extend(local_integrals)
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "POLE_ALIGNED_ENERGY_INTEGRATION",
                "completed_witness_count": witness_counter,
                "planned_witness_count": len(witnesses),
            },
        )
    write_csv(PANELS, all_panels)
    write_csv(INTEGRALS, integrals)
    material = [row for row in classifications if bool(row["material_simple_pole"])]
    removable = [
        row for row in classifications
        if bool(row["removable_zero_residue_pole"])
    ]
    unresolved = [
        row for row in classifications
        if not bool(row["pole_classification_resolved"])
    ]
    final_rows = [row for row in integrals if int(row["energy_order"]) == 12]
    material_leaf_coverage = all(
        any(
            row["witness_id"] == witness["witness_id"]
            and bool(row["material_simple_pole"])
            and parse_bool(row["inside_failed_leaf_energy_interval"])
            for row in classifications
        )
        for witness in witnesses
    )
    formal_end = M5283.formal_inventory_digest()
    checks = {
        "every_failed_contract_crosses_a_material_pole": material_leaf_coverage,
        "all_in_interval_poles_classified": not unresolved,
        "at_least_one_material_and_one_removable_pole": (
            bool(material) and bool(removable)
        ),
        "all_material_residue_fits_controlled": all(
            float(row["maximum_fit_relative_residual"])
            <= FIT_RELATIVE_RESIDUAL_LIMIT
            and float(row["fit_residue_relative_change"])
            <= FIT_RESIDUE_CHANGE_LIMIT
            for row in material
        ),
        "all_three_pole_aligned_energy_integrals_converge": (
            len(final_rows) == len(witnesses)
            and all(parse_bool(row["passes_pole_aligned_energy_gate"]) for row in final_rows)
        ),
        "integration_precision_initialized": mp.mp.dps >= M5280.MP_DECIMAL_DIGITS,
        "formalization_workbench_unchanged": (
            formal_end == read_json(RESULT_5310)["formalization_workbench_end_digest"]
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    decision = (
        "MATERIAL_POLE_CAUSE_PROVED_AND_SUBTRACTION_PREFLIGHT_PASSES__"
        "BUILD_RESUMABLE_OUTER_SOFT_INTEGRAL"
        if accepted
        else "MATERIAL_POLE_PREFLIGHT_REQUIRES_REFINEMENT"
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "material-pole-aligned-energy-preflight",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": decision,
        "witness_count": len(witnesses),
        "geometric_pole_count": len(poles),
        "classified_in_interval_pole_count": len(classifications),
        "material_simple_pole_count": len(material),
        "removable_zero_residue_pole_count": len(removable),
        "unresolved_pole_count": len(unresolved),
        "pole_aligned_panel_count": len(all_panels),
        "maximum_corrected_order4_order8_relative_change": max(
            float(row["corrected_order4_order8_relative_change"])
            for row in final_rows
        ),
        "maximum_corrected_order8_order12_relative_change": max(
            float(row["corrected_order8_order12_relative_change"])
            for row in final_rows
        ),
        "maximum_direct_order4_order8_relative_change": max(
            float(row["direct_order4_order8_relative_change"])
            for row in final_rows
        ),
        "formalization_workbench_reference_digest": read_json(RESULT_5310)[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == read_json(RESULT_5310)["formalization_workbench_end_digest"]
            else -1
        ),
        "claim_boundary": {
            "valid_for_material_pole_cause_at_three_failed_witnesses": accepted,
            "valid_for_pole_aligned_energy_preflight": accepted,
            "valid_for_full_fixed_decay_energy_soft_integral": False,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "Three failed leaves are diagnosed and repaired at their "
                "representative soft coordinates; the continuous outer soft "
                "integral has not yet run."
            ),
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "maximum_silent_work_hours": 4,
        },
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETE" if accepted else "REFINEMENT_REQUIRED",
            "decision": decision,
        },
    )
    return result


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": detail}


def render_document(result: dict[str, Any], passed: bool) -> None:
    text = f"""# 5311 — Material-pole-aligned energy preflight

## Result

The 5310 rectangular refinement failure is not an unexplained numerical
instability.  Exact continuation of the parent collision geometry places a
material energy pole inside the worst failed leaf of each affected topology
contract (`3`, `8`, and `29`).  The same scans also identify removable
zero-residue poles rather than treating every geometric collision as singular.

For each witness, the material Laurent term is fitted twice, subtracted before
quadrature, and restored analytically as
`R[log(E_hi-p)-log(E_lo-p)]`.  The remaining energy integral is evaluated on
panels aligned to the pole centers and regulator widths.

- failed-leaf witnesses: `{result['witness_count']}`;
- geometric poles scanned: `{result['geometric_pole_count']}`;
- material simple poles: `{result['material_simple_pole_count']}`;
- removable zero-residue poles: `{result['removable_zero_residue_pole_count']}`;
- unresolved poles: `{result['unresolved_pole_count']}`;
- aligned energy panels: `{result['pole_aligned_panel_count']}`;
- maximum corrected Q4/Q8 change:
  `{result['maximum_corrected_order4_order8_relative_change']:.12g}`;
- maximum corrected Q8/Q12 change:
  `{result['maximum_corrected_order8_order12_relative_change']:.12g}`;
- unaligned direct Q4/Q8 control change:
  `{result['maximum_direct_order4_order8_relative_change']:.12g}`.

Decision: **{result['decision']}**.

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

This proves the cause and subtraction route at three representative failed
soft coordinates.  It does not yet perform the continuous outer soft-angle
integral, the decay-angle integral, a full phase-space coefficient, local GR,
or the full MTS theory.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    witnesses = read_csv(WITNESSES)
    poles = read_csv(GEOMETRIC_POLES)
    fits = read_csv(POLE_FITS)
    classifications = read_csv(POLE_CLASSIFICATION)
    panels = read_csv(PANELS)
    integrals = read_csv(INTEGRALS)
    source_files_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    final_rows = [row for row in integrals if int(row["energy_order"]) == 12]
    gates = [
        validation_gate(
            "result_pipeline_accepted",
            bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "three_failed_leaf_witnesses_complete",
            len(witnesses) == 3
            and {int(row["contract_index"]) for row in witnesses}
            == set(WITNESS_CONTRACTS),
            f"rows={len(witnesses)}",
        ),
        validation_gate(
            "geometric_pole_scan_and_fit_tables_complete",
            len(poles) == int(result["geometric_pole_count"])
            and len(fits) == 2 * len(classifications)
            and all(
                parse_bool(row["pole_classification_resolved"])
                for row in classifications
            ),
            f"poles={len(poles)}; fits={len(fits)}",
        ),
        validation_gate(
            "every_failed_leaf_crosses_material_pole",
            all(
                any(
                    row["witness_id"] == witness["witness_id"]
                    and parse_bool(row["material_simple_pole"])
                    and parse_bool(row["inside_failed_leaf_energy_interval"])
                    for row in classifications
                )
                for witness in witnesses
            ),
            f"material={result['material_simple_pole_count']}",
        ),
        validation_gate(
            "pole_aligned_energy_integrals_converge",
            len(integrals) == 3 * len(ENERGY_ORDERS)
            and len(final_rows) == 3
            and all(
                parse_bool(row["passes_pole_aligned_energy_gate"])
                for row in final_rows
            ),
            f"integrals={len(integrals)}; panels={len(panels)}",
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == result["formalization_workbench_end_digest"]
            == result["formalization_workbench_reference_digest"]
            and int(result["formalization_workbench_modified_file_count"]) == 0,
            result["formalization_workbench_end_digest"],
        ),
        validation_gate(
            "recorded_source_paths_and_hashes_current",
            source_files_current,
            f"rows={len(result['source_files'])}",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
        validation_gate(
            "broader_claims_locked_false",
            all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            )
            and not bool(
                result["claim_boundary"][
                    "valid_for_full_fixed_decay_energy_soft_integral"
                ]
            ),
            "no outer-soft, decay-angle, phase-space, local-GR, or full-MTS claim",
        ),
    ]
    passed = all(bool(row["passed"]) for row in gates)
    write_csv(VALIDATION, gates)
    write_csv(RESIDUAL_VALIDATION, gates)
    render_document(result, passed)
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_MATERIAL_POLE_ALIGNED_ENERGY_PREFLIGHT"
            if passed
            else "MATERIAL_POLE_ALIGNED_ENERGY_PREFLIGHT_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("dry-run", "run", "validate"), required=True
    )
    return parser.parse_args()


def main() -> int:
    set_below_normal_priority()
    arguments = parse_args()
    if arguments.mode == "dry-run":
        result = dry_run()
    elif arguments.mode == "run":
        result = execute()
    else:
        result = validate_outputs()
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
