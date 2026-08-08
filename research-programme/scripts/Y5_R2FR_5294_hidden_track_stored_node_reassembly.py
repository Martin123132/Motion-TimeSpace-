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
SOURCE = FUNCTIONAL_RG / "5294"

SCRIPT_5293 = (
    SCRIPTS / "Y5_R2FR_5293_hidden_track_pole_atlas_and_symmetry_transport.py"
)
RESULT_5293 = (
    FUNCTIONAL_RG / "5293" / "hidden_track_pole_atlas_result.json"
)
VALIDATION_5293 = (
    FUNCTIONAL_RG / "5293" / "hidden_track_pole_atlas_validation.csv"
)
HIDDEN_POLES_5293 = (
    FUNCTIONAL_RG / "5293" / "MC02_MC08_hidden_track_pole_residues.csv"
)
RESULT_5292 = FUNCTIONAL_RG / "5292" / "order4_inner_energy_result.json"
NODE_MANIFEST_5292 = (
    FUNCTIONAL_RG / "5292" / "order4_node_run_manifest.csv"
)
COMPONENT_TOTALS_5292 = (
    FUNCTIONAL_RG / "5292" / "order4_inner_component_totals.csv"
)
ANGULAR_NODES_5291 = FUNCTIONAL_RG / "5291" / "angular_order4_nodes.csv"
OUTER_5290 = (
    FUNCTIONAL_RG / "5290" / "all_family_order2_outer_totals.csv"
)
RESULT_5291 = (
    FUNCTIONAL_RG / "5291" / "order4_complete_singularity_atlas_result.json"
)

DRY_RUN = SOURCE / "hidden_track_reassembly_dry_run.json"
CORRECTIONS = SOURCE / "hidden_track_component_corrections.csv"
COMPONENT_TOTALS = SOURCE / "hidden_track_component_totals.csv"
INNER_TOTALS = SOURCE / "hidden_track_inner_energy_totals.csv"
INNER_CONVERGENCE = SOURCE / "hidden_track_inner_energy_convergence.csv"
OUTER_TOTALS = SOURCE / "hidden_track_order4_outer_totals.csv"
ANGULAR_COMPARISON = (
    SOURCE / "hidden_track_order2_order4_angular_comparison.csv"
)
RESULT = SOURCE / "hidden_track_reassembly_result.json"
VALIDATION = SOURCE / "hidden_track_reassembly_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5294_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5294-Y5-R2FR-hidden-track-stored-node-reassembly.md"

CHECKPOINT = 5294
PARENT_CHECKPOINT = 5293
MARKER = "MTS_5294_HIDDEN_TRACK_STORED_NODE_REASSEMBLY"
REVISION = "hidden-track-stored-node-reassembly-v1"
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
ANGULAR_RELATIVE_CHANGE_LIMIT = 5.0e-3
UNTOUCHED_REPLAY_LIMIT = 1.0e-14
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


M5293 = load_module("mts_5293_for_5294", SCRIPT_5293)
M5292 = M5293.M5292
M5291 = M5293.M5291
M5283 = M5293.M5283
M5267 = M5293.M5267


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
        SCRIPT_5293,
        RESULT_5293,
        VALIDATION_5293,
        HIDDEN_POLES_5293,
        RESULT_5292,
        NODE_MANIFEST_5292,
        COMPONENT_TOTALS_5292,
        ANGULAR_NODES_5291,
        OUTER_5290,
        RESULT_5291,
        M5283.TOTALS_5281,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def supplemental_poles() -> dict[
    tuple[str, str, str],
    list[dict[str, complex]],
]:
    grouped: dict[
        tuple[str, str, str],
        list[dict[str, complex]],
    ] = defaultdict(list)
    for row in read_csv(HIDDEN_POLES_5293):
        if not parse_bool(row["valid_for_hidden_track_pole_subtraction"]):
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
            }
        )
    return grouped


def physical_multiplier() -> float:
    source = next(
        row
        for row in read_csv(M5283.TOTALS_5281)
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    )
    return float(source["kernel_multiplier"]) * float(
        source["physical_A00_weight"]
    )


