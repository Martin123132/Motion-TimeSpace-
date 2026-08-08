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
SOURCE = FUNCTIONAL_RG / "5295"

SCRIPT_5291 = (
    SCRIPTS / "Y5_R2FR_5291_order4_complete_singularity_atlas.py"
)
SCRIPT_5293 = (
    SCRIPTS
    / "Y5_R2FR_5293_hidden_track_pole_atlas_and_symmetry_transport.py"
)
RESULT_5294 = (
    FUNCTIONAL_RG / "5294" / "hidden_track_reassembly_result.json"
)
VALIDATION_5294 = (
    FUNCTIONAL_RG / "5294" / "hidden_track_reassembly_validation.csv"
)

DRY_RUN = SOURCE / "order6_exact_component_atlas_dry_run.json"
ANGULAR_NODES = SOURCE / "angular_order6_nodes.csv"
EXACT_JOBS = SOURCE / "angular_order6_exact_component_jobs.csv"
SCAN_JOBS = SOURCE / "angular_order6_exact_scan_jobs.csv"
GEOMETRIC_POLES = SOURCE / "angular_order6_geometric_poles.csv"
EXPANDED_POLES = SOURCE / "angular_order6_expanded_geometric_poles.csv"
CLASSIFIED_POLES = SOURCE / "angular_order6_exact_mask_poles.csv"
CHANNEL_ROOTS = SOURCE / "angular_order6_channel_roots.csv"
POLE_SAMPLES = SOURCE / "angular_order6_pole_samples.csv"
POLE_FITS = SOURCE / "angular_order6_pole_fits.csv"
POLE_RESIDUES = SOURCE / "angular_order6_selected_pole_residues.csv"
AMBIGUOUS_POLE_BOUNDS = (
    SOURCE / "angular_order6_bounded_ambiguous_pole_residues.csv"
)
ENDPOINT_SAMPLES = SOURCE / "angular_order6_endpoint_samples.csv"
ENDPOINT_FITS = SOURCE / "angular_order6_endpoint_fits.csv"
ENDPOINT_COEFFICIENTS = (
    SOURCE / "angular_order6_endpoint_coefficients.csv"
)
ENDPOINT_CANCELLATIONS = (
    SOURCE / "angular_order6_endpoint_cancellations.csv"
)
RESULT = SOURCE / "order6_exact_component_atlas_result.json"
VALIDATION = SOURCE / "order6_exact_component_atlas_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5295_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST / "5295-Y5-R2FR-order6-exact-component-singularity-atlas.md"
)

CHECKPOINT = 5295
PARENT_CHECKPOINT = 5294
MARKER = "MTS_5295_ORDER6_EXACT_COMPONENT_SINGULARITY_ATLAS"
REVISION = "order6-exact-component-singularity-atlas-v1"
ANGULAR_ORDER = 6
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
HIDDEN_COMPONENT_TEMPLATES = {
    "MC02": "MC03",
    "MC08": "MC07",
}
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


M5291 = load_module("mts_5291_for_5295", SCRIPT_5291)
M5293 = load_module("mts_5293_for_5295", SCRIPT_5293)
M5288 = M5291.M5288
M5287 = M5291.M5287
M5286 = M5291.M5286
M5283 = M5291.M5283
M5280 = M5291.M5280
M5267 = M5291.M5267
np = M5291.np
mp = M5291.mp
ORIGINAL_MANIFEST_JOB = M5291.manifest_job


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


