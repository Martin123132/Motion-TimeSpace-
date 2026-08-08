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
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5292"
NODE_RUNS = SOURCE / "nodes"

SCRIPT_5291 = SCRIPTS / "Y5_R2FR_5291_order4_complete_singularity_atlas.py"
RESULT_5291 = (
    FUNCTIONAL_RG / "5291" / "order4_complete_singularity_atlas_result.json"
)
VALIDATION_5291 = (
    FUNCTIONAL_RG
    / "5291"
    / "order4_complete_singularity_atlas_validation.csv"
)
ANGULAR_NODES_5291 = FUNCTIONAL_RG / "5291" / "angular_order4_nodes.csv"
POLE_RESIDUES_5291 = (
    FUNCTIONAL_RG / "5291" / "angular_order4_selected_pole_residues.csv"
)
ENDPOINT_COEFFICIENTS_5291 = (
    FUNCTIONAL_RG / "5291" / "angular_order4_endpoint_coefficients.csv"
)
ENDPOINT_CANCELLATIONS_5291 = (
    FUNCTIONAL_RG / "5291" / "angular_order4_endpoint_cancellations.csv"
)
BOUNDS_5291 = (
    FUNCTIONAL_RG
    / "5291"
    / "angular_order4_bounded_ambiguous_pole_residues.csv"
)
OUTER_5290 = (
    FUNCTIONAL_RG / "5290" / "all_family_order2_outer_totals.csv"
)

DRY_RUN = SOURCE / "order4_inner_energy_dry_run.json"
NODE_MANIFEST = SOURCE / "order4_node_run_manifest.csv"
COMPONENT_TOTALS = SOURCE / "order4_inner_component_totals.csv"
INNER_TOTALS = SOURCE / "order4_inner_energy_totals.csv"
INNER_CONVERGENCE = SOURCE / "order4_inner_energy_convergence.csv"
OUTER_TOTALS = SOURCE / "order4_outer_totals.csv"
ANGULAR_COMPARISON = SOURCE / "order2_order4_angular_comparison.csv"
RESULT = SOURCE / "order4_inner_energy_result.json"
VALIDATION = SOURCE / "order4_inner_energy_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5292_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5292-Y5-R2FR-order4-inner-energy-and-order2-comparison.md"

CHECKPOINT = 5292
PARENT_CHECKPOINT = 5291
MARKER = "MTS_5292_ORDER4_INNER_ENERGY_AND_ORDER2_COMPARISON"
REVISION = "order4-inner-energy-order2-comparison-v1"
ANGULAR_ORDER = 4
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
LEGACY_SIX_IDS = ("MC03", "MC04", "MC07", "MC12", "MC14", "MC15")
HIDDEN_IDS = ("MC02", "MC08")
ENERGY_ORDERS = (4, 8)
INNER_RELATIVE_CHANGE_LIMIT = 5.0e-3
OUTER_ENERGY_RELATIVE_CHANGE_LIMIT = 5.0e-3
ANGULAR_RELATIVE_CHANGE_LIMIT = 5.0e-3
COEFFICIENT_RELATIVE_CHANGE_LIMIT = 1.0e-6
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


M5291 = load_module("mts_5291_for_5292", SCRIPT_5291)
M5290 = M5291.M5290
M5289 = M5291.M5289
M5288 = M5291.M5288
M5287 = M5291.M5287
M5283 = M5291.M5283
M5280 = M5291.M5280
M5267 = M5291.M5267
np = M5291.np
mp = M5291.mp


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    process_handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(process_handle, 0x00004000)


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
        while block := handle.read(1024 * 1024):
            value.update(block)
    return value.hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def relative_complex_difference(first: complex, second: complex) -> float:
    return abs(first - second) / max(abs(first), abs(second), 1.0e-300)


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5291,
        RESULT_5291,
        VALIDATION_5291,
        ANGULAR_NODES_5291,
        POLE_RESIDUES_5291,
        ENDPOINT_COEFFICIENTS_5291,
        ENDPOINT_CANCELLATIONS_5291,
        BOUNDS_5291,
        OUTER_5290,
        M5283.TOTALS_5281,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def pole_lookup() -> dict[
    tuple[str, str, str],
    list[dict[str, complex]],
]:
    grouped: dict[
        tuple[str, str, str],
        list[dict[str, complex]],
    ] = defaultdict(list)
    for row in read_csv(POLE_RESIDUES_5291):
        if not parse_bool(row["valid_for_order4_pole_subtraction"]):
            continue
        grouped[
            (
                row["angular_node_id"],
                row["epsilon_id"],
                row["component_id"],
            )
        ].append(
            {
                "pole": complex(
                    float(row["pole_real"]),
                    float(row["pole_imaginary"]),
                ),
                "residue": complex(
                    float(row["true_limit_residue_real"]),
                    float(row["true_limit_residue_imaginary"]),
                ),
                "bounded_ambiguous": complex(
                    1.0 if parse_bool(row["bounded_ambiguous_residue"]) else 0.0,
                    0.0,
                ),
            }
        )
    return grouped