def reassemble_components() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    poles = supplemental_poles()
    old_components = read_csv(COMPONENT_TOTALS_5292)
    old_lookup = {
        (
            row["angular_node_id"],
            row["epsilon_id"],
            int(row["energy_order"]),
            row["component_id"],
        ): row
        for row in old_components
    }
    minimum = float(M5267.ENERGY_MINIMUM)
    maximum = float(M5267.ENERGY_MAXIMUM)
    corrections: list[dict[str, Any]] = []
    components: list[dict[str, Any]] = []
    for manifest_index, manifest_row in enumerate(
        read_csv(NODE_MANIFEST_5292),
        start=1,
    ):
        node_id = manifest_row["angular_node_id"]
        energy_rows = read_csv(
            Path(manifest_row["energy_component_rows_path"])
        )
        quadrature: dict[
            tuple[str, int, str],
            complex,
        ] = defaultdict(complex)
        for source in energy_rows:
            key = (
                node_id,
                source["epsilon_id"],
                source["component_id"],
            )
            local_terms = poles.get(key, [])
            if not local_terms:
                continue
            energy = float(source["soft_energy"])
            singular = sum(
                (
                    term["residue"] / (energy - term["pole"])
                    for term in local_terms
                ),
                0.0j,
            )
            quadrature[
                (
                    source["epsilon_id"],
                    int(source["energy_order"]),
                    source["component_id"],
                )
            ] += float(source["mapped_energy_weight"]) * singular
        for epsilon_id in REGULATOR_IDS:
            for order in ENERGY_ORDERS:
                for component_id in COMPONENT_IDS:
                    old = old_lookup[
                        (node_id, epsilon_id, order, component_id)
                    ]
                    old_value = complex(
                        float(old["corrected_energy_integral_real"]),
                        float(old["corrected_energy_integral_imaginary"]),
                    )
                    local_terms = poles.get(
                        (node_id, epsilon_id, component_id),
                        [],
                    )
                    quadrature_value = quadrature.get(
                        (epsilon_id, order, component_id),
                        0.0j,
                    )
                    analytic_value = sum(
                        (
                            term["residue"]
                            * (
                                cmath.log(maximum - term["pole"])
                                - cmath.log(minimum - term["pole"])
                            )
                            for term in local_terms
                        ),
                        0.0j,
                    )
                    corrected = (
                        old_value - quadrature_value + analytic_value
                    )
                    corrections.append(
                        {
                            "angular_node_id": node_id,
                            "epsilon_id": epsilon_id,
                            "energy_order": order,
                            "component_id": component_id,
                            "supplemental_pole_count": len(local_terms),
                            **complex_fields(
                                "old_corrected_energy_integral",
                                old_value,
                            ),
                            **complex_fields(
                                "supplemental_quadrature_singular",
                                quadrature_value,
                            ),
                            **complex_fields(
                                "supplemental_analytic_singular",
                                analytic_value,
                            ),
                            **complex_fields(
                                "new_corrected_energy_integral",
                                corrected,
                            ),
                            "valid_for_hidden_track_stored_reassembly": True,
                            "valid_for_full_phase_space_coefficient": False,
                            "valid_for_numeric_UV_claim": False,
                            "valid_for_local_GR_claim": False,
                            "valid_for_full_MTS_claim": False,
                        }
                    )
                    components.append(
                        {
                            "angular_node_id": node_id,
                            "epsilon_id": epsilon_id,
                            "energy_order": order,
                            "component_id": component_id,
                            **complex_fields(
                                "corrected_energy_integral",
                                corrected,
                            ),
                            "supplemental_pole_count": len(local_terms),
                            "valid_for_hidden_track_stored_reassembly": True,
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
                "stage": "STORED_NODE_REASSEMBLY",
                "last_completed_angular_node_id": node_id,
                "completed_angular_node_count": manifest_index,
                "total_angular_node_count": 16,
            },
        )
    return corrections, components


