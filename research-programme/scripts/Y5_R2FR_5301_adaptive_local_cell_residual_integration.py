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
SOURCE = FUNCTIONAL_RG / "5301"

SCRIPT_5291 = SCRIPTS / "Y5_R2FR_5291_order4_complete_singularity_atlas.py"
SCRIPT_5297 = SCRIPTS / "Y5_R2FR_5297_order8_exact_component_singularity_atlas.py"
SCRIPT_5300 = SCRIPTS / "Y5_R2FR_5300_adaptive_interior_ridge_width_probe.py"
RESULT_5300 = (
    FUNCTIONAL_RG / "5300" / "adaptive_ridge_width_probe_result.json"
)
VALIDATION_5300 = (
    FUNCTIONAL_RG / "5300" / "adaptive_ridge_width_probe_validation.csv"
)
ORBITS_5300 = FUNCTIONAL_RG / "5300" / "adaptive_ridge_orbit_values.csv"
ORBITS_5299 = FUNCTIONAL_RG / "5299" / "angular_sign_orbit_samples.csv"
OUTER_5298 = FUNCTIONAL_RG / "5298" / "order8_outer_totals.csv"
VALIDATION_5297 = (
    FUNCTIONAL_RG / "5297" / "order8_exact_component_atlas_validation.csv"
)
ORDER4_CACHE = FUNCTIONAL_RG / "5291"

DRY_RUN = SOURCE / "adaptive_local_cell_dry_run.json"
TARGETS = SOURCE / "adaptive_local_cell_target_orbits.csv"
ATLAS_DRY_RUN = SOURCE / "adaptive_local_cell_atlas_dry_run.json"
ADAPTIVE_NODES = SOURCE / "adaptive_local_cell_signed_nodes.csv"
EXACT_JOBS = SOURCE / "adaptive_local_cell_exact_component_jobs.csv"
SCAN_JOBS = SOURCE / "adaptive_local_cell_exact_scan_jobs.csv"
GEOMETRIC_POLES = SOURCE / "adaptive_local_cell_geometric_poles.csv"
EXPANDED_POLES = SOURCE / "adaptive_local_cell_expanded_geometric_poles.csv"
CLASSIFIED_POLES = SOURCE / "adaptive_local_cell_exact_mask_poles.csv"
CHANNEL_ROOTS = SOURCE / "adaptive_local_cell_channel_roots.csv"
POLE_SAMPLES = SOURCE / "adaptive_local_cell_pole_samples.csv"
POLE_FITS = SOURCE / "adaptive_local_cell_pole_fits.csv"
POLE_RESIDUES = SOURCE / "adaptive_local_cell_selected_pole_residues.csv"
AMBIGUOUS_BOUNDS = SOURCE / "adaptive_local_cell_ambiguous_pole_bounds.csv"
ENDPOINT_SAMPLES = SOURCE / "adaptive_local_cell_endpoint_samples.csv"
ENDPOINT_FITS = SOURCE / "adaptive_local_cell_endpoint_fits.csv"
ENDPOINT_COEFFICIENTS = (
    SOURCE / "adaptive_local_cell_endpoint_coefficients.csv"
)
ENDPOINT_CANCELLATIONS = (
    SOURCE / "adaptive_local_cell_endpoint_cancellations.csv"
)
ATLAS_RESULT = SOURCE / "adaptive_local_cell_atlas_result.json"
NODE_RUNS = SOURCE / "nodes"
NODE_MANIFEST = SOURCE / "adaptive_local_cell_node_run_manifest.csv"
COMPONENT_TOTALS = SOURCE / "adaptive_local_cell_component_totals.csv"
INNER_TOTALS = SOURCE / "adaptive_local_cell_inner_energy_totals.csv"
INNER_CONVERGENCE = (
    SOURCE / "adaptive_local_cell_inner_energy_convergence.csv"
)
ORBIT_VALUES = SOURCE / "adaptive_local_cell_orbit_values.csv"
INTERPOLANT_BASIS = SOURCE / "order8_even_interpolant_basis.csv"
RESIDUAL_SAMPLES = SOURCE / "adaptive_local_cell_residual_samples.csv"
QUADRATURE_WEIGHTS = SOURCE / "adaptive_local_cell_quadrature_weights.csv"
INTEGRATION_COMPARISON = (
    SOURCE / "adaptive_local_cell_integration_comparison.csv"
)
CACHE_ISOLATION = SOURCE / "order4_cache_isolation_audit.csv"
CONTOUR_SILENCE = SOURCE / "contour_resolved_pole_silence.csv"
RESULT = SOURCE / "adaptive_local_cell_residual_integration_result.json"
VALIDATION = SOURCE / "adaptive_local_cell_residual_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5301_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5301-Y5-R2FR-adaptive-local-cell-residual-integration.md"

CHECKPOINT = 5301
PARENT_CHECKPOINT = 5300
MARKER = "MTS_5301_ADAPTIVE_LOCAL_CELL_RESIDUAL_INTEGRATION"
REVISION = "adaptive-local-cell-residual-integration-v1"
EXPECTED_ORBIT_COUNT = 6
EXPECTED_NODE_COUNT = 24
ENERGY_ORDERS = (4, 8)
CORE_MODEL_CHANGE_LIMIT = 5.0e-2
CORE_BOUNDARY_RESIDUAL_RATIO_LIMIT = 2.5e-1
CONTOUR_EXACT_RELATIVE_ERROR_LIMIT = 1.0e-9
CONTOUR_ORDER_CHANGE_LIMIT = 1.0e-5
CONTOUR_OFFSET_SCALES = (
    0.25,
    0.5,
    1.0,
    2.0,
    4.0,
    8.0,
    16.0,
    32.0,
    64.0,
    128.0,
)
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


M5300 = load_module("mts_5300_for_5301", SCRIPT_5300)
M5283 = M5300.M5283
np = M5300.M5295.np
mp = M5300.mp


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    process_handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(process_handle, 0x00004000)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )
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


def relative_complex_change(first: complex, second: complex) -> float:
    return abs(second - first) / max(abs(second), 1.0e-300)