def endpoint_lookup() -> dict[tuple[str, str, str], complex]:
    return {
        (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
        ): complex(
            float(row["endpoint_log_coefficient_real"]),
            float(row["endpoint_log_coefficient_imaginary"]),
        )
        for row in read_csv(ENDPOINT_COEFFICIENTS_5291)
        if parse_bool(row["valid_for_lower_endpoint_log_subtraction"])
    }


def physical_multiplier() -> float:
    source = next(
        row
        for row in read_csv(M5283.TOTALS_5281)
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    )
    return float(source["kernel_multiplier"]) * float(
        source["physical_A00_weight"]
    )


def analytic_integrals(
    angular_node_id: str,
    poles: dict[tuple[str, str, str], list[dict[str, complex]]],
    endpoints: dict[tuple[str, str, str], complex],
) -> dict[tuple[str, str], complex]:
    minimum = float(M5267.ENERGY_MINIMUM)
    maximum = float(M5267.ENERGY_MAXIMUM)
    values: dict[tuple[str, str], complex] = defaultdict(complex)
    for epsilon_id in REGULATOR_IDS:
        for component_id in COMPONENT_IDS:
            key = (angular_node_id, epsilon_id, component_id)
            for term in poles.get(key, []):
                pole = term["pole"]
                values[(epsilon_id, component_id)] += term["residue"] * (
                    cmath.log(maximum - pole)
                    - cmath.log(minimum - pole)
                )
            if key in endpoints:
                values[(epsilon_id, component_id)] += endpoints[key] * (
                    math.log(maximum) - math.log(minimum)
                )
    return values


def node_panels(
    angular_node_id: str,
    context: dict[str, Any],
    poles: dict[tuple[str, str, str], list[dict[str, complex]]],
) -> tuple[list[dict[str, Any]], int, int]:
    mask_boundaries = M5280.exact_energy_mask_boundaries(context)
    centers = [
        {"center": term["pole"].real}
        for key, terms in poles.items()
        if key[0] == angular_node_id
        for term in terms
    ]
    panels = M5287.endpoint_refined_panels(
        M5280.composite_panel_rows(mask_boundaries, centers)
    )
    return panels, len(mask_boundaries), len(centers)


def node_paths(node_id: str) -> dict[str, Path]:
    root = NODE_RUNS / node_id
    return {
        "root": root,
        "energy_nodes": root / "energy_component_nodes.csv",
        "component_totals": root / "component_totals.csv",
        "inner_totals": root / "inner_energy_totals.csv",
        "convergence": root / "inner_energy_convergence.csv",
        "result": root / "result.json",
    }


def node_cache_valid(node: dict[str, Any]) -> bool:
    paths = node_paths(node["angular_node_id"])
    required = tuple(
        path for key, path in paths.items() if key != "root"
    )
    if not all(path.exists() for path in required):
        return False
    result = read_json(paths["result"])
    return (
        result.get("revision") == REVISION
        and result.get("singularity_atlas_sha256") == digest(RESULT_5291)
        and bool(result.get("node_run_completed"))
    )


