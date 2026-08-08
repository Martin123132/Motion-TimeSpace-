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
SOURCE = FUNCTIONAL_RG / "5293"

SCRIPT_5292 = (
    SCRIPTS / "Y5_R2FR_5292_order4_inner_energy_and_order2_comparison.py"
)
RESULT_5292 = FUNCTIONAL_RG / "5292" / "order4_inner_energy_result.json"
MANIFEST_5292 = FUNCTIONAL_RG / "5292" / "order4_node_run_manifest.csv"
RESULT_5291 = (
    FUNCTIONAL_RG / "5291" / "order4_complete_singularity_atlas_result.json"
)
VALIDATION_5291 = (
    FUNCTIONAL_RG
    / "5291"
    / "order4_complete_singularity_atlas_validation.csv"
)
ANGULAR_NODES_5291 = FUNCTIONAL_RG / "5291" / "angular_order4_nodes.csv"
ORDER2_RESULT_5290 = (
    FUNCTIONAL_RG / "5290" / "all_family_subtraction_result.json"
)

DRY_RUN = SOURCE / "hidden_track_pole_atlas_dry_run.json"
DERIVED_JOBS = SOURCE / "hidden_inventory_derived_jobs.csv"
SYMMETRY_AUDIT = SOURCE / "MC02_MC08_decay_reflection_symmetry.csv"
SCAN_JOBS = SOURCE / "MC02_owner_scan_jobs.csv"
SCANNED_POLES = SOURCE / "MC02_owner_geometric_poles.csv"
CLASSIFIED_POLES = SOURCE / "MC02_owner_exact_mask_poles.csv"
CHANNEL_ROOTS = SOURCE / "MC02_owner_channel_roots.csv"
POLE_SAMPLES = SOURCE / "MC02_owner_pole_samples.csv"
POLE_FITS = SOURCE / "MC02_owner_pole_fits.csv"
OWNER_RESIDUES = SOURCE / "MC02_owner_selected_pole_residues.csv"
FINAL_RESIDUES = SOURCE / "MC02_MC08_hidden_track_pole_residues.csv"
AMBIGUOUS_BOUNDS = SOURCE / "hidden_track_ambiguous_pole_bounds.csv"
RESULT = SOURCE / "hidden_track_pole_atlas_result.json"
VALIDATION = SOURCE / "hidden_track_pole_atlas_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5293_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5293-Y5-R2FR-hidden-track-pole-atlas-and-symmetry-transport.md"

CHECKPOINT = 5293
PARENT_CHECKPOINT = 5292
MARKER = "MTS_5293_HIDDEN_TRACK_POLE_ATLAS_AND_SYMMETRY_TRANSPORT"
REVISION = "hidden-track-pole-atlas-symmetry-transport-v1"
OWNER_COMPONENT_ID = "MC02"
MIRROR_COMPONENT_ID = "MC08"
HIDDEN_COMPONENT_TEMPLATES = {
    "MC02": "MC03",
    "MC08": "MC07",
}
REGULATOR_IDS = ("E040", "E020")
SYMMETRY_TEST_ENERGIES = (
    2.0e-4,
    2.0e-3,
    1.0e-1,
    5.0e-1,
    9.0e-1,
    9.7e-1,
    9.85e-1,
    9.95e-1,
)
SYMMETRY_RELATIVE_LIMIT = 1.0e-12
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


