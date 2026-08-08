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
SOURCE = FUNCTIONAL_RG / "5290"

SCRIPT_5289 = SCRIPTS / "Y5_R2FR_5289_MC04_MC12_angular_pole_derivation.py"
RESULT_5289 = FUNCTIONAL_RG / "5289" / "MC04_MC12_angular_pole_result.json"
VALIDATION_5289 = (
    FUNCTIONAL_RG / "5289" / "MC04_MC12_angular_pole_validation.csv"
)
RESULT_5288 = (
    FUNCTIONAL_RG / "5288" / "failed_angular_node_singularity_result.json"
)
VALIDATION_5288 = (
    FUNCTIONAL_RG / "5288" / "failed_angular_node_singularity_validation.csv"
)
POLES_5288 = (
    FUNCTIONAL_RG / "5288" / "failed_node_selected_pole_residues.csv"
)
POLES_5289 = (
    FUNCTIONAL_RG / "5289" / "MC04_MC12_selected_pole_residues.csv"
)
ENDPOINTS_5288 = (
    FUNCTIONAL_RG / "5288" / "lower_endpoint_selected_coefficients.csv"
)
ENDPOINT_PAIRS_5288 = (
    FUNCTIONAL_RG / "5288" / "lower_endpoint_physical_coefficients.csv"
)
ENERGY_NODES_5287 = (
    FUNCTIONAL_RG / "5287" / "angular_node_energy_component_nodes.csv"
)
COMPONENT_TOTALS_5287 = (
    FUNCTIONAL_RG / "5287" / "angular_node_inner_component_totals.csv"
)
TOTALS_5287 = (
    FUNCTIONAL_RG / "5287" / "angular_node_inner_energy_totals.csv"
)
ANGULAR_NODES_5286 = FUNCTIONAL_RG / "5286" / "angular_order2_nodes.csv"

DRY_RUN = SOURCE / "all_family_subtraction_dry_run.json"
CORRECTIONS = SOURCE / "all_family_component_corrections.csv"
COMPONENT_TOTALS = SOURCE / "all_family_component_totals.csv"
INNER_TOTALS = SOURCE / "all_family_inner_energy_totals.csv"
CONVERGENCE = SOURCE / "all_family_inner_energy_convergence.csv"
OUTER_TOTALS = SOURCE / "all_family_order2_outer_totals.csv"
RESULT = SOURCE / "all_family_subtraction_result.json"
VALIDATION = SOURCE / "all_family_subtraction_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5290_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5290-Y5-R2FR-all-family-stored-node-subtraction-reassembly.md"

CHECKPOINT = 5290
PARENT_CHECKPOINT = 5289
MARKER = "MTS_5290_ALL_FAMILY_STORED_NODE_SUBTRACTION_REASSEMBLY"
REVISION = "all-family-stored-node-subtraction-reassembly-v1"
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
OUTER_RELATIVE_CHANGE_LIMIT = 5.0e-3
CLAIM_FIELDS = (
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    process_handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(process_handle, 0x00004000)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5289 = load_module("mts_5289_for_5290", SCRIPT_5289)
M5288 = M5289.M5288
M5287 = M5289.M5287
M5283 = M5289.M5283
M5267 = M5289.M5267


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
        SCRIPT_5289,
        RESULT_5289,
        VALIDATION_5289,
        RESULT_5288,
        VALIDATION_5288,
        POLES_5288,
        POLES_5289,
        ENDPOINTS_5288,
        ENDPOINT_PAIRS_5288,
        ENERGY_NODES_5287,
        COMPONENT_TOTALS_5287,
        TOTALS_5287,
        ANGULAR_NODES_5286,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def material_pole_lookup() -> dict[
    tuple[str, str, str],
    list[dict[str, complex]],
]:
    lookup: dict[
        tuple[str, str, str],
        list[dict[str, complex]],
    ] = defaultdict(list)
    for path in (POLES_5288, POLES_5289):
        for row in read_csv(path):
            if not parse_bool(row["material_pole"]):
                continue
            if not parse_bool(row["pole_residue_controls_pass"]):
                raise RuntimeError(f"uncontrolled material pole in {path}")
            key = (
                row["angular_node_id"],
                row["epsilon_id"],
                row["component_id"],
            )
            lookup[key].append(
                {
                    "pole": complex(
                        float(row["pole_real"]),
                        float(row["pole_imaginary"]),
                    ),
                    "residue": complex(
                        float(row["true_limit_residue_real"]),
                        float(row["true_limit_residue_imaginary"]),
                    ),
                }
            )
    return lookup


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
        for row in read_csv(ENDPOINTS_5288)
        if parse_bool(row["lower_endpoint_log_singular"])
        and parse_bool(row["endpoint_fit_controls_pass"])
    }