def node_convergence_rows(
    node_id: str,
    totals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for channel in (
        "eight_component_integral",
        "six_component_integral",
        "hidden_component_integral",
    ):
        lower_source = next(
            row
            for row in totals
            if row["row_type"] == "PHYSICAL_INNER_ENERGY"
            and int(row["energy_order"]) == min(ENERGY_ORDERS)
        )
        upper_source = next(
            row
            for row in totals
            if row["row_type"] == "PHYSICAL_INNER_ENERGY"
            and int(row["energy_order"]) == max(ENERGY_ORDERS)
        )
        lower = complex(
            float(lower_source[f"{channel}_real"]),
            float(lower_source[f"{channel}_imaginary"]),
        )
        upper = complex(
            float(upper_source[f"{channel}_real"]),
            float(upper_source[f"{channel}_imaginary"]),
        )
        change = relative_complex_difference(lower, upper)
        rows.append(
            {
                "angular_node_id": node_id,
                "channel": channel,
                "lower_energy_order": min(ENERGY_ORDERS),
                "upper_energy_order": max(ENERGY_ORDERS),
                **complex_fields("lower_value", lower),
                **complex_fields("upper_value", upper),
                "relative_change": change,
                "passes_energy_gate": (
                    change <= INNER_RELATIVE_CHANGE_LIMIT
                    if channel == "eight_component_integral"
                    else ""
                ),
                "valid_for_order4_inner_energy_convergence": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def integrate_node(
    node: dict[str, Any],
    base_context: dict[str, Any],
    poles: dict[tuple[str, str, str], list[dict[str, complex]]],
    endpoints: dict[tuple[str, str, str], complex],
) -> dict[str, Any]:
    node_id = node["angular_node_id"]
    paths = node_paths(node_id)
    paths["root"].mkdir(parents=True, exist_ok=True)
    context = M5287.local_context(base_context, node)
    panels, mask_count, pole_center_count = node_panels(
        node_id,
        context,
        poles,
    )
    analytic = analytic_integrals(node_id, poles, endpoints)
    cache: dict[tuple[str, float, str], Any] = {}
    energy_rows: list[dict[str, Any]] = []
    component_rows: list[dict[str, Any]] = []
    regulator_rows: list[dict[str, Any]] = []
    evaluation_counter = 0
    audited_counter = 0
    for epsilon_id in REGULATOR_IDS:
        for order in ENERGY_ORDERS:
            quadrature_nodes, quadrature_weights = (
                np.polynomial.legendre.leggauss(order)
            )
            raw_components: dict[str, complex] = defaultdict(complex)
            regular_components: dict[str, complex] = defaultdict(complex)
            for panel_index, panel in enumerate(panels, start=1):
                left = float(panel["lower"])
                right = float(panel["upper"])
                half_width = 0.5 * (right - left)
                midpoint = 0.5 * (right + left)
                for local_index, (quadrature_node, quadrature_weight) in (
                    enumerate(
                        zip(quadrature_nodes, quadrature_weights),
                        start=1,
                    )
                ):
                    energy = midpoint + half_width * float(quadrature_node)
                    mapped_weight = half_width * float(quadrature_weight)
                    for component_id in COMPONENT_IDS:
                        evaluation_counter += 1
                        audit = evaluation_counter % 128 == 0
                        audited_counter += int(audit)
                        evaluation = M5287.evaluate_component_cached(
                            context,
                            epsilon_id,
                            component_id,
                            energy,
                            cache,
                            convergence_audit=audit,
                        )
                        raw = complex(evaluation["residue"])
                        key = (node_id, epsilon_id, component_id)
                        pole_singular = sum(
                            (
                                term["residue"]
                                / (energy - term["pole"])
                                for term in poles.get(key, [])
                            ),
                            0.0j,
                        )
                        endpoint_singular = (
                            endpoints[key] / energy
                            if key in endpoints
                            else 0.0j
                        )
                        regular = raw - pole_singular - endpoint_singular
                        raw_components[component_id] += mapped_weight * raw
                        regular_components[
                            component_id
                        ] += mapped_weight * regular
                        energy_rows.append(
                            {
                                "angular_node_id": node_id,
                                "soft_cosine": node["soft_cosine"],
                                "decay_cosine": node["decay_cosine"],
                                "epsilon_id": epsilon_id,
                                "energy_order": order,
                                "panel_id": panel["panel_id"],
                                "panel_index": panel_index,
                                "local_node_index": local_index,
                                "soft_energy": energy,
                                "mapped_energy_weight": mapped_weight,
                                "component_id": component_id,
                                "mask_active": evaluation["mask_active"],
                                **complex_fields("raw_residue", raw),
                                **complex_fields(
                                    "subtracted_pole_singular",
                                    pole_singular,
                                ),
                                **complex_fields(
                                    "subtracted_endpoint_singular",
                                    endpoint_singular,
                                ),
                                **complex_fields(
                                    "regularized_residue",
                                    regular,
                                ),
                                "coefficient_relative_change": evaluation[
                                    "coefficient_relative_change"
                                ],
                                "convergence_audited": evaluation[
                                    "convergence_audited"
                                ],
                                "valid_for_order4_inner_energy_run": True,
                                "valid_for_full_phase_space_coefficient": False,
                                "valid_for_numeric_UV_claim": False,
                                "valid_for_local_GR_claim": False,
                                "valid_for_full_MTS_claim": False,
                            }
                        )
                atomic_json(
                    STATUS,
                    {
                        "checkpoint": CHECKPOINT,
                        "state": "RUNNING",
                        "stage": "ORDER4_INNER_ENERGY",
                        "angular_node_id": node_id,
                        "epsilon_id": epsilon_id,
                        "energy_order": order,
                        "last_panel_index": panel_index,
                        "panel_count": len(panels),
                        "component_evaluation_count": evaluation_counter,
                    },
                )
            corrected: dict[str, complex] = {}
            for component_id in COMPONENT_IDS:
                corrected[component_id] = (
                    regular_components[component_id]
                    + analytic.get((epsilon_id, component_id), 0.0j)
                )
                component_rows.append(
                    {
                        "angular_node_id": node_id,
                        "soft_cosine": node["soft_cosine"],
                        "decay_cosine": node["decay_cosine"],
                        "epsilon_id": epsilon_id,
                        "energy_order": order,
                        "component_id": component_id,
                        **complex_fields(
                            "raw_energy_integral",
                            raw_components[component_id],
                        ),
                        **complex_fields(
                            "analytic_singular_integral",
                            analytic.get(
                                (epsilon_id, component_id),
                                0.0j,
                            ),
                        ),
                        **complex_fields(
                            "corrected_energy_integral",
                            corrected[component_id],
                        ),
                        "subtracted_pole_count": len(
                            poles.get(
                                (node_id, epsilon_id, component_id),
                                [],
                            )
                        ),
                        "subtracted_endpoint_term": (
                            (node_id, epsilon_id, component_id) in endpoints
                        ),
                        "valid_for_order4_inner_energy_run": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
            eight = sum(corrected.values(), 0.0j)
            six = sum(
                corrected[component_id]
                for component_id in LEGACY_SIX_IDS
            )
            hidden = sum(
                corrected[component_id] for component_id in HIDDEN_IDS
            )
            regulator_rows.append(
                {
                    "angular_node_id": node_id,
                    "soft_cosine": node["soft_cosine"],
                    "decay_cosine": node["decay_cosine"],
                    "row_type": "REGULATOR_INNER_ENERGY",
                    "epsilon_id": epsilon_id,
                    "energy_order": order,
                    **complex_fields("eight_component_integral", eight),
                    **complex_fields("six_component_integral", six),
                    **complex_fields("hidden_component_integral", hidden),
                    "energy_panel_count": len(panels),
                    "exact_mask_boundary_count": mask_count,
                    "subtracted_pole_count": sum(
                        len(
                            poles.get(
                                (node_id, epsilon_id, component_id),
                                [],
                            )
                        )
                        for component_id in COMPONENT_IDS
                    ),
                    "subtracted_endpoint_term_count": sum(
                        (node_id, epsilon_id, component_id) in endpoints
                        for component_id in COMPONENT_IDS
                    ),
                    "valid_for_order4_inner_energy_run": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    multiplier = physical_multiplier()
    regulator_lookup = {
        (int(row["energy_order"]), row["epsilon_id"]): row
        for row in regulator_rows
    }
    total_rows = list(regulator_rows)
    for order in ENERGY_ORDERS:
        physical_values: dict[str, complex] = {}
        for channel in (
            "eight_component_integral",
            "six_component_integral",
            "hidden_component_integral",
        ):
            e040 = regulator_lookup[(order, "E040")]
            e020 = regulator_lookup[(order, "E020")]
            physical_values[channel] = multiplier * (
                2.0
                * complex(
                    float(e020[f"{channel}_real"]),
                    float(e020[f"{channel}_imaginary"]),
                )
                - complex(
                    float(e040[f"{channel}_real"]),
                    float(e040[f"{channel}_imaginary"]),
                )
            )
        total_rows.append(
            {
                "angular_node_id": node_id,
                "soft_cosine": node["soft_cosine"],
                "decay_cosine": node["decay_cosine"],
                "row_type": "PHYSICAL_INNER_ENERGY",
                "epsilon_id": "2E020_MINUS_E040",
                "energy_order": order,
                **complex_fields(
                    "eight_component_integral",
                    physical_values["eight_component_integral"],
                ),
                **complex_fields(
                    "six_component_integral",
                    physical_values["six_component_integral"],
                ),
                **complex_fields(
                    "hidden_component_integral",
                    physical_values["hidden_component_integral"],
                ),
                "valid_for_order4_inner_energy_run": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    convergence = node_convergence_rows(node_id, total_rows)
    audited_rows = [
        row
        for row in energy_rows
        if parse_bool(row["convergence_audited"])
    ]
    maximum_coefficient_change = max(
        (
            float(row["coefficient_relative_change"])
            for row in audited_rows
        ),
        default=0.0,
    )
    eight_change = float(
        next(
            row
            for row in convergence
            if row["channel"] == "eight_component_integral"
        )["relative_change"]
    )
    all_finite = all(
        math.isfinite(float(row[field]))
        for rows in (component_rows, total_rows, convergence)
        for row in rows
        for field in row
        if field.endswith("_real")
        or field.endswith("_imaginary")
        or field.endswith("_magnitude")
        or field == "relative_change"
    )
    node_accepted = (
        len(component_rows) == 32
        and len(total_rows) == 6
        and len(convergence) == 3
        and all_finite
        and audited_counter > 0
        and maximum_coefficient_change
        <= COEFFICIENT_RELATIVE_CHANGE_LIMIT
    )
    write_csv(paths["energy_nodes"], energy_rows)
    write_csv(paths["component_totals"], component_rows)
    write_csv(paths["inner_totals"], total_rows)
    write_csv(paths["convergence"], convergence)
    result = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "angular_node_id": node_id,
        "singularity_atlas_sha256": digest(RESULT_5291),
        "node_run_completed": node_accepted,
        "node_energy_converged": (
            eight_change <= INNER_RELATIVE_CHANGE_LIMIT
        ),
        "eight_component_energy_relative_change": eight_change,
        "component_evaluation_count": evaluation_counter,
        "convergence_audit_count": audited_counter,
        "maximum_coefficient_relative_change": maximum_coefficient_change,
        "energy_panel_count": len(panels),
        "exact_mask_boundary_count": mask_count,
        "pole_center_count": pole_center_count,
        "energy_component_row_count": len(energy_rows),
        "component_total_count": len(component_rows),
        "inner_total_count": len(total_rows),
        "all_finite": all_finite,
    }
    atomic_json(paths["result"], result)
    return result


def aggregate_nodes(
    nodes: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    manifest: list[dict[str, Any]] = []
    components: list[dict[str, Any]] = []
    totals: list[dict[str, Any]] = []
    convergence: list[dict[str, Any]] = []
    for node in nodes:
        node_id = node["angular_node_id"]
        paths = node_paths(node_id)
        result = read_json(paths["result"])
        manifest.append(
            {
                "angular_node_id": node_id,
                "soft_cosine": node["soft_cosine"],
                "decay_cosine": node["decay_cosine"],
                "angular_weight": node["angular_weight"],
                "angular_jacobian": node["angular_jacobian"],
                "node_run_completed": result["node_run_completed"],
                "node_energy_converged": result[
                    "node_energy_converged"
                ],
                "eight_component_energy_relative_change": result[
                    "eight_component_energy_relative_change"
                ],
                "component_evaluation_count": result[
                    "component_evaluation_count"
                ],
                "energy_panel_count": result["energy_panel_count"],
                "energy_component_rows_path": str(paths["energy_nodes"]),
                "energy_component_rows_sha256": digest(
                    paths["energy_nodes"]
                ),
                "node_result_path": str(paths["result"]),
                "valid_for_order4_inner_energy_run": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        components.extend(read_csv(paths["component_totals"]))
        totals.extend(read_csv(paths["inner_totals"]))
        convergence.extend(read_csv(paths["convergence"]))
    return manifest, components, totals, convergence


def outer_rows(
    nodes: list[dict[str, Any]],
    totals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    weights = {
        row["angular_node_id"]: (
            float(row["angular_weight"])
            * float(row["angular_jacobian"])
        )
        for row in nodes
    }
    rows: list[dict[str, Any]] = []
    for order in ENERGY_ORDERS:
        values: dict[str, complex] = {}
        for channel in (
            "eight_component_integral",
            "six_component_integral",
            "hidden_component_integral",
        ):
            values[channel] = sum(
                weights[row["angular_node_id"]]
                * complex(
                    float(row[f"{channel}_real"]),
                    float(row[f"{channel}_imaginary"]),
                )
                for row in totals
                if row["row_type"] == "PHYSICAL_INNER_ENERGY"
                and int(row["energy_order"]) == order
            )
        rows.append(
            {
                "angular_order": ANGULAR_ORDER,
                "energy_order": order,
                **complex_fields(
                    "eight_component_integral",
                    values["eight_component_integral"],
                ),
                **complex_fields(
                    "six_component_integral",
                    values["six_component_integral"],
                ),
                **complex_fields(
                    "hidden_component_integral",
                    values["hidden_component_integral"],
                ),
                "angular_endpoint_limit": float(
                    M5280.M5274.M5270.ANGULAR_LIMIT
                ),
                "angular_jacobian": M5280.M5278.ANGULAR_JACOBIAN,
                "valid_for_order4_angular_smoke": True,
                "valid_for_angular_convergence": False,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def angular_comparison_rows(
    outer4: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    order2_source = next(
        row
        for row in read_csv(OUTER_5290)
        if int(row["energy_order"]) == max(ENERGY_ORDERS)
    )
    order4_source = next(
        row
        for row in outer4
        if int(row["energy_order"]) == max(ENERGY_ORDERS)
    )
    rows: list[dict[str, Any]] = []
    for channel in (
        "eight_component_integral",
        "six_component_integral",
        "hidden_component_integral",
    ):
        lower = complex(
            float(order2_source[f"{channel}_real"]),
            float(order2_source[f"{channel}_imaginary"]),
        )
        upper = complex(
            float(order4_source[f"{channel}_real"]),
            float(order4_source[f"{channel}_imaginary"]),
        )
        change = relative_complex_difference(lower, upper)
        rows.append(
            {
                "channel": channel,
                "lower_angular_order": 2,
                "upper_angular_order": 4,
                "energy_order": max(ENERGY_ORDERS),
                **complex_fields("order2_value", lower),
                **complex_fields("order4_value", upper),
                "relative_change": change,
                "passes_order2_order4_smoke_gate": (
                    change <= ANGULAR_RELATIVE_CHANGE_LIMIT
                    if channel == "eight_component_integral"
                    else ""
                ),
                "valid_for_order2_order4_angular_comparison": True,
                "valid_for_full_angular_convergence": False,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    NODE_RUNS.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5291,
        RESULT_5291,
        VALIDATION_5291,
        ANGULAR_NODES_5291,
        POLE_RESIDUES_5291,
        ENDPOINT_COEFFICIENTS_5291,
        ENDPOINT_CANCELLATIONS_5291,
        BOUNDS_5291,
        OUTER_5290,
    )
    parent = read_json(RESULT_5291)
    nodes = read_csv(ANGULAR_NODES_5291)
    pole_rows = [
        row
        for row in read_csv(POLE_RESIDUES_5291)
        if parse_bool(row["valid_for_order4_pole_subtraction"])
    ]
    endpoint_rows = [
        row
        for row in read_csv(ENDPOINT_COEFFICIENTS_5291)
        if parse_bool(row["valid_for_lower_endpoint_log_subtraction"])
    ]
    checks = {
        "required_sources_exist": all(path.exists() for path in required),
        "parent_5291_accepted": bool(parent["acceptance_passed"]),
        "parent_5291_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5291)
        ),
        "sixteen_order4_nodes_parse": len(nodes) == 16,
        "all_subtraction_poles_numeric": bool(pole_rows)
        and all(
            math.isfinite(float(row[field]))
            for row in pole_rows
            for field in (
                "pole_real",
                "pole_imaginary",
                "true_limit_residue_real",
                "true_limit_residue_imaginary",
            )
        ),
        "sixty_four_endpoint_terms_available": len(endpoint_rows) == 64,
        "all_endpoint_cancellations_certified": all(
            parse_bool(row["endpoint_cancellation_passed"])
            for row in read_csv(ENDPOINT_CANCELLATIONS_5291)
        ),
        "bounded_ambiguous_error_below_budget": (
            float(
                parent[
                    "bounded_ambiguous_global_relative_error_bound"
                ]
            )
            <= float(
                parent[
                    "bounded_ambiguous_global_relative_bound_limit"
                ]
            )
        ),
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
        "angular_node_count": len(nodes),
        "subtracted_pole_term_count": len(pole_rows),
        "subtracted_endpoint_term_count": len(endpoint_rows),
        "already_completed_node_count": sum(
            node_cache_valid(node) for node in nodes
        ),
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_ORDER4_INNER_ENERGY"
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
    set_below_normal_priority()
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    M5291.install_bounded_root_refinement_fallback()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5292 dry run did not pass")
    parent = read_json(RESULT_5291)
    nodes = read_csv(ANGULAR_NODES_5291)
    poles = pole_lookup()
    endpoints = endpoint_lookup()
    base_context = M5280.source_context()
    for node_index, node in enumerate(nodes, start=1):
        if not node_cache_valid(node):
            integrate_node(node, base_context, poles, endpoints)
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "ORDER4_NODE_SEQUENCE",
                "last_completed_angular_node_id": node[
                    "angular_node_id"
                ],
                "completed_angular_node_count": node_index,
                "total_angular_node_count": len(nodes),
            },
        )
    manifest, components, totals, convergence = aggregate_nodes(nodes)
    outer = outer_rows(nodes, totals)
    comparison = angular_comparison_rows(outer)
    write_csv(NODE_MANIFEST, manifest)
    write_csv(COMPONENT_TOTALS, components)
    write_csv(INNER_TOTALS, totals)
    write_csv(INNER_CONVERGENCE, convergence)
    write_csv(OUTER_TOTALS, outer)
    write_csv(ANGULAR_COMPARISON, comparison)

    eight_node_changes = [
        float(row["relative_change"])
        for row in convergence
        if row["channel"] == "eight_component_integral"
    ]
    maximum_node_change = max(eight_node_changes)
    outer_lookup = {
        int(row["energy_order"]): row for row in outer
    }
    outer4 = complex(
        float(
            outer_lookup[min(ENERGY_ORDERS)][
                "eight_component_integral_real"
            ]
        ),
        float(
            outer_lookup[min(ENERGY_ORDERS)][
                "eight_component_integral_imaginary"
            ]
        ),
    )
    outer8 = complex(
        float(
            outer_lookup[max(ENERGY_ORDERS)][
                "eight_component_integral_real"
            ]
        ),
        float(
            outer_lookup[max(ENERGY_ORDERS)][
                "eight_component_integral_imaginary"
            ]
        ),
    )
    outer_energy_change = relative_complex_difference(outer4, outer8)
    angular_change = float(
        next(
            row
            for row in comparison
            if row["channel"] == "eight_component_integral"
        )["relative_change"]
    )
    all_finite = all(
        math.isfinite(float(row[field]))
        for rows in (components, totals, convergence, outer, comparison)
        for row in rows
        for field in row
        if field.endswith("_real")
        or field.endswith("_imaginary")
        or field.endswith("_magnitude")
        or field == "relative_change"
    )
    checks = {
        "all_sixteen_node_runs_completed": (
            len(manifest) == 16
            and all(parse_bool(row["node_run_completed"]) for row in manifest)
        ),
        "all_node_shards_hash": all(
            digest(Path(row["energy_component_rows_path"]))
            == row["energy_component_rows_sha256"]
            for row in manifest
        ),
        "component_totals_complete": len(components) == 16 * 32,
        "inner_totals_complete": len(totals) == 16 * 6,
        "inner_convergence_complete": len(convergence) == 16 * 3,
        "all_values_finite": all_finite,
        "all_nodes_pass_inner_energy_gate": (
            maximum_node_change <= INNER_RELATIVE_CHANGE_LIMIT
        ),
        "order4_outer_passes_energy_gate": (
            outer_energy_change <= OUTER_ENERGY_RELATIVE_CHANGE_LIMIT
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    angular_smoke_passed = (
        angular_change <= ANGULAR_RELATIVE_CHANGE_LIMIT
    )
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "order4-inner-energy-and-order2-comparison",
        "checks": checks,
        "acceptance_passed": accepted,
        "angular_node_count": len(nodes),
        "completed_node_count": len(manifest),
        "component_evaluation_count": sum(
            int(row["component_evaluation_count"]) for row in manifest
        ),
        "component_total_count": len(components),
        "inner_total_count": len(totals),
        "inner_convergence_count": len(convergence),
        "maximum_node_inner_energy_relative_change": maximum_node_change,
        "order4_outer_energy_relative_change": outer_energy_change,
        "order2_order4_angular_relative_change": angular_change,
        "inner_energy_relative_change_limit": (
            INNER_RELATIVE_CHANGE_LIMIT
        ),
        "angular_relative_change_limit": ANGULAR_RELATIVE_CHANGE_LIMIT,
        "order2_order4_angular_smoke_passed": angular_smoke_passed,
        "order4_energy8_eight_component_integral": {
            "real": outer8.real,
            "imaginary": outer8.imag,
        },
        "bounded_ambiguous_global_absolute_error_bound": parent[
            "bounded_ambiguous_global_absolute_error_bound"
        ],
        "bounded_ambiguous_global_relative_error_bound": parent[
            "bounded_ambiguous_global_relative_error_bound"
        ],
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
            "resumable_node_shards": str(NODE_RUNS),
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "ORDER2_ORDER4_ANGULAR_CHANGE_PASSES_SMOKE__"
            "REQUIRE_ORDER6_CONFIRMATION"
            if accepted and angular_smoke_passed
            else "ORDER4_VALID_BUT_ANGULAR_NOT_CONVERGED__"
            "ADVANCE_ORDER6"
            if accepted
            else "ORDER4_INNER_ENERGY_REQUIRES_LOCAL_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_order4_inner_energy_run": accepted,
            "valid_for_order2_order4_angular_smoke": accepted,
            "valid_for_full_angular_convergence": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "A valid order-two/order-four comparison is only the "
                "first angular convergence rung. Order six is required "
                "even if the order-two/order-four smoke gate passes."
            ),
        },
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETE" if accepted else "FAILED",
            "decision": result["decision"],
            "maximum_node_inner_energy_relative_change": maximum_node_change,
            "order4_outer_energy_relative_change": outer_energy_change,
            "order2_order4_angular_relative_change": angular_change,
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
    checks = "\n".join(
        f"- `{key}`: **{'PASS' if value else 'FAIL'}**"
        for key, value in sorted(result["checks"].items())
    )
    outer = result["order4_energy8_eight_component_integral"]
    text = f"""# 5292 — Order-four inner energy and order-two comparison

## Result

All `{result['angular_node_count']}` order-four angular nodes were
evaluated with the complete 5291 singular atlas. The large raw
component-node tables remain in resumable per-node shards rather than
being duplicated into one oversized file.

- component evaluations:
  `{result['component_evaluation_count']}`;
- maximum nodewise energy `4 -> 8` change:
  `{result['maximum_node_inner_energy_relative_change']:.12g}`;
- order-four outer energy `4 -> 8` change:
  `{result['order4_outer_energy_relative_change']:.12g}`;
- order-two to order-four angular change:
  `{result['order2_order4_angular_relative_change']:.12g}`;
- order-four energy-eight total:
  `{outer['real']:.12g} {outer['imaginary']:+.12g} i`;
- bounded ambiguous-pole relative error:
  `{result['bounded_ambiguous_global_relative_error_bound']:.12g}`.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Interpretation

The energy coordinate and angular coordinate are tested separately.
Passing the inner-energy gates shows that any order-two/order-four
difference is angular, not a disguised failed energy quadrature.

## Claim boundary

No full phase-space or UV coefficient is claimed. A single
order-two/order-four comparison cannot establish angular convergence;
order six remains mandatory even if the first angular smoke gate passes.

## Next target

{result['decision']}
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    required = (
        DRY_RUN,
        NODE_MANIFEST,
        COMPONENT_TOTALS,
        INNER_TOTALS,
        INNER_CONVERGENCE,
        OUTER_TOTALS,
        ANGULAR_COMPARISON,
        RESULT,
        STATUS,
    )
    result = read_json(RESULT)
    source_files = result["source_files"]
    source_hashes_match = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in source_files
    )
    manifest = read_csv(NODE_MANIFEST)
    csv_paths = (
        NODE_MANIFEST,
        COMPONENT_TOTALS,
        INNER_TOTALS,
        INNER_CONVERGENCE,
        OUTER_TOTALS,
        ANGULAR_COMPARISON,
    )
    parsed = {path: read_csv(path) for path in csv_paths}
    all_text = "\n".join(
        path.read_text(encoding="utf-8") for path in required
    )
    claims_false = all(
        not bool(result["claim_boundary"][field])
        for field in CLAIM_FIELDS
    )
    current_formal_digest = M5283.formal_inventory_digest()
    gates = [
        validation_gate(
            "SOURCE_PATHS_EXIST",
            all(Path(row["path"]).exists() for row in source_files),
            f"{len(source_files)} source paths",
        ),
        validation_gate(
            "SOURCE_HASHES_MATCH",
            source_hashes_match,
            "all recorded source hashes reproduce",
        ),
        validation_gate(
            "PARENT_5291_ACCEPTED",
            bool(read_json(RESULT_5291)["acceptance_passed"]),
            read_json(RESULT_5291)["decision"],
        ),
        validation_gate(
            "ORDER4_INNER_ENERGY_RUN_ACCEPTED",
            bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            all(parsed[path] for path in csv_paths),
            f"{len(csv_paths)}/{len(csv_paths)} non-empty CSVs",
        ),
        validation_gate(
            "SIXTEEN_NODE_SHARDS_HASH",
            len(manifest) == 16
            and all(
                Path(row["energy_component_rows_path"]).exists()
                and digest(Path(row["energy_component_rows_path"]))
                == row["energy_component_rows_sha256"]
                for row in manifest
            ),
            "16/16 resumable node shards",
        ),
        validation_gate(
            "ENERGY_CONVERGENCE_CLOSED",
            float(result["maximum_node_inner_energy_relative_change"])
            <= INNER_RELATIVE_CHANGE_LIMIT
            and float(result["order4_outer_energy_relative_change"])
            <= OUTER_ENERGY_RELATIVE_CHANGE_LIMIT,
            (
                "node="
                f"{result['maximum_node_inner_energy_relative_change']}; "
                "outer="
                f"{result['order4_outer_energy_relative_change']}"
            ),
        ),
        validation_gate(
            "NO_MISSING_MARKERS",
            "MISSING_" not in all_text,
            "no MISSING_ token in checkpoint summary artifacts",
        ),
        validation_gate(
            "CLAIMS_LOCKED_FALSE",
            claims_false,
            "phase-space, UV, local-GR, and full-MTS claims false",
        ),
        validation_gate(
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            current_formal_digest
            == result["formalization_workbench_reference_digest"],
            (
                "reference="
                f"{result['formalization_workbench_reference_digest']}; "
                f"current={current_formal_digest}"
            ),
        ),
        validation_gate(
            "RESOURCE_CONTRACT_RECORDED",
            result["resource_contract"]["maximum_task_python_processes"]
            == 1
            and result["resource_contract"]["worker_math_threads"] == 1
            and result["resource_contract"]["windows_priority"]
            == "BelowNormal",
            "one single-thread BelowNormal process with node shards",
        ),
    ]
    passed = all(row["passed"] for row in gates)
    write_csv(VALIDATION, gates)
    write_csv(RESIDUAL_VALIDATION, gates)
    render_document(result, passed)
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_ORDER4_INNER_ENERGY_AND_ORDER2_COMPARISON"
            if passed
            else "ORDER4_INNER_ENERGY_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
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