M5292 = load_module("mts_5292_for_5293", SCRIPT_5292)
M5291 = M5292.M5291
M5290 = M5292.M5290
M5288 = M5292.M5288
M5287 = M5292.M5287
M5286 = M5291.M5286
M5283 = M5292.M5283
M5280 = M5292.M5280
M5267 = M5292.M5267
np = M5292.np
mp = M5292.mp


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
        SCRIPT_5292,
        RESULT_5292,
        MANIFEST_5292,
        RESULT_5291,
        VALIDATION_5291,
        ANGULAR_NODES_5291,
        ORDER2_RESULT_5290,
        M5267.MANIFEST_5239,
        M5283.TOTALS_5281,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def complex_dictionary(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def suffix_windings(
    component: dict[str, Any],
) -> dict[str, int]:
    values: dict[str, int] = {}
    for branch in ("representative", "reciprocal"):
        label = component[branch]["representing_pairs"][0][0]
        suffix = label.rsplit("_", 1)[-1]
        values[suffix] = int(component[branch]["winding_correction"])
    if set(values) != {"u", "v"}:
        raise RuntimeError(f"incomplete hidden winding map: {values}")
    return values


def derived_hidden_job(
    epsilon_id: str,
    component_id: str,
    template_component_id: str,
    base_context: dict[str, Any],
) -> dict[str, Any]:
    template = copy.deepcopy(
        M5291.manifest_job(epsilon_id, template_component_id)
    )
    component = base_context["inventories"][epsilon_id]["components"][
        component_id
    ]
    windings = suffix_windings(component)
    template.update(
        {
            "component_id": component_id,
            "job_id": f"{epsilon_id}_{component_id}_DERIVED",
            "family": component["family"],
            "owner_summand": component["owner_summand"],
            "base_raw_contribution": complex_dictionary(
                complex(component["raw_contribution"])
            ),
            "representative_pair": component["representative"][
                "representing_pairs"
            ][0],
            "reciprocal_pair": component["reciprocal"][
                "representing_pairs"
            ][0],
            "representative_anchor": complex_dictionary(
                complex(component["representative_root"])
            ),
            "reciprocal_anchor": complex_dictionary(
                complex(component["reciprocal_root"])
            ),
            "representative_chamber": int(
                component["representative"]["chamber_index"]
            ),
            "reciprocal_chamber": int(
                component["reciprocal"]["chamber_index"]
            ),
            "expected_u_winding": windings["u"],
            "expected_v_winding": windings["v"],
            "match_projective_residual": float(
                component["reciprocal_pair_residual"]
            ),
            "job_input_hash": "DERIVED_FROM_EXACT_5277_5280_INVENTORY",
        }
    )
    return template


def derived_job_rows(
    base_context: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    dict[tuple[str, str], dict[str, Any]],
]:
    rows: list[dict[str, Any]] = []
    jobs: dict[tuple[str, str], dict[str, Any]] = {}
    for epsilon_id in REGULATOR_IDS:
        for component_id, template_component_id in (
            HIDDEN_COMPONENT_TEMPLATES.items()
        ):
            job = derived_hidden_job(
                epsilon_id,
                component_id,
                template_component_id,
                base_context,
            )
            jobs[(epsilon_id, component_id)] = job
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "component_id": component_id,
                    "template_component_id": template_component_id,
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
                "reciprocal_anchor_real": job["reciprocal_anchor"]["real"],
                "reciprocal_anchor_imaginary": job[
                    "reciprocal_anchor"
                ]["imaginary"],
                "expected_u_winding": job["expected_u_winding"],
                "expected_v_winding": job["expected_v_winding"],
                "source_topology": job["source_topology"],
                "source_topology_sha256": job[
                    "source_topology_sha256"
                ],
                "derivation": (
                    "template supplies only frozen topology/config; "
                    "component pair, anchors, chambers, and windings are "
                    "copied from the exact parent inventory"
                ),
                    "valid_for_hidden_inventory_derived_job": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows, jobs


def reflected_node_lookup(
    nodes: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    coordinate_lookup = {
        (
            round(float(row["soft_cosine"]), 12),
            round(float(row["decay_cosine"]), 12),
        ): row
        for row in nodes
    }
    return {
        row["angular_node_id"]: coordinate_lookup[
            (
                round(float(row["soft_cosine"]), 12),
                round(-float(row["decay_cosine"]), 12),
            )
        ]
        for row in nodes
    }


def symmetry_audit_rows(
    nodes: list[dict[str, Any]],
    base_context: dict[str, Any],
) -> list[dict[str, Any]]:
    reflections = reflected_node_lookup(nodes)
    rows: list[dict[str, Any]] = []
    for owner_node in nodes:
        mirror_node = reflections[owner_node["angular_node_id"]]
        owner_context = M5287.local_context(base_context, owner_node)
        mirror_context = M5287.local_context(base_context, mirror_node)
        owner_cache: dict[tuple[str, float, str], Any] = {}
        mirror_cache: dict[tuple[str, float, str], Any] = {}
        for epsilon_id in REGULATOR_IDS:
            for energy in SYMMETRY_TEST_ENERGIES:
                owner = M5287.evaluate_component_cached(
                    owner_context,
                    epsilon_id,
                    OWNER_COMPONENT_ID,
                    energy,
                    owner_cache,
                    convergence_audit=True,
                )
                mirror = M5287.evaluate_component_cached(
                    mirror_context,
                    epsilon_id,
                    MIRROR_COMPONENT_ID,
                    energy,
                    mirror_cache,
                    convergence_audit=True,
                )
                owner_value = complex(owner["residue"])
                mirror_value = complex(mirror["residue"])
                relative = relative_complex_difference(
                    owner_value,
                    mirror_value,
                )
                passed = (
                    relative <= SYMMETRY_RELATIVE_LIMIT
                    and parse_bool(owner["mask_active"])
                    == parse_bool(mirror["mask_active"])
                )
                rows.append(
                    {
                        "owner_angular_node_id": owner_node[
                            "angular_node_id"
                        ],
                        "owner_component_id": OWNER_COMPONENT_ID,
                        "mirror_angular_node_id": mirror_node[
                            "angular_node_id"
                        ],
                        "mirror_component_id": MIRROR_COMPONENT_ID,
                        "epsilon_id": epsilon_id,
                        "soft_energy": energy,
                        **complex_fields("owner_residue", owner_value),
                        **complex_fields("mirror_residue", mirror_value),
                        "relative_difference": relative,
                        "owner_mask_active": owner["mask_active"],
                        "mirror_mask_active": mirror["mask_active"],
                        "symmetry_passed": passed,
                        "valid_for_hidden_decay_reflection_transport": passed,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    return rows


def scan_key(
    node_id: str,
    epsilon_id: str,
    component_id: str,
) -> str:
    return f"{node_id}|{epsilon_id}|{component_id}"


def scan_owner_poles(
    nodes: list[dict[str, Any]],
    jobs: dict[tuple[str, str], dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[tuple[str, str, str], dict[str, Any]],
]:
    existing_jobs = read_csv(SCAN_JOBS) if SCAN_JOBS.exists() else []
    existing_poles = read_csv(SCANNED_POLES) if SCANNED_POLES.exists() else []
    completed = {
        row["scan_key"]
        for row in existing_jobs
        if parse_bool(row["scan_completed"])
        and row.get("revision", "") == REVISION
    }
    scan_rows = [
        dict(row)
        for row in existing_jobs
        if row["scan_key"] in completed
        and row.get("revision", "") == REVISION
    ]
    poles = [
        dict(row)
        for row in existing_poles
        if scan_key(
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
        )
        in completed
    ]
    problems: dict[tuple[str, str, str], dict[str, Any]] = {}
    for node in nodes:
        for epsilon_id in REGULATOR_IDS:
            for component_id in HIDDEN_COMPONENT_TEMPLATES:
                key = (
                    node["angular_node_id"],
                    epsilon_id,
                    component_id,
                )
                text_key = scan_key(
                    node["angular_node_id"],
                    epsilon_id,
                    component_id,
                )
                problem = M5286.angular_problem(
                    jobs[(epsilon_id, component_id)],
                    float(node["soft_cosine"]),
                    float(node["decay_cosine"]),
                )
                problems[key] = problem
                if text_key in completed:
                    continue
                _, _, local_poles, _ = M5267.M5239.scan_problem(problem)
                local_rows = [
                    {
                        "angular_node_id": node["angular_node_id"],
                        "soft_cosine": node["soft_cosine"],
                        "decay_cosine": node["decay_cosine"],
                        "epsilon_id": epsilon_id,
                        "component_id": component_id,
                        "scan_owner_component_id": component_id,
                        "family_scan_source_component_id": component_id,
                        "family_scan_transport": False,
                        **source,
                        "valid_for_hidden_owner_pole_scan": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                    for source in local_poles
                ]
                poles.extend(local_rows)
                scan_rows.append(
                    {
                        "scan_key": text_key,
                        "angular_node_id": node["angular_node_id"],
                        "epsilon_id": epsilon_id,
                        "component_id": component_id,
                        "geometric_pole_count": len(local_rows),
                        "scan_completed": True,
                        "revision": REVISION,
                        "valid_for_hidden_owner_pole_scan": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
                completed.add(text_key)
                write_csv(SCAN_JOBS, scan_rows)
                if poles:
                    write_csv(SCANNED_POLES, poles)
                atomic_json(
                    STATUS,
                    {
                        "checkpoint": CHECKPOINT,
                        "state": "RUNNING",
                        "stage": "HIDDEN_OWNER_SCAN",
                        "last_completed_scan_key": text_key,
                        "completed_scan_count": len(completed),
                        "total_scan_count": (
                            len(nodes)
                            * len(REGULATOR_IDS)
                            * len(HIDDEN_COMPONENT_TEMPLATES)
                        ),
                        "geometric_pole_count": len(poles),
                    },
                )
    return scan_rows, poles, problems


def derive_owner_residues(
    roots: list[dict[str, Any]],
    problems: dict[tuple[str, str, str], dict[str, Any]],
    base_context: dict[str, Any],
    nodes: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    M5291.configure_generalized_5288(nodes)
    M5288.STATUS = STATUS
    M5288.CHECKPOINT = CHECKPOINT
    samples: list[dict[str, Any]] = []
    fits: list[dict[str, Any]] = []
    residues: list[dict[str, Any]] = []
    original_radii = M5288.pole_fit_radii
    for node in nodes:
        node_id = node["angular_node_id"]
        local_roots = [
            row for row in roots if row["angular_node_id"] == node_id
        ]
        M5288.pole_fit_radii = (
            lambda root, _rows, local=local_roots: original_radii(
                root,
                local,
            )
        )
        for root in local_roots:
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
        if local_roots:
            write_csv(POLE_SAMPLES, samples)
            write_csv(POLE_FITS, fits)
            write_csv(OWNER_RESIDUES, residues)
    M5288.pole_fit_radii = original_radii
    return samples, fits, residues


def transport_residues(
    owner_rows: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    reflections = reflected_node_lookup(nodes)
    final_rows = [dict(row) for row in owner_rows]
    for row in final_rows:
        row["symmetry_derived"] = False
        row["symmetry_source_angular_node_id"] = row[
            "angular_node_id"
        ]
        row["symmetry_source_component_id"] = OWNER_COMPONENT_ID
    for source in owner_rows:
        mirror_node = reflections[source["angular_node_id"]]
        row = dict(source)
        row["angular_node_id"] = mirror_node["angular_node_id"]
        row["soft_cosine"] = mirror_node["soft_cosine"]
        row["decay_cosine"] = mirror_node["decay_cosine"]
        row["component_id"] = MIRROR_COMPONENT_ID
        row["pole_id"] = str(row["pole_id"]).replace(
            OWNER_COMPONENT_ID,
            MIRROR_COMPONENT_ID,
            1,
        )
        row["symmetry_derived"] = True
        row["symmetry_sign"] = 1
        row["symmetry_source_angular_node_id"] = source[
            "angular_node_id"
        ]
        row["symmetry_source_component_id"] = OWNER_COMPONENT_ID
        final_rows.append(row)
    return final_rows


def resolve_controls_and_bounds(
    final_rows: list[dict[str, Any]],
    owner_fits: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], float, float]:
    fit_groups: dict[
        tuple[str, str, str, str],
        list[dict[str, Any]],
    ] = defaultdict(list)
    for row in owner_fits:
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
    multiplier = abs(M5292.physical_multiplier())
    minimum = float(M5267.ENERGY_MINIMUM)
    maximum = float(M5267.ENERGY_MAXIMUM)
    bounds: list[dict[str, Any]] = []
    global_absolute_bound = 0.0
    for row in final_rows:
        row["symmetry_derived"] = False
        row["symmetry_source_angular_node_id"] = row[
            "angular_node_id"
        ]
        row["symmetry_source_component_id"] = row["component_id"]
        controlled = parse_bool(row["pole_residue_controls_pass"])
        material = parse_bool(row["material_pole"])
        row["bounded_ambiguous_residue"] = False
        row["valid_for_hidden_track_pole_subtraction"] = (
            controlled and material
        )
        row["hidden_track_pole_resolution"] = (
            "CERTIFIED_MATERIAL_SIMPLE_POLE"
            if controlled and material
            else "CERTIFIED_REMOVABLE_BOUNDED_ZERO"
            if controlled
            else "UNRESOLVED"
        )
        if controlled:
            continue
        source_node_id = row["angular_node_id"]
        source_pole_id = row["pole_id"]
        local_fits = fit_groups[
            (
                source_node_id,
                row["epsilon_id"],
                row["component_id"],
                source_pole_id,
            )
        ]
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
        row["valid_for_hidden_track_pole_subtraction"] = bound_valid
        row["hidden_track_pole_resolution"] = (
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
                "symmetry_source_angular_node_id": source_node_id,
                "residue_magnitude_upper_bound": envelope,
                "maximum_fit_relative_residual": maximum_fit_residual,
                "maximum_coefficient_relative_change": (
                    maximum_coefficient_change
                ),
                "analytic_log_factor_magnitude": abs(analytic_log),
                "physical_outer_absolute_bound": physical_outer_bound,
                "bound_valid": bound_valid,
                "valid_for_hidden_track_pole_subtraction": bound_valid,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        global_absolute_bound += physical_outer_bound
    reference = read_json(ORDER2_RESULT_5290)[
        "order2_energy8_eight_component_integral"
    ]
    reference_magnitude = abs(
        complex(float(reference["real"]), float(reference["imaginary"]))
    )
    global_relative_bound = global_absolute_bound / max(
        reference_magnitude,
        1.0e-300,
    )
    if bounds:
        write_csv(AMBIGUOUS_BOUNDS, bounds)
    write_csv(FINAL_RESIDUES, final_rows)
    return final_rows, bounds, global_absolute_bound, global_relative_bound


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5292,
        RESULT_5292,
        MANIFEST_5292,
        RESULT_5291,
        VALIDATION_5291,
        ANGULAR_NODES_5291,
        ORDER2_RESULT_5290,
        M5267.MANIFEST_5239,
    )
    parent = read_json(RESULT_5292)
    checks = {
        "required_sources_exist": all(path.exists() for path in required),
        "failed_5292_run_completed_all_nodes": (
            parent["decision"] == "ORDER4_INNER_ENERGY_REQUIRES_LOCAL_REPAIR"
            and len(read_csv(MANIFEST_5292)) == 16
            and all(
                parse_bool(row["node_run_completed"])
                for row in read_csv(MANIFEST_5292)
            )
        ),
        "parent_5291_atlas_accepted": bool(
            read_json(RESULT_5291)["acceptance_passed"]
        ),
        "parent_5291_atlas_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5291)
        ),
        "sixteen_order4_nodes_parse": (
            len(read_csv(ANGULAR_NODES_5291)) == 16
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
        "planned_hidden_owner_scan_count": 64,
        "decision": (
            "DRY_RUN_ACCEPTED__DERIVE_HIDDEN_TRACK_POLE_ATLAS"
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
        raise RuntimeError("5293 dry run did not pass")
    parent = read_json(RESULT_5292)
    nodes = read_csv(ANGULAR_NODES_5291)
    base_context = M5280.source_context()
    job_rows, jobs = derived_job_rows(base_context)
    write_csv(DERIVED_JOBS, job_rows)
    symmetry = symmetry_audit_rows(nodes, base_context)
    write_csv(SYMMETRY_AUDIT, symmetry)
    scan_jobs, scanned, problems = scan_owner_poles(nodes, jobs)
    if not scanned:
        raise RuntimeError("hidden-track scan found no geometric poles")
    classified = M5291.classify_exact_masks(
        scanned,
        nodes,
        base_context,
    )
    write_csv(CLASSIFIED_POLES, classified)
    M5291.configure_generalized_5288(nodes)
    M5288.STATUS = STATUS
    M5288.CHECKPOINT = CHECKPOINT
    roots = M5288.refine_active_channel_roots(classified, problems)
    if not roots:
        raise RuntimeError("hidden-track exact masks activate no roots")
    write_csv(CHANNEL_ROOTS, roots)
    samples, fits, owner_residues = derive_owner_residues(
        roots,
        problems,
        base_context,
        nodes,
    )
    (
        final_residues,
        ambiguous_bounds,
        ambiguous_absolute_bound,
        ambiguous_relative_bound,
    ) = resolve_controls_and_bounds(owner_residues, fits, nodes)
    material = [
        row
        for row in final_residues
        if parse_bool(row["material_pole"])
    ]
    bounded = [
        row
        for row in final_residues
        if parse_bool(row["bounded_ambiguous_residue"])
    ]
    removable = [
        row
        for row in final_residues
        if not parse_bool(row["material_pole"])
        and not parse_bool(row["bounded_ambiguous_residue"])
    ]
    maximum_symmetry_residual = max(
        float(row["relative_difference"]) for row in symmetry
    )
    maximum_root_residual = max(
        float(row["channel_root_residual"]) for row in roots
    )
    maximum_fit_residual = max(
        float(row["fit_relative_residual"]) for row in owner_residues
    )
    checks = {
        "four_inventory_derived_jobs_complete": (
            len(job_rows) == 4
            and all(
                parse_bool(row["valid_for_hidden_inventory_derived_job"])
                for row in job_rows
            )
        ),
        "MC02_MC08_global_decay_reflection_transport_rejected": (
            len(symmetry)
            == 16 * len(REGULATOR_IDS) * len(SYMMETRY_TEST_ENERGIES)
            and maximum_symmetry_residual > 1.0e-2
            and any(
                not parse_bool(row["symmetry_passed"]) for row in symmetry
            )
        ),
        "all_sixty_four_hidden_scans_complete": (
            len(scan_jobs) == 64
            and len({row["scan_key"] for row in scan_jobs}) == 64
        ),
        "all_hidden_geometric_poles_classified": (
            len(classified) == len(scanned)
        ),
        "all_exact_active_roots_have_owner_residue": (
            len(roots) == len(owner_residues)
        ),
        "all_hidden_rows_derived_independently": (
            len(final_residues) == len(owner_residues)
            and all(
                not parse_bool(row["symmetry_derived"])
                for row in final_residues
            )
        ),
        "at_least_one_new_hidden_material_pole": bool(material),
        "all_hidden_roots_resolved_by_control_or_bound": all(
            parse_bool(row["pole_residue_controls_pass"])
            or (
                parse_bool(row["bounded_ambiguous_residue"])
                and parse_bool(
                    row["valid_for_hidden_track_pole_subtraction"]
                )
            )
            for row in final_residues
        ),
        "all_ambiguous_bounds_valid": all(
            parse_bool(row["bound_valid"]) for row in ambiguous_bounds
        ),
        "ambiguous_global_bound_below_budget": (
            ambiguous_relative_bound
            <= AMBIGUOUS_GLOBAL_RELATIVE_BOUND_LIMIT
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
        "mode": "hidden-track-pole-atlas-and-symmetry-transport",
        "checks": checks,
        "acceptance_passed": accepted,
        "derived_job_count": len(job_rows),
        "symmetry_audit_count": len(symmetry),
        "maximum_symmetry_relative_residual": maximum_symmetry_residual,
        "owner_scan_count": len(scan_jobs),
        "owner_geometric_pole_count": len(scanned),
        "exact_active_owner_root_count": len(roots),
        "owner_selected_residue_count": len(owner_residues),
        "independent_final_residue_count": len(final_residues),
        "material_hidden_pole_count": len(material),
        "removable_hidden_pole_count": len(removable),
        "bounded_ambiguous_hidden_pole_count": len(bounded),
        "maximum_channel_root_residual": maximum_root_residual,
        "maximum_selected_pole_fit_residual": maximum_fit_residual,
        "ambiguous_global_absolute_error_bound": (
            ambiguous_absolute_bound
        ),
        "ambiguous_global_relative_error_bound": (
            ambiguous_relative_bound
        ),
        "pole_sample_count": len(samples),
        "pole_fit_count": len(fits),
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
            "CERTIFY_HIDDEN_TRACK_POLE_ATLAS__"
            "REASSEMBLE_STORED_ORDER4_NODES"
            if accepted
            else "HIDDEN_TRACK_POLE_ATLAS_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_hidden_track_pole_atlas": accepted,
            "valid_for_stored_node_reassembly": accepted,
            "valid_for_full_angular_convergence": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This repairs the omitted MC02/MC08 source-pair tracks. "
                "The completed order-four nodes must still be "
                "reassembled and pass their energy gates."
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
            "material_hidden_pole_count": len(material),
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
    text = f"""# 5293 — Hidden-track pole atlas and symmetry transport

## Result

Checkpoint 5292 showed that the order-four failures were dominated by
`MC02/MC08`. The prior atlas had reused a visible component's track
because the family label matched. The exact parent inventory instead
contains distinct source-pair indices, anchors, chambers, and windings.
This checkpoint derives the missing `MC02` jobs from those parent-owned
fields. The low-energy relation `MC02(s,d)=MC08(s,-d)` fails globally
after exact-mask branch changes, so both hidden components are scanned
and residue-fitted independently rather than transported.

- independent hidden scans: `{result['owner_scan_count']}`;
- geometric poles: `{result['owner_geometric_pole_count']}`;
- exact-active owner roots: `{result['exact_active_owner_root_count']}`;
- independently derived material hidden poles:
  `{result['material_hidden_pole_count']}`;
- removable hidden roots:
  `{result['removable_hidden_pole_count']}`;
- bounded ambiguous hidden roots:
  `{result['bounded_ambiguous_hidden_pole_count']}`;
- maximum symmetry residual:
  `{result['maximum_symmetry_relative_residual']:.12g}`.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This is a derived numerical repair of the hidden source tracks, not a
phase-space or UV claim. Its effect must be checked by reassembling the
already evaluated order-four nodes.

## Next target

Replay the 5292 stored quadrature nodes with these supplemental poles.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    required = (
        DRY_RUN,
        DERIVED_JOBS,
        SYMMETRY_AUDIT,
        SCAN_JOBS,
        SCANNED_POLES,
        CLASSIFIED_POLES,
        CHANNEL_ROOTS,
        POLE_SAMPLES,
        POLE_FITS,
        OWNER_RESIDUES,
        FINAL_RESIDUES,
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
        DERIVED_JOBS,
        SYMMETRY_AUDIT,
        SCAN_JOBS,
        SCANNED_POLES,
        CLASSIFIED_POLES,
        CHANNEL_ROOTS,
        POLE_SAMPLES,
        POLE_FITS,
        OWNER_RESIDUES,
        FINAL_RESIDUES,
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
            "HIDDEN_TRACK_ATLAS_ACCEPTED",
            bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            all(parsed[path] for path in csv_paths),
            f"{len(csv_paths)}/{len(csv_paths)} non-empty CSVs",
        ),
        validation_gate(
            "SYMMETRY_AND_SCAN_COUNTS_CLOSE",
            len(parsed[SYMMETRY_AUDIT]) == 256
            and len(parsed[SCAN_JOBS]) == 64,
            (
                f"symmetry={len(parsed[SYMMETRY_AUDIT])}; "
                f"scans={len(parsed[SCAN_JOBS])}"
            ),
        ),
        validation_gate(
            "ALL_HIDDEN_ROOTS_RESOLVED",
            len(parsed[FINAL_RESIDUES])
            == len(parsed[OWNER_RESIDUES])
            and all(
                parse_bool(row["pole_residue_controls_pass"])
                or (
                    parse_bool(row["bounded_ambiguous_residue"])
                    and parse_bool(
                        row[
                            "valid_for_hidden_track_pole_subtraction"
                        ]
                    )
                )
                for row in parsed[FINAL_RESIDUES]
            ),
            (
                f"owner={len(parsed[OWNER_RESIDUES])}; "
                f"final={len(parsed[FINAL_RESIDUES])}; "
                f"material={result['material_hidden_pole_count']}"
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
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_HIDDEN_TRACK_POLE_ATLAS"
            if passed
            else "HIDDEN_TRACK_POLE_ATLAS_VALIDATION_FAILED"
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