def configure_reused_atlas_library() -> None:
    M5291.SOURCE = SOURCE
    M5291.SCAN_JOBS = SCAN_JOBS
    M5291.OWNER_POLES = GEOMETRIC_POLES
    M5291.EXPANDED_POLES = EXPANDED_POLES
    M5291.CLASSIFIED_POLES = CLASSIFIED_POLES
    M5291.CHANNEL_ROOTS = CHANNEL_ROOTS
    M5291.POLE_SAMPLES = POLE_SAMPLES
    M5291.POLE_FITS = POLE_FITS
    M5291.POLE_RESIDUES = POLE_RESIDUES
    M5291.AMBIGUOUS_POLE_BOUNDS = AMBIGUOUS_POLE_BOUNDS
    M5291.ENDPOINT_SAMPLES = ENDPOINT_SAMPLES
    M5291.ENDPOINT_FITS = ENDPOINT_FITS
    M5291.ENDPOINT_COEFFICIENTS = ENDPOINT_COEFFICIENTS
    M5291.ENDPOINT_CANCELLATIONS = ENDPOINT_CANCELLATIONS
    M5291.STATUS = STATUS
    M5291.CHECKPOINT = CHECKPOINT
    M5291.REVISION = REVISION
    M5291.ANGULAR_ORDER = ANGULAR_ORDER
    M5291.COMPONENT_IDS = COMPONENT_IDS
    M5291.SCAN_OWNER_IDS = COMPONENT_IDS
    M5291.COMPONENT_SCAN_OWNER = {
        component_id: component_id for component_id in COMPONENT_IDS
    }
    M5288.STATUS = STATUS
    M5288.CHECKPOINT = CHECKPOINT


def angular_nodes() -> list[dict[str, Any]]:
    rows = M5291.angular_nodes()
    for row in rows:
        row["valid_for_order6_singularity_atlas"] = True
        row["valid_for_order4_singularity_atlas"] = False
    return rows


def exact_jobs(
    base_context: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    dict[tuple[str, str], dict[str, Any]],
]:
    rows: list[dict[str, Any]] = []
    jobs: dict[tuple[str, str], dict[str, Any]] = {}
    for epsilon_id in REGULATOR_IDS:
        for component_id in COMPONENT_IDS:
            if component_id in HIDDEN_COMPONENT_TEMPLATES:
                template_component_id = HIDDEN_COMPONENT_TEMPLATES[
                    component_id
                ]
                job = M5293.derived_hidden_job(
                    epsilon_id,
                    component_id,
                    template_component_id,
                    base_context,
                )
                source_kind = "EXACT_PARENT_INVENTORY_DERIVED_JOB"
            else:
                template_component_id = component_id
                job = copy.deepcopy(
                    ORIGINAL_MANIFEST_JOB(epsilon_id, component_id)
                )
                source_kind = "PARENT_MANIFEST_JOB"
            jobs[(epsilon_id, component_id)] = job
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "component_id": component_id,
                    "template_component_id": template_component_id,
                    "source_kind": source_kind,
                    "job_id": job["job_id"],
                    "family": job["family"],
                    "owner_summand": job["owner_summand"],
                    "representative_pair": "|".join(
                        job["representative_pair"]
                    ),
                    "reciprocal_pair": "|".join(job["reciprocal_pair"]),
                    "representative_anchor_real": job[
                        "representative_anchor"
                    ]["real"],
                    "representative_anchor_imaginary": job[
                        "representative_anchor"
                    ]["imaginary"],
                    "reciprocal_anchor_real": job["reciprocal_anchor"][
                        "real"
                    ],
                    "reciprocal_anchor_imaginary": job[
                        "reciprocal_anchor"
                    ]["imaginary"],
                    "expected_u_winding": job["expected_u_winding"],
                    "expected_v_winding": job["expected_v_winding"],
                    "source_topology": job["source_topology"],
                    "source_topology_sha256": job[
                        "source_topology_sha256"
                    ],
                    "valid_for_order6_exact_component_scan": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows, jobs


