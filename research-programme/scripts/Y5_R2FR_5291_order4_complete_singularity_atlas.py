from __future__ import annotations

import argparse
import cmath
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
SOURCE = FUNCTIONAL_RG / "5291"

SCRIPT_5290 = (
    SCRIPTS
    / "Y5_R2FR_5290_all_family_stored_node_subtraction_reassembly.py"
)
RESULT_5290 = (
    FUNCTIONAL_RG / "5290" / "all_family_subtraction_result.json"
)
VALIDATION_5290 = (
    FUNCTIONAL_RG / "5290" / "all_family_subtraction_validation.csv"
)

DRY_RUN = SOURCE / "order4_complete_singularity_atlas_dry_run.json"
ANGULAR_NODES = SOURCE / "angular_order4_nodes.csv"
SCAN_JOBS = SOURCE / "angular_order4_scan_jobs.csv"
OWNER_POLES = SOURCE / "angular_order4_owner_geometric_poles.csv"
EXPANDED_POLES = SOURCE / "angular_order4_expanded_geometric_poles.csv"
CLASSIFIED_POLES = SOURCE / "angular_order4_exact_mask_poles.csv"
CHANNEL_ROOTS = SOURCE / "angular_order4_channel_roots.csv"
POLE_SAMPLES = SOURCE / "angular_order4_pole_samples.csv"
POLE_FITS = SOURCE / "angular_order4_pole_fits.csv"
POLE_RESIDUES = SOURCE / "angular_order4_selected_pole_residues.csv"
AMBIGUOUS_POLE_BOUNDS = (
    SOURCE / "angular_order4_bounded_ambiguous_pole_residues.csv"
)
ENDPOINT_SAMPLES = SOURCE / "angular_order4_endpoint_samples.csv"
ENDPOINT_FITS = SOURCE / "angular_order4_endpoint_fits.csv"
ENDPOINT_COEFFICIENTS = (
    SOURCE / "angular_order4_endpoint_coefficients.csv"
)
ENDPOINT_CANCELLATIONS = (
    SOURCE / "angular_order4_endpoint_cancellations.csv"
)
RESULT = SOURCE / "order4_complete_singularity_atlas_result.json"
VALIDATION = SOURCE / "order4_complete_singularity_atlas_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5291_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5291-Y5-R2FR-order4-complete-singularity-atlas.md"

CHECKPOINT = 5291
PARENT_CHECKPOINT = 5290
MARKER = "MTS_5291_ORDER4_COMPLETE_SINGULARITY_ATLAS"
REVISION = "order4-complete-singularity-atlas-v1"
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
SCAN_OWNER_IDS = ("MC03", "MC04", "MC07", "MC12", "MC14", "MC15")
COMPONENT_SCAN_OWNER = {
    "MC02": "MC03",
    "MC03": "MC03",
    "MC04": "MC04",
    "MC07": "MC07",
    "MC08": "MC07",
    "MC12": "MC12",
    "MC14": "MC14",
    "MC15": "MC15",
}
ENDPOINT_ENERGIES = (
    1.01e-4,
    1.10e-4,
    1.22e-4,
    1.38e-4,
    1.58e-4,
    1.82e-4,
    2.12e-4,
    2.50e-4,
    3.00e-4,
    3.65e-4,
    4.50e-4,
    5.60e-4,
    7.10e-4,
    9.00e-4,
    1.10e-3,
)
ENDPOINT_UPPERS = (6.0e-4, 1.1e-3)
ENDPOINT_DEGREES = (2, 3)
ENDPOINT_FIT_RESIDUAL_LIMIT = 2.0e-5
ENDPOINT_REFINEMENT_CHANGE_LIMIT = 2.0e-4
ENDPOINT_DEGREE_CHANGE_LIMIT = 2.0e-4
ENDPOINT_EXPONENT_TOLERANCE = 5.0e-2
ENDPOINT_STRENGTH_RATIO_FLOOR = 0.25
ENDPOINT_ABSOLUTE_FLOOR = 1.0e-6
ENDPOINT_CANCELLATION_RELATIVE_LIMIT = 1.0e-8
AMBIGUOUS_RESIDUE_ENVELOPE_SAFETY_FACTOR = 2.0
AMBIGUOUS_RESIDUE_INDIVIDUAL_LIMIT = 1.0e-2
AMBIGUOUS_FIT_RESIDUAL_LIMIT = 1.0e-2
AMBIGUOUS_GLOBAL_RELATIVE_BOUND_LIMIT = 1.0e-4
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


M5290 = load_module("mts_5290_for_5291", SCRIPT_5290)
M5289 = M5290.M5289
M5288 = M5290.M5288
M5287 = M5290.M5287
M5286 = M5289.M5286
M5283 = M5290.M5283
M5280 = M5289.M5280
M5267 = M5290.M5267
np = M5288.np
mp = M5288.mp

RELAXED_ROOT_REFINEMENT_COUNT = 0
MAXIMUM_RELAXED_ROOT_RESIDUAL = 0.0


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


def compact_node_cache(
    path: Path,
    valid_node_ids: set[str],
    unique_fields: tuple[str, ...] = (),
) -> None:
    if not path.exists():
        return
    rows = [
        dict(row)
        for row in read_csv(path)
        if row.get("angular_node_id", "") in valid_node_ids
    ]
    if unique_fields:
        rows = list(
            {
                tuple(str(row[field]) for field in unique_fields): row
                for row in rows
            }.values()
        )
    write_csv(path, rows)


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


