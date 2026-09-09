from __future__ import annotations

import csv
import ctypes
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any


for variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[variable] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5450"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5386 = SCRIPTS / "Y5_R2FR_5386_D4_nested_contour_integrand_enclosure.py"
SCRIPT_5395 = (
    SCRIPTS
    / "Y5_R2FR_5395_D4_correlated_material_residue_supremum_and_numeric_pole_W3.py"
)
EVENTS = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
ENERGY_ARCS = (
    FUNCTIONAL_RG / "5385" / "D4_expanded_energy_full_catalog_clearance_arcs.csv"
)
CONTOUR_BOUNDS = (
    FUNCTIONAL_RG / "5386" / "D4_nested_contour_integrand_event_bounds.csv"
)
CONTOUR_RESULT = FUNCTIONAL_RG / "5386" / "D4_nested_contour_integrand_result.json"
RATIO_BOXES = FUNCTIONAL_RG / "5392" / "D4_desingularized_endpoint_ratio_boxes.csv"
BRANCHES = FUNCTIONAL_RG / "5393" / "D4_material_pole_branch_ownership.csv"
RESIDUES = FUNCTIONAL_RG / "5395" / "D4_material_residue_supremum.csv"
ANALYTICITY = FUNCTIONAL_RG / "5448" / "D4_event_local_analyticity_result.json"

DOCUMENT = (
    POST
    / "5450-Y5-R2FR-D4-event-endpoint-Cauchy-subtraction-and-correlated-probe.md"
)
THEOREM = OUTPUT / "D4_event_endpoint_Cauchy_subtraction_bounds.csv"
PROBES = OUTPUT / "D4_correlated_event_curve_contour_probes.csv"
PROBE_SUMMARY = OUTPUT / "D4_correlated_event_curve_probe_summary.csv"
SOURCES = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5450_VALIDATION.csv"
RESULT = OUTPUT / "D4_event_endpoint_Cauchy_subtraction_result.json"

CHECKPOINT = 5450
REVISION = "D4-event-endpoint-Cauchy-subtraction-correlated-probe-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
ENERGY_ARC_COUNT = 32
GLOBAL_ARC_COUNT = 1
ENERGY_CONTOUR_RADIUS = 1.0e-5
INNER_FRACTION = 0.75
OUTER_FRACTION = 0.50
SMOKE_EPSILON_BINS = (-1, 8)
SMOKE_X_HALF_WIDTH = 1.0e-8


def set_below_normal_priority() -> None:
    try:
        ctypes.windll.kernel32.SetPriorityClass(
            ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
        )
    except (AttributeError, OSError):
        pass


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5386,
        SCRIPT_5395,
        EVENTS,
        ENERGY_ARCS,
        CONTOUR_BOUNDS,
        CONTOUR_RESULT,
        RATIO_BOXES,
        BRANCHES,
        RESIDUES,
        ANALYTICITY,
    )


def source_interface_audit() -> dict[str, bool]:
    contour_source = SCRIPT_5386.read_text(encoding="utf-8")
    residue_source = SCRIPT_5395.read_text(encoding="utf-8")
    return {
        "nested_value_is_energy_displacement_times_global_regularized_parent": (
            "return energy_displacement * global_regularized_direct_interval("
            in contour_source
        ),
        "active_invariant_is_energy_displacement_times_channel_quotient": (
            "energy_displacement * channel_quotient" in contour_source
        ),
        "point_witness_multiplies_parent_by_energy_displacement": (
            "parent_regularized = parent_global_regularized * M5258.midpoint("
            in contour_source
        ),
        "center_residue_uses_exact_double_regularized_parent": (
            "coefficient, coefficient_data = exact_double_regularized_direct("
            in residue_source
        ),
        "center_residue_divides_the_same_three_geometric_factors": all(
            expression in residue_source
            for expression in (
                'geometric["relative_root"]',
                'geometric["selected_global_root"]',
                'geometric["collision_jacobian"]',
            )
        ),
    }