def install_exact_job_lookup(
    jobs: dict[tuple[str, str], dict[str, Any]],
) -> None:
    def lookup(epsilon_id: str, component_id: str) -> dict[str, Any]:
        return jobs[(epsilon_id, component_id)]

    M5291.manifest_job = lookup


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5291,
        SCRIPT_5293,
        RESULT_5294,
        VALIDATION_5294,
        M5267.MANIFEST_5239,
        M5283.TOTALS_5281,
        M5280.M5274.M5231.RESULT,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def pole_row_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(row["angular_node_id"]),
        str(row["epsilon_id"]),
        str(row["component_id"]),
        str(row["pole_id"]),
    )


def repair_pole_coefficient_convergence(
    roots: list[dict[str, Any]],
    problems: dict[tuple[str, str, str], dict[str, Any]],
    base_context: dict[str, Any],
    nodes: list[dict[str, Any]],
    samples: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    residues: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    int,
]:
    targets = [
        row
        for row in residues
        if not parse_bool(row["pole_residue_controls_pass"])
        and float(row["maximum_coefficient_relative_change"])
        > M5288.COEFFICIENT_CHANGE_LIMIT
    ]
    if not targets:
        return samples, fits, residues, 0
    root_lookup = {pole_row_key(row): row for row in roots}
    local_roots = {
        node["angular_node_id"]: [
            row
            for row in roots
            if row["angular_node_id"] == node["angular_node_id"]
        ]
        for node in nodes
    }
    original_radius_function = M5288.pole_fit_radii
    exponent_modules = {M5280, M5287.M5280}
    original_exponents = {
        module: (
            module.FAST_DELTA_EXPONENT,
            module.AUDIT_DELTA_EXPONENT,
        )
        for module in exponent_modules
    }
    original_dps = mp.mp.dps
    repaired = 0
    try:
        mp.mp.dps = max(int(original_dps), 100)
        for module in exponent_modules:
            module.FAST_DELTA_EXPONENT = 32
            module.AUDIT_DELTA_EXPONENT = 24
        for target in targets:
            key = pole_row_key(target)
            root = root_lookup[key]
            node_roots = local_roots[root["angular_node_id"]]
            M5288.pole_fit_radii = (
                lambda source, _rows, local=node_roots: (
                    original_radius_function(source, local)
                )
            )
            new_samples, new_fits, new_residues = (
                M5288.derive_pole_residues(
                    [root],
                    problems,
                    base_context,
                )
            )
            if len(new_residues) != 1:
                raise RuntimeError(
                    f"high-precision pole repair failed for {key}"
                )
            samples = [
                row for row in samples if pole_row_key(row) != key
            ] + new_samples
            fits = [
                row for row in fits if pole_row_key(row) != key
            ] + new_fits
            residues = [
                row for row in residues if pole_row_key(row) != key
            ] + new_residues
            repaired += 1
            write_csv(POLE_SAMPLES, samples)
            write_csv(POLE_FITS, fits)
            write_csv(POLE_RESIDUES, residues)
    finally:
        M5288.pole_fit_radii = original_radius_function
        mp.mp.dps = original_dps
        for module, exponents in original_exponents.items():
            (
                module.FAST_DELTA_EXPONENT,
                module.AUDIT_DELTA_EXPONENT,
            ) = exponents
    return samples, fits, residues, repaired


def polynomial_endpoint_fit(
    rows: list[dict[str, Any]],
    upper: float,
    degree: int,
) -> tuple[complex, float, int]:
    local = sorted(
        [
            row
            for row in rows
            if float(row["soft_energy"]) <= upper
        ],
        key=lambda row: float(row["soft_energy"]),
    )
    if len(local) < degree + 2:
        raise RuntimeError(
            f"insufficient endpoint samples: {len(local)} for degree {degree}"
        )
    energies = np.asarray(
        [float(row["soft_energy"]) for row in local],
        dtype=np.float64,
    )
    contributions = np.asarray(
        [
            complex(
                float(row["raw_residue_real"]),
                float(row["raw_residue_imaginary"]),
            )
            for row in local
        ],
        dtype=np.complex128,
    )
    scaled = energies / upper
    transformed = energies * contributions
    matrix = np.column_stack(
        [scaled**power for power in range(degree + 1)]
    )
    coefficients, _, _, _ = np.linalg.lstsq(
        matrix,
        transformed,
        rcond=None,
    )
    predicted = matrix @ coefficients
    residual = float(
        np.max(np.abs(predicted - transformed))
        / max(float(np.max(np.abs(transformed))), 1.0e-300)
    )
    return complex(coefficients[0]), residual, len(local)