def install_bounded_root_refinement_fallback() -> None:
    original = M5280.M5275.refine_relative_root
    if getattr(original, "_mts_5291_bounded_fallback", False):
        return

    def robust_refine_relative_root(
        event: dict[str, Any],
        target: Any,
        labels: tuple[str, str],
        initial_root: complex,
    ) -> tuple[Any, float, float]:
        global RELAXED_ROOT_REFINEMENT_COUNT
        global MAXIMUM_RELAXED_ROOT_RESIDUAL
        try:
            return original(event, target, labels, initial_root)
        except ValueError:
            initial = mp.mpc(
                mp.mpf(repr(float(initial_root.real))),
                mp.mpf(repr(float(initial_root.imag))),
            )

            def collision_equation(relative_root: Any) -> Any:
                *_, roots = M5280.M5275.local_root_data(
                    event,
                    target,
                    labels,
                    relative_root,
                )
                return roots[0] - roots[1]

            perturbation = mp.mpf("1e-10")
            refined = mp.findroot(
                collision_equation,
                (
                    initial * (1 - perturbation),
                    initial * (1 + perturbation),
                ),
                tol=mp.mpf("1e-40"),
                maxsteps=150,
            )
            residual = float(abs(collision_equation(refined)))
            if not math.isfinite(residual) or residual > 1.0e-20:
                raise RuntimeError(
                    "bounded relative-root fallback did not reach the "
                    f"1e-20 residual gate: {residual}"
                )
            distance = (
                M5280.M5275.M5274.M5237.M5030.chordal_distance(
                    complex(initial_root),
                    complex(refined),
                )
            )
            RELAXED_ROOT_REFINEMENT_COUNT += 1
            MAXIMUM_RELAXED_ROOT_RESIDUAL = max(
                MAXIMUM_RELAXED_ROOT_RESIDUAL,
                residual,
            )
            return refined, residual, float(distance)

    robust_refine_relative_root._mts_5291_bounded_fallback = True
    M5280.M5275.refine_relative_root = robust_refine_relative_root


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5290,
        RESULT_5290,
        VALIDATION_5290,
        M5288.SCRIPT_5287,
        M5267.MANIFEST_5239,
        M5283.TOTALS_5281,
        M5280.M5274.M5231.RESULT,
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
                    "valid_for_order4_singularity_atlas": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def manifest_job(
    epsilon_id: str,
    component_id: str,
) -> dict[str, Any]:
    manifest = M5267.read_json(M5267.MANIFEST_5239)
    return next(
        job
        for job in manifest["jobs"]
        if job["epsilon_id"] == epsilon_id
        and job["component_id"] == component_id
    )


def scan_key(
    angular_node_id: str,
    epsilon_id: str,
    component_id: str,
) -> str:
    return "|".join((angular_node_id, epsilon_id, component_id))