def ridge_coordinates() -> tuple[float, float, float]:
    rows = read_csv(ORBITS_5300)
    lookup = {
        row["target_id"]: float(row["absolute_soft_cosine"])
        for row in rows
    }
    return (
        lookup["RIDGE_LOWER_DIAGONAL_MIDPOINT"],
        lookup["RIDGE_ANCHOR_EXISTING_ORDER4"],
        lookup["RIDGE_UPPER_DIAGONAL_MIDPOINT"],
    )


def target_rows() -> list[dict[str, Any]]:
    lower, center, upper = ridge_coordinates()
    coordinate_rows = (
        ("CELL_LC", lower, center),
        ("CELL_CL", center, lower),
        ("CELL_LU", lower, upper),
        ("CELL_UL", upper, lower),
        ("CELL_CU", center, upper),
        ("CELL_UC", upper, center),
    )
    return [
        {
            "target_id": target_id,
            "absolute_soft_cosine": soft_value,
            "absolute_decay_cosine": decay_value,
            "sign_orbit_node_count": 4,
            "requires_new_exact_node_runs": True,
            "selection_reason": (
                "complete the missing off-diagonal entries of the "
                "three-by-three local ridge cell"
            ),
            "valid_for_adaptive_local_cell_target": True,
            **{field: False for field in CLAIM_FIELDS},
        }
        for target_id, soft_value, decay_value in coordinate_rows
    ]