def refine_active_endpoint_coefficients(
    samples: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for row in samples:
        key = (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
        )
        grouped.setdefault(key, []).append(row)
    refined_rows: list[dict[str, Any]] = []
    refinement_fits: list[dict[str, Any]] = []
    refined_count = 0
    lower_upper = float(M5291.ENDPOINT_UPPERS[0])
    upper_upper = float(M5291.ENDPOINT_UPPERS[1])
    for source in coefficients:
        row = dict(source)
        if not parse_bool(row["lower_endpoint_log_singular"]):
            row["endpoint_refinement_method"] = (
                "UNCHANGED_NONSINGULAR_CLASSIFICATION"
            )
            row["valid_for_order6_endpoint_subtraction"] = False
            refined_rows.append(row)
            continue
        key = (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
        )
        local = grouped[key]
        selected, selected_residual, selected_count = (
            polynomial_endpoint_fit(local, lower_upper, 6)
        )
        alternate, alternate_residual, alternate_count = (
            polynomial_endpoint_fit(local, lower_upper, 5)
        )
        coarse, coarse_residual, coarse_count = polynomial_endpoint_fit(
            local,
            upper_upper,
            6,
        )
        degree_change = M5291.relative_complex_difference(
            selected,
            alternate,
        )
        refinement_change = M5291.relative_complex_difference(
            selected,
            coarse,
        )
        controls_pass = (
            selected_residual <= M5291.ENDPOINT_FIT_RESIDUAL_LIMIT
            and refinement_change
            <= M5291.ENDPOINT_REFINEMENT_CHANGE_LIMIT
            and degree_change <= M5291.ENDPOINT_DEGREE_CHANGE_LIMIT
            and abs(float(row["endpoint_power_exponent"]) + 1.0)
            <= M5291.ENDPOINT_EXPONENT_TOLERANCE
        )
        row.update(M5291.complex_fields(
            "endpoint_log_coefficient",
            selected,
        ))
        row["fit_relative_residual"] = selected_residual
        row["refinement_relative_change"] = refinement_change
        row["degree_relative_change"] = degree_change
        row["endpoint_fit_controls_pass"] = controls_pass
        row["valid_for_lower_endpoint_log_subtraction"] = controls_pass
        row["valid_for_order6_endpoint_subtraction"] = controls_pass
        row["endpoint_refinement_method"] = (
            "ACTIVE_DEGREE6_CROSS_WINDOW_REFINEMENT"
        )
        refined_rows.append(row)
        for label, upper, degree, value, residual, count in (
            (
                "SELECTED",
                lower_upper,
                6,
                selected,
                selected_residual,
                selected_count,
            ),
            (
                "DEGREE_CONTROL",
                lower_upper,
                5,
                alternate,
                alternate_residual,
                alternate_count,
            ),
            (
                "WINDOW_CONTROL",
                upper_upper,
                6,
                coarse,
                coarse_residual,
                coarse_count,
            ),
        ):
            refinement_fits.append(
                {
                    "angular_node_id": key[0],
                    "epsilon_id": key[1],
                    "component_id": key[2],
                    "upper_energy": upper,
                    "degree": degree,
                    "sample_count": count,
                    **M5291.complex_fields(
                        "endpoint_log_coefficient",
                        value,
                    ),
                    "fit_relative_residual": residual,
                    "refinement_role": label,
                    "valid_for_order6_endpoint_refinement": True,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
        refined_count += 1
    return fits + refinement_fits, refined_rows, refined_count


def dry_run() -> dict[str, Any]:
    configure_reused_atlas_library()
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5294)
    nodes = angular_nodes()
    manifest = read_json(M5267.MANIFEST_5239)
    manifest_pairs = {
        (row["epsilon_id"], row["component_id"])
        for row in manifest["jobs"]
    }
    checks = {
        "required_sources_exist": all(
            path.exists()
            for path in (
                SCRIPT_5291,
                SCRIPT_5293,
                RESULT_5294,
                VALIDATION_5294,
                M5267.MANIFEST_5239,
                M5283.TOTALS_5281,
            )
        ),
        "parent_5294_accepted": bool(parent["acceptance_passed"]),
        "parent_5294_validated": all(
            parse_bool(row["passed"])
            for row in read_csv(VALIDATION_5294)
        ),
        "thirty_six_order6_nodes_constructed": len(nodes) == 36,
        "all_node_coordinates_inside_angular_domain": all(
            abs(float(row["soft_cosine"]))
            < float(M5280.M5274.M5270.ANGULAR_LIMIT)
            and abs(float(row["decay_cosine"]))
            < float(M5280.M5274.M5270.ANGULAR_LIMIT)
            for row in nodes
        ),
        "visible_manifest_jobs_complete": all(
            (epsilon_id, component_id) in manifest_pairs
            for epsilon_id in REGULATOR_IDS
            for component_id in COMPONENT_IDS
            if component_id not in HIDDEN_COMPONENT_TEMPLATES
        ),
        "hidden_parent_inventories_complete": all(
            component_id
            in M5280.source_context()["inventories"][epsilon_id][
                "components"
            ]
            for epsilon_id in REGULATOR_IDS
            for component_id in HIDDEN_COMPONENT_TEMPLATES
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
            "DRY_RUN_ACCEPTED__BUILD_ORDER6_EXACT_COMPONENT_ATLAS"
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
    configure_reused_atlas_library()
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    M5291.install_bounded_root_refinement_fallback()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5295 dry run did not pass")
    parent = read_json(RESULT_5294)
    nodes = angular_nodes()
    write_csv(ANGULAR_NODES, nodes)
    base_context = M5280.source_context()
    job_rows, jobs = exact_jobs(base_context)
    write_csv(EXACT_JOBS, job_rows)
    install_exact_job_lookup(jobs)

    scan_jobs, geometric_poles, problems = M5291.scan_owner_poles(nodes)
    if not geometric_poles:
        raise RuntimeError("order-six exact scan produced no poles")
    expanded, expanded_problems = M5291.expand_family_rows(
        geometric_poles,
        problems,
    )
    write_csv(EXPANDED_POLES, expanded)
    classified = M5291.classify_exact_masks(
        expanded,
        nodes,
        base_context,
    )
    write_csv(CLASSIFIED_POLES, classified)
    M5291.configure_generalized_5288(nodes)
    roots = M5288.refine_active_channel_roots(
        classified,
        expanded_problems,
    )
    if not roots:
        raise RuntimeError("order-six exact masks activate no roots")
    write_csv(CHANNEL_ROOTS, roots)
    pole_samples, pole_fits, pole_residues = (
        M5291.derive_all_pole_residues(
            roots,
            expanded_problems,
            base_context,
            nodes,
        )
    )
    (
        pole_samples,
        pole_fits,
        pole_residues,
        high_precision_pole_repair_count,
    ) = repair_pole_coefficient_convergence(
        roots,
        expanded_problems,
        base_context,
        nodes,
        pole_samples,
        pole_fits,
        pole_residues,
    )
    order2_parent = read_json(M5291.RESULT_5290)
    (
        ambiguous_bounds,
        ambiguous_absolute_bound,
        ambiguous_relative_bound,
    ) = M5291.resolve_bounded_ambiguous_poles(
        pole_residues,
        pole_fits,
        nodes,
        order2_parent,
    )
    for row in pole_residues:
        row["valid_for_order6_pole_subtraction"] = parse_bool(
            row["valid_for_order4_pole_subtraction"]
        )
        row["order6_pole_resolution"] = row["order4_pole_resolution"]
        row["valid_for_order4_pole_subtraction"] = False
    write_csv(POLE_RESIDUES, pole_residues)
    for row in ambiguous_bounds:
        row["valid_for_order6_pole_subtraction"] = parse_bool(
            row["valid_for_order4_pole_subtraction"]
        )
        row["valid_for_order4_pole_subtraction"] = False
    write_csv(AMBIGUOUS_POLE_BOUNDS, ambiguous_bounds)

    endpoint_samples = M5291.endpoint_sample_rows(nodes, base_context)
    endpoint_fits, endpoint_coefficients = M5291.endpoint_fit_rows(
        endpoint_samples
    )
    (
        endpoint_fits,
        endpoint_coefficients,
        high_order_endpoint_refinement_count,
    ) = refine_active_endpoint_coefficients(
        endpoint_samples,
        endpoint_fits,
        endpoint_coefficients,
    )
    write_csv(ENDPOINT_FITS, endpoint_fits)
    write_csv(ENDPOINT_COEFFICIENTS, endpoint_coefficients)
    endpoint_cancellations = M5291.endpoint_cancellation_rows(
        endpoint_coefficients,
        nodes,
    )
    write_csv(ENDPOINT_CANCELLATIONS, endpoint_cancellations)

    material = [
        row
        for row in pole_residues
        if parse_bool(row["material_pole"])
    ]
    bounded = [
        row
        for row in pole_residues
        if parse_bool(row["bounded_ambiguous_residue"])
    ]
    removable = [
        row
        for row in pole_residues
        if not parse_bool(row["material_pole"])
        and not parse_bool(row["bounded_ambiguous_residue"])
    ]
    singular_endpoints = [
        row
        for row in endpoint_coefficients
        if parse_bool(row["valid_for_order6_endpoint_subtraction"])
    ]
    expected_scans = len(nodes) * len(REGULATOR_IDS) * len(COMPONENT_IDS)
    maximum_root_residual = max(
        float(row["channel_root_residual"]) for row in roots
    )
    maximum_fit_residual = max(
        float(row["fit_relative_residual"]) for row in pole_residues
    )
    maximum_endpoint_cancellation = max(
        max(
            float(row["E040_cancellation_relative_residual"]),
            float(row["E020_cancellation_relative_residual"]),
            float(row["physical_cancellation_relative_residual"]),
        )
        for row in endpoint_cancellations
    )
    checks = {
        "thirty_six_order6_nodes_written": len(nodes) == 36,
        "sixteen_exact_component_jobs_derived": (
            len(job_rows) == 16
            and all(
                parse_bool(row["valid_for_order6_exact_component_scan"])
                for row in job_rows
            )
        ),
        "all_576_exact_scans_complete": (
            len(scan_jobs) == expected_scans
            and len({row["scan_key"] for row in scan_jobs})
            == expected_scans
            and all(parse_bool(row["scan_completed"]) for row in scan_jobs)
        ),
        "no_family_transport_used": (
            len(expanded) == len(geometric_poles)
            and all(
                not parse_bool(row["family_scan_transport"])
                for row in expanded
            )
        ),
        "all_geometric_poles_exact_mask_classified": (
            len(classified) == len(expanded)
        ),
        "all_exact_active_roots_have_residue_classification": (
            len(roots) == len(pole_residues)
        ),
        "all_roots_resolved_by_control_or_bound": all(
            parse_bool(row["pole_residue_controls_pass"])
            or (
                parse_bool(row["bounded_ambiguous_residue"])
                and parse_bool(row["valid_for_order6_pole_subtraction"])
            )
            for row in pole_residues
        ),
        "at_least_one_material_pole_certified": bool(material),
        "all_material_poles_valid_for_subtraction": all(
            parse_bool(row["valid_for_order6_pole_subtraction"])
            for row in material
        ),
        "all_ambiguous_bounds_valid": (
            len(ambiguous_bounds) == len(bounded)
            and all(parse_bool(row["bound_valid"]) for row in ambiguous_bounds)
        ),
        "ambiguous_global_bound_below_budget": (
            ambiguous_relative_bound
            <= M5291.AMBIGUOUS_GLOBAL_RELATIVE_BOUND_LIMIT
        ),
        "endpoint_grid_complete": (
            len(endpoint_samples)
            == len(nodes)
            * len(REGULATOR_IDS)
            * len(COMPONENT_IDS)
            * len(M5291.ENDPOINT_ENERGIES)
        ),
        "endpoint_coefficients_complete": (
            len(endpoint_coefficients)
            == len(nodes) * len(REGULATOR_IDS) * len(COMPONENT_IDS)
        ),
        "all_singular_endpoint_controls_pass": all(
            parse_bool(row["valid_for_order6_endpoint_subtraction"])
            for row in singular_endpoints
        ),
        "all_nodewise_endpoint_cancellations_pass": (
            len(endpoint_cancellations) == len(nodes)
            and all(
                parse_bool(row["endpoint_cancellation_passed"])
                for row in endpoint_cancellations
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
        "mode": "order6-exact-component-singularity-atlas",
        "checks": checks,
        "acceptance_passed": accepted,
        "angular_order": ANGULAR_ORDER,
        "angular_node_count": len(nodes),
        "exact_component_job_count": len(job_rows),
        "exact_scan_count": len(scan_jobs),
        "geometric_pole_count": len(geometric_poles),
        "exact_active_root_count": len(roots),
        "selected_pole_residue_count": len(pole_residues),
        "material_pole_count": len(material),
        "removable_bounded_zero_count": len(removable),
        "bounded_ambiguous_pole_count": len(bounded),
        "bounded_ambiguous_global_absolute_error_bound": (
            ambiguous_absolute_bound
        ),
        "bounded_ambiguous_global_relative_error_bound": (
            ambiguous_relative_bound
        ),
        "maximum_channel_root_residual": maximum_root_residual,
        "maximum_selected_pole_fit_residual": maximum_fit_residual,
        "pole_sample_count": len(pole_samples),
        "pole_fit_count": len(pole_fits),
        "high_precision_pole_repair_count": (
            high_precision_pole_repair_count
        ),
        "endpoint_sample_count": len(endpoint_samples),
        "endpoint_fit_count": len(endpoint_fits),
        "endpoint_coefficient_count": len(endpoint_coefficients),
        "high_order_endpoint_refinement_count": (
            high_order_endpoint_refinement_count
        ),
        "singular_endpoint_term_count": len(singular_endpoints),
        "endpoint_cancellation_count": len(endpoint_cancellations),
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
            "CERTIFY_ORDER6_EXACT_COMPONENT_ATLAS__RUN_ORDER6_ENERGY"
            if accepted
            else "ORDER6_EXACT_COMPONENT_ATLAS_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_order6_exact_component_atlas": accepted,
            "valid_for_order6_inner_energy_run": accepted,
            "valid_for_full_angular_convergence": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This atlas scans all eight exact source-pair tracks at "
                "the thirty-six order-six nodes. It supplies derived "
                "singular subtractions but does not evaluate the "
                "order-six energy integral."
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
            "exact_scan_count": len(scan_jobs),
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
    text = f"""# 5295 — Order-six exact-component singularity atlas

## Result

The order-six tensor-product Gauss grid contains
`{result['angular_node_count']}` nodes. Unlike the first order-four
atlas, this pass scans all eight exact component tracks independently.
The hidden `MC02/MC08` jobs inherit only frozen topology settings; their
pair indices, anchors, chambers, windings, and raw contributions come
from the exact parent inventory.

- exact component jobs: `{result['exact_component_job_count']}`;
- independent scans: `{result['exact_scan_count']}`;
- geometric poles: `{result['geometric_pole_count']}`;
- exact-active roots: `{result['exact_active_root_count']}`;
- material poles: `{result['material_pole_count']}`;
- removable bounded zeros: `{result['removable_bounded_zero_count']}`;
- bounded ambiguous residues:
  `{result['bounded_ambiguous_pole_count']}`;
- aggregate ambiguous relative bound:
  `{result['bounded_ambiguous_global_relative_error_bound']:.12g}`;
- endpoint subtraction terms:
  `{result['singular_endpoint_term_count']}`;
- largest endpoint cancellation residual:
  `{result['maximum_endpoint_cancellation_relative_residual']:.12g}`.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Interpretation

This is a direct forward construction, not a missing-input ledger. It
removes the family-transport shortcut that caused the order-four hidden
track failure and derives every order-six subtraction at its own node.

## Claim boundary

No full phase-space, UV, local-GR, or full-MTS claim follows from this
atlas. The next gate is the independently evaluated order-six energy
integral and its order-four/order-six angular comparison.
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
        AMBIGUOUS_POLE_BOUNDS,
        ENDPOINT_SAMPLES,
        ENDPOINT_FITS,
        ENDPOINT_COEFFICIENTS,
        ENDPOINT_CANCELLATIONS,
        RESULT,
        STATUS,
    )
    files_exist = all(path.exists() for path in required)
    result = read_json(RESULT)
    source_hashes_match = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    nodes = read_csv(ANGULAR_NODES)
    jobs = read_csv(EXACT_JOBS)
    scans = read_csv(SCAN_JOBS)
    roots = read_csv(CHANNEL_ROOTS)
    residues = read_csv(POLE_RESIDUES)
    endpoints = read_csv(ENDPOINT_COEFFICIENTS)
    cancellations = read_csv(ENDPOINT_CANCELLATIONS)
    formal_end = M5283.formal_inventory_digest()
    gates = [
        validation_gate(
            "V01_REQUIRED_OUTPUTS_EXIST",
            files_exist,
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
            "V04_ORDER6_GRID_COMPLETE",
            len(nodes) == 36,
            f"nodes={len(nodes)}",
        ),
        validation_gate(
            "V05_EXACT_JOB_AND_SCAN_COUNTS",
            len(jobs) == 16
            and len(scans) == 576
            and len({row["scan_key"] for row in scans}) == 576,
            f"jobs={len(jobs)} scans={len(scans)}",
        ),
        validation_gate(
            "V06_ROOT_RESIDUE_BIJECTION",
            len(roots) == len(residues) and bool(roots),
            f"roots={len(roots)} residues={len(residues)}",
        ),
        validation_gate(
            "V07_ALL_SUBTRACTIONS_CERTIFIED",
            all(
                parse_bool(row["pole_residue_controls_pass"])
                or (
                    parse_bool(row["bounded_ambiguous_residue"])
                    and parse_bool(
                        row["valid_for_order6_pole_subtraction"]
                    )
                )
                for row in residues
            ),
            f"residues={len(residues)}",
        ),
        validation_gate(
            "V08_ENDPOINT_CONTROLS_COMPLETE",
            len(endpoints) == 576
            and len(cancellations) == 36
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
            all(not bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS),
            "phase-space, UV, local-GR, and full-MTS claims false",
        ),
    ]
    passed = all(row["passed"] for row in gates)
    write_csv(VALIDATION, gates)
    write_csv(RESIDUAL_VALIDATION, gates)
    render_document(result, passed)
    validation = {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_ORDER6_EXACT_COMPONENT_SINGULARITY_ATLAS"
            if passed
            else "ORDER6_EXACT_COMPONENT_ATLAS_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }
    return validation


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