def scan_owner_poles(
    nodes: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[tuple[str, str, str], dict[str, Any]],
]:
    existing_jobs = read_csv(SCAN_JOBS) if SCAN_JOBS.exists() else []
    existing_poles = read_csv(OWNER_POLES) if OWNER_POLES.exists() else []
    valid_node_ids = {row["angular_node_id"] for row in nodes}
    completed = {
        row["scan_key"]
        for row in existing_jobs
        if parse_bool(row["scan_completed"])
        and row.get("revision", "") == REVISION
        and row.get("angular_node_id", "") in valid_node_ids
    }
    jobs = [
        dict(row)
        for row in existing_jobs
        if row["scan_key"] in completed
        and row.get("revision", "") == REVISION
    ]
    poles = [
        dict(row)
        for row in existing_poles
        if row.get("angular_node_id", "") in valid_node_ids
        and scan_key(
            row["angular_node_id"],
            row["epsilon_id"],
            row["scan_owner_component_id"],
        )
        in completed
    ]
    problems: dict[tuple[str, str, str], dict[str, Any]] = {}
    total_jobs = len(nodes) * len(REGULATOR_IDS) * len(SCAN_OWNER_IDS)
    for node in nodes:
        for epsilon_id in REGULATOR_IDS:
            for owner_component_id in SCAN_OWNER_IDS:
                key = (
                    node["angular_node_id"],
                    epsilon_id,
                    owner_component_id,
                )
                key_text = scan_key(*key)
                problem = M5286.angular_problem(
                    manifest_job(epsilon_id, owner_component_id),
                    float(node["soft_cosine"]),
                    float(node["decay_cosine"]),
                )
                problems[key] = problem
                if key_text in completed:
                    continue
                _, _, local_poles, _ = M5267.M5239.scan_problem(problem)
                local_rows = [
                    {
                        "angular_node_id": node["angular_node_id"],
                        "soft_cosine": node["soft_cosine"],
                        "decay_cosine": node["decay_cosine"],
                        "epsilon_id": epsilon_id,
                        "scan_owner_component_id": owner_component_id,
                        **source,
                        "symmetry_derived": False,
                        "valid_for_order4_owner_pole_scan": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                    for source in local_poles
                ]
                poles.extend(local_rows)
                jobs.append(
                    {
                        "scan_key": key_text,
                        "angular_node_id": node["angular_node_id"],
                        "soft_cosine": node["soft_cosine"],
                        "decay_cosine": node["decay_cosine"],
                        "epsilon_id": epsilon_id,
                        "scan_owner_component_id": owner_component_id,
                        "geometric_pole_count": len(local_rows),
                        "scan_completed": True,
                        "revision": REVISION,
                        "valid_for_order4_owner_pole_scan": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
                completed.add(key_text)
                write_csv(SCAN_JOBS, jobs)
                if poles:
                    write_csv(OWNER_POLES, poles)
                atomic_json(
                    STATUS,
                    {
                        "checkpoint": CHECKPOINT,
                        "state": "RUNNING",
                        "stage": "OWNER_GEOMETRIC_SCAN",
                        "last_completed_scan_key": key_text,
                        "completed_scan_job_count": len(completed),
                        "total_scan_job_count": total_jobs,
                        "owner_geometric_pole_count": len(poles),
                    },
                )
    write_csv(SCAN_JOBS, jobs)
    write_csv(OWNER_POLES, poles)
    return jobs, poles, problems


def expand_family_rows(
    owner_rows: list[dict[str, Any]],
    owner_problems: dict[tuple[str, str, str], dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    dict[tuple[str, str, str], dict[str, Any]],
]:
    aliases = defaultdict(list)
    for component_id, owner_component_id in COMPONENT_SCAN_OWNER.items():
        aliases[owner_component_id].append(component_id)
    rows: list[dict[str, Any]] = []
    problems: dict[tuple[str, str, str], dict[str, Any]] = {}
    for source in owner_rows:
        owner_component_id = source["scan_owner_component_id"]
        owner_key = (
            source["angular_node_id"],
            source["epsilon_id"],
            owner_component_id,
        )
        for component_id in aliases[owner_component_id]:
            row = dict(source)
            row["component_id"] = component_id
            row["family_scan_transport"] = (
                component_id != owner_component_id
            )
            row["family_scan_source_component_id"] = owner_component_id
            row["pole_id"] = str(row["pole_id"]).replace(
                owner_component_id,
                component_id,
                1,
            )
            rows.append(row)
            problems[
                (
                    row["angular_node_id"],
                    row["epsilon_id"],
                    component_id,
                )
            ] = owner_problems[owner_key]
    return rows, problems


def classify_exact_masks(
    scanned: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
    base_context: dict[str, Any],
) -> list[dict[str, Any]]:
    contexts = {
        node["angular_node_id"]: M5287.local_context(base_context, node)
        for node in nodes
    }
    rows: list[dict[str, Any]] = []
    for source in scanned:
        angular_node_id = source["angular_node_id"]
        epsilon_id = source["epsilon_id"]
        component_id = source["component_id"]
        context = contexts[angular_node_id]
        event = dict(context["source_event"])
        event["soft_energy"] = float(source["real_axis_center"])
        inventory = context["inventories"][epsilon_id]
        rationals = M5280.M5274.M5231.root_rationals(
            event,
            inventory["target"],
        )
        selection = M5280.M5279.algebraic_component_selector(
            event,
            inventory["target"],
            inventory["components"][component_id],
            rationals,
        )
        (
            exact_active,
            orientation,
            owned_labels,
            surface_values,
        ) = M5280.M5277.exact_mask_orientation(
            selection["selected_labels"],
            event,
            context["surfaces"],
        )
        rows.append(
            {
                "angular_node_id": angular_node_id,
                "soft_cosine": source["soft_cosine"],
                "decay_cosine": source["decay_cosine"],
                "epsilon_id": epsilon_id,
                "component_id": component_id,
                "family_scan_source_component_id": source[
                    "family_scan_source_component_id"
                ],
                "family_scan_transport": source["family_scan_transport"],
                "pole_id": source["pole_id"],
                "primary_surface_id": source["primary_surface_id"],
                "real_axis_center": source["real_axis_center"],
                "pole_real": source["pole_real"],
                "pole_imaginary": source["pole_imaginary"],
                "old_causal_family_active": source[
                    "causal_family_active"
                ],
                "exact_mask_active": exact_active,
                "promoted_by_exact_mask": (
                    exact_active
                    and not parse_bool(source["causal_family_active"])
                ),
                "selected_role": selection["selected_role"],
                "representing_pair": "|".join(
                    selection["selected_labels"]
                ),
                "orientation": orientation,
                "first_label_owned": owned_labels[0],
                "second_label_owned": owned_labels[1],
                "first_surface_value": surface_values[0],
                "second_surface_value": surface_values[1],
                "reciprocal_residual": selection["reciprocal_residual"],
                "valid_for_order4_exact_mask_classification": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def configure_generalized_5288(
    nodes: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    lookup = {row["angular_node_id"]: row for row in nodes}
    M5288.angular_node_lookup = lambda: lookup
    M5288.POLE_TARGETS = tuple(
        (node_id, "ALL_COMPONENTS") for node_id in lookup
    )
    M5288.STATUS = STATUS
    M5288.CHECKPOINT = CHECKPOINT
    return lookup


def derive_all_pole_residues(
    roots: list[dict[str, Any]],
    problems: dict[tuple[str, str, str], dict[str, Any]],
    base_context: dict[str, Any],
    nodes: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    configure_generalized_5288(nodes)
    valid_node_ids = {row["angular_node_id"] for row in nodes}
    samples: list[dict[str, Any]] = (
        [
            dict(row)
            for row in read_csv(POLE_SAMPLES)
            if row.get("angular_node_id", "") in valid_node_ids
        ]
        if POLE_SAMPLES.exists()
        else []
    )
    fits: list[dict[str, Any]] = (
        [
            dict(row)
            for row in read_csv(POLE_FITS)
            if row.get("angular_node_id", "") in valid_node_ids
        ]
        if POLE_FITS.exists()
        else []
    )
    residues: list[dict[str, Any]] = (
        [
            dict(row)
            for row in read_csv(POLE_RESIDUES)
            if row.get("angular_node_id", "") in valid_node_ids
        ]
        if POLE_RESIDUES.exists()
        else []
    )
    completed = {
        (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
            row["pole_id"],
        )
        for row in residues
    }
    samples = [
        row
        for row in samples
        if (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
            row["pole_id"],
        )
        in completed
    ]
    fits = [
        row
        for row in fits
        if (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
            row["pole_id"],
        )
        in completed
    ]
    samples = list(
        {
            (
                row["angular_node_id"],
                row["epsilon_id"],
                row["component_id"],
                row["pole_id"],
                str(row["radius_index"]),
                str(row["fraction"]),
            ): row
            for row in samples
        }.values()
    )
    fits = list(
        {
            (
                row["angular_node_id"],
                row["epsilon_id"],
                row["component_id"],
                row["pole_id"],
                str(row["radius_index"]),
                str(row["degree"]),
            ): row
            for row in fits
        }.values()
    )
    original_pole_fit_radii = M5288.pole_fit_radii
    newly_completed = 0
    for node in nodes:
        node_id = node["angular_node_id"]
        local_roots = [
            row for row in roots if row["angular_node_id"] == node_id
        ]
        M5288.pole_fit_radii = (
            lambda root, _roots, local=local_roots: (
                original_pole_fit_radii(root, local)
            )
        )
        for root in local_roots:
            root_key = (
                root["angular_node_id"],
                root["epsilon_id"],
                root["component_id"],
                root["pole_id"],
            )
            if root_key in completed:
                continue
            local_samples, local_fits, local_residues = (
                M5288.derive_pole_residues(
                    [root],
                    problems,
                    base_context,
                )
            )
            samples.extend(local_samples)
            fits.extend(local_fits)
            residues.extend(local_residues)
            completed.add(root_key)
            newly_completed += 1
            if newly_completed % 8 == 0:
                write_csv(POLE_SAMPLES, samples)
                write_csv(POLE_FITS, fits)
                write_csv(POLE_RESIDUES, residues)
        if local_roots:
            write_csv(POLE_SAMPLES, samples)
            write_csv(POLE_FITS, fits)
            write_csv(POLE_RESIDUES, residues)
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "POLE_RESIDUE_DERIVATION",
                "last_completed_angular_node_id": node_id,
                "active_root_count": len(roots),
                "selected_pole_residue_count": len(residues),
            },
        )
    M5288.pole_fit_radii = original_pole_fit_radii
    return samples, fits, residues


def resolve_bounded_ambiguous_poles(
    residues: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
    parent: dict[str, Any],
) -> tuple[list[dict[str, Any]], float, float]:
    fit_groups: dict[
        tuple[str, str, str, str],
        list[dict[str, Any]],
    ] = defaultdict(list)
    for row in fits:
        fit_groups[
            (
                row["angular_node_id"],
                row["epsilon_id"],
                row["component_id"],
                row["pole_id"],
            )
        ].append(row)
    node_weights = {
        row["angular_node_id"]: (
            float(row["angular_weight"])
            * float(row["angular_jacobian"])
        )
        for row in nodes
    }
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
    bounds: list[dict[str, Any]] = []
    global_absolute_bound = 0.0
    for row in residues:
        controlled = parse_bool(row["pole_residue_controls_pass"])
        material = parse_bool(row["material_pole"])
        row["bounded_ambiguous_residue"] = False
        row["valid_for_order4_pole_subtraction"] = (
            controlled and material
        )
        row["order4_pole_resolution"] = (
            "CERTIFIED_MATERIAL_SIMPLE_POLE"
            if controlled and material
            else "CERTIFIED_REMOVABLE_BOUNDED_ZERO"
            if controlled
            else "UNRESOLVED"
        )
        if controlled:
            continue
        key = (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
            row["pole_id"],
        )
        local_fits = fit_groups[key]
        magnitudes = [
            float(source["fitted_residue_magnitude"])
            for source in local_fits
        ]
        envelope = AMBIGUOUS_RESIDUE_ENVELOPE_SAFETY_FACTOR * max(
            magnitudes
        )
        maximum_fit_residual = max(
            float(source["fit_relative_residual"])
            for source in local_fits
        )
        maximum_coefficient_change = max(
            float(source["maximum_coefficient_relative_change"])
            for source in local_fits
        )
        pole = complex(
            float(row["pole_real"]),
            float(row["pole_imaginary"]),
        )
        analytic_log = cmath.log(maximum - pole) - cmath.log(
            minimum - pole
        )
        regulator_weight = 2.0 if row["epsilon_id"] == "E020" else 1.0
        physical_outer_bound = (
            multiplier
            * regulator_weight
            * node_weights[row["angular_node_id"]]
            * envelope
            * abs(analytic_log)
        )
        bound_valid = (
            math.isfinite(envelope)
            and envelope <= AMBIGUOUS_RESIDUE_INDIVIDUAL_LIMIT
            and maximum_fit_residual <= AMBIGUOUS_FIT_RESIDUAL_LIMIT
            and maximum_coefficient_change
            <= M5288.COEFFICIENT_CHANGE_LIMIT
            and math.isfinite(physical_outer_bound)
        )
        row["bounded_ambiguous_residue"] = True
        row["valid_for_order4_pole_subtraction"] = bound_valid
        row["order4_pole_resolution"] = (
            "BOUNDED_SMALL_AMBIGUOUS_RESIDUE_SUBTRACTION"
            if bound_valid
            else "UNRESOLVED_AMBIGUOUS_RESIDUE"
        )
        row["ambiguous_residue_upper_bound"] = envelope
        row["ambiguous_physical_outer_absolute_bound"] = (
            physical_outer_bound
        )
        bounds.append(
            {
                "angular_node_id": row["angular_node_id"],
                "epsilon_id": row["epsilon_id"],
                "component_id": row["component_id"],
                "pole_id": row["pole_id"],
                "pole_real": row["pole_real"],
                "pole_imaginary": row["pole_imaginary"],
                "selected_residue_magnitude": row[
                    "true_limit_residue_magnitude"
                ],
                "fit_residue_minimum_magnitude": min(magnitudes),
                "fit_residue_maximum_magnitude": max(magnitudes),
                "envelope_safety_factor": (
                    AMBIGUOUS_RESIDUE_ENVELOPE_SAFETY_FACTOR
                ),
                "residue_magnitude_upper_bound": envelope,
                "maximum_fit_relative_residual": maximum_fit_residual,
                "maximum_coefficient_relative_change": (
                    maximum_coefficient_change
                ),
                "analytic_log_factor_magnitude": abs(analytic_log),
                "regulator_extrapolation_absolute_weight": (
                    regulator_weight
                ),
                "angular_measure_weight": node_weights[
                    row["angular_node_id"]
                ],
                "kernel_and_A00_multiplier_magnitude": multiplier,
                "physical_outer_absolute_bound": physical_outer_bound,
                "bound_valid": bound_valid,
                "valid_for_order4_pole_subtraction": bound_valid,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        global_absolute_bound += physical_outer_bound
    if not bounds:
        raise RuntimeError("no bounded ambiguous pole rows were produced")
    outer = parent["order2_energy8_eight_component_integral"]
    parent_outer_magnitude = abs(
        complex(float(outer["real"]), float(outer["imaginary"]))
    )
    global_relative_bound = global_absolute_bound / max(
        parent_outer_magnitude,
        1.0e-300,
    )
    write_csv(AMBIGUOUS_POLE_BOUNDS, bounds)
    write_csv(POLE_RESIDUES, residues)
    return bounds, global_absolute_bound, global_relative_bound


def endpoint_sample_rows(
    nodes: list[dict[str, Any]],
    base_context: dict[str, Any],
) -> list[dict[str, Any]]:
    expected_count = (
        len(nodes)
        * len(REGULATOR_IDS)
        * len(COMPONENT_IDS)
        * len(ENDPOINT_ENERGIES)
    )
    if ENDPOINT_SAMPLES.exists():
        existing = [dict(row) for row in read_csv(ENDPOINT_SAMPLES)]
        if len(existing) == expected_count:
            return existing
    rows: list[dict[str, Any]] = []
    for node_index, node in enumerate(nodes, start=1):
        context = M5287.local_context(base_context, node)
        cache: dict[tuple[str, float, str], Any] = {}
        audit_counter = 0
        for epsilon_id in REGULATOR_IDS:
            for energy in ENDPOINT_ENERGIES:
                for component_id in COMPONENT_IDS:
                    audit_counter += 1
                    evaluation = M5287.evaluate_component_cached(
                        context,
                        epsilon_id,
                        component_id,
                        energy,
                        cache,
                        convergence_audit=(audit_counter % 128 == 0),
                    )
                    contribution = complex(evaluation["residue"])
                    rows.append(
                        {
                            "angular_node_id": node["angular_node_id"],
                            "soft_cosine": node["soft_cosine"],
                            "decay_cosine": node["decay_cosine"],
                            "epsilon_id": epsilon_id,
                            "component_id": component_id,
                            "soft_energy": energy,
                            "mask_active": evaluation["mask_active"],
                            **complex_fields(
                                "raw_residue",
                                contribution,
                            ),
                            **complex_fields(
                                "energy_times_residue",
                                energy * contribution,
                            ),
                            "coefficient_relative_change": evaluation[
                                "coefficient_relative_change"
                            ],
                            "convergence_audited": evaluation[
                                "convergence_audited"
                            ],
                            "valid_for_order4_endpoint_fit": True,
                            "valid_for_full_phase_space_coefficient": False,
                            "valid_for_numeric_UV_claim": False,
                            "valid_for_local_GR_claim": False,
                            "valid_for_full_MTS_claim": False,
                        }
                    )
        write_csv(ENDPOINT_SAMPLES, rows)
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "ENDPOINT_SAMPLING",
                "last_completed_angular_node_id": node[
                    "angular_node_id"
                ],
                "completed_angular_node_count": node_index,
                "endpoint_sample_count": len(rows),
            },
        )
    return rows


def endpoint_fit_rows(
    samples: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[
        tuple[str, str, str],
        list[dict[str, Any]],
    ] = defaultdict(list)
    for row in samples:
        grouped[
            (
                row["angular_node_id"],
                row["epsilon_id"],
                row["component_id"],
            )
        ].append(row)
    fits: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []
    for key, source_local in sorted(grouped.items()):
        local_fits: dict[tuple[float, int], dict[str, Any]] = {}
        for upper in ENDPOINT_UPPERS:
            local = sorted(
                [
                    row
                    for row in source_local
                    if float(row["soft_energy"]) <= upper
                ],
                key=lambda row: float(row["soft_energy"]),
            )
            if len(local) < max(ENDPOINT_DEGREES) + 2:
                raise RuntimeError(
                    f"insufficient endpoint samples for {key} at {upper}"
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
            for degree in ENDPOINT_DEGREES:
                matrix = np.column_stack(
                    [
                        scaled**power
                        for power in range(degree + 1)
                    ]
                )
                coefficients, _, _, _ = np.linalg.lstsq(
                    matrix,
                    transformed,
                    rcond=None,
                )
                predicted = matrix @ coefficients
                coefficient = complex(coefficients[0])
                residual = float(
                    np.max(np.abs(predicted - transformed))
                    / max(
                        float(np.max(np.abs(transformed))),
                        1.0e-300,
                    )
                )
                strength_ratio = abs(coefficient) / max(
                    float(np.max(np.abs(transformed))),
                    1.0e-300,
                )
                fit = {
                    "angular_node_id": key[0],
                    "epsilon_id": key[1],
                    "component_id": key[2],
                    "upper_energy": upper,
                    "degree": degree,
                    "sample_count": len(local),
                    **complex_fields(
                        "endpoint_log_coefficient",
                        coefficient,
                    ),
                    "fit_relative_residual": residual,
                    "endpoint_strength_ratio": strength_ratio,
                    "all_samples_mask_active": all(
                        parse_bool(row["mask_active"]) for row in local
                    ),
                    "maximum_coefficient_relative_change": max(
                        float(row["coefficient_relative_change"])
                        for row in local
                    ),
                    "valid_for_order4_endpoint_asymptotic_fit": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
                fits.append(fit)
                local_fits[(upper, degree)] = fit
        selected = local_fits[(ENDPOINT_UPPERS[0], 2)]
        coarse = local_fits[(ENDPOINT_UPPERS[1], 2)]
        alternate_degree = local_fits[(ENDPOINT_UPPERS[0], 3)]
        selected_value = complex(
            selected["endpoint_log_coefficient_real"],
            selected["endpoint_log_coefficient_imaginary"],
        )
        coarse_value = complex(
            coarse["endpoint_log_coefficient_real"],
            coarse["endpoint_log_coefficient_imaginary"],
        )
        degree_value = complex(
            alternate_degree["endpoint_log_coefficient_real"],
            alternate_degree["endpoint_log_coefficient_imaginary"],
        )
        refinement_change = relative_complex_difference(
            selected_value,
            coarse_value,
        )
        degree_change = relative_complex_difference(
            selected_value,
            degree_value,
        )
        smallest = sorted(
            source_local,
            key=lambda row: float(row["soft_energy"]),
        )[:2]
        first_energy = float(smallest[0]["soft_energy"])
        second_energy = float(smallest[1]["soft_energy"])
        first_magnitude = float(smallest[0]["raw_residue_magnitude"])
        second_magnitude = float(smallest[1]["raw_residue_magnitude"])
        exponent = (
            math.log(second_magnitude / first_magnitude)
            / math.log(second_energy / first_energy)
            if min(first_magnitude, second_magnitude) > 1.0e-300
            else 0.0
        )
        singular = (
            abs(selected_value) > ENDPOINT_ABSOLUTE_FLOOR
            and float(selected["endpoint_strength_ratio"])
            >= ENDPOINT_STRENGTH_RATIO_FLOOR
            and parse_bool(selected["all_samples_mask_active"])
        )
        controls_pass = (
            float(selected["fit_relative_residual"])
            <= ENDPOINT_FIT_RESIDUAL_LIMIT
            and refinement_change <= ENDPOINT_REFINEMENT_CHANGE_LIMIT
            and degree_change <= ENDPOINT_DEGREE_CHANGE_LIMIT
            and (
                not singular
                or abs(exponent + 1.0)
                <= ENDPOINT_EXPONENT_TOLERANCE
            )
        )
        selected_rows.append(
            {
                "angular_node_id": key[0],
                "epsilon_id": key[1],
                "component_id": key[2],
                **complex_fields(
                    "endpoint_log_coefficient",
                    selected_value,
                ),
                "endpoint_power_exponent": exponent,
                "endpoint_strength_ratio": selected[
                    "endpoint_strength_ratio"
                ],
                "fit_relative_residual": selected[
                    "fit_relative_residual"
                ],
                "refinement_relative_change": refinement_change,
                "degree_relative_change": degree_change,
                "maximum_coefficient_relative_change": selected[
                    "maximum_coefficient_relative_change"
                ],
                "lower_endpoint_log_singular": singular,
                "endpoint_classification": (
                    "ACTIVE_A_OVER_E_LOG_ENDPOINT"
                    if singular
                    else "NO_MATERIAL_A_OVER_E_ENDPOINT"
                ),
                "endpoint_fit_controls_pass": controls_pass,
                "valid_for_lower_endpoint_log_subtraction": (
                    singular and controls_pass
                ),
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return fits, selected_rows


def endpoint_cancellation_rows(
    coefficients: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    lookup = {
        (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
        ): row
        for row in coefficients
    }
    rows: list[dict[str, Any]] = []
    for node in nodes:
        node_id = node["angular_node_id"]
        regulator_totals: dict[str, complex] = {}
        regulator_scales: dict[str, float] = {}
        regulator_components: dict[str, list[str]] = {}
        regulator_controls: dict[str, bool] = {}
        for epsilon_id in REGULATOR_IDS:
            local = [
                lookup[(node_id, epsilon_id, component_id)]
                for component_id in COMPONENT_IDS
            ]
            active = [
                row
                for row in local
                if parse_bool(row["lower_endpoint_log_singular"])
            ]
            values = [
                complex(
                    float(row["endpoint_log_coefficient_real"]),
                    float(row["endpoint_log_coefficient_imaginary"]),
                )
                for row in active
            ]
            regulator_totals[epsilon_id] = sum(values, 0.0j)
            regulator_scales[epsilon_id] = sum(
                abs(value) for value in values
            )
            regulator_components[epsilon_id] = [
                row["component_id"] for row in active
            ]
            regulator_controls[epsilon_id] = all(
                parse_bool(row["valid_for_lower_endpoint_log_subtraction"])
                for row in active
            )
        physical_total = (
            2.0 * regulator_totals["E020"]
            - regulator_totals["E040"]
        )
        physical_scale = (
            2.0 * regulator_scales["E020"]
            + regulator_scales["E040"]
        )
        e040_ratio = abs(regulator_totals["E040"]) / max(
            regulator_scales["E040"],
            1.0e-300,
        )
        e020_ratio = abs(regulator_totals["E020"]) / max(
            regulator_scales["E020"],
            1.0e-300,
        )
        physical_ratio = abs(physical_total) / max(
            physical_scale,
            1.0e-300,
        )
        active_sets_match = (
            regulator_components["E040"]
            == regulator_components["E020"]
        )
        cancellation_passed = (
            active_sets_match
            and all(regulator_controls.values())
            and max(e040_ratio, e020_ratio, physical_ratio)
            <= ENDPOINT_CANCELLATION_RELATIVE_LIMIT
        )
        rows.append(
            {
                "angular_node_id": node_id,
                "soft_cosine": node["soft_cosine"],
                "decay_cosine": node["decay_cosine"],
                "active_endpoint_components": "|".join(
                    regulator_components["E040"]
                ),
                "active_component_count": len(
                    regulator_components["E040"]
                ),
                "regulator_active_sets_match": active_sets_match,
                **complex_fields(
                    "E040_total_endpoint_log_coefficient",
                    regulator_totals["E040"],
                ),
                "E040_cancellation_relative_residual": e040_ratio,
                **complex_fields(
                    "E020_total_endpoint_log_coefficient",
                    regulator_totals["E020"],
                ),
                "E020_cancellation_relative_residual": e020_ratio,
                **complex_fields(
                    "physical_total_endpoint_log_coefficient",
                    physical_total,
                ),
                "physical_cancellation_relative_residual": physical_ratio,
                "endpoint_cancellation_classification": (
                    "NODEWISE_LOG_ENDPOINT_CANCELLATION"
                    if cancellation_passed
                    else "UNRESOLVED_NODEWISE_LOG_ENDPOINT"
                ),
                "endpoint_cancellation_passed": cancellation_passed,
                "valid_for_order4_combined_endpoint_subtraction": (
                    cancellation_passed
                ),
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
        SCRIPT_5290,
        RESULT_5290,
        VALIDATION_5290,
        M5267.MANIFEST_5239,
        M5283.TOTALS_5281,
    )
    parent = read_json(RESULT_5290)
    nodes = angular_nodes()
    checks = {
        "required_sources_exist": all(path.exists() for path in required),
        "parent_5290_accepted": bool(parent["acceptance_passed"]),
        "parent_5290_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5290)
        ),
        "sixteen_order4_angular_nodes_constructed": len(nodes) == 16,
        "all_node_coordinates_inside_angular_domain": all(
            abs(float(row["soft_cosine"]))
            < float(M5280.M5274.M5270.ANGULAR_LIMIT)
            and abs(float(row["decay_cosine"]))
            < float(M5280.M5274.M5270.ANGULAR_LIMIT)
            for row in nodes
        ),
        "eight_component_family_map_complete": (
            set(COMPONENT_SCAN_OWNER) == set(COMPONENT_IDS)
            and set(COMPONENT_SCAN_OWNER.values()) == set(SCAN_OWNER_IDS)
        ),
        "all_six_scan_owners_have_manifest_jobs": all(
            any(
                job["epsilon_id"] == epsilon_id
                and job["component_id"] == component_id
                for job in read_json(M5267.MANIFEST_5239)["jobs"]
            )
            for epsilon_id in REGULATOR_IDS
            for component_id in SCAN_OWNER_IDS
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
        "planned_owner_scan_job_count": (
            len(nodes) * len(REGULATOR_IDS) * len(SCAN_OWNER_IDS)
        ),
        "planned_endpoint_sample_count": (
            len(nodes)
            * len(REGULATOR_IDS)
            * len(COMPONENT_IDS)
            * len(ENDPOINT_ENERGIES)
        ),
        "decision": (
            "DRY_RUN_ACCEPTED__BUILD_ORDER4_COMPLETE_SINGULARITY_ATLAS"
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
    install_bounded_root_refinement_fallback()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5291 dry run did not pass")
    parent = read_json(RESULT_5290)
    nodes = angular_nodes()
    write_csv(ANGULAR_NODES, nodes)
    valid_node_ids = {row["angular_node_id"] for row in nodes}
    compact_node_cache(
        SCAN_JOBS,
        valid_node_ids,
        ("scan_key",),
    )
    compact_node_cache(OWNER_POLES, valid_node_ids)
    compact_node_cache(
        POLE_SAMPLES,
        valid_node_ids,
        (
            "angular_node_id",
            "epsilon_id",
            "component_id",
            "pole_id",
            "radius_index",
            "fraction",
        ),
    )
    compact_node_cache(
        POLE_FITS,
        valid_node_ids,
        (
            "angular_node_id",
            "epsilon_id",
            "component_id",
            "pole_id",
            "radius_index",
            "degree",
        ),
    )
    compact_node_cache(
        POLE_RESIDUES,
        valid_node_ids,
        (
            "angular_node_id",
            "epsilon_id",
            "component_id",
            "pole_id",
        ),
    )
    cached_paths = (
        SCAN_JOBS,
        OWNER_POLES,
        EXPANDED_POLES,
        CLASSIFIED_POLES,
        CHANNEL_ROOTS,
        POLE_SAMPLES,
        POLE_FITS,
        POLE_RESIDUES,
    )
    use_complete_cache = all(path.exists() for path in cached_paths)
    if use_complete_cache:
        scan_jobs = read_csv(SCAN_JOBS)
        owner_poles = read_csv(OWNER_POLES)
        expanded = read_csv(EXPANDED_POLES)
        classified = read_csv(CLASSIFIED_POLES)
        roots = read_csv(CHANNEL_ROOTS)
        pole_samples = read_csv(POLE_SAMPLES)
        pole_fits = read_csv(POLE_FITS)
        pole_residues = read_csv(POLE_RESIDUES)
        use_complete_cache = (
            len(scan_jobs)
            == len(nodes) * len(REGULATOR_IDS) * len(SCAN_OWNER_IDS)
            and len(expanded) == len(classified)
            and len(roots) == len(pole_residues)
            and bool(roots)
        )
    base_context: Any = None
    if not use_complete_cache:
        base_context = M5280.source_context()
        scan_jobs, owner_poles, owner_problems = scan_owner_poles(nodes)
        expanded, problems = expand_family_rows(
            owner_poles,
            owner_problems,
        )
        if not expanded:
            raise RuntimeError("order-four scan produced no geometric poles")
        write_csv(EXPANDED_POLES, expanded)
        classified = classify_exact_masks(expanded, nodes, base_context)
        write_csv(CLASSIFIED_POLES, classified)
        configure_generalized_5288(nodes)
        roots = M5288.refine_active_channel_roots(classified, problems)
        if not roots:
            raise RuntimeError(
                "order-four exact masks activate no channel roots"
            )
        write_csv(CHANNEL_ROOTS, roots)
        pole_samples, pole_fits, pole_residues = (
            derive_all_pole_residues(
                roots,
                problems,
                base_context,
                nodes,
            )
        )
    (
        ambiguous_pole_bounds,
        ambiguous_global_absolute_bound,
        ambiguous_global_relative_bound,
    ) = resolve_bounded_ambiguous_poles(
        pole_residues,
        pole_fits,
        nodes,
        parent,
    )
    if not ENDPOINT_SAMPLES.exists():
        base_context = M5280.source_context()
    endpoint_samples = endpoint_sample_rows(nodes, base_context)
    endpoint_fits, endpoint_coefficients = endpoint_fit_rows(
        endpoint_samples
    )
    write_csv(ENDPOINT_FITS, endpoint_fits)
    write_csv(ENDPOINT_COEFFICIENTS, endpoint_coefficients)
    endpoint_cancellations = endpoint_cancellation_rows(
        endpoint_coefficients,
        nodes,
    )
    write_csv(ENDPOINT_CANCELLATIONS, endpoint_cancellations)

    material_poles = [
        row
        for row in pole_residues
        if parse_bool(row["material_pole"])
    ]
    removable_poles = [
        row
        for row in pole_residues
        if not parse_bool(row["material_pole"])
        and not parse_bool(row["bounded_ambiguous_residue"])
    ]
    bounded_ambiguous_poles = [
        row
        for row in pole_residues
        if parse_bool(row["bounded_ambiguous_residue"])
    ]
    singular_endpoints = [
        row
        for row in endpoint_coefficients
        if parse_bool(row["lower_endpoint_log_singular"])
    ]
    maximum_root_residual = max(
        float(row["channel_root_residual"]) for row in roots
    )
    maximum_pole_fit_residual = max(
        float(row["fit_relative_residual"]) for row in pole_residues
    )
    maximum_pole_coefficient_change = max(
        float(row["maximum_coefficient_relative_change"])
        for row in pole_residues
    )
    maximum_endpoint_fit_residual = max(
        float(row["fit_relative_residual"])
        for row in endpoint_coefficients
    )
    maximum_endpoint_cancellation_residual = max(
        max(
            float(row["E040_cancellation_relative_residual"]),
            float(row["E020_cancellation_relative_residual"]),
            float(row["physical_cancellation_relative_residual"]),
        )
        for row in endpoint_cancellations
    )
    expected_scan_jobs = (
        len(nodes) * len(REGULATOR_IDS) * len(SCAN_OWNER_IDS)
    )
    checks = {
        "sixteen_order4_nodes_written": len(nodes) == 16,
        "all_owner_scan_jobs_completed": (
            len(scan_jobs) == expected_scan_jobs
            and len({row["scan_key"] for row in scan_jobs})
            == expected_scan_jobs
            and all(parse_bool(row["scan_completed"]) for row in scan_jobs)
        ),
        "all_geometric_poles_expanded_to_family_components": (
            len(expanded) >= len(owner_poles)
            and set(row["component_id"] for row in expanded)
            <= set(COMPONENT_IDS)
        ),
        "all_expanded_poles_exact_mask_classified": (
            len(classified) == len(expanded)
        ),
        "all_exact_active_roots_have_residue_classification": (
            len(roots) == len(pole_residues)
        ),
        "all_roots_resolved_by_control_or_bound": all(
            parse_bool(row["pole_residue_controls_pass"])
            or (
                parse_bool(row["bounded_ambiguous_residue"])
                and parse_bool(row["valid_for_order4_pole_subtraction"])
            )
            for row in pole_residues
        ),
        "all_ambiguous_residue_bounds_valid": (
            len(ambiguous_pole_bounds) == len(bounded_ambiguous_poles)
            and all(
                parse_bool(row["bound_valid"])
                for row in ambiguous_pole_bounds
            )
        ),
        "ambiguous_global_bound_below_budget": (
            ambiguous_global_relative_bound
            <= AMBIGUOUS_GLOBAL_RELATIVE_BOUND_LIMIT
        ),
        "bounded_root_refinement_fallbacks_below_gate": (
            MAXIMUM_RELAXED_ROOT_RESIDUAL <= 1.0e-20
        ),
        "at_least_one_material_pole_certified": bool(material_poles),
        "all_material_poles_valid_for_subtraction": all(
            parse_bool(row["valid_for_failed_node_pole_subtraction"])
            for row in material_poles
        ),
        "endpoint_grid_complete": (
            len(endpoint_samples)
            == len(nodes)
            * len(REGULATOR_IDS)
            * len(COMPONENT_IDS)
            * len(ENDPOINT_ENERGIES)
        ),
        "endpoint_coefficients_complete": (
            len(endpoint_coefficients)
            == len(nodes) * len(REGULATOR_IDS) * len(COMPONENT_IDS)
        ),
        "all_singular_endpoint_controls_pass": all(
            parse_bool(row["valid_for_lower_endpoint_log_subtraction"])
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
        "mode": "order4-complete-singularity-atlas",
        "checks": checks,
        "acceptance_passed": accepted,
        "angular_order": ANGULAR_ORDER,
        "angular_node_count": len(nodes),
        "owner_scan_job_count": len(scan_jobs),
        "owner_geometric_pole_count": len(owner_poles),
        "expanded_geometric_pole_count": len(expanded),
        "exact_active_root_count": len(roots),
        "selected_pole_residue_count": len(pole_residues),
        "material_pole_count": len(material_poles),
        "removable_bounded_zero_count": len(removable_poles),
        "bounded_ambiguous_pole_count": len(bounded_ambiguous_poles),
        "bounded_ambiguous_global_absolute_error_bound": (
            ambiguous_global_absolute_bound
        ),
        "bounded_ambiguous_global_relative_error_bound": (
            ambiguous_global_relative_bound
        ),
        "bounded_ambiguous_global_relative_bound_limit": (
            AMBIGUOUS_GLOBAL_RELATIVE_BOUND_LIMIT
        ),
        "pole_sample_count": len(pole_samples),
        "pole_fit_count": len(pole_fits),
        "maximum_channel_root_residual": maximum_root_residual,
        "maximum_selected_pole_fit_residual": maximum_pole_fit_residual,
        "maximum_pole_coefficient_relative_change": (
            maximum_pole_coefficient_change
        ),
        "bounded_root_refinement_fallback_count": (
            RELAXED_ROOT_REFINEMENT_COUNT
        ),
        "maximum_bounded_root_refinement_residual": (
            MAXIMUM_RELAXED_ROOT_RESIDUAL
        ),
        "endpoint_sample_count": len(endpoint_samples),
        "endpoint_fit_count": len(endpoint_fits),
        "endpoint_coefficient_count": len(endpoint_coefficients),
        "singular_endpoint_term_count": len(singular_endpoints),
        "endpoint_cancellation_count": len(endpoint_cancellations),
        "maximum_selected_endpoint_fit_residual": (
            maximum_endpoint_fit_residual
        ),
        "maximum_endpoint_cancellation_relative_residual": (
            maximum_endpoint_cancellation_residual
        ),
        "material_pole_components": sorted(
            {row["component_id"] for row in material_poles}
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
            "scan_resume_ledger": str(SCAN_JOBS),
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "CERTIFY_ORDER4_COMPLETE_SINGULARITY_ATLAS__"
            "RUN_ORDER4_INNER_ENERGY_AND_COMPARE_ORDER2"
            if accepted
            else "ORDER4_SINGULARITY_ATLAS_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_order4_complete_singularity_atlas": accepted,
            "valid_for_order4_inner_energy_run": accepted,
            "valid_for_angular_convergence": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This checkpoint certifies singular subtractions at the "
                "sixteen order-four angular nodes. It does not yet "
                "evaluate the order-four energy integrals or establish "
                "angular convergence."
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
            "material_pole_count": len(material_poles),
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
    text = f"""# 5291 — Order-four complete singularity atlas

## Result

The order-four tensor-product Gauss grid contains
`{result['angular_node_count']}` angular nodes. Every node was scanned
for the six parent-owned source families; the two hidden direct
components inherit only the geometric family locations and are then
classified and evaluated independently by the exact algebraic selector.

- owner scan jobs: `{result['owner_scan_job_count']}`;
- owner geometric poles: `{result['owner_geometric_pole_count']}`;
- expanded component pole candidates:
  `{result['expanded_geometric_pole_count']}`;
- exact-active roots: `{result['exact_active_root_count']}`;
- material poles: `{result['material_pole_count']}`;
- removable bounded zeros: `{result['removable_bounded_zero_count']}`;
- bounded small ambiguous residues:
  `{result['bounded_ambiguous_pole_count']}`;
- their aggregate physical outer relative bound:
  `{result['bounded_ambiguous_global_relative_error_bound']:.12g}`;
- bounded high-precision root fallbacks:
  `{result['bounded_root_refinement_fallback_count']}`;
- largest bounded-fallback residual:
  `{result['maximum_bounded_root_refinement_residual']:.12g}`;
- material-pole components:
  `{result['material_pole_components']}`;
- singular endpoint terms:
  `{result['singular_endpoint_term_count']}`;
- singular endpoint components:
  `{result['singular_endpoint_components']}`.

The largest selected pole-fit residual is
`{result['maximum_selected_pole_fit_residual']:.12g}`. The largest
nodewise endpoint-cancellation residual is
`{result['maximum_endpoint_cancellation_relative_residual']:.12g}`.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Interpretation

This is a forward numerical result, not another missing-input ledger.
It constructs the complete singular subtraction data needed at the
new angular nodes. It does not reuse the order-two poles as if they
were angle-independent.

## Claim boundary

No full phase-space, UV, local-GR, or full-MTS claim follows from a
singularity atlas. Angular convergence still requires an independent
order-four inner-energy evaluation and comparison with checkpoint 5290.

## Next target

Run the order-four energy integrals using every certified simple-pole
and `A/E` endpoint subtraction, then compare the order-four outer total
with the accepted order-two total.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    required = (
        DRY_RUN,
        ANGULAR_NODES,
        SCAN_JOBS,
        OWNER_POLES,
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
    result = read_json(RESULT)
    source_files = result["source_files"]
    source_hashes_match = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in source_files
    )
    csv_paths = (
        ANGULAR_NODES,
        SCAN_JOBS,
        OWNER_POLES,
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
            "PARENT_5290_ACCEPTED",
            bool(read_json(RESULT_5290)["acceptance_passed"]),
            read_json(RESULT_5290)["decision"],
        ),
        validation_gate(
            "ORDER4_SINGULARITY_ATLAS_ACCEPTED",
            bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            all(parsed[path] for path in csv_paths),
            f"{len(csv_paths)}/{len(csv_paths)} non-empty CSVs",
        ),
        validation_gate(
            "SIXTEEN_NODES_AND_192_SCANS",
            len(parsed[ANGULAR_NODES]) == 16
            and len(parsed[SCAN_JOBS]) == 192,
            (
                f"nodes={len(parsed[ANGULAR_NODES])}; "
                f"scans={len(parsed[SCAN_JOBS])}"
            ),
        ),
        validation_gate(
            "POLE_CONTROLS_CLOSE",
            len(parsed[CHANNEL_ROOTS]) == len(parsed[POLE_RESIDUES])
            and all(
                parse_bool(row["pole_residue_controls_pass"])
                or (
                    parse_bool(row["bounded_ambiguous_residue"])
                    and parse_bool(
                        row["valid_for_order4_pole_subtraction"]
                    )
                )
                for row in parsed[POLE_RESIDUES]
            ),
            (
                f"roots={len(parsed[CHANNEL_ROOTS])}; "
                f"residues={len(parsed[POLE_RESIDUES])}; "
                f"material={result['material_pole_count']}; "
                "bounded="
                f"{result['bounded_ambiguous_pole_count']}; "
                "global-relative-bound="
                f"{result['bounded_ambiguous_global_relative_error_bound']}"
            ),
        ),
        validation_gate(
            "ENDPOINT_CONTROLS_CLOSE",
            len(parsed[ENDPOINT_CANCELLATIONS]) == 16
            and all(
                parse_bool(row["endpoint_cancellation_passed"])
                for row in parsed[ENDPOINT_CANCELLATIONS]
            ),
            (
                f"terms={result['singular_endpoint_term_count']}; "
                "16/16 node cancellations"
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
            "one single-thread BelowNormal process with resumable scan",
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
            "VALIDATED_ORDER4_COMPLETE_SINGULARITY_ATLAS"
            if passed
            else "ORDER4_SINGULARITY_ATLAS_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }
    return validation


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
