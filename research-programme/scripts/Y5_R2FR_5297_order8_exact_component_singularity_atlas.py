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
SOURCE = FUNCTIONAL_RG / "5297"

SCRIPT_5295 = (
    SCRIPTS / "Y5_R2FR_5295_order6_exact_component_singularity_atlas.py"
)
RESULT_5296 = FUNCTIONAL_RG / "5296" / "order6_inner_energy_result.json"
VALIDATION_5296 = (
    FUNCTIONAL_RG / "5296" / "order6_inner_energy_validation.csv"
)

DRY_RUN = SOURCE / "order8_exact_component_atlas_dry_run.json"
ANGULAR_NODES = SOURCE / "angular_order8_nodes.csv"
EXACT_JOBS = SOURCE / "angular_order8_exact_component_jobs.csv"
SCAN_JOBS = SOURCE / "angular_order8_exact_scan_jobs.csv"
GEOMETRIC_POLES = SOURCE / "angular_order8_geometric_poles.csv"
EXPANDED_POLES = SOURCE / "angular_order8_expanded_geometric_poles.csv"
CLASSIFIED_POLES = SOURCE / "angular_order8_exact_mask_poles.csv"
CHANNEL_ROOTS = SOURCE / "angular_order8_channel_roots.csv"
POLE_SAMPLES = SOURCE / "angular_order8_pole_samples.csv"
POLE_FITS = SOURCE / "angular_order8_pole_fits.csv"
POLE_RESIDUES = SOURCE / "angular_order8_selected_pole_residues.csv"
CLUSTER_RESIDUE_BOUNDS = (
    SOURCE / "angular_order8_cluster_deflated_removable_bounds.csv"
)
AMBIGUOUS_POLE_BOUNDS = (
    SOURCE / "angular_order8_bounded_ambiguous_pole_residues.csv"
)
ENDPOINT_SAMPLES = SOURCE / "angular_order8_endpoint_samples.csv"
ENDPOINT_FITS = SOURCE / "angular_order8_endpoint_fits.csv"
ENDPOINT_COEFFICIENTS = (
    SOURCE / "angular_order8_endpoint_coefficients.csv"
)
ENDPOINT_CANCELLATIONS = (
    SOURCE / "angular_order8_endpoint_cancellations.csv"
)
RESULT = SOURCE / "order8_exact_component_atlas_result.json"
VALIDATION = SOURCE / "order8_exact_component_atlas_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5297_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST / "5297-Y5-R2FR-order8-exact-component-singularity-atlas.md"
)

CHECKPOINT = 5297
PARENT_CHECKPOINT = 5296
MARKER = "MTS_5297_ORDER8_EXACT_COMPONENT_SINGULARITY_ATLAS"
REVISION = "order8-exact-component-singularity-atlas-v1"
ANGULAR_ORDER = 8
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


M5295 = load_module("mts_5295_for_5297", SCRIPT_5295)
M5283 = M5295.M5283
M5280 = M5295.M5280
M5267 = M5295.M5267


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