def adaptive_nodes() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target_index, target in enumerate(target_rows(), start=1):
        absolute_soft = float(target["absolute_soft_cosine"])
        absolute_decay = float(target["absolute_decay_cosine"])
        for soft_sign_index, soft_sign in enumerate((-1.0, 1.0), start=1):
            for decay_sign_index, decay_sign in enumerate(
                (-1.0, 1.0),
                start=1,
            ):
                rows.append(
                    {
                        "angular_node_id": (
                            f"AC{target_index:02d}_"
                            f"S{soft_sign_index:02d}_"
                            f"D{decay_sign_index:02d}"
                        ),
                        "target_id": target["target_id"],
                        "absolute_soft_cosine": absolute_soft,
                        "absolute_decay_cosine": absolute_decay,
                        "soft_sign": int(soft_sign),
                        "decay_sign": int(decay_sign),
                        "soft_cosine": soft_sign * absolute_soft,
                        "decay_cosine": decay_sign * absolute_decay,
                        "angular_weight": 1.0,
                        "angular_jacobian": (
                            M5300.M5280.M5278.ANGULAR_JACOBIAN
                        ),
                        "diagnostic_measure_weight_only": True,
                        "valid_for_adaptive_local_cell_node": True,
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
    return rows


def pole_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(row["angular_node_id"]),
        str(row["epsilon_id"]),
        str(row["component_id"]),
        str(row["pole_id"]),
    )


def unresolved_residue_rows() -> list[dict[str, str]]:
    if not POLE_RESIDUES.exists():
        return []
    return [
        row
        for row in read_csv(POLE_RESIDUES)
        if not parse_bool(row["pole_residue_controls_pass"])
        and not (
            parse_bool(row["bounded_ambiguous_residue"])
            and parse_bool(
                row["valid_for_adaptive_ridge_pole_subtraction"]
            )
        )
    ]


def refined_pole_lookup() -> dict[
    tuple[str, str, str, str],
    complex,
]:
    return {
        pole_key(row): complex(
            float(row["refined_pole_real"]),
            float(row["refined_pole_imaginary"]),
        )
        for row in read_csv(CHANNEL_ROOTS)
    }


def contour_aware_pole_lookup(
    include_unresolved: bool = False,
) -> dict[
    tuple[str, str, str],
    list[dict[str, Any]],
]:
    roots = refined_pole_lookup()
    grouped: dict[
        tuple[str, str, str],
        list[dict[str, Any]],
    ] = {}
    for row in read_csv(POLE_RESIDUES):
        valid_subtraction = parse_bool(
            row["valid_for_adaptive_ridge_pole_subtraction"]
        )
        center_only = parse_bool(
            row.get("valid_for_contour_center_only", False)
        )
        unresolved = (
            not parse_bool(row["pole_residue_controls_pass"])
            and not valid_subtraction
        )
        if include_unresolved and unresolved:
            center_only = True
        if not valid_subtraction and not center_only:
            continue
        key = (
            row["angular_node_id"],
            row["epsilon_id"],
            row["component_id"],
        )
        pole = roots.get(
            pole_key(row),
            complex(float(row["pole_real"]), float(row["pole_imaginary"])),
        )
        residue = (
            complex(
                float(row["true_limit_residue_real"]),
                float(row["true_limit_residue_imaginary"]),
            )
            if valid_subtraction
            else 0.0j
        )
        grouped.setdefault(key, []).append(
            {
                "pole": pole,
                "residue": residue,
                "bounded_ambiguous": complex(
                    1.0
                    if parse_bool(row["bounded_ambiguous_residue"])
                    else 0.0,
                    0.0,
                ),
                "contour_center_only": center_only,
                "pole_id": row["pole_id"],
            }
        )
    return grouped


def adaptive_node_panels(
    angular_node_id: str,
    context: dict[str, Any],
    poles: dict[
        tuple[str, str, str],
        list[dict[str, Any]],
    ],
) -> tuple[list[dict[str, Any]], int, int]:
    mask_boundaries = M5300.M5280.exact_energy_mask_boundaries(context)
    local_terms = [
        term
        for key, terms in poles.items()
        if key[0] == angular_node_id
        for term in terms
    ]
    centers = [{"center": term["pole"].real} for term in local_terms]
    base_panels = M5300.M5280.composite_panel_rows(
        mask_boundaries,
        centers,
    )
    minimum = float(M5300.M5292.M5267.ENERGY_MINIMUM)
    maximum = float(M5300.M5292.M5267.ENERGY_MAXIMUM)
    boundaries = {
        float(row["lower"]) for row in base_panels
    } | {float(row["upper"]) for row in base_panels}
    for term in local_terms:
        if not bool(term.get("contour_center_only", False)):
            continue
        pole = complex(term["pole"])
        distance = max(abs(pole.imag), 1.0e-14)
        for scale in CONTOUR_OFFSET_SCALES:
            for sign in (-1.0, 1.0):
                coordinate = pole.real + sign * scale * distance
                if minimum < coordinate < maximum:
                    boundaries.add(coordinate)
    ordered = sorted(boundaries)
    refined_input = [
        {
            "lower": lower,
            "upper": upper,
        }
        for lower, upper in zip(ordered[:-1], ordered[1:])
    ]
    panels = M5300.M5295.M5287.endpoint_refined_panels(
        refined_input
    )
    return panels, len(mask_boundaries), len(centers)


def pole_kernel_quadrature(
    pole: complex,
    panels: list[dict[str, Any]],
    order: int,
) -> complex:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    total = 0.0j
    for panel in panels:
        lower = float(panel["lower"])
        upper = float(panel["upper"])
        half_width = 0.5 * (upper - lower)
        midpoint = 0.5 * (upper + lower)
        total += sum(
            (
                half_width
                * float(weight)
                / (
                    midpoint
                    + half_width * float(node)
                    - pole
                )
                for node, weight in zip(nodes, weights)
            ),
            0.0j,
        )
    return total


def contour_silence_rows() -> list[dict[str, Any]]:
    unresolved = unresolved_residue_rows()
    if not unresolved:
        return read_csv(CONTOUR_SILENCE)
    nodes = {
        row["angular_node_id"]: row for row in read_csv(ADAPTIVE_NODES)
    }
    roots = refined_pole_lookup()
    poles = contour_aware_pole_lookup(include_unresolved=True)
    base_context = M5300.M5280.source_context()
    minimum = float(M5300.M5292.M5267.ENERGY_MINIMUM)
    maximum = float(M5300.M5292.M5267.ENERGY_MAXIMUM)
    panel_cache: dict[str, list[dict[str, Any]]] = {}
    rows: list[dict[str, Any]] = []
    for residue in unresolved:
        node_id = residue["angular_node_id"]
        if node_id not in panel_cache:
            context = M5300.M5295.M5287.local_context(
                base_context,
                nodes[node_id],
            )
            panel_cache[node_id] = adaptive_node_panels(
                node_id,
                context,
                poles,
            )[0]
        panels = panel_cache[node_id]
        pole = roots[pole_key(residue)]
        exact = cmath.log(maximum - pole) - cmath.log(minimum - pole)
        order4 = pole_kernel_quadrature(pole, panels, 4)
        order8 = pole_kernel_quadrature(pole, panels, 8)
        exact_error = relative_complex_change(exact, order8)
        order_change = relative_complex_change(order4, order8)
        passed = (
            abs(pole.imag) > 0.0
            and exact_error <= CONTOUR_EXACT_RELATIVE_ERROR_LIMIT
            and order_change <= CONTOUR_ORDER_CHANGE_LIMIT
        )
        rows.append(
            {
                "angular_node_id": node_id,
                "epsilon_id": residue["epsilon_id"],
                "component_id": residue["component_id"],
                "pole_id": residue["pole_id"],
                "pole_real": pole.real,
                "pole_imaginary": pole.imag,
                "distance_from_real_contour": abs(pole.imag),
                "energy_panel_count": len(panels),
                "minimum_energy_panel_width": min(
                    float(panel["upper"]) - float(panel["lower"])
                    for panel in panels
                ),
                **complex_fields("analytic_pole_kernel_integral", exact),
                **complex_fields("order4_pole_kernel_integral", order4),
                **complex_fields("order8_pole_kernel_integral", order8),
                "order8_exact_relative_error": exact_error,
                "order4_order8_relative_change": order_change,
                "order8_exact_relative_error_limit": (
                    CONTOUR_EXACT_RELATIVE_ERROR_LIMIT
                ),
                "order4_order8_relative_change_limit": (
                    CONTOUR_ORDER_CHANGE_LIMIT
                ),
                "contour_quadrature_controls_pass": passed,
                "valid_for_contour_center_only": passed,
                "valid_for_unsubtracted_original_integrand": passed,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def repair_atlas_with_contour_silence() -> dict[str, Any]:
    silence = contour_silence_rows()
    write_csv(CONTOUR_SILENCE, silence)
    if not silence or not all(
        parse_bool(row["contour_quadrature_controls_pass"])
        for row in silence
    ):
        raise RuntimeError("contour-silence repair did not pass")
    silence_lookup = {pole_key(row): row for row in silence}
    residues = read_csv(POLE_RESIDUES)
    for row in residues:
        local = silence_lookup.get(pole_key(row))
        if local is None:
            continue
        row["bounded_ambiguous_residue"] = False
        row["pole_residue_controls_pass"] = True
        row["valid_for_adaptive_ridge_pole_subtraction"] = False
        row["valid_for_contour_center_only"] = True
        row["contour_quadrature_controls_pass"] = True
        row["contour_order8_exact_relative_error"] = local[
            "order8_exact_relative_error"
        ]
        row["contour_order4_order8_relative_change"] = local[
            "order4_order8_relative_change"
        ]
        row["order6_pole_resolution"] = (
            "CONTOUR_RESOLVED_ORIGINAL_INTEGRAND_NO_SUBTRACTION"
        )
        row["pole_classification"] = (
            "EXACT_ACTIVE_OFF_CONTOUR_POLE_DIRECT_QUADRATURE"
        )
    write_csv(POLE_RESIDUES, residues)
    repaired_keys = set(silence_lookup)
    bounds = [
        row
        for row in read_csv(AMBIGUOUS_BOUNDS)
        if pole_key(row) not in repaired_keys
    ]
    write_csv(AMBIGUOUS_BOUNDS, bounds)
    unresolved = [
        row
        for row in residues
        if not parse_bool(row["pole_residue_controls_pass"])
        and not (
            parse_bool(row["bounded_ambiguous_residue"])
            and parse_bool(
                row["valid_for_adaptive_ridge_pole_subtraction"]
            )
        )
    ]
    result = read_json(ATLAS_RESULT)
    result["checks"]["all_roots_resolved"] = not unresolved
    result["checks"]["all_ambiguous_bounds_valid"] = all(
        parse_bool(row["bound_valid"]) for row in bounds
    )
    result["checks"]["all_contour_silence_controls_pass"] = all(
        parse_bool(row["contour_quadrature_controls_pass"])
        for row in silence
    )
    result["acceptance_passed"] = all(result["checks"].values())
    result["bounded_ambiguous_pole_count"] = sum(
        parse_bool(row["bounded_ambiguous_residue"]) for row in residues
    )
    result["contour_center_only_pole_count"] = len(silence)
    result["maximum_contour_order8_exact_relative_error"] = max(
        float(row["order8_exact_relative_error"]) for row in silence
    )
    result["maximum_contour_order4_order8_relative_change"] = max(
        float(row["order4_order8_relative_change"]) for row in silence
    )
    result["decision"] = (
        "CERTIFY_LOCAL_CELL_ATLAS_WITH_CONTOUR_SILENCE__RUN_NODES"
        if result["acceptance_passed"]
        else "LOCAL_CELL_ATLAS_CONTOUR_REPAIR_FAILED"
    )
    result["claim_boundary"]["valid_for_adaptive_ridge_atlas"] = bool(
        result["acceptance_passed"]
    )
    result["claim_boundary"]["valid_for_adaptive_ridge_node_run"] = bool(
        result["acceptance_passed"]
    )
    atomic_json(ATLAS_RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": (
                "ATLAS_REPAIRED"
                if result["acceptance_passed"]
                else "FAILED"
            ),
            "decision": result["decision"],
            "contour_center_only_pole_count": len(silence),
        },
    )
    if not result["acceptance_passed"]:
        raise RuntimeError(result["decision"])
    return result


def configure_reused_pipeline() -> None:
    assignments = {
        "SOURCE": SOURCE,
        "ATLAS_DRY_RUN": ATLAS_DRY_RUN,
        "ADAPTIVE_NODES": ADAPTIVE_NODES,
        "EXACT_JOBS": EXACT_JOBS,
        "SCAN_JOBS": SCAN_JOBS,
        "GEOMETRIC_POLES": GEOMETRIC_POLES,
        "EXPANDED_POLES": EXPANDED_POLES,
        "CLASSIFIED_POLES": CLASSIFIED_POLES,
        "CHANNEL_ROOTS": CHANNEL_ROOTS,
        "POLE_SAMPLES": POLE_SAMPLES,
        "POLE_FITS": POLE_FITS,
        "POLE_RESIDUES": POLE_RESIDUES,
        "AMBIGUOUS_BOUNDS": AMBIGUOUS_BOUNDS,
        "ENDPOINT_SAMPLES": ENDPOINT_SAMPLES,
        "ENDPOINT_FITS": ENDPOINT_FITS,
        "ENDPOINT_COEFFICIENTS": ENDPOINT_COEFFICIENTS,
        "ENDPOINT_CANCELLATIONS": ENDPOINT_CANCELLATIONS,
        "ATLAS_RESULT": ATLAS_RESULT,
        "NODE_RUNS": NODE_RUNS,
        "NODE_MANIFEST": NODE_MANIFEST,
        "COMPONENT_TOTALS": COMPONENT_TOTALS,
        "INNER_TOTALS": INNER_TOTALS,
        "INNER_CONVERGENCE": INNER_CONVERGENCE,
        "STATUS": STATUS,
        "CHECKPOINT": CHECKPOINT,
        "PARENT_CHECKPOINT": PARENT_CHECKPOINT,
        "MARKER": MARKER,
        "REVISION": REVISION,
        "RESULT_5299": RESULT_5300,
        "VALIDATION_5299": VALIDATION_5300,
        "EXPECTED_ADAPTIVE_NODE_COUNT": EXPECTED_NODE_COUNT,
        "EXPECTED_ADAPTIVE_ORBIT_COUNT": EXPECTED_ORBIT_COUNT,
        "adaptive_nodes": adaptive_nodes,
    }
    for name, value in assignments.items():
        setattr(M5300, name, value)
    M5300.M5295.M5291.install_bounded_root_refinement_fallback()
    robust_refinement = (
        M5300.M5295.M5291.M5280.M5275.refine_relative_root
    )
    M5300.M5280.M5275.refine_relative_root = robust_refinement
    M5300.M5292.M5280.M5275.refine_relative_root = robust_refinement
    M5300.M5292.M5287.M5280.M5275.refine_relative_root = (
        robust_refinement
    )
    M5300.pole_lookup = contour_aware_pole_lookup
    M5300.M5292.node_panels = adaptive_node_panels


def order4_cache_rows() -> list[dict[str, Any]]:
    paths = (
        ORDER4_CACHE / "angular_order4_scan_jobs.csv",
        ORDER4_CACHE / "angular_order4_owner_geometric_poles.csv",
        ORDER4_CACHE / "angular_order4_pole_samples.csv",
        ORDER4_CACHE / "angular_order4_pole_fits.csv",
        ORDER4_CACHE / "angular_order4_selected_pole_residues.csv",
        ORDER4_CACHE / "angular_order4_bounded_ambiguous_pole_residues.csv",
    )
    rows: list[dict[str, Any]] = []
    for path in paths:
        parsed = read_csv(path)
        foreign = [
            row
            for row in parsed
            if not row.get("angular_node_id", "").startswith("A04_")
        ]
        rows.append(
            {
                "path": str(path),
                "row_count": len(parsed),
                "foreign_node_row_count": len(foreign),
                "expected_node_prefix": "A04_",
                "cache_isolated": not foreign,
                "valid_for_cache_isolation_audit": not foreign,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def lagrange_coefficients(
    squared_nodes: list[float],
    basis_index: int,
) -> list[float]:
    coefficients = np.asarray([1.0], dtype=np.float64)
    denominator = 1.0
    selected = squared_nodes[basis_index]
    for other_index, other in enumerate(squared_nodes):
        if other_index == basis_index:
            continue
        coefficients = np.polynomial.polynomial.polymul(
            coefficients,
            np.asarray([-other, 1.0], dtype=np.float64),
        )
        denominator *= selected - other
    return [float(value / denominator) for value in coefficients]


def basis_value(coefficients: list[float], coordinate: float) -> float:
    squared = coordinate * coordinate
    return float(
        sum(
            coefficient * squared**power
            for power, coefficient in enumerate(coefficients)
        )
    )


def basis_integral(
    coefficients: list[float],
    lower: float,
    upper: float,
) -> float:
    return float(
        sum(
            coefficient
            * (
                upper ** (2 * power + 1)
                - lower ** (2 * power + 1)
            )
            / (2 * power + 1)
            for power, coefficient in enumerate(coefficients)
        )
    )


def interpolation_model() -> dict[str, Any]:
    rows = [
        row
        for row in read_csv(ORBITS_5299)
        if int(row["angular_order"]) == 8
    ]
    coordinates = sorted(
        {float(row["absolute_soft_cosine"]) for row in rows}
    )
    squared = [value * value for value in coordinates]
    coefficients = [
        lagrange_coefficients(squared, basis_index)
        for basis_index in range(len(coordinates))
    ]
    values = {
        (
            float(row["absolute_soft_cosine"]),
            float(row["absolute_decay_cosine"]),
        ): complex(
            float(row["sign_orbit_integrand_real"]),
            float(row["sign_orbit_integrand_imaginary"]),
        )
        for row in rows
    }
    return {
        "coordinates": coordinates,
        "coefficients": coefficients,
        "values": values,
    }


def interpolant_value(
    model: dict[str, Any],
    soft_value: float,
    decay_value: float,
) -> complex:
    coordinates = model["coordinates"]
    coefficients = model["coefficients"]
    values = model["values"]
    return sum(
        (
            values[(soft_node, decay_node)]
            * basis_value(coefficients[soft_index], soft_value)
            * basis_value(coefficients[decay_index], decay_value)
            for soft_index, soft_node in enumerate(coordinates)
            for decay_index, decay_node in enumerate(coordinates)
        ),
        0.0j,
    )


def interpolant_integral(
    model: dict[str, Any],
    lower: float,
    upper: float,
) -> complex:
    coordinates = model["coordinates"]
    coefficients = model["coefficients"]
    values = model["values"]
    weights = [
        basis_integral(local, lower, upper) for local in coefficients
    ]
    return sum(
        (
            values[(soft_node, decay_node)]
            * weights[soft_index]
            * weights[decay_index]
            for soft_index, soft_node in enumerate(coordinates)
            for decay_index, decay_node in enumerate(coordinates)
        ),
        0.0j,
    )


def order8_outer_value() -> complex:
    row = next(
        row
        for row in read_csv(OUTER_5298)
        if int(row["energy_order"]) == max(ENERGY_ORDERS)
    )
    return complex(
        float(row["eight_component_integral_real"]),
        float(row["eight_component_integral_imaginary"]),
    )


def baseline_reproduction() -> tuple[complex, complex, float]:
    model = interpolation_model()
    angular_limit = float(M5300.M5280.M5274.M5270.ANGULAR_LIMIT)
    jacobian = float(M5300.M5280.M5278.ANGULAR_JACOBIAN)
    reproduced = (
        jacobian * interpolant_integral(model, 0.0, angular_limit)
    )
    stored = order8_outer_value()
    return reproduced, stored, relative_complex_change(stored, reproduced)


def dry_run() -> dict[str, Any]:
    configure_reused_pipeline()
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5300)
    targets = target_rows()
    nodes = adaptive_nodes()
    cache_rows = order4_cache_rows()
    write_csv(TARGETS, targets)
    write_csv(CACHE_ISOLATION, cache_rows)
    reproduced, stored, reproduction_change = baseline_reproduction()
    checks = {
        "parent_5300_accepted": bool(parent["acceptance_passed"]),
        "parent_5300_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5300)
        ),
        "order8_atlas_still_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5297)
        ),
        "order4_cache_isolated": all(
            parse_bool(row["cache_isolated"]) for row in cache_rows
        ),
        "six_missing_cell_orbits_selected": len(targets) == 6,
        "twenty_four_signed_nodes_constructed": len(nodes) == 24,
        "all_targets_have_complete_sign_orbits": all(
            sum(node["target_id"] == target["target_id"] for node in nodes)
            == 4
            for target in targets
        ),
        "order8_even_interpolant_reproduces_outer_total": (
            reproduction_change <= 1.0e-9
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
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "target_orbit_count": len(targets),
        "signed_node_count": len(nodes),
        "planned_exact_scan_count": len(nodes) * 2 * 8,
        **complex_fields("reproduced_order8_outer", reproduced),
        **complex_fields("stored_order8_outer", stored),
        "order8_outer_reproduction_relative_change": reproduction_change,
        "decision": (
            "DRY_RUN_ACCEPTED__BUILD_LOCAL_CELL"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(DRY_RUN, result)
    return result


def new_orbit_rows(
    totals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    nodes = read_csv(ADAPTIVE_NODES)
    target_lookup = {
        row["angular_node_id"]: row["target_id"] for row in nodes
    }
    physical = [
        row
        for row in totals
        if row["row_type"] == "PHYSICAL_INNER_ENERGY"
        and int(row["energy_order"]) == max(ENERGY_ORDERS)
    ]
    rows: list[dict[str, Any]] = []
    for target_id in sorted(set(target_lookup.values())):
        local = [
            row
            for row in physical
            if target_lookup[row["angular_node_id"]] == target_id
        ]
        value = sum(
            (
                complex(
                    float(row["eight_component_integral_real"]),
                    float(row["eight_component_integral_imaginary"]),
                )
                for row in local
            ),
            0.0j,
        )
        node = next(row for row in nodes if row["target_id"] == target_id)
        rows.append(
            {
                "target_id": target_id,
                "source": "NEW_ADAPTIVE_EXACT_NODES",
                "absolute_soft_cosine": node["absolute_soft_cosine"],
                "absolute_decay_cosine": node["absolute_decay_cosine"],
                "signed_node_count": len(local),
                **complex_fields("sign_orbit_integrand", value),
                "valid_for_adaptive_local_cell": True,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def complete_cell_values(
    new_rows: list[dict[str, Any]],
) -> dict[tuple[float, float], complex]:
    values = {
        (
            float(row["absolute_soft_cosine"]),
            float(row["absolute_decay_cosine"]),
        ): complex(
            float(row["sign_orbit_integrand_real"]),
            float(row["sign_orbit_integrand_imaginary"]),
        )
        for row in new_rows
    }
    diagonal = read_csv(ORBITS_5300)
    for row in diagonal:
        soft_value = float(row["absolute_soft_cosine"])
        decay_value = float(row["absolute_decay_cosine"])
        values[(soft_value, decay_value)] = complex(
            float(row["sign_orbit_integrand_real"]),
            float(row["sign_orbit_integrand_imaginary"]),
        )
    return values


def integration_products(
    values: dict[tuple[float, float], complex],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    coordinates = list(ridge_coordinates())
    lower, center, upper = coordinates
    model = interpolation_model()
    residual_rows: list[dict[str, Any]] = []
    residuals: dict[tuple[float, float], complex] = {}
    for soft_index, soft_value in enumerate(coordinates):
        for decay_index, decay_value in enumerate(coordinates):
            exact = values[(soft_value, decay_value)]
            baseline = interpolant_value(model, soft_value, decay_value)
            residual = exact - baseline
            residuals[(soft_value, decay_value)] = residual
            residual_rows.append(
                {
                    "soft_index": soft_index,
                    "decay_index": decay_index,
                    "absolute_soft_cosine": soft_value,
                    "absolute_decay_cosine": decay_value,
                    **complex_fields("exact_sign_orbit", exact),
                    **complex_fields("order8_even_interpolant", baseline),
                    **complex_fields("local_residual", residual),
                    "cell_boundary_node": (
                        soft_index in (0, 2) or decay_index in (0, 2)
                    ),
                    "valid_for_adaptive_local_cell_residual": True,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )

    squared_three = [value * value for value in coordinates]
    three_coefficients = [
        lagrange_coefficients(squared_three, basis_index)
        for basis_index in range(3)
    ]
    three_weights = [
        basis_integral(coefficients, lower, upper)
        for coefficients in three_coefficients
    ]
    endpoint_coordinates = [lower, upper]
    squared_two = [value * value for value in endpoint_coordinates]
    two_coefficients = [
        lagrange_coefficients(squared_two, basis_index)
        for basis_index in range(2)
    ]
    two_weights = [
        basis_integral(coefficients, lower, upper)
        for coefficients in two_coefficients
    ]
    weight_rows: list[dict[str, Any]] = []
    for model_id, local_coordinates, local_coefficients, local_weights in (
        (
            "BIQUADRATIC_RESIDUAL",
            coordinates,
            three_coefficients,
            three_weights,
        ),
        (
            "BILINEAR_CORNER_RESIDUAL",
            endpoint_coordinates,
            two_coefficients,
            two_weights,
        ),
    ):
        for basis_index, coordinate in enumerate(local_coordinates):
            weight_rows.append(
                {
                    "model_id": model_id,
                    "basis_index": basis_index,
                    "coordinate": coordinate,
                    "squared_coordinate": coordinate * coordinate,
                    "basis_coefficients_ascending": "|".join(
                        f"{value:.17g}"
                        for value in local_coefficients[basis_index]
                    ),
                    "integrated_basis_weight": local_weights[basis_index],
                    "cell_lower": lower,
                    "cell_upper": upper,
                    "valid_for_local_cell_quadrature": True,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )

    interpolant_basis_rows: list[dict[str, Any]] = []
    for basis_index, coordinate in enumerate(model["coordinates"]):
        coefficients = model["coefficients"][basis_index]
        interpolant_basis_rows.append(
            {
                "basis_index": basis_index,
                "coordinate": coordinate,
                "squared_coordinate": coordinate * coordinate,
                "basis_coefficients_ascending": "|".join(
                    f"{value:.17g}" for value in coefficients
                ),
                "full_domain_integrated_basis_weight": basis_integral(
                    coefficients,
                    0.0,
                    float(M5300.M5280.M5274.M5270.ANGULAR_LIMIT),
                ),
                "cell_integrated_basis_weight": basis_integral(
                    coefficients,
                    lower,
                    upper,
                ),
                "valid_for_order8_even_interpolant": True,
                **{field: False for field in CLAIM_FIELDS},
            }
        )

    jacobian = float(M5300.M5280.M5278.ANGULAR_JACOBIAN)
    quadratic_residual = jacobian * sum(
        (
            residuals[(soft_value, decay_value)]
            * three_weights[soft_index]
            * three_weights[decay_index]
            for soft_index, soft_value in enumerate(coordinates)
            for decay_index, decay_value in enumerate(coordinates)
        ),
        0.0j,
    )
    linear_residual = jacobian * sum(
        (
            residuals[(soft_value, decay_value)]
            * two_weights[soft_index]
            * two_weights[decay_index]
            for soft_index, soft_value in enumerate(endpoint_coordinates)
            for decay_index, decay_value in enumerate(
                endpoint_coordinates
            )
        ),
        0.0j,
    )
    baseline_cell = jacobian * interpolant_integral(
        model,
        lower,
        upper,
    )
    outer = order8_outer_value()
    quadratic_candidate = outer + quadratic_residual
    linear_candidate = outer + linear_residual
    model_change = relative_complex_change(
        linear_residual,
        quadratic_residual,
    )
    candidate_change = relative_complex_change(
        linear_candidate,
        quadratic_candidate,
    )
    center_residual = abs(residuals[(center, center)])
    boundary_residual = max(
        abs(value)
        for (soft_value, decay_value), value in residuals.items()
        if soft_value in (lower, upper) or decay_value in (lower, upper)
    )
    boundary_ratio = boundary_residual / max(center_residual, 1.0e-300)
    integration_rows = [
        {
            "model_id": "BILINEAR_CORNER_RESIDUAL",
            **complex_fields("baseline_cell_integral", baseline_cell),
            **complex_fields("local_residual_correction", linear_residual),
            **complex_fields("corrected_global_candidate", linear_candidate),
            "valid_for_local_cell_correction_candidate": False,
            **{field: False for field in CLAIM_FIELDS},
        },
        {
            "model_id": "BIQUADRATIC_RESIDUAL",
            **complex_fields("baseline_cell_integral", baseline_cell),
            **complex_fields(
                "local_residual_correction",
                quadratic_residual,
            ),
            **complex_fields(
                "corrected_global_candidate",
                quadratic_candidate,
            ),
            "valid_for_local_cell_correction_candidate": (
                model_change <= CORE_MODEL_CHANGE_LIMIT
                and boundary_ratio
                <= CORE_BOUNDARY_RESIDUAL_RATIO_LIMIT
            ),
            **{field: False for field in CLAIM_FIELDS},
        },
    ]
    metrics = {
        "cell_lower": lower,
        "cell_center": center,
        "cell_upper": upper,
        "cell_side_length": upper - lower,
        "cell_area_before_angular_jacobian": (upper - lower) ** 2,
        "local_residual_model_relative_change": model_change,
        "corrected_candidate_relative_change": candidate_change,
        "boundary_to_center_residual_ratio": boundary_ratio,
        "core_model_stable": model_change <= CORE_MODEL_CHANGE_LIMIT,
        "core_support_contained": (
            boundary_ratio <= CORE_BOUNDARY_RESIDUAL_RATIO_LIMIT
        ),
        **complex_fields("baseline_cell_integral", baseline_cell),
        **complex_fields("linear_residual_correction", linear_residual),
        **complex_fields(
            "quadratic_residual_correction",
            quadratic_residual,
        ),
        **complex_fields("stored_order8_outer", outer),
        **complex_fields(
            "quadratic_corrected_global_candidate",
            quadratic_candidate,
        ),
    }
    return (
        residual_rows,
        weight_rows,
        interpolant_basis_rows,
        {
            "integration_rows": integration_rows,
            "metrics": metrics,
        },
    )


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5291,
        SCRIPT_5297,
        SCRIPT_5300,
        RESULT_5300,
        VALIDATION_5300,
        ORBITS_5300,
        ORBITS_5299,
        OUTER_5298,
        ATLAS_RESULT,
        ADAPTIVE_NODES,
        POLE_RESIDUES,
        ENDPOINT_COEFFICIENTS,
        CONTOUR_SILENCE,
    )
    return [
        {"path": str(path), "sha256": digest(path)} for path in paths
    ]


def execute() -> dict[str, Any]:
    set_below_normal_priority()
    mp.mp.dps = M5300.M5280.MP_DECIMAL_DIGITS
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5301 dry run did not pass")
    configure_reused_pipeline()
    cached_failed_atlas = (
        ATLAS_RESULT.exists()
        and SCAN_JOBS.exists()
        and len(read_csv(SCAN_JOBS)) == EXPECTED_NODE_COUNT * 2 * 8
        and not bool(read_json(ATLAS_RESULT)["acceptance_passed"])
    )
    if cached_failed_atlas:
        atlas = repair_atlas_with_contour_silence()
    else:
        try:
            atlas = M5300.build_or_reuse_atlas()
        except RuntimeError:
            atlas = repair_atlas_with_contour_silence()
    configure_reused_pipeline()
    manifest, components, totals, convergence = (
        M5300.run_or_reuse_nodes()
    )
    normalized_manifest = [
        M5300.normalize_integration_flags(row) for row in manifest
    ]
    normalized_components = [
        M5300.normalize_integration_flags(row) for row in components
    ]
    normalized_totals = [
        M5300.normalize_integration_flags(row) for row in totals
    ]
    normalized_convergence = [
        M5300.normalize_integration_flags(row) for row in convergence
    ]
    write_csv(NODE_MANIFEST, normalized_manifest)
    write_csv(COMPONENT_TOTALS, normalized_components)
    write_csv(INNER_TOTALS, normalized_totals)
    write_csv(INNER_CONVERGENCE, normalized_convergence)

    orbit_rows = new_orbit_rows(normalized_totals)
    write_csv(ORBIT_VALUES, orbit_rows)
    values = complete_cell_values(orbit_rows)
    (
        residual_rows,
        weight_rows,
        interpolant_basis_rows,
        integration,
    ) = integration_products(values)
    write_csv(RESIDUAL_SAMPLES, residual_rows)
    write_csv(QUADRATURE_WEIGHTS, weight_rows)
    write_csv(INTERPOLANT_BASIS, interpolant_basis_rows)
    write_csv(INTEGRATION_COMPARISON, integration["integration_rows"])

    parent = read_json(RESULT_5300)
    silence = read_csv(CONTOUR_SILENCE)
    formal_end = M5283.formal_inventory_digest()
    metrics = integration["metrics"]
    maximum_energy_change = max(
        float(row["eight_component_energy_relative_change"])
        for row in normalized_manifest
    )
    checks = {
        "adaptive_atlas_accepted": bool(atlas["acceptance_passed"]),
        "all_twenty_four_node_runs_completed": (
            len(normalized_manifest) == EXPECTED_NODE_COUNT
            and all(
                parse_bool(row["node_run_completed"])
                for row in normalized_manifest
            )
        ),
        "all_nodes_pass_energy_gate": all(
            parse_bool(row["node_energy_converged"])
            for row in normalized_manifest
        ),
        "six_new_sign_orbits_complete": (
            len(orbit_rows) == EXPECTED_ORBIT_COUNT
            and all(int(row["signed_node_count"]) == 4 for row in orbit_rows)
        ),
        "three_by_three_cell_complete": len(values) == 9,
        "order8_interpolant_reproduces_outer_total": (
            dry["order8_outer_reproduction_relative_change"] <= 1.0e-9
        ),
        "all_contour_silence_controls_pass": (
            bool(silence)
            and all(
                parse_bool(row["contour_quadrature_controls_pass"])
                for row in silence
            )
        ),
        "integration_precision_initialized": (
            mp.mp.dps >= M5300.M5280.MP_DECIMAL_DIGITS
        ),
        "all_residual_samples_finite": all(
            math.isfinite(float(row["local_residual_real"]))
            and math.isfinite(float(row["local_residual_imaginary"]))
            for row in residual_rows
        ),
        "formalization_workbench_unchanged": (
            formal_end == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    if not accepted:
        decision = "LOCAL_CELL_PIPELINE_REQUIRES_REPAIR"
    elif not metrics["core_model_stable"]:
        decision = "LOCAL_CELL_RESOLVED_BUT_MODEL_UNSTABLE__REFINE_CORE"
    elif not metrics["core_support_contained"]:
        decision = "LOCAL_CELL_MODEL_STABLE__MAP_OUTER_COLLAR"
    else:
        decision = "LOCAL_CELL_CORRECTION_STABLE__TEST_EXTERIOR_RESIDUAL"
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "adaptive-local-cell-residual-integration",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": decision,
        "adaptive_signed_node_count": len(normalized_manifest),
        "new_sign_orbit_count": len(orbit_rows),
        "atlas_exact_scan_count": int(atlas["exact_scan_count"]),
        "atlas_exact_active_root_count": int(
            atlas["exact_active_root_count"]
        ),
        "atlas_material_pole_count": int(atlas["material_pole_count"]),
        "contour_center_only_pole_count": len(silence),
        "integration_mp_decimal_digits": mp.mp.dps,
        "maximum_contour_order8_exact_relative_error": max(
            float(row["order8_exact_relative_error"])
            for row in silence
        ),
        "maximum_contour_order4_order8_relative_change": max(
            float(row["order4_order8_relative_change"])
            for row in silence
        ),
        "component_evaluation_count": sum(
            int(row["component_evaluation_count"])
            for row in normalized_manifest
        ),
        "maximum_node_inner_energy_relative_change": (
            maximum_energy_change
        ),
        **metrics,
        "core_model_change_limit": CORE_MODEL_CHANGE_LIMIT,
        "core_boundary_residual_ratio_limit": (
            CORE_BOUNDARY_RESIDUAL_RATIO_LIMIT
        ),
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
            "resumable_scan_ledger": str(SCAN_JOBS),
        },
        "claim_boundary": {
            "valid_for_adaptive_local_cell_diagnostic": accepted,
            "valid_for_local_cell_correction_candidate": (
                accepted
                and bool(metrics["core_model_stable"])
                and bool(metrics["core_support_contained"])
            ),
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "The local residual is integrated only inside the "
                "bracket cell. Full angular convergence additionally "
                "requires a stable local model and a bounded exterior "
                "residual."
            ),
        },
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETE" if accepted else "FAILED",
            "decision": decision,
            "local_residual_model_relative_change": metrics[
                "local_residual_model_relative_change"
            ],
            "boundary_to_center_residual_ratio": metrics[
                "boundary_to_center_residual_ratio"
            ],
        },
    )
    return result


def validation_gate(
    gate_id: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {"gate_id": gate_id, "passed": passed, "detail": detail}


def render_document(result: dict[str, Any], passed: bool) -> None:
    checks = "\n".join(
        f"- `{key}`: **{'PASS' if value else 'FAIL'}**"
        for key, value in sorted(result["checks"].items())
    )
    text = f"""# 5301 — Adaptive local-cell residual integration

## Result

Six new off-diagonal sign orbits complete a three-by-three angular
cell around the order-four interior hotspot. The calculation subtracts
the exact tensor-product even interpolant represented by the accepted
order-eight Gauss rule, then integrates the remaining local residual.

- signed nodes: `{result['adaptive_signed_node_count']}`;
- exact scans: `{result['atlas_exact_scan_count']}`;
- off-contour poles integrated without fitted residues:
  `{result['contour_center_only_pole_count']}`;
- integration arithmetic precision:
  `{result['integration_mp_decimal_digits']}` decimal digits;
- maximum analytic/order-eight pole-kernel error:
  `{result['maximum_contour_order8_exact_relative_error']:.12g}`;
- component evaluations: `{result['component_evaluation_count']}`;
- maximum nodewise energy change:
  `{result['maximum_node_inner_energy_relative_change']:.12g}`;
- cell interval:
  `[{result['cell_lower']:.12g}, {result['cell_upper']:.12g}]`;
- bilinear-to-biquadratic residual change:
  `{result['local_residual_model_relative_change']:.12g}`;
- boundary/center residual ratio:
  `{result['boundary_to_center_residual_ratio']:.12g}`;
- biquadratic local correction:
  `{result['quadratic_residual_correction_real']:.12g} +
  {result['quadratic_residual_correction_imaginary']:.12g} i`;
- corrected global candidate:
  `{result['quadratic_corrected_global_candidate_real']:.12g} +
  {result['quadratic_corrected_global_candidate_imaginary']:.12g} i`.

Decision: **{result['decision']}**.

## Acceptance gates

{checks}

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

This checkpoint performs a real two-dimensional local residual
integration. It does not claim full angular convergence unless the
local model is stable and the residual is shown to be contained or
bounded outside the cell. It makes no full phase-space, UV, local-GR,
or full-MTS claim.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    manifest = read_csv(NODE_MANIFEST)
    scans = read_csv(SCAN_JOBS)
    residuals = read_csv(RESIDUAL_SAMPLES)
    integrations = read_csv(INTEGRATION_COMPARISON)
    cache_rows = read_csv(CACHE_ISOLATION)
    silence = read_csv(CONTOUR_SILENCE)
    gates = [
        validation_gate(
            "result_accepted",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "twenty_four_nodes",
            len(manifest) == EXPECTED_NODE_COUNT,
            f"nodes={len(manifest)}",
        ),
        validation_gate(
            "three_hundred_eighty_four_scans",
            len(scans) == EXPECTED_NODE_COUNT * 2 * 8,
            f"scans={len(scans)}",
        ),
        validation_gate(
            "nine_residual_samples",
            len(residuals) == 9,
            f"residuals={len(residuals)}",
        ),
        validation_gate(
            "two_nested_local_models",
            len(integrations) == 2,
            f"models={len(integrations)}",
        ),
        validation_gate(
            "all_nodes_energy_converged",
            all(
                parse_bool(row["node_energy_converged"])
                for row in manifest
            ),
            "all node shards pass the 0.5 percent energy gate",
        ),
        validation_gate(
            "contour_silence_certified",
            bool(silence)
            and all(
                parse_bool(row["contour_quadrature_controls_pass"])
                for row in silence
            ),
            f"contour_rows={len(silence)}",
        ),
        validation_gate(
            "integration_precision_initialized",
            int(result["integration_mp_decimal_digits"])
            >= int(M5300.M5280.MP_DECIMAL_DIGITS),
            (
                f"digits={result['integration_mp_decimal_digits']}; "
                f"required={M5300.M5280.MP_DECIMAL_DIGITS}"
            ),
        ),
        validation_gate(
            "order4_cache_isolated",
            all(parse_bool(row["cache_isolated"]) for row in cache_rows),
            "no foreign angular-node prefixes remain",
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == str(result["formalization_workbench_end_digest"]),
            str(result["formalization_workbench_end_digest"]),
        ),
        validation_gate(
            "claims_locked_false",
            all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            ),
            "no full angular, phase-space, UV, local-GR, or MTS claim",
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
            "VALIDATED_ADAPTIVE_LOCAL_CELL_RESIDUAL_INTEGRATION"
            if passed
            else "ADAPTIVE_LOCAL_CELL_VALIDATION_FAILED"
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