def event_branch_map() -> dict[str, dict[str, str]]:
    events = {row["event_id"]: row for row in read_csv(EVENTS)}
    branches = [
        row
        for row in read_csv(BRANCHES)
        if row["pole_class"] == "MATERIAL_SIMPLE_POLE"
    ]
    mapped: dict[str, dict[str, str]] = {}
    for event_id, event in events.items():
        matches = [
            branch
            for branch in branches
            if branch["term_id"] == event["term_id"]
            and branch["primary_surface_id"] == event["primary_surface_id"]
            and event_id
            in {branch["support_start_event"], branch["support_end_event"]}
        ]
        if len(matches) != 1:
            raise RuntimeError(f"{event_id} has {len(matches)} branch owners")
        mapped[event_id] = matches[0]
    return mapped


def theorem_rows(interface: dict[str, bool]) -> list[dict[str, Any]]:
    arcs = read_csv(ENERGY_ARCS)
    bounds = {row["event_id"]: row for row in read_csv(CONTOUR_BOUNDS)}
    residues = {row["branch_owner_id"]: row for row in read_csv(RESIDUES)}
    branch_map = event_branch_map()
    identity_passes = all(interface.values())
    rows: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        event_arcs = [row for row in arcs if row["event_id"] == event_id]
        radii = [float(row["energy_contour_radius"]) for row in event_arcs]
        radius = min(radii)
        contour = bounds[event_id]
        branch = branch_map[event_id]
        residue = residues[branch["branch_owner_id"]]
        numerator_bound = float(
            contour[
                "maximum_event_integrand_abs_upper_without_physical_multiplier"
            ]
        )
        residue_bound = float(residue["material_residue_abs_upper"])
        inner_radius = INNER_FRACTION * radius
        outer_radius = OUTER_FRACTION * radius
        regular_bound = numerator_bound / (radius - inner_radius)
        rows.append(
            {
                "event_id": event_id,
                "event_type": next(
                    row["event_type"]
                    for row in event_arcs
                    if row["event_id"] == event_id
                ),
                "branch_owner_id": branch["branch_owner_id"],
                "term_id": branch["term_id"],
                "primary_surface_id": branch["primary_surface_id"],
                "energy_contour_radius": radius,
                "energy_contour_radius_maximum": max(radii),
                "energy_contour_arc_count": len(event_arcs),
                "minimum_nonactive_root_separation_lower": min(
                    float(row["minimum_nonactive_root_separation_lower"])
                    for row in event_arcs
                ),
                "minimum_full_catalog_clearance_margin_lower": min(
                    float(row["minimum_full_catalog_clearance_margin_lower"])
                    for row in event_arcs
                ),
                "Q_boundary_abs_upper": numerator_bound,
                "rho_abs_upper": residue_bound,
                "inner_Cauchy_radius": inner_radius,
                "outer_parent_radius": outer_radius,
                "inner_outer_overlap_width": inner_radius - outer_radius,
                "inner_regular_part_abs_upper": regular_bound,
                "full_chord_regular_integral_per_x_abs_upper": (
                    2.0 * inner_radius * regular_bound
                ),
                "outer_principal_part_triangle_abs_upper": (
                    residue_bound / outer_radius
                ),
                "exact_identity": (
                    "F(delta)=rho/delta+G(delta); "
                    "Q(delta)=delta F(delta); "
                    "rho=Q(0); G=(Q-Q(0))/delta"
                ),
                "Cauchy_bound": (
                    "sup_|delta|<=a |G| <= M_Q/(R-a), "
                    "a=0.75R"
                ),
                "overlap_cover_rule": (
                    "inner if sup|delta|<=0.75R; outer if inf|delta|>=0.50R"
                ),
                "valid_for_exact_endpoint_principal_part_subtraction": (
                    identity_passes
                ),
                "valid_for_event_curve_inner_Cauchy_bound": (
                    identity_passes
                    and radius > inner_radius > outer_radius > 0.0
                    and numerator_bound > 0.0
                    and residue_bound > 0.0
                    and all(parse_bool(row["energy_arc_passes"]) for row in event_arcs)
                ),
                "valid_for_full_event_cell_finite_cover": False,
                "valid_for_D4_event_local_W3_bound": False,
                "valid_for_D4_numeric_W3_bound": False,
                "valid_for_all_operator_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def ratio_coordinate_bounds(parent: Any, row: dict[str, str]) -> tuple[float, float]:
    boxes = [
        parent.M5385.M5381.parse_complex_box(text)
        for text in row["desingularized_Krawczyk_images"].split("|")
    ]
    dimension = int(row["desingularized_system_dimension"])
    coordinate_index = 3 if dimension == 5 else 2
    lower, upper = parent.M5258.real_bounds(boxes[coordinate_index])
    midpoint = 0.5 * (lower + upper)
    half_width = min(SMOKE_X_HALF_WIDTH, 0.5 * (upper - lower))
    if half_width <= 0.0:
        half_width = SMOKE_X_HALF_WIDTH
    return midpoint - half_width, midpoint + half_width


def correlated_arc_probe(
    parent: Any,
    references: Any,
    event: dict[str, str],
    branch: dict[str, str],
    ratio_row: dict[str, str],
    energy_arc_index: int,
) -> dict[str, Any]:
    started = time.perf_counter()
    configuration = (
        parent.M5385.M5380.M5379.M5378.M5359.event_configuration(
            event, references
        )
    )
    x_lower, x_upper = ratio_coordinate_bounds(parent, ratio_row)
    epsilon_row: dict[str, Any] = {
        "regulator_bin_index": int(ratio_row["epsilon_bin_index"]),
        "epsilon_subdivision_index": 0,
        "epsilon_subdivision_count": 1,
        "epsilon_real_lower": float(ratio_row["epsilon_real_lower"]),
        "epsilon_real_upper": float(ratio_row["epsilon_real_upper"]),
        "epsilon_imaginary_lower": float(ratio_row["epsilon_imaginary_lower"]),
        "epsilon_imaginary_upper": float(ratio_row["epsilon_imaginary_upper"]),
    }
    segment: dict[str, Any] = {
        "branch_owner_id": branch["branch_owner_id"],
        "term_id": branch["term_id"],
        "primary_surface_id": branch["primary_surface_id"],
        "sign": int(configuration["sign"]),
    }
    base: dict[str, Any] = {
        "event_id": event["event_id"],
        "event_type": event["event_type"],
        "branch_owner_id": branch["branch_owner_id"],
        "term_id": event["term_id"],
        "primary_surface_id": event["primary_surface_id"],
        "epsilon_bin_index": int(ratio_row["epsilon_bin_index"]),
        "epsilon_real_lower": epsilon_row["epsilon_real_lower"],
        "epsilon_real_upper": epsilon_row["epsilon_real_upper"],
        "epsilon_imaginary_lower": epsilon_row["epsilon_imaginary_lower"],
        "epsilon_imaginary_upper": epsilon_row["epsilon_imaginary_upper"],
        "x_lower": x_lower,
        "x_upper": x_upper,
        "x_width": x_upper - x_lower,
        "energy_phase_arc_index": energy_arc_index,
        "energy_phase_arc_count": ENERGY_ARC_COUNT,
        "global_phase_arc_count": GLOBAL_ARC_COUNT,
    }
    try:
        inputs, root_diagnostics = parent.correlated_inputs(
            segment, epsilon_row, x_lower, x_upper
        )
        interval = parent.M5386.iv
        phase = (
            2
            * interval.pi
            * interval.mpf([energy_arc_index, energy_arc_index + 1])
            / ENERGY_ARC_COUNT
        )
        energy_displacement = interval.mpf(str(ENERGY_CONTOUR_RADIUS)) * (
            interval.cos(phase) + 1j * interval.sin(phase)
        )
        geometry = parent.M5385.expanded_geometry(
            configuration, inputs, energy_displacement
        )
        global_phase = 2 * interval.pi * interval.mpf([0, 1])
        global_radius = float(parent.M5386.GLOBAL_CONTOUR_RELATIVE_RADIUS) * max(
            1.0,
            parent.M5258.upper_abs(geometry["selected_root"]),
        )
        global_displacement = interval.mpf(str(global_radius)) * (
            interval.cos(global_phase) + 1j * interval.sin(global_phase)
        )
        target = parent.M5258.cpoint(-9) + 1j * inputs["epsilon"]
        active_endpoint = 4 if configuration["role"] == "reciprocal" else 0
        channel_quotient = parent.M5386.energy_channel_quotient(
            configuration,
            inputs,
            energy_displacement,
            active_endpoint,
        )
        right_invariant_overrides = None
        if configuration["surface_id"] == "direct:shared:s13":
            shared_quotient = parent.M5386.shared_channel_quotient(
                configuration, inputs, energy_displacement
            )
            right_invariant_overrides = {
                frozenset((1, 3)): energy_displacement * shared_quotient
            }
        right_edge_overrides = None
        if configuration["event_type"] == "BRANCH_DEATH":
            right_edge_overrides = parent.M5386.first_plus_edge_overrides(
                configuration,
                inputs,
                geometry,
                energy_displacement,
                global_displacement,
                target,
            )
            right_edge_overrides.update(
                parent.M5386.first_minus_edge_overrides(
                    configuration,
                    inputs,
                    geometry,
                    global_displacement,
                    target,
                )
            )
            right_edge_overrides.update(
                parent.M5386.internal_hard_pair_edge_overrides(
                    configuration,
                    inputs,
                    geometry,
                    global_displacement,
                )
            )
            right_edge_overrides.update(
                parent.M5386.second_external_edge_overrides(
                    configuration,
                    inputs,
                    geometry,
                    global_displacement,
                    target,
                )
            )
        diagnostics = parent.M5258.IntervalDiagnostics()
        parent.M5386.ACTIVE_QUOTIENT_PROBES.clear()
        parent.M5386.STABLE_EDGE_PROBES.clear()
        parent.M5386.FIRST_PLUS_EDGE_PROBES.clear()
        with parent.M5386.amplitude_primitives(probe_active_quotients=True):
            value = parent.M5386.nested_exact_regularized_direct_interval(
                configuration,
                inputs,
                geometry,
                target,
                energy_displacement,
                global_displacement,
                channel_quotient,
                active_endpoint,
                diagnostics,
                right_invariant_overrides,
                right_edge_overrides,
            )
            factors = parent.M5386.energy_contour_geometric_factors(
                configuration, inputs, geometry
            )
            event_integrand = value
            factor_lowers: dict[str, float] = {}
            for factor_name, factor_key in (
                ("relative_root", "relative_root"),
                ("selected_global_root", "selected_global_root"),
                ("collision_jacobian", "collision_jacobian"),
            ):
                factor = factors[factor_key]
                factor_lowers[factor_name] = parent.M5258.lower_abs(factor)
                event_integrand = parent.M5258.safe_divide(
                    event_integrand,
                    factor,
                    diagnostics,
                    f"correlated_event_geometric_factor:{factor_name}",
                )
        value_upper = parent.M5258.upper_abs(value)
        integrand_upper = parent.M5258.upper_abs(event_integrand)
        displacement_lower = parent.M5258.lower_abs(energy_displacement)
        displacement_upper = parent.M5258.upper_abs(energy_displacement)
        finite_values = (
            value_upper,
            integrand_upper,
            displacement_lower,
            displacement_upper,
            diagnostics.minimum_denominator_lower,
            *factor_lowers.values(),
        )
        passed = (
            all(math.isfinite(float(value)) for value in finite_values)
            and value_upper > 0.0
            and integrand_upper > 0.0
            and displacement_lower > 0.0
            and all(value > 0.0 for value in factor_lowers.values())
            and diagnostics.minimum_denominator_lower > 0.0
        )
        return {
            **base,
            "probe_passed": passed,
            "failure_type": "",
            "failure_message": "",
            "energy_displacement_modulus_lower": displacement_lower,
            "energy_displacement_modulus_upper": displacement_upper,
            "value_abs_upper": value_upper,
            "event_integrand_abs_upper_without_physical_multiplier": integrand_upper,
            "minimum_denominator_lower": diagnostics.minimum_denominator_lower,
            "relative_root_modulus_lower": factor_lowers["relative_root"],
            "selected_global_root_modulus_lower": factor_lowers[
                "selected_global_root"
            ],
            "collision_jacobian_modulus_lower": factor_lowers[
                "collision_jacobian"
            ],
            "material_root_denominator_abs_lower": root_diagnostics[
                "material_coefficient_denominator_abs_lower"
            ],
            "implicit_material_derivative_abs_lower": root_diagnostics[
                "implicit_material_derivative_abs_lower"
            ],
            "runtime_seconds": time.perf_counter() - started,
            "valid_for_correlated_event_curve_contour_smoke": passed,
            "valid_for_full_event_cell_finite_cover": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    except Exception as error:
        return {
            **base,
            "probe_passed": False,
            "failure_type": type(error).__name__,
            "failure_message": str(error).splitlines()[0][:400],
            "energy_displacement_modulus_lower": math.nan,
            "energy_displacement_modulus_upper": math.nan,
            "value_abs_upper": math.nan,
            "event_integrand_abs_upper_without_physical_multiplier": math.nan,
            "minimum_denominator_lower": math.nan,
            "relative_root_modulus_lower": math.nan,
            "selected_global_root_modulus_lower": math.nan,
            "collision_jacobian_modulus_lower": math.nan,
            "material_root_denominator_abs_lower": math.nan,
            "implicit_material_derivative_abs_lower": math.nan,
            "runtime_seconds": time.perf_counter() - started,
            "valid_for_correlated_event_curve_contour_smoke": False,
            "valid_for_full_event_cell_finite_cover": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }


def correlated_probe_rows(parent: Any) -> list[dict[str, Any]]:
    references, _ = parent.M5385.M5380.M5379.M5378.M5359.reference_rows()
    events = {row["event_id"]: row for row in read_csv(EVENTS)}
    ratios = {
        (row["event_id"], int(row["epsilon_bin_index"])): row
        for row in read_csv(RATIO_BOXES)
    }
    branches = event_branch_map()
    rows: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        for epsilon_bin in SMOKE_EPSILON_BINS:
            ratio_row = ratios[(event_id, epsilon_bin)]
            for energy_arc_index in range(ENERGY_ARC_COUNT):
                rows.append(
                    correlated_arc_probe(
                        parent,
                        references,
                        events[event_id],
                        branches[event_id],
                        ratio_row,
                        energy_arc_index,
                    )
                )
    return rows


def probe_summary_rows(probes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        selected = [row for row in probes if row["event_id"] == event_id]
        passed = [row for row in selected if row["probe_passed"]]
        rows.append(
            {
                "event_id": event_id,
                "probe_count": len(selected),
                "passed_probe_count": len(passed),
                "failed_probe_count": len(selected) - len(passed),
                "epsilon_bins": "|".join(
                    str(value)
                    for value in sorted({row["epsilon_bin_index"] for row in selected})
                ),
                "maximum_event_integrand_abs_upper_without_physical_multiplier": max(
                    (
                        float(
                            row[
                                "event_integrand_abs_upper_without_physical_multiplier"
                            ]
                        )
                        for row in passed
                    ),
                    default=math.nan,
                ),
                "minimum_denominator_lower": min(
                    (float(row["minimum_denominator_lower"]) for row in passed),
                    default=math.nan,
                ),
                "minimum_collision_jacobian_modulus_lower": min(
                    (
                        float(row["collision_jacobian_modulus_lower"])
                        for row in passed
                    ),
                    default=math.nan,
                ),
                "correlated_event_curve_probe_passes": (
                    len(selected) == len(SMOKE_EPSILON_BINS) * ENERGY_ARC_COUNT
                    and len(passed) == len(selected)
                ),
                "valid_for_full_event_cell_finite_cover": False,
                "valid_for_D4_event_local_W3_bound": False,
                "valid_for_all_operator_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def render_document(
    payload: dict[str, Any],
    theorem: list[dict[str, Any]],
    summaries: list[dict[str, Any]],
) -> None:
    lines = [
        "# 5450: D4 event-endpoint Cauchy subtraction and correlated probe",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Exact endpoint identity",
        "",
        "The 5386 parent interface is not the singular coefficient `F` itself. Its exact return value is `Q(delta)=delta F(delta)`, after the same global-pole regularization and the same three geometric divisions used by the 5395 centre residue. Consequently",
        "",
        "```text",
        "rho=Q(0),",
        "F(delta)=rho/delta+G(delta),",
        "G(delta)=[Q(delta)-Q(0)]/delta.",
        "```",
        "",
        "If `Q` is holomorphic on `|delta|<=R` and `sup_|delta|=R |Q|<=M_Q`, its Taylor coefficients obey `|q_n|<=M_Q/R^n`. Therefore, for every `a<R`,",
        "",
        "```text",
        "sup_|delta|<=a |G(delta)|",
        " <= sum_(n>=1) M_Q a^(n-1)/R^n",
        " = M_Q/(R-a).",
        "```",
        "",
        "This is the finite regular-part bound that replaces the divergent `rho/|delta|` triangle estimate at the connector endpoint. No plateau, fitted closure or zero-residue assumption is introduced.",
        "",
        "## Overlap rule",
        "",
        "The source contour has `R=1e-5`. The inner owner is valid through `0.75R`; the existing parent away evaluator is used only once `|delta|>=0.50R`. The positive `0.25R` overlap means adaptive boxes do not have to resolve the artificial switching circle exactly.",
        "",
        "| event | branch | M_Q | sup inner | rho bound | overlap |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in theorem:
        lines.append(
            f"| `{row['event_id']}` | `{row['branch_owner_id']}` | "
            f"{row['Q_boundary_abs_upper']} | "
            f"{row['inner_regular_part_abs_upper']} | "
            f"{row['rho_abs_upper']} | "
            f"{row['inner_outer_overlap_width']} |"
        )
    lines.extend(
        [
            "",
            "## Correlated parent probe",
            "",
            "The formula was also exercised through a different input route: each moving endpoint coordinate was replaced by a small independent correlated `x` interval, its material root was recomputed by the 5395 implicit-root machinery, and the exact 5386 `Q` contour was rerun on both regulator-edge boxes and all 32 energy arcs.",
            "",
            "| event | probes | passed | max correlated M_Q | min denominator |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in summaries:
        lines.append(
            f"| `{row['event_id']}` | {row['probe_count']} | "
            f"{row['passed_probe_count']} | "
            f"{row['maximum_event_integrand_abs_upper_without_physical_multiplier']} | "
            f"{row['minimum_denominator_lower']} |"
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This proves the subtraction identity and a finite event-curve inner bound, and it verifies that the exact parent contour survives an independent correlated-x transplant. It does not yet cover the full 19 mapped cells: the next runner must tile connector `(x,t)` boxes with the overlapping inner/outer rule and bound the nonsingular upper/cutoff logarithm. Event-local `W3`, combined `W3`, the D4 regulator limit, all-operator local GR and full MTS remain false.",
            "",
        ]
    )
    atomic_text(DOCUMENT, "\n".join(lines))


def run() -> dict[str, Any]:
    set_below_normal_priority()
    started_utc = datetime.now(timezone.utc)
    started = time.perf_counter()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    analytic = read_json(ANALYTICITY)
    contour_result = read_json(CONTOUR_RESULT)
    interface = source_interface_audit()
    theorem = theorem_rows(interface)
    parent = load_module("mts_5395_for_5450", SCRIPT_5395)
    parent.set_below_normal_priority()
    parent.M5386.iv.dps = parent.M5386.INTERVAL_DIGITS
    probes = correlated_probe_rows(parent)
    summaries = probe_summary_rows(probes)
    failed_probes = [row for row in probes if not row["probe_passed"]]
    expected_probe_count = (
        len(EVENT_IDS) * len(SMOKE_EPSILON_BINS) * ENERGY_ARC_COUNT
    )
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "EXACT_ENDPOINT_SUBTRACTION_DERIVED__CORRELATED_PARENT_CONTOUR_PROBE_PASSES__BUILD_FINITE_XT_COVER"
            if not failed_probes
            else "EXACT_ENDPOINT_SUBTRACTION_DERIVED__CORRELATED_PROBE_EXPOSES_FAILURES"
        ),
        "source_interface_audit": interface,
        "event_count": len(theorem),
        "probe_count": len(probes),
        "expected_probe_count": expected_probe_count,
        "passed_probe_count": len(probes) - len(failed_probes),
        "failed_probe_count": len(failed_probes),
        "failure_classes": sorted(
            {
                f"{row['failure_type']}:{row['failure_message']}"
                for row in failed_probes
            }
        ),
        "energy_contour_radius": ENERGY_CONTOUR_RADIUS,
        "inner_fraction": INNER_FRACTION,
        "outer_fraction": OUTER_FRACTION,
        "minimum_inner_outer_overlap_width": min(
            float(row["inner_outer_overlap_width"]) for row in theorem
        ),
        "maximum_inner_regular_part_abs_upper": max(
            float(row["inner_regular_part_abs_upper"]) for row in theorem
        ),
        "runtime_seconds": time.perf_counter() - started,
        "next_target": "EVENT_ENDPOINT_OVERLAP_XT_FINITE_COVER_AND_NONSINGULAR_PRIMITIVE",
        "valid_for_exact_endpoint_principal_part_subtraction": all(
            row["valid_for_exact_endpoint_principal_part_subtraction"]
            for row in theorem
        ),
        "valid_for_event_curve_inner_Cauchy_bound": all(
            row["valid_for_event_curve_inner_Cauchy_bound"] for row in theorem
        ),
        "valid_for_correlated_event_curve_contour_smoke": not failed_probes,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_D4_numeric_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("all_exact_parent_interface_clauses_are_present", all(interface.values()), interface),
        check("checkpoint_5448_analyticity_is_valid", analytic.get("all_event_remainders_holomorphic") is True and analytic.get("failed_validation_count") == 0, analytic.get("decision")),
        check("checkpoint_5386_full_contour_is_valid", contour_result.get("validation_passed") is True and contour_result.get("valid_for_D4_nested_contour_integrand_enclosure", contour_result.get("claim_boundary", {}).get("valid_for_D4_nested_contour_integrand_enclosure")) is True, contour_result.get("decision")),
        check("all_eight_events_have_unique_branch_owners", len(event_branch_map()) == len(EVENT_IDS), sorted(event_branch_map())),
        check("all_event_curve_Cauchy_bounds_are_finite", all(row["valid_for_event_curve_inner_Cauchy_bound"] and math.isfinite(float(row["inner_regular_part_abs_upper"])) and float(row["inner_regular_part_abs_upper"]) > 0.0 for row in theorem), len(theorem)),
        check("inner_outer_overlap_is_strictly_positive", all(float(row["inner_outer_overlap_width"]) > 0.0 for row in theorem), payload["minimum_inner_outer_overlap_width"]),
        check("probe_matrix_is_complete", len(probes) == expected_probe_count, f"{len(probes)}/{expected_probe_count}"),
        check("correlated_parent_contour_probes_all_pass", not failed_probes, payload["failure_classes"]),
        check("every_event_has_both_regulator_edge_boxes", all({row["epsilon_bin_index"] for row in probes if row["event_id"] == event_id} == set(SMOKE_EPSILON_BINS) for event_id in EVENT_IDS), list(SMOKE_EPSILON_BINS)),
        check("broad_claims_remain_false", not payload["valid_for_full_event_cell_finite_cover"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_D4_numeric_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "5450 is endpoint theorem plus correlated smoke only"),
    ]
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started_utc
    ]
    validations.append(
        check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"modified_file_count={len(formalization_touches)}",
        )
    )
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    source_rows = [
        {
            "checkpoint": CHECKPOINT,
            "path": str(path.resolve()),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "",
        }
        for path in source_paths()
    ]
    atomic_csv(THEOREM, theorem)
    atomic_csv(PROBES, probes)
    atomic_csv(PROBE_SUMMARY, summaries)
    atomic_csv(SOURCES, source_rows)
    atomic_csv(VALIDATION, validations)
    render_document(payload, theorem, summaries)
    atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