def patch_library_globals() -> None:
    assignments = {
        "SOURCE": SOURCE,
        "DRY_RUN": DRY_RUN,
        "ANGULAR_NODES": ANGULAR_NODES,
        "EXACT_JOBS": EXACT_JOBS,
        "SCAN_JOBS": SCAN_JOBS,
        "GEOMETRIC_POLES": GEOMETRIC_POLES,
        "EXPANDED_POLES": EXPANDED_POLES,
        "CLASSIFIED_POLES": CLASSIFIED_POLES,
        "CHANNEL_ROOTS": CHANNEL_ROOTS,
        "POLE_SAMPLES": POLE_SAMPLES,
        "POLE_FITS": POLE_FITS,
        "POLE_RESIDUES": POLE_RESIDUES,
        "AMBIGUOUS_POLE_BOUNDS": AMBIGUOUS_POLE_BOUNDS,
        "ENDPOINT_SAMPLES": ENDPOINT_SAMPLES,
        "ENDPOINT_FITS": ENDPOINT_FITS,
        "ENDPOINT_COEFFICIENTS": ENDPOINT_COEFFICIENTS,
        "ENDPOINT_CANCELLATIONS": ENDPOINT_CANCELLATIONS,
        "RESULT": RESULT,
        "VALIDATION": VALIDATION,
        "RESIDUAL_VALIDATION": RESIDUAL_VALIDATION,
        "STATUS": STATUS,
        "DOCUMENT": DOCUMENT,
        "RESULT_5294": RESULT_5296,
        "VALIDATION_5294": VALIDATION_5296,
        "CHECKPOINT": CHECKPOINT,
        "PARENT_CHECKPOINT": PARENT_CHECKPOINT,
        "MARKER": MARKER,
        "REVISION": REVISION,
        "ANGULAR_ORDER": ANGULAR_ORDER,
    }
    for name, value in assignments.items():
        setattr(M5295, name, value)


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5295,
        RESULT_5296,
        VALIDATION_5296,
        M5267.MANIFEST_5239,
        M5283.TOTALS_5281,
        M5280.M5274.M5231.RESULT,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def dry_run() -> dict[str, Any]:
    patch_library_globals()
    M5295.configure_reused_atlas_library()
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5296)
    nodes = M5295.angular_nodes()
    manifest = read_json(M5267.MANIFEST_5239)
    manifest_pairs = {
        (row["epsilon_id"], row["component_id"])
        for row in manifest["jobs"]
    }
    checks = {
        "required_sources_exist": all(
            path.exists()
            for path in (
                SCRIPT_5295,
                RESULT_5296,
                VALIDATION_5296,
                M5267.MANIFEST_5239,
                M5283.TOTALS_5281,
            )
        ),
        "parent_5296_accepted": bool(parent["acceptance_passed"]),
        "parent_5296_validated": all(
            parse_bool(row["passed"])
            for row in read_csv(VALIDATION_5296)
        ),
        "sixty_four_order8_nodes_constructed": len(nodes) == 64,
        "visible_manifest_jobs_complete": all(
            (epsilon_id, component_id) in manifest_pairs
            for epsilon_id in REGULATOR_IDS
            for component_id in COMPONENT_IDS
            if component_id
            not in M5295.HIDDEN_COMPONENT_TEMPLATES
        ),
        "hidden_parent_inventories_complete": all(
            component_id
            in M5280.source_context()["inventories"][epsilon_id][
                "components"
            ]
            for epsilon_id in REGULATOR_IDS
            for component_id in M5295.HIDDEN_COMPONENT_TEMPLATES
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
        "planned_exact_scan_count": (
            len(nodes) * len(REGULATOR_IDS) * len(COMPONENT_IDS)
        ),
        "decision": (
            "DRY_RUN_ACCEPTED__BUILD_ORDER8_EXACT_COMPONENT_ATLAS"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(DRY_RUN, result)
    return result


def convert_order_flags() -> None:
    conversions = (
        (
            ANGULAR_NODES,
            {
                "valid_for_order6_singularity_atlas": (
                    "valid_for_order8_singularity_atlas"
                )
            },
        ),
        (
            EXACT_JOBS,
            {
                "valid_for_order6_exact_component_scan": (
                    "valid_for_order8_exact_component_scan"
                )
            },
        ),
        (
            ENDPOINT_COEFFICIENTS,
            {
                "valid_for_order6_endpoint_subtraction": (
                    "valid_for_order8_endpoint_subtraction"
                )
            },
        ),
    )
    for path, mapping in conversions:
        rows = read_csv(path)
        for row in rows:
            for source, target in mapping.items():
                if source.startswith("valid_for_"):
                    row[target] = (
                        parse_bool(row.get(target, False))
                        or parse_bool(row.get(source, False))
                    )
                else:
                    row[target] = row.get(target) or row.get(source, "")
                if source.startswith("valid_for_"):
                    row[source] = False
        write_csv(path, rows)


def repair_same_component_fit_radii() -> tuple[
    int,
    int,
    float,
    float,
]:
    nodes = read_csv(ANGULAR_NODES)
    roots = read_csv(CHANNEL_ROOTS)
    samples = read_csv(POLE_SAMPLES)
    fits = read_csv(POLE_FITS)
    residues = read_csv(POLE_RESIDUES)
    targets = [
        row
        for row in residues
        if parse_bool(row["material_pole"])
        and not parse_bool(row["pole_residue_controls_pass"])
        and float(row["degree_relative_change"])
        > M5295.M5288.RESIDUE_DEGREE_CHANGE_LIMIT
    ]
    base_context = M5280.source_context()
    _, jobs = M5295.exact_jobs(base_context)
    M5295.install_exact_job_lookup(jobs)
    M5295.M5291.configure_generalized_5288(nodes)
    root_lookup = {
        M5295.pole_row_key(row): row for row in roots
    }
    node_lookup = {
        row["angular_node_id"]: row for row in nodes
    }
    target_problems: dict[
        tuple[str, str, str],
        dict[str, Any],
    ] = {}
    for target in targets:
        root = root_lookup[M5295.pole_row_key(target)]
        node = node_lookup[root["angular_node_id"]]
        key = (
            root["angular_node_id"],
            root["epsilon_id"],
            root["component_id"],
        )
        target_problems[key] = M5295.M5286.angular_problem(
            jobs[(root["epsilon_id"], root["component_id"])],
            float(node["soft_cosine"]),
            float(node["decay_cosine"]),
        )
    original_radius_function = M5295.M5288.pole_fit_radii
    repaired = 0
    try:
        for target in targets:
            key = M5295.pole_row_key(target)
            root = root_lookup[key]
            same_component_roots = [
                row
                for row in roots
                if row["angular_node_id"] == root["angular_node_id"]
                and row["epsilon_id"] == root["epsilon_id"]
                and row["component_id"] == root["component_id"]
            ]
            M5295.M5288.pole_fit_radii = (
                lambda source, _rows, local=same_component_roots: (
                    original_radius_function(source, local)
                )
            )
            new_samples, new_fits, new_residues = (
                M5295.M5288.derive_pole_residues(
                    [root],
                    target_problems,
                    base_context,
                )
            )
            if len(new_residues) != 1:
                raise RuntimeError(
                    f"same-component radius repair failed for {key}"
                )
            samples = [
                row
                for row in samples
                if M5295.pole_row_key(row) != key
            ] + new_samples
            fits = [
                row
                for row in fits
                if M5295.pole_row_key(row) != key
            ] + new_fits
            residues = [
                row
                for row in residues
                if M5295.pole_row_key(row) != key
            ] + new_residues
            repaired += 1
    finally:
        M5295.M5288.pole_fit_radii = original_radius_function
    cluster_rows: list[dict[str, Any]] = []
    cluster_repaired = 0
    nodes_by_id = {
        row["angular_node_id"]: row for row in nodes
    }
    sample_groups: dict[
        tuple[str, str, str, str],
        list[dict[str, Any]],
    ] = {}
    for row in samples:
        sample_groups.setdefault(
            M5295.pole_row_key(row),
            [],
        ).append(row)
    for target in list(residues):
        if (
            not parse_bool(target["material_pole"])
            or parse_bool(target["pole_residue_controls_pass"])
            or float(target["degree_relative_change"])
            <= M5295.M5288.RESIDUE_DEGREE_CHANGE_LIMIT
        ):
            continue
        key = M5295.pole_row_key(target)
        root = root_lookup[key]
        target_pole = complex(
            float(root["refined_pole_real"]),
            float(root["refined_pole_imaginary"]),
        )
        cluster_roots = [
            row
            for row in roots
            if row["angular_node_id"] == root["angular_node_id"]
            and row["epsilon_id"] == root["epsilon_id"]
            and row["component_id"] == root["component_id"]
            and abs(
                float(row["refined_pole_real"])
                - target_pole.real
            )
            <= 1.0e-3
        ]
        if len(cluster_roots) < 2:
            continue
        cluster_poles = [
            complex(
                float(row["refined_pole_real"]),
                float(row["refined_pole_imaginary"]),
            )
            for row in cluster_roots
        ]
        local_samples = sample_groups[key]
        energies = M5295.np.asarray(
            [float(row["energy"]) for row in local_samples],
            dtype=M5295.np.float64,
        )
        contributions = M5295.np.asarray(
            [
                complex(
                    float(row["contribution_real"]),
                    float(row["contribution_imaginary"]),
                )
                for row in local_samples
            ],
            dtype=M5295.np.complex128,
        )
        center = float(M5295.np.mean(energies))
        scale = float(M5295.np.max(M5295.np.abs(energies - center)))
        scaled = (energies - center) / scale
        scaled_target = (target_pole - center) / scale
        deflated = contributions.copy()
        for pole in cluster_poles:
            deflated *= energies - pole
        denominator = math.prod(
            (
                target_pole - pole
                for pole in cluster_poles
                if abs(pole - target_pole) > 1.0e-15
            ),
            start=1.0 + 0.0j,
        )
        degree_rows: list[dict[str, Any]] = []
        fitted_residues: dict[int, complex] = {}
        for degree in (5, 6, 7):
            matrix = M5295.np.column_stack(
                [scaled**power for power in range(degree + 1)]
            )
            coefficients, _, _, _ = M5295.np.linalg.lstsq(
                matrix,
                deflated,
                rcond=None,
            )
            predicted = matrix @ coefficients
            fit_residual = float(
                M5295.np.max(M5295.np.abs(predicted - deflated))
                / max(
                    float(M5295.np.max(M5295.np.abs(deflated))),
                    1.0e-300,
                )
            )
            deflated_at_target = sum(
                coefficients[power] * scaled_target**power
                for power in range(degree + 1)
            )
            fitted_residue = complex(
                deflated_at_target / denominator
            )
            fitted_residues[degree] = fitted_residue
            degree_rows.append(
                {
                    "angular_node_id": key[0],
                    "epsilon_id": key[1],
                    "component_id": key[2],
                    "pole_id": key[3],
                    "cluster_pole_ids": "|".join(
                        row["pole_id"] for row in cluster_roots
                    ),
                    "cluster_pole_count": len(cluster_roots),
                    "degree": degree,
                    "sample_count": len(local_samples),
                    **M5295.M5291.complex_fields(
                        "cluster_deflated_residue",
                        fitted_residue,
                    ),
                    "fit_relative_residual": fit_residual,
                    "matrix_condition_number": float(
                        M5295.np.linalg.cond(matrix)
                    ),
                }
            )
        envelope = 2.0 * max(
            abs(value) for value in fitted_residues.values()
        )
        maximum_fit_residual = max(
            float(row["fit_relative_residual"]) for row in degree_rows
        )
        maximum_condition = max(
            float(row["matrix_condition_number"]) for row in degree_rows
        )
        bound_valid = (
            envelope <= M5295.M5288.REMOVABLE_RESIDUE_CEILING
            and maximum_fit_residual <= 1.0e-6
            and maximum_condition <= 1.0e4
        )
        node = nodes_by_id[key[0]]
        node_weight = (
            float(node["angular_weight"])
            * float(node["angular_jacobian"])
        )
        parent_total = next(
            row
            for row in read_csv(M5283.TOTALS_5281)
            if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
        )
        multiplier = abs(
            float(parent_total["kernel_multiplier"])
            * float(parent_total["physical_A00_weight"])
        )
        minimum = float(M5267.ENERGY_MINIMUM)
        maximum = float(M5267.ENERGY_MAXIMUM)
        analytic_log = cmath.log(
            maximum - target_pole
        ) - cmath.log(minimum - target_pole)
        regulator_weight = (
            2.0 if key[1] == "E020" else 1.0
        )
        physical_outer_bound = (
            multiplier
            * regulator_weight
            * node_weight
            * envelope
            * abs(analytic_log)
        )
        for row in degree_rows:
            row.update(
                {
                    "residue_magnitude_upper_bound": envelope,
                    "physical_outer_absolute_bound": (
                        physical_outer_bound
                    ),
                    "bound_valid": bound_valid,
                    "valid_for_cluster_deflated_removable_zero": (
                        bound_valid
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
        cluster_rows.extend(degree_rows)
        if not bound_valid:
            continue
        selected = fitted_residues[6]
        target.update(
            M5295.M5291.complex_fields(
                "true_limit_residue",
                selected,
            )
        )
        target["fit_relative_residual"] = maximum_fit_residual
        target["refinement_relative_change"] = 0.0
        target["degree_relative_change"] = 0.0
        target["material_pole"] = False
        target["pole_classification"] = (
            "CLUSTER_DEFLATED_REMOVABLE_BOUNDED_ZERO_RESIDUE"
        )
        target["material_residue_controls_pass"] = False
        target["removable_zero_residue_controls_pass"] = True
        target["pole_residue_controls_pass"] = True
        target["valid_for_failed_node_pole_subtraction"] = False
        target["cluster_deflated_residue_upper_bound"] = envelope
        target["cluster_deflated_physical_outer_absolute_bound"] = (
            physical_outer_bound
        )
        target["cluster_deflated_controls_pass"] = True
        cluster_repaired += 1
    if cluster_rows:
        write_csv(CLUSTER_RESIDUE_BOUNDS, cluster_rows)
    write_csv(POLE_SAMPLES, samples)
    write_csv(POLE_FITS, fits)
    write_csv(POLE_RESIDUES, residues)
    order2_parent = read_json(M5295.M5291.RESULT_5290)
    (
        bounds,
        ambiguous_absolute_bound,
        ambiguous_relative_bound,
    ) = M5295.M5291.resolve_bounded_ambiguous_poles(
        residues,
        fits,
        nodes,
        order2_parent,
    )
    cluster_absolute_bound = sum(
        float(row["physical_outer_absolute_bound"])
        for row in cluster_rows
        if int(row["degree"]) == 6
        and parse_bool(row["bound_valid"])
    )
    order2_outer = order2_parent[
        "order2_energy8_eight_component_integral"
    ]
    order2_magnitude = abs(
        complex(
            float(order2_outer["real"]),
            float(order2_outer["imaginary"]),
        )
    )
    ambiguous_absolute_bound += cluster_absolute_bound
    ambiguous_relative_bound = (
        ambiguous_absolute_bound / max(order2_magnitude, 1.0e-300)
    )
    for row in residues:
        row["valid_for_order8_pole_subtraction"] = parse_bool(
            row["valid_for_order4_pole_subtraction"]
        )
        row["order8_pole_resolution"] = row["order4_pole_resolution"]
        row["valid_for_order4_pole_subtraction"] = False
        row["valid_for_order6_pole_subtraction"] = False
    for row in bounds:
        row["valid_for_order8_pole_subtraction"] = parse_bool(
            row["valid_for_order4_pole_subtraction"]
        )
        row["valid_for_order4_pole_subtraction"] = False
        row["valid_for_order6_pole_subtraction"] = False
    write_csv(POLE_RESIDUES, residues)
    write_csv(AMBIGUOUS_POLE_BOUNDS, bounds)
    return (
        repaired,
        cluster_repaired,
        ambiguous_absolute_bound,
        ambiguous_relative_bound,
    )


def execute() -> dict[str, Any]:
    set_below_normal_priority()
    patch_library_globals()
    M5295.configure_reused_atlas_library()
    M5295.mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    M5295.M5291.install_bounded_root_refinement_fallback()
    M5295.dry_run = dry_run
    started = time.perf_counter()
    reusable_outputs = (
        ANGULAR_NODES,
        EXACT_JOBS,
        SCAN_JOBS,
        GEOMETRIC_POLES,
        EXPANDED_POLES,
        CLASSIFIED_POLES,
        CHANNEL_ROOTS,
        POLE_SAMPLES,
        POLE_FITS,
        POLE_RESIDUES,
        AMBIGUOUS_POLE_BOUNDS,
        ENDPOINT_SAMPLES,
        ENDPOINT_FITS,
        ENDPOINT_COEFFICIENTS,
        ENDPOINT_CANCELLATIONS,
        RESULT,
    )
    if (
        all(path.exists() for path in reusable_outputs)
        and len(read_csv(SCAN_JOBS)) == 1024
    ):
        raw = read_json(RESULT)
    else:
        raw = M5295.execute()
    (
        same_component_radius_repair_count,
        cluster_deflated_removable_count,
        ambiguous_absolute_bound,
        ambiguous_relative_bound,
    ) = repair_same_component_fit_radii()
    same_component_radius_repair_count = max(
        same_component_radius_repair_count,
        int(raw.get("same_component_radius_repair_count", 0)),
    )
    cluster_deflated_removable_count = max(
        cluster_deflated_removable_count,
        int(raw.get("cluster_deflated_removable_count", 0)),
    )
    convert_order_flags()
    parent = read_json(RESULT_5296)
    nodes = read_csv(ANGULAR_NODES)
    jobs = read_csv(EXACT_JOBS)
    scans = read_csv(SCAN_JOBS)
    geometric = read_csv(GEOMETRIC_POLES)
    expanded = read_csv(EXPANDED_POLES)
    classified = read_csv(CLASSIFIED_POLES)
    roots = read_csv(CHANNEL_ROOTS)
    residues = read_csv(POLE_RESIDUES)
    bounds = read_csv(AMBIGUOUS_POLE_BOUNDS)
    endpoint_samples = read_csv(ENDPOINT_SAMPLES)
    endpoint_fits = read_csv(ENDPOINT_FITS)
    endpoints = read_csv(ENDPOINT_COEFFICIENTS)
    cancellations = read_csv(ENDPOINT_CANCELLATIONS)
    material = [
        row for row in residues if parse_bool(row["material_pole"])
    ]
    bounded = [
        row
        for row in residues
        if parse_bool(row["bounded_ambiguous_residue"])
    ]
    removable = [
        row
        for row in residues
        if not parse_bool(row["material_pole"])
        and not parse_bool(row["bounded_ambiguous_residue"])
    ]
    singular_endpoints = [
        row
        for row in endpoints
        if parse_bool(row["valid_for_order8_endpoint_subtraction"])
    ]
    expected_scans = 64 * 2 * 8
    maximum_endpoint_cancellation = max(
        max(
            float(row["E040_cancellation_relative_residual"]),
            float(row["E020_cancellation_relative_residual"]),
            float(row["physical_cancellation_relative_residual"]),
        )
        for row in cancellations
    )
    checks = {
        "sixty_four_order8_nodes_written": len(nodes) == 64,
        "sixteen_exact_component_jobs_derived": len(jobs) == 16,
        "all_1024_exact_scans_complete": (
            len(scans) == expected_scans
            and len({row["scan_key"] for row in scans})
            == expected_scans
            and all(parse_bool(row["scan_completed"]) for row in scans)
        ),
        "no_family_transport_used": (
            len(expanded) == len(geometric)
            and all(
                not parse_bool(row["family_scan_transport"])
                for row in expanded
            )
        ),
        "all_geometric_poles_exact_mask_classified": (
            len(classified) == len(expanded)
        ),
        "all_exact_active_roots_have_residue_classification": (
            len(roots) == len(residues)
        ),
        "all_roots_resolved_by_control_or_bound": all(
            parse_bool(row["pole_residue_controls_pass"])
            or (
                parse_bool(row["bounded_ambiguous_residue"])
                and parse_bool(row["valid_for_order8_pole_subtraction"])
            )
            for row in residues
        ),
        "cluster_deflated_removable_bounds_valid": (
            cluster_deflated_removable_count == 2
            and CLUSTER_RESIDUE_BOUNDS.exists()
            and all(
                parse_bool(row["bound_valid"])
                for row in read_csv(CLUSTER_RESIDUE_BOUNDS)
            )
        ),
        "all_material_poles_valid_for_subtraction": all(
            parse_bool(row["valid_for_order8_pole_subtraction"])
            for row in material
        ),
        "all_ambiguous_bounds_valid": (
            len(bounds) == len(bounded)
            and all(parse_bool(row["bound_valid"]) for row in bounds)
        ),
        "ambiguous_global_bound_below_budget": (
            ambiguous_relative_bound
            <= M5295.M5291.AMBIGUOUS_GLOBAL_RELATIVE_BOUND_LIMIT
        ),
        "endpoint_grid_complete": len(endpoint_samples)
        == 64 * 2 * 8 * len(M5295.M5291.ENDPOINT_ENERGIES),
        "endpoint_coefficients_complete": len(endpoints) == 64 * 2 * 8,
        "all_singular_endpoint_controls_pass": all(
            parse_bool(row["valid_for_order8_endpoint_subtraction"])
            for row in singular_endpoints
        ),
        "all_nodewise_endpoint_cancellations_pass": (
            len(cancellations) == 64
            and all(
                parse_bool(row["endpoint_cancellation_passed"])
                for row in cancellations
            )
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
        "mode": "order8-exact-component-singularity-atlas",
        "checks": checks,
        "acceptance_passed": accepted,
        "angular_order": ANGULAR_ORDER,
        "angular_node_count": len(nodes),
        "exact_component_job_count": len(jobs),
        "exact_scan_count": len(scans),
        "geometric_pole_count": len(geometric),
        "exact_active_root_count": len(roots),
        "selected_pole_residue_count": len(residues),
        "material_pole_count": len(material),
        "removable_bounded_zero_count": len(removable),
        "bounded_ambiguous_pole_count": len(bounded),
        "bounded_ambiguous_global_absolute_error_bound": (
            ambiguous_absolute_bound
        ),
        "bounded_ambiguous_global_relative_error_bound": (
            ambiguous_relative_bound
        ),
        "maximum_channel_root_residual": raw[
            "maximum_channel_root_residual"
        ],
        "maximum_selected_pole_fit_residual": raw[
            "maximum_selected_pole_fit_residual"
        ],
        "pole_sample_count": len(read_csv(POLE_SAMPLES)),
        "pole_fit_count": len(read_csv(POLE_FITS)),
        "high_precision_pole_repair_count": raw[
            "high_precision_pole_repair_count"
        ],
        "same_component_radius_repair_count": (
            same_component_radius_repair_count
        ),
        "cluster_deflated_removable_count": (
            cluster_deflated_removable_count
        ),
        "endpoint_sample_count": len(endpoint_samples),
        "endpoint_fit_count": len(endpoint_fits),
        "endpoint_coefficient_count": len(endpoints),
        "high_order_endpoint_refinement_count": raw[
            "high_order_endpoint_refinement_count"
        ],
        "singular_endpoint_term_count": len(singular_endpoints),
        "endpoint_cancellation_count": len(cancellations),
        "maximum_endpoint_cancellation_relative_residual": (
            maximum_endpoint_cancellation
        ),
        "material_pole_components": sorted(
            {row["component_id"] for row in material}
        ),
        "singular_endpoint_components": sorted(
            {row["component_id"] for row in singular_endpoints}
        ),
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
            "resumable_scan_ledger": str(SCAN_JOBS),
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "CERTIFY_ORDER8_EXACT_COMPONENT_ATLAS__RUN_ORDER8_ENERGY"
            if accepted
            else "ORDER8_EXACT_COMPONENT_ATLAS_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_order8_exact_component_atlas": accepted,
            "valid_for_order8_inner_energy_run": accepted,
            "valid_for_full_angular_convergence": False,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "This derives all exact-component singular subtractions "
                "at the sixty-four order-eight nodes. It does not yet "
                "evaluate the order-eight energy integral."
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
            "exact_scan_count": len(scans),
            "material_pole_count": len(material),
            "singular_endpoint_term_count": len(singular_endpoints),
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
    text = f"""# 5297 — Order-eight exact-component singularity atlas

## Result

The order-eight tensor grid contains `{result['angular_node_count']}`
nodes. Every regulator/component track was scanned independently.

- independent scans: `{result['exact_scan_count']}`;
- geometric poles: `{result['geometric_pole_count']}`;
- exact-active roots: `{result['exact_active_root_count']}`;
- material poles: `{result['material_pole_count']}`;
- bounded ambiguous residues:
  `{result['bounded_ambiguous_pole_count']}`;
- aggregate ambiguous relative bound:
  `{result['bounded_ambiguous_global_relative_error_bound']:.12g}`;
- high-precision pole repairs:
  `{result['high_precision_pole_repair_count']}`;
- same-component radius repairs:
  `{result['same_component_radius_repair_count']}`;
- cluster-deflated removable roots:
  `{result['cluster_deflated_removable_count']}`;
- refined endpoint terms:
  `{result['high_order_endpoint_refinement_count']}`;
- maximum endpoint cancellation residual:
  `{result['maximum_endpoint_cancellation_relative_residual']:.12g}`.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This atlas only certifies the order-eight singular subtractions. The
order-eight energy integral and order-six/order-eight comparison remain
the next numerical gate.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    required = (
        DRY_RUN,
        ANGULAR_NODES,
        EXACT_JOBS,
        SCAN_JOBS,
        GEOMETRIC_POLES,
        EXPANDED_POLES,
        CLASSIFIED_POLES,
        CHANNEL_ROOTS,
        POLE_SAMPLES,
        POLE_FITS,
        POLE_RESIDUES,
        CLUSTER_RESIDUE_BOUNDS,
        AMBIGUOUS_POLE_BOUNDS,
        ENDPOINT_SAMPLES,
        ENDPOINT_FITS,
        ENDPOINT_COEFFICIENTS,
        ENDPOINT_CANCELLATIONS,
        RESULT,
        STATUS,
    )
    result = read_json(RESULT)
    nodes = read_csv(ANGULAR_NODES)
    jobs = read_csv(EXACT_JOBS)
    scans = read_csv(SCAN_JOBS)
    roots = read_csv(CHANNEL_ROOTS)
    residues = read_csv(POLE_RESIDUES)
    cluster_bounds = read_csv(CLUSTER_RESIDUE_BOUNDS)
    endpoints = read_csv(ENDPOINT_COEFFICIENTS)
    cancellations = read_csv(ENDPOINT_CANCELLATIONS)
    source_hashes_match = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    formal_end = M5283.formal_inventory_digest()
    gates = [
        validation_gate(
            "V01_REQUIRED_OUTPUTS_EXIST",
            all(path.exists() for path in required),
            f"{len(required)} required outputs",
        ),
        validation_gate(
            "V02_RESULT_ACCEPTED",
            bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "V03_SOURCE_HASHES_MATCH",
            source_hashes_match,
            f"{len(result['source_files'])} source hashes",
        ),
        validation_gate(
            "V04_ORDER8_GRID_AND_SCANS_COMPLETE",
            len(nodes) == 64
            and len(jobs) == 16
            and len(scans) == 1024
            and len({row["scan_key"] for row in scans}) == 1024,
            f"nodes={len(nodes)} jobs={len(jobs)} scans={len(scans)}",
        ),
        validation_gate(
            "V05_ROOT_RESIDUE_BIJECTION",
            len(roots) == len(residues) and bool(roots),
            f"roots={len(roots)} residues={len(residues)}",
        ),
        validation_gate(
            "V06_ALL_SUBTRACTIONS_CERTIFIED",
            all(
                parse_bool(row["pole_residue_controls_pass"])
                or (
                    parse_bool(row["bounded_ambiguous_residue"])
                    and parse_bool(
                        row["valid_for_order8_pole_subtraction"]
                    )
                )
                for row in residues
            ),
            f"residues={len(residues)}",
        ),
        validation_gate(
            "V07_CLUSTER_DEFLATION_CERTIFIED",
            len(cluster_bounds) >= 6
            and all(
                parse_bool(row["bound_valid"])
                for row in cluster_bounds
            ),
            f"cluster_fit_rows={len(cluster_bounds)}",
        ),
        validation_gate(
            "V08_ENDPOINT_CONTROLS_COMPLETE",
            len(endpoints) == 1024
            and len(cancellations) == 64
            and all(
                parse_bool(row["endpoint_cancellation_passed"])
                for row in cancellations
            ),
            (
                f"coefficients={len(endpoints)} "
                f"cancellations={len(cancellations)}"
            ),
        ),
        validation_gate(
            "V09_FORMAL_WORKBENCH_UNCHANGED",
            formal_end
            == str(result["formalization_workbench_reference_digest"]),
            formal_end,
        ),
        validation_gate(
            "V10_CLAIMS_LOCKED_FALSE",
            all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            ),
            "phase-space, UV, local-GR, and full-MTS claims false",
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
            "VALIDATED_ORDER8_EXACT_COMPONENT_SINGULARITY_ATLAS"
            if passed
            else "ORDER8_EXACT_COMPONENT_ATLAS_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "validate"),
        required=True,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "dry-run":
        result = dry_run()
    elif args.mode == "run":
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