def energy_node_groups() -> dict[
    tuple[str, str, int, str],
    list[dict[str, str]],
]:
    groups: dict[
        tuple[str, str, int, str],
        list[dict[str, str]],
    ] = defaultdict(list)
    for row in read_csv(ENERGY_NODES_5287):
        groups[
            (
                row["angular_node_id"],
                row["epsilon_id"],
                int(row["energy_order"]),
                row["component_id"],
            )
        ].append(row)
    return groups


def integration_multiplier() -> float:
    parent_total = next(
        row
        for row in read_csv(M5283.TOTALS_5281)
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    )
    return float(parent_total["kernel_multiplier"]) * float(
        parent_total["physical_A00_weight"]
    )


def reassemble_components() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    poles = material_pole_lookup()
    endpoints = endpoint_lookup()
    node_groups = energy_node_groups()
    minimum = float(M5267.ENERGY_MINIMUM)
    maximum = float(M5267.ENERGY_MAXIMUM)
    correction_rows: list[dict[str, Any]] = []
    component_rows: list[dict[str, Any]] = []
    for source in read_csv(COMPONENT_TOTALS_5287):
        key = (
            source["angular_node_id"],
            source["epsilon_id"],
            int(source["energy_order"]),
            source["component_id"],
        )
        nodes = node_groups[key]
        local_poles = poles.get((key[0], key[1], key[3]), [])
        endpoint = endpoints.get((key[0], key[1], key[3]), 0.0j)
        pole_quadrature = 0.0j
        pole_analytic = 0.0j
        for pole_row in local_poles:
            pole = pole_row["pole"]
            residue = pole_row["residue"]
            pole_quadrature += sum(
                float(row["mapped_energy_weight"])
                * residue
                / (float(row["soft_energy"]) - pole)
                for row in nodes
            )
            pole_analytic += residue * (
                cmath.log(maximum - pole)
                - cmath.log(minimum - pole)
            )
        endpoint_quadrature = (
            sum(
                float(row["mapped_energy_weight"])
                * endpoint
                / float(row["soft_energy"])
                for row in nodes
            )
            if endpoint != 0.0j
            else 0.0j
        )
        endpoint_analytic = (
            endpoint * math.log(maximum / minimum)
            if endpoint != 0.0j
            else 0.0j
        )
        old_value = complex(
            float(source["corrected_energy_integral_real"]),
            float(source["corrected_energy_integral_imaginary"]),
        )
        adjustment = (
            pole_analytic
            - pole_quadrature
            + endpoint_analytic
            - endpoint_quadrature
        )
        corrected = old_value + adjustment
        common = {
            "angular_node_id": key[0],
            "epsilon_id": key[1],
            "energy_order": key[2],
            "component_id": key[3],
        }
        correction_rows.append(
            {
                **common,
                "material_pole_count": len(local_poles),
                "endpoint_term_present": endpoint != 0.0j,
                **complex_fields("pole_quadrature", pole_quadrature),
                **complex_fields("pole_analytic", pole_analytic),
                **complex_fields(
                    "endpoint_quadrature",
                    endpoint_quadrature,
                ),
                **complex_fields(
                    "endpoint_analytic",
                    endpoint_analytic,
                ),
                **complex_fields("total_adjustment", adjustment),
                "stored_node_count": len(nodes),
                "new_point_evaluation_count": 0,
                "valid_for_all_family_stored_node_reassembly": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        component_rows.append(
            {
                **common,
                **complex_fields("parent_corrected_integral", old_value),
                **complex_fields(
                    "all_family_corrected_integral",
                    corrected,
                ),
                "material_pole_count": len(local_poles),
                "endpoint_term_present": endpoint != 0.0j,
                "new_point_evaluation_count": 0,
                "valid_for_all_family_stored_node_reassembly": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return correction_rows, component_rows


def total_rows(
    components: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    angular_nodes = {
        row["angular_node_id"]: row
        for row in read_csv(ANGULAR_NODES_5286)
    }
    lookup = {
        (
            row["angular_node_id"],
            row["epsilon_id"],
            int(row["energy_order"]),
            row["component_id"],
        ): complex(
            float(row["all_family_corrected_integral_real"]),
            float(row["all_family_corrected_integral_imaginary"]),
        )
        for row in components
    }
    rows: list[dict[str, Any]] = []
    multiplier = integration_multiplier()
    for angular_node_id, angular_node in angular_nodes.items():
        regulator_values: dict[
            tuple[int, str],
            dict[str, complex],
        ] = {}
        for order in ENERGY_ORDERS:
            for epsilon_id in REGULATOR_IDS:
                local = {
                    component_id: lookup[
                        (
                            angular_node_id,
                            epsilon_id,
                            order,
                            component_id,
                        )
                    ]
                    for component_id in COMPONENT_IDS
                }
                channels = {
                    "eight_component_integral": sum(
                        local.values(),
                        0.0j,
                    ),
                    "six_component_integral": sum(
                        (
                            local[component_id]
                            for component_id in LEGACY_SIX_IDS
                        ),
                        0.0j,
                    ),
                    "hidden_component_integral": sum(
                        (
                            local[component_id]
                            for component_id in HIDDEN_IDS
                        ),
                        0.0j,
                    ),
                }
                regulator_values[(order, epsilon_id)] = channels
                rows.append(
                    {
                        "angular_node_id": angular_node_id,
                        "soft_cosine": angular_node["soft_cosine"],
                        "decay_cosine": angular_node["decay_cosine"],
                        "row_type": "REGULATOR_INNER_ENERGY",
                        "epsilon_id": epsilon_id,
                        "energy_order": order,
                        **complex_fields(
                            "eight_component_integral",
                            channels["eight_component_integral"],
                        ),
                        **complex_fields(
                            "six_component_integral",
                            channels["six_component_integral"],
                        ),
                        **complex_fields(
                            "hidden_component_integral",
                            channels["hidden_component_integral"],
                        ),
                        "valid_for_all_family_inner_energy": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
            physical = {
                channel: multiplier
                * (
                    2.0
                    * regulator_values[(order, "E020")][channel]
                    - regulator_values[(order, "E040")][channel]
                )
                for channel in regulator_values[(order, "E040")]
            }
            rows.append(
                {
                    "angular_node_id": angular_node_id,
                    "soft_cosine": angular_node["soft_cosine"],
                    "decay_cosine": angular_node["decay_cosine"],
                    "row_type": "PHYSICAL_INNER_ENERGY",
                    "epsilon_id": "2E020_MINUS_E040",
                    "energy_order": order,
                    **complex_fields(
                        "eight_component_integral",
                        physical["eight_component_integral"],
                    ),
                    **complex_fields(
                        "six_component_integral",
                        physical["six_component_integral"],
                    ),
                    **complex_fields(
                        "hidden_component_integral",
                        physical["hidden_component_integral"],
                    ),
                    "valid_for_all_family_inner_energy": True,
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
        SCRIPT_5289,
        RESULT_5289,
        VALIDATION_5289,
        RESULT_5288,
        VALIDATION_5288,
        POLES_5288,
        POLES_5289,
        ENDPOINTS_5288,
        ENDPOINT_PAIRS_5288,
        ENERGY_NODES_5287,
        COMPONENT_TOTALS_5287,
        TOTALS_5287,
        ANGULAR_NODES_5286,
    )
    parent = read_json(RESULT_5289)
    checks = {
        "required_sources_exist": all(path.exists() for path in required),
        "parent_5289_accepted": bool(parent["acceptance_passed"]),
        "parent_5289_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5289)
        ),
        "parent_authorizes_combined_runner": bool(
            parent["claim_boundary"][
                "valid_for_all_family_combined_subtraction_runner"
            ]
        ),
        "twelve_material_pole_rows_available": (
            sum(
                parse_bool(row["material_pole"])
                for path in (POLES_5288, POLES_5289)
                for row in read_csv(path)
            )
            == 12
        ),
        "sixteen_endpoint_rows_available": (
            sum(
                parse_bool(row["lower_endpoint_log_singular"])
                for row in read_csv(ENDPOINTS_5288)
            )
            == 16
        ),
        "stored_nodes_and_components_parse": (
            bool(read_csv(ENERGY_NODES_5287))
            and len(read_csv(COMPONENT_TOTALS_5287)) == 128
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
        "decision": (
            "DRY_RUN_ACCEPTED__REASSEMBLE_ALL_CERTIFIED_SINGULAR_TERMS"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "new_point_evaluation_count": 0,
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
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5290 dry run did not pass")
    parent = read_json(RESULT_5289)
    corrections, components = reassemble_components()
    totals = total_rows(components)
    convergence = M5287.convergence_rows(totals)
    outer = M5287.outer_rows(read_csv(ANGULAR_NODES_5286), totals)
    node_eight_changes = [
        float(row["relative_change"])
        for row in convergence
        if row["channel"] == "eight_component_integral"
    ]
    maximum_node_change = max(node_eight_changes)
    outer_lookup = {
        int(row["energy_order"]): row for row in outer
    }
    outer_order4 = complex(
        float(outer_lookup[4]["eight_component_integral_real"]),
        float(outer_lookup[4]["eight_component_integral_imaginary"]),
    )
    outer_order8 = complex(
        float(outer_lookup[8]["eight_component_integral_real"]),
        float(outer_lookup[8]["eight_component_integral_imaginary"]),
    )
    outer_change = relative_complex_difference(
        outer_order4,
        outer_order8,
    )
    untouched = [
        row
        for row in components
        if int(row["material_pole_count"]) == 0
        and not parse_bool(row["endpoint_term_present"])
    ]
    maximum_untouched_replay_error = max(
        (
            relative_complex_difference(
                complex(
                    float(row["parent_corrected_integral_real"]),
                    float(row["parent_corrected_integral_imaginary"]),
                ),
                complex(
                    float(row["all_family_corrected_integral_real"]),
                    float(row["all_family_corrected_integral_imaginary"]),
                ),
            )
            for row in untouched
        ),
        default=0.0,
    )
    maximum_endpoint_pair_residual = max(
        max(
            float(
                row[
                    "E040_pair_cancellation_relative_residual"
                ]
            ),
            float(
                row[
                    "E020_pair_cancellation_relative_residual"
                ]
            ),
            float(
                row[
                    "physical_pair_cancellation_relative_residual"
                ]
            ),
        )
        for row in read_csv(ENDPOINT_PAIRS_5288)
    )
    energy_converged = (
        maximum_node_change <= INNER_RELATIVE_CHANGE_LIMIT
        and outer_change <= OUTER_RELATIVE_CHANGE_LIMIT
    )
    finite_fields = all(
        math.isfinite(float(value))
        for rows in (corrections, components, totals, convergence, outer)
        for row in rows
        for field, value in row.items()
        if field.endswith(("_real", "_imaginary", "_magnitude"))
    )
    checks = {
        "all_128_components_reassembled": len(components) == 128,
        "all_128_correction_rows_written": len(corrections) == 128,
        "all_24_inner_total_rows_written": len(totals) == 24,
        "no_new_point_evaluations": all(
            int(row["new_point_evaluation_count"]) == 0
            for row in corrections
        ),
        "untouched_components_replay_exactly": (
            maximum_untouched_replay_error <= 1.0e-15
        ),
        "endpoint_pair_cancellation_retained": (
            maximum_endpoint_pair_residual <= 1.0e-8
        ),
        "all_outputs_finite": finite_fields,
        "all_nodes_pass_inner_energy_gate": (
            maximum_node_change <= INNER_RELATIVE_CHANGE_LIMIT
        ),
        "order2_outer_passes_energy_gate": (
            outer_change <= OUTER_RELATIVE_CHANGE_LIMIT
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
        "mode": "all-family-stored-node-subtraction-reassembly",
        "checks": checks,
        "acceptance_passed": accepted,
        "component_correction_count": len(corrections),
        "component_total_count": len(components),
        "inner_total_count": len(totals),
        "material_pole_count": sum(
            len(rows) for rows in material_pole_lookup().values()
        ),
        "endpoint_term_count": len(endpoint_lookup()),
        "new_point_evaluation_count": 0,
        "maximum_untouched_component_replay_error": (
            maximum_untouched_replay_error
        ),
        "maximum_endpoint_pair_cancellation_residual": (
            maximum_endpoint_pair_residual
        ),
        "maximum_node_inner_energy_relative_change": (
            maximum_node_change
        ),
        "outer_energy_order_relative_change": outer_change,
        "order2_energy8_eight_component_integral": {
            "real": outer_order8.real,
            "imaginary": outer_order8.imag,
        },
        "combined_subtraction_energy_converged": energy_converged,
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
            "new_point_evaluation_count": 0,
            "sustained_redline_forbidden": True,
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "ACCEPT_ORDER2_ALL_FAMILY_ENERGY_CONVERGENCE__"
            "ADVANCE_ANGULAR_ORDER_COMPARISON"
            if accepted and energy_converged
            else "ALL_FAMILY_REASSEMBLY_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_all_family_stored_node_reassembly": accepted,
            "valid_for_order2_inner_energy_convergence": (
                accepted and energy_converged
            ),
            "valid_for_angular_order_comparison": (
                accepted and energy_converged
            ),
            "valid_for_angular_convergence": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "All certified pole and endpoint terms are now "
                "reassembled and the order-two inner-energy rule "
                "converges. Angular-order and endpoint-cap convergence "
                "remain open."
            ),
        },
    }
    write_csv(CORRECTIONS, corrections)
    write_csv(COMPONENT_TOTALS, components)
    write_csv(INNER_TOTALS, totals)
    write_csv(CONVERGENCE, convergence)
    write_csv(OUTER_TOTALS, outer)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
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


def render_document(result: dict[str, Any], validation_passed: bool) -> None:
    text = f"""# 5290 — All-family stored-node subtraction reassembly

## Result

This checkpoint reuses all `42,624` component-node evaluations from 5287.
It adds no new point evaluations. The stored component integrals are
corrected by the analytic integrals minus the stored-node quadrature sums
of:

- the `MC03/MC08` promoted material poles from 5288;
- the `MC04/MC12` promoted material poles from 5289;
- the paired lower-endpoint `A_X/E` terms from 5288.

The endpoint analytic terms remain pair-cancelled; their maximum relative
pair residual is
`{result['maximum_endpoint_pair_cancellation_residual']:.12g}`.

## Convergence

- material pole terms: `{result['material_pole_count']}`;
- endpoint terms: `{result['endpoint_term_count']}`;
- maximum nodewise energy `4 -> 8` change:
  `{result['maximum_node_inner_energy_relative_change']:.12g}`;
- order-two outer energy `4 -> 8` change:
  `{result['outer_energy_order_relative_change']:.12g}`;
- order-two energy-8 value:
  `{result['order2_energy8_eight_component_integral']}`;
- validation passed: `{validation_passed}`.

## Decision

`{result['decision']}`

This closes the inner-energy convergence gate at angular order two. It
does not yet close angular-order convergence, angular endpoint caps, full
phase space, UV, local-GR, or full-MTS claims.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    required_csvs = (
        CORRECTIONS,
        COMPONENT_TOTALS,
        INNER_TOTALS,
        CONVERGENCE,
        OUTER_TOTALS,
    )
    if not RESULT.exists():
        raise RuntimeError(f"missing result: {RESULT}")
    result = read_json(RESULT)
    csv_rows = {path: read_csv(path) for path in required_csvs}
    serialized = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (*required_csvs, RESULT)
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
            "PARENT_5289_ACCEPTED",
            bool(read_json(RESULT_5289)["acceptance_passed"]),
            str(read_json(RESULT_5289)["decision"]),
        ),
        validation_gate(
            "ALL_FAMILY_REASSEMBLY_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            len(csv_rows) == len(required_csvs)
            and all(csv_rows.values()),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "ENERGY_CONVERGENCE_CLOSED",
            bool(result["combined_subtraction_energy_converged"]),
            (
                f"node={result['maximum_node_inner_energy_relative_change']}; "
                f"outer={result['outer_energy_order_relative_change']}"
            ),
        ),
        validation_gate(
            "NO_NEW_POINT_EVALUATIONS",
            result["new_point_evaluation_count"] == 0,
            "stored-node algebraic reassembly",
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
            "one single-thread process; zero new point evaluations",
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
            "VALIDATED_ALL_FAMILY_STORED_NODE_REASSEMBLY"
            if passed
            else "ALL_FAMILY_STORED_NODE_VALIDATION_FAILED"
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