def total_rows(
    components: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    nodes = {
        row["angular_node_id"]: row
        for row in read_csv(ANGULAR_NODES_5291)
    }
    lookup = {
        (
            row["angular_node_id"],
            row["epsilon_id"],
            int(row["energy_order"]),
            row["component_id"],
        ): complex(
            float(row["corrected_energy_integral_real"]),
            float(row["corrected_energy_integral_imaginary"]),
        )
        for row in components
    }
    rows: list[dict[str, Any]] = []
    multiplier = physical_multiplier()
    for node_id, node in nodes.items():
        regulator_values: dict[
            tuple[int, str],
            dict[str, complex],
        ] = {}
        for order in ENERGY_ORDERS:
            for epsilon_id in REGULATOR_IDS:
                local = {
                    component_id: lookup[
                        (node_id, epsilon_id, order, component_id)
                    ]
                    for component_id in COMPONENT_IDS
                }
                values = {
                    "eight_component_integral": sum(
                        local.values(),
                        0.0j,
                    ),
                    "six_component_integral": sum(
                        local[component_id]
                        for component_id in LEGACY_SIX_IDS
                    ),
                    "hidden_component_integral": sum(
                        local[component_id] for component_id in HIDDEN_IDS
                    ),
                }
                regulator_values[(order, epsilon_id)] = values
                rows.append(
                    {
                        "angular_node_id": node_id,
                        "soft_cosine": node["soft_cosine"],
                        "decay_cosine": node["decay_cosine"],
                        "row_type": "REGULATOR_INNER_ENERGY",
                        "epsilon_id": epsilon_id,
                        "energy_order": order,
                        **{
                            key: value
                            for channel, value in values.items()
                            for key, value in complex_fields(
                                channel,
                                value,
                            ).items()
                        },
                        "valid_for_hidden_track_stored_reassembly": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
        for order in ENERGY_ORDERS:
            physical = {
                channel: multiplier
                * (
                    2.0 * regulator_values[(order, "E020")][channel]
                    - regulator_values[(order, "E040")][channel]
                )
                for channel in regulator_values[(order, "E040")]
            }
            rows.append(
                {
                    "angular_node_id": node_id,
                    "soft_cosine": node["soft_cosine"],
                    "decay_cosine": node["decay_cosine"],
                    "row_type": "PHYSICAL_INNER_ENERGY",
                    "epsilon_id": "2E020_MINUS_E040",
                    "energy_order": order,
                    **{
                        key: value
                        for channel, value in physical.items()
                        for key, value in complex_fields(
                            channel,
                            value,
                        ).items()
                    },
                    "valid_for_hidden_track_stored_reassembly": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def convergence_rows(
    totals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    node_ids = sorted({row["angular_node_id"] for row in totals})
    for node_id in node_ids:
        for channel in (
            "eight_component_integral",
            "six_component_integral",
            "hidden_component_integral",
        ):
            lower_source = next(
                row
                for row in totals
                if row["angular_node_id"] == node_id
                and row["row_type"] == "PHYSICAL_INNER_ENERGY"
                and int(row["energy_order"]) == min(ENERGY_ORDERS)
            )
            upper_source = next(
                row
                for row in totals
                if row["angular_node_id"] == node_id
                and row["row_type"] == "PHYSICAL_INNER_ENERGY"
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
                    **complex_fields("lower_value", lower),
                    **complex_fields("upper_value", upper),
                    "relative_change": change,
                    "passes_energy_gate": (
                        change <= INNER_RELATIVE_CHANGE_LIMIT
                        if channel == "eight_component_integral"
                        else ""
                    ),
                    "valid_for_hidden_track_stored_reassembly": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def outer_rows(
    totals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    nodes = read_csv(ANGULAR_NODES_5291)
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
                "angular_order": 4,
                "energy_order": order,
                **{
                    key: value
                    for channel, value in values.items()
                    for key, value in complex_fields(channel, value).items()
                },
                "valid_for_hidden_track_stored_reassembly": True,
                "valid_for_full_angular_convergence": False,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def angular_comparison_rows(
    outer: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    lower_source = next(
        row
        for row in read_csv(OUTER_5290)
        if int(row["energy_order"]) == max(ENERGY_ORDERS)
    )
    upper_source = next(
        row
        for row in outer
        if int(row["energy_order"]) == max(ENERGY_ORDERS)
    )
    rows: list[dict[str, Any]] = []
    for channel in (
        "eight_component_integral",
        "six_component_integral",
        "hidden_component_integral",
    ):
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
    required = (
        SCRIPT_5293,
        RESULT_5293,
        VALIDATION_5293,
        HIDDEN_POLES_5293,
        RESULT_5292,
        NODE_MANIFEST_5292,
        COMPONENT_TOTALS_5292,
        ANGULAR_NODES_5291,
        OUTER_5290,
    )
    parent = read_json(RESULT_5293)
    supplemental = [
        row
        for row in read_csv(HIDDEN_POLES_5293)
        if parse_bool(row["valid_for_hidden_track_pole_subtraction"])
    ]
    checks = {
        "required_sources_exist": all(path.exists() for path in required),
        "parent_5293_accepted": bool(parent["acceptance_passed"]),
        "parent_5293_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5293)
        ),
        "all_sixteen_5292_node_shards_available": (
            len(read_csv(NODE_MANIFEST_5292)) == 16
            and all(
                Path(row["energy_component_rows_path"]).exists()
                for row in read_csv(NODE_MANIFEST_5292)
            )
        ),
        "supplemental_hidden_poles_numeric": bool(supplemental)
        and all(
            math.isfinite(float(row[field]))
            for row in supplemental
            for field in (
                "pole_real",
                "pole_imaginary",
                "true_limit_residue_real",
                "true_limit_residue_imaginary",
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
        "supplemental_pole_term_count": len(supplemental),
        "new_point_evaluation_count": 0,
        "decision": (
            "DRY_RUN_ACCEPTED__REASSEMBLE_HIDDEN_TRACK_POLES"
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
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5294 dry run did not pass")
    parent = read_json(RESULT_5293)
    corrections, components = reassemble_components()
    totals = total_rows(components)
    convergence = convergence_rows(totals)
    outer = outer_rows(totals)
    comparison = angular_comparison_rows(outer)
    write_csv(CORRECTIONS, corrections)
    write_csv(COMPONENT_TOTALS, components)
    write_csv(INNER_TOTALS, totals)
    write_csv(INNER_CONVERGENCE, convergence)
    write_csv(OUTER_TOTALS, outer)
    write_csv(ANGULAR_COMPARISON, comparison)

    eight_changes = [
        float(row["relative_change"])
        for row in convergence
        if row["channel"] == "eight_component_integral"
    ]
    maximum_node_change = max(eight_changes)
    outer_lookup = {
        int(row["energy_order"]): row for row in outer
    }
    outer4 = complex(
        float(
            outer_lookup[4]["eight_component_integral_real"]
        ),
        float(
            outer_lookup[4]["eight_component_integral_imaginary"]
        ),
    )
    outer8 = complex(
        float(
            outer_lookup[8]["eight_component_integral_real"]
        ),
        float(
            outer_lookup[8]["eight_component_integral_imaginary"]
        ),
    )
    outer_change = relative_complex_difference(outer4, outer8)
    angular_change = float(
        next(
            row
            for row in comparison
            if row["channel"] == "eight_component_integral"
        )["relative_change"]
    )
    untouched_errors = [
        relative_complex_difference(
            complex(
                float(row["old_corrected_energy_integral_real"]),
                float(row["old_corrected_energy_integral_imaginary"]),
            ),
            complex(
                float(row["new_corrected_energy_integral_real"]),
                float(row["new_corrected_energy_integral_imaginary"]),
            ),
        )
        for row in corrections
        if int(row["supplemental_pole_count"]) == 0
    ]
    maximum_untouched_error = max(untouched_errors, default=0.0)
    all_finite = all(
        math.isfinite(float(row[field]))
        for rows in (corrections, components, totals, convergence, outer)
        for row in rows
        for field in row
        if field.endswith("_real")
        or field.endswith("_imaginary")
        or field.endswith("_magnitude")
        or field == "relative_change"
    )
    checks = {
        "all_512_components_reassembled": (
            len(components) == 16 * 2 * 2 * 8
            and len(corrections) == len(components)
        ),
        "zero_new_point_evaluations": True,
        "all_values_finite": all_finite,
        "untouched_components_replay_exactly": (
            maximum_untouched_error <= UNTOUCHED_REPLAY_LIMIT
        ),
        "all_nodes_pass_inner_energy_gate": (
            maximum_node_change <= INNER_RELATIVE_CHANGE_LIMIT
        ),
        "order4_outer_passes_energy_gate": (
            outer_change <= OUTER_RELATIVE_CHANGE_LIMIT
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
    combined_ambiguity_absolute = float(
        read_json(RESULT_5291)[
            "bounded_ambiguous_global_absolute_error_bound"
        ]
    ) + float(parent["ambiguous_global_absolute_error_bound"])
    combined_ambiguity_relative = float(
        read_json(RESULT_5291)[
            "bounded_ambiguous_global_relative_error_bound"
        ]
    ) + float(parent["ambiguous_global_relative_error_bound"])
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "hidden-track-stored-node-reassembly",
        "checks": checks,
        "acceptance_passed": accepted,
        "supplemental_pole_term_count": sum(
            len(rows) for rows in supplemental_poles().values()
        ),
        "component_correction_count": len(corrections),
        "component_total_count": len(components),
        "inner_total_count": len(totals),
        "inner_convergence_count": len(convergence),
        "maximum_untouched_component_replay_error": (
            maximum_untouched_error
        ),
        "maximum_node_inner_energy_relative_change": maximum_node_change,
        "order4_outer_energy_relative_change": outer_change,
        "order2_order4_angular_relative_change": angular_change,
        "order2_order4_angular_smoke_passed": angular_smoke_passed,
        "order4_energy8_eight_component_integral": {
            "real": outer8.real,
            "imaginary": outer8.imag,
        },
        "combined_bounded_ambiguity_absolute_error": (
            combined_ambiguity_absolute
        ),
        "combined_bounded_ambiguity_relative_error": (
            combined_ambiguity_relative
        ),
        "new_point_evaluation_count": 0,
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
            "new_point_evaluations": 0,
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "ORDER2_ORDER4_ANGULAR_CHANGE_PASSES_SMOKE__"
            "REQUIRE_ORDER6_CONFIRMATION"
            if accepted and angular_smoke_passed
            else "HIDDEN_TRACK_REPAIR_CLOSES_ENERGY__"
            "ANGULAR_NOT_CONVERGED__ADVANCE_ORDER6"
            if accepted
            else "HIDDEN_TRACK_REASSEMBLY_REQUIRES_LOCAL_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_hidden_track_stored_reassembly": accepted,
            "valid_for_order2_order4_angular_smoke": accepted,
            "valid_for_full_angular_convergence": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "Stored-node reassembly can close the order-four energy "
                "gate without new evaluations. Full angular convergence "
                "still requires an order-six comparison."
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
            "order4_outer_energy_relative_change": outer_change,
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
    text = f"""# 5294 — Hidden-track stored-node reassembly

## Result

The 5292 order-four point evaluations were not rerun. The independently
derived `MC02/MC08` hidden-track poles were subtracted from the stored
quadrature values and their exact logarithmic integrals restored.

- supplemental pole terms:
  `{result['supplemental_pole_term_count']}`;
- new point evaluations: `{result['new_point_evaluation_count']}`;
- maximum node energy `4 -> 8` change:
  `{result['maximum_node_inner_energy_relative_change']:.12g}`;
- order-four outer energy `4 -> 8` change:
  `{result['order4_outer_energy_relative_change']:.12g}`;
- order-two to order-four angular change:
  `{result['order2_order4_angular_relative_change']:.12g}`;
- corrected order-four energy-eight total:
  `{outer['real']:.12g} {outer['imaginary']:+.12g} i`;
- combined bounded-pole relative ambiguity:
  `{result['combined_bounded_ambiguity_relative_error']:.12g}`.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This can establish a valid order-two/order-four angular smoke only.
Order six remains necessary before angular convergence or a full
phase-space coefficient can be claimed.

## Next target

{result['decision']}
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    required = (
        DRY_RUN,
        CORRECTIONS,
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
    csv_paths = (
        CORRECTIONS,
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
            "PARENT_5293_ACCEPTED",
            bool(read_json(RESULT_5293)["acceptance_passed"]),
            read_json(RESULT_5293)["decision"],
        ),
        validation_gate(
            "HIDDEN_TRACK_REASSEMBLY_ACCEPTED",
            bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            all(parsed[path] for path in csv_paths),
            f"{len(csv_paths)}/{len(csv_paths)} non-empty CSVs",
        ),
        validation_gate(
            "ZERO_NEW_POINT_EVALUATIONS",
            int(result["new_point_evaluation_count"]) == 0,
            "stored-node algebraic reassembly",
        ),
        validation_gate(
            "ENERGY_CONVERGENCE_CLOSED",
            float(result["maximum_node_inner_energy_relative_change"])
            <= INNER_RELATIVE_CHANGE_LIMIT
            and float(result["order4_outer_energy_relative_change"])
            <= OUTER_RELATIVE_CHANGE_LIMIT,
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
            "no MISSING_ token in checkpoint artifacts",
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
            "one single-thread BelowNormal process; no point evaluations",
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
            "VALIDATED_HIDDEN_TRACK_STORED_NODE_REASSEMBLY"
            if passed
            else "HIDDEN_TRACK_REASSEMBLY_VALIDATION_FAILED"
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
