from __future__ import annotations

import argparse
import csv
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

from mpmath import iv


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
OUTPUT = FUNCTIONAL_RG / "5384"
DOCUMENT = POST / "5384-Y5-R2FR-D4-nested-global-contour-root-clearance-certificate.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5384_VALIDATION.csv"

SCRIPT_5381 = SCRIPTS / "Y5_R2FR_5381_D4_parent_residue_geometric_denominator_enclosure.py"
RESULT_5381 = FUNCTIONAL_RG / "5381" / "D4_parent_residue_geometric_denominator_result.json"
VALIDATION_5381 = FUNCTIONAL_RG / "5381" / "D4_parent_residue_geometric_denominator_validation.csv"
SCRIPT_5383 = SCRIPTS / "Y5_R2FR_5383_D4_double_Cauchy_parent_C0_residue.py"
RESULT_5383 = FUNCTIONAL_RG / "5383" / "D4_double_Cauchy_parent_C0_result.json"
VALIDATION_5383 = FUNCTIONAL_RG / "5383" / "D4_double_Cauchy_parent_C0_validation.csv"
BOXES_5380 = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_boxes.csv"
EVENTS_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"

CHECKPOINT = 5384
MARKER = "MTS_5384_D4_NESTED_GLOBAL_CONTOUR_ROOT_CLEARANCE_CERTIFICATE"
REVISION = "D4-nested-global-contour-root-clearance-certificate-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
INTERVAL_DIGITS = 50
ENERGY_PHASE_ARC_COUNT = 32
ENERGY_CONTOUR_RELATIVE_RADIUS = "1e-6"
GLOBAL_CONTOUR_RELATIVE_RADIUS = "1e-7"
GLOBAL_ROOT_LABELS = ("plus_u", "plus_v", "minus_u", "minus_v")

CLAIM_CLEARANCE = "valid_for_D4_nested_global_contour_root_clearance"
OPEN_CLAIMS = (
    "valid_for_D4_nested_contour_integrand_enclosure",
    "valid_for_D4_energy_contour_exclusive_parent_pole",
    "valid_for_D4_finite_plus_double_pole_coefficient_enclosure",
    "valid_for_D4_endpoint_C_regulator_zero_limit",
    "valid_for_D4_numeric_H3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
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


M5381 = load_module("mts_5381_for_5384", SCRIPT_5381)
M5383 = load_module("mts_5383_for_5384", SCRIPT_5383)
M5380 = M5381.M5380


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def open_claims() -> dict[str, bool]:
    return {claim: False for claim in OPEN_CLAIMS}


def source_paths() -> tuple[Path, ...]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5381,
        RESULT_5381,
        VALIDATION_5381,
        SCRIPT_5383,
        RESULT_5383,
        VALIDATION_5383,
        BOXES_5380,
        EVENTS_5358,
    )
    return tuple(dict.fromkeys(path.resolve() for path in paths))


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "MISSING",
            CLAIM_CLEARANCE: False,
            **open_claims(),
        }
        for path in source_paths()
    ]


def preflight() -> dict[str, Any]:
    paths = source_paths()
    result_5381 = read_json(RESULT_5381)
    result_5383 = read_json(RESULT_5383)
    source_boxes = read_csv(BOXES_5380)
    checks = {
        "all_direct_sources_exist": all(path.is_file() for path in paths),
        "checkpoint_5381_passes": result_5381.get("validation_passed") is True
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5381)),
        "checkpoint_5383_passes": result_5383.get("validation_passed") is True
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5383)),
        "geometric_denominator_enclosure_is_claimed": result_5381.get(
            "claim_boundary", {}
        ).get("valid_for_D4_parent_residue_geometric_denominator_enclosure")
        is True,
        "numerical_double_Cauchy_residue_is_claimed": result_5383.get(
            "claim_boundary", {}
        ).get("valid_for_D4_numerical_double_Cauchy_parent_C0_residue")
        is True,
        "contour_radii_match_checkpoint_5383": M5383.ENERGY_PRIMARY_RELATIVE_RADIUS
        == ENERGY_CONTOUR_RELATIVE_RADIUS
        and M5383.GLOBAL_CONTOUR_RELATIVE_RADIUS
        == GLOBAL_CONTOUR_RELATIVE_RADIUS,
        "all_64_complex_event_boxes_are_present": len(source_boxes)
        == len(EVENT_IDS) * M5380.EPSILON_BIN_COUNT,
        "all_eight_event_ids_are_present": sorted(
            {row["event_id"] for row in source_boxes}
        )
        == list(EVENT_IDS),
        "formal_workbench_inventory_is_unchanged": M5380.M5379.M5378.M5359.M5342.M5283.formal_inventory_digest()
        == M5380.M5379.M5378.M5359.M5342.FORMAL_DIGEST,
        "scripts_cache_is_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {"checks": checks, "all_pass": all(checks.values())}


def exact_algebra_audit() -> dict[str, Any]:
    import sympy as sp

    recoil, cosine, decay_cosine, q_value, relative = sp.symbols(
        "R c d q y", nonzero=True
    )
    sine, decay_sine = sp.symbols("s t", nonzero=True)
    relative_cosine = (
        (relative + 1 / relative) * sine * decay_sine / 2
        + cosine * decay_cosine
    )
    first_energy = (
        1 + recoil**2 - relative_cosine * (1 - recoil**2)
    ) / 2
    longitudinal = (
        relative_cosine * (1 - recoil) ** 2 - (1 - recoil**2)
    ) / 2
    holomorphic = relative * recoil * decay_sine + longitudinal * sine
    antiholomorphic = recoil * decay_sine / relative + longitudinal * sine
    momentum_z = longitudinal * cosine + recoil * decay_cosine
    plus_denominator = first_energy + momentum_z
    minus_denominator = first_energy - momentum_z
    relations = (
        sine**2 + cosine**2 - 1,
        decay_sine**2 + decay_cosine**2 - 1,
    )
    generators = (
        sine,
        decay_sine,
        recoil,
        cosine,
        decay_cosine,
        q_value,
        relative,
    )
    null_numerator = sp.together(
        plus_denominator * minus_denominator
        - holomorphic * antiholomorphic
    ).as_numer_denom()[0]
    null_remainder = sp.reduced(
        sp.expand(null_numerator), list(relations), *generators
    )[1]
    factor_f1 = (
        q_value * recoil * cosine
        + q_value * recoil
        - q_value * cosine
        - q_value
        + recoil * cosine
        + recoil
        - cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * cosine
        - q_value * recoil
        - q_value * cosine
        - q_value
        + recoil * cosine
        - recoil
        - cosine
        + 1
    )
    representative = (
        sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + cosine) * factor_f2)
    )
    collision_residual = (
        sine * plus_denominator
        + q_value * (1 + cosine) * holomorphic
    )
    collision_numerator = sp.together(
        collision_residual.subs(relative, representative)
    ).as_numer_denom()[0]
    collision_remainder = sp.reduced(
        sp.expand(collision_numerator),
        list(relations),
        sine,
        decay_sine,
        recoil,
        cosine,
        decay_cosine,
        q_value,
    )[1]
    reciprocal_numerator_difference = sp.together(
        antiholomorphic.subs(relative, 1 / representative)
        - holomorphic.subs(relative, representative)
    ).as_numer_denom()[0]
    reciprocal_remainder = sp.reduced(
        sp.expand(reciprocal_numerator_difference),
        list(relations),
        sine,
        decay_sine,
        recoil,
        cosine,
        decay_cosine,
        q_value,
    )[1]
    return {
        "first_internal_null_remainder": str(sp.factor(null_remainder)),
        "representative_collision_remainder": str(
            sp.factor(collision_remainder)
        ),
        "reciprocal_chart_mapping_remainder": str(
            sp.factor(reciprocal_remainder)
        ),
        "all_exact_remainders_are_zero": null_remainder == 0
        and collision_remainder == 0
        and reciprocal_remainder == 0,
    }


def projective_root_pairs(
    factors: tuple[Any, Any, Any, Any], label: str, external_root: Any
) -> tuple[tuple[Any, Any, str], tuple[Any, Any, str]]:
    plus_denominator, minus_denominator, holomorphic, antiholomorphic = factors
    if label == "plus_u":
        return (
            (external_root * plus_denominator, holomorphic, "primary"),
            (external_root * antiholomorphic, minus_denominator, "opposite"),
        )
    if label == "plus_v":
        return (
            (antiholomorphic, external_root * plus_denominator, "primary"),
            (minus_denominator, external_root * holomorphic, "opposite"),
        )
    if label == "minus_u":
        return (
            (-plus_denominator, external_root * holomorphic, "primary"),
            (-antiholomorphic, external_root * minus_denominator, "opposite"),
        )
    if label == "minus_v":
        return (
            (-external_root * antiholomorphic, plus_denominator, "primary"),
            (-external_root * minus_denominator, holomorphic, "opposite"),
        )
    raise ValueError(f"unsupported global-root label {label}")


def projective_separation_bound(
    factors: tuple[Any, Any, Any, Any],
    label: str,
    external_root: Any,
    selected_root: Any,
) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for numerator, denominator, chart in projective_root_pairs(
        factors, label, external_root
    ):
        translated_numerator = numerator - selected_root * denominator
        numerator_lower = M5381.modulus_lower(translated_numerator)
        denominator_upper = M5381.modulus_upper(denominator)
        separation_lower = (
            numerator_lower / denominator_upper
            if denominator_upper > 0
            else math.inf
        )
        candidates.append(
            {
                "method": "projective_translated_root_factor",
                "chart": chart,
                "translated_numerator_modulus_lower": numerator_lower,
                "projective_denominator_modulus_upper": denominator_upper,
                "separation_modulus_lower": separation_lower,
            }
        )
    return max(candidates, key=lambda row: row["separation_modulus_lower"])


def contour_certificate(
    configuration: dict[str, Any],
    epsilon: Any,
    state_boxes: list[Any],
    phase_interval: Any,
) -> dict[str, Any]:
    material_recoil = state_boxes[0] + 1j * state_boxes[1]
    event_pole_energy = 1 - material_recoil**2
    energy_radius = iv.mpf(ENERGY_CONTOUR_RELATIVE_RADIUS)
    energy_displacement = energy_radius * (
        iv.cos(phase_interval) + 1j * iv.sin(phase_interval)
    )
    energy = event_pole_energy + energy_displacement
    energy_recoil_radicand = 1 - energy
    recoil = M5381.positive_complex_sqrt(energy_recoil_radicand)
    coordinate_index = (
        2 if configuration["event_type"] == "BRANCH_DEATH" else 3
    )
    soft_cosine = configuration["sign"] * state_boxes[coordinate_index]
    soft_sine = (
        M5381.positive_complex_sqrt(1 - soft_cosine**2)
        if configuration["event_type"] == "BRANCH_DEATH"
        else state_boxes[4]
    )
    decay_cosine = iv.mpc(configuration["decay_cosine"])
    decay_sine = iv.mpc(
        math.sqrt(1 - float(configuration["decay_cosine"]) ** 2)
    )
    epsilon_squared = epsilon**2
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * M5381.positive_complex_sqrt(-q_value)
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1
    )
    representative_denominator = (
        decay_sine * (1 + soft_cosine) * factor_f2
    )
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / representative_denominator
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    relative_cosine = (
        (relative + 1 / relative) * soft_sine * decay_sine / 2
        + soft_cosine * decay_cosine
    )
    first_energy = (
        1 + recoil**2 - relative_cosine * (1 - recoil**2)
    ) / 2
    longitudinal = (
        relative_cosine * (1 - recoil) ** 2 - (1 - recoil**2)
    ) / 2
    holomorphic = relative * recoil * decay_sine + longitudinal * soft_sine
    antiholomorphic = (
        recoil * decay_sine / relative + longitudinal * soft_sine
    )
    momentum_z = longitudinal * soft_cosine + recoil * decay_cosine
    first_factors = (
        first_energy + momentum_z,
        first_energy - momentum_z,
        holomorphic,
        antiholomorphic,
    )
    soft_factors = (
        1 + soft_cosine,
        1 - soft_cosine,
        soft_sine,
        soft_sine,
    )
    second_selected_label = configuration["root_labels"][1]
    if second_selected_label == "plus_u":
        selected_root = external_root * (1 + soft_cosine) / soft_sine
        selected_root_denominators = (soft_sine,)
    elif second_selected_label == "plus_v":
        selected_root = soft_sine / (
            (1 + soft_cosine) * external_root
        )
        selected_root_denominators = (1 + soft_cosine, external_root)
    else:
        raise ValueError(
            f"unsupported selected soft root {second_selected_label}"
        )
    global_radius_upper = float(GLOBAL_CONTOUR_RELATIVE_RADIUS) * max(
        1.0, M5381.modulus_upper(selected_root)
    )
    selected_keys = {
        (0, configuration["root_labels"][0]),
        (2, configuration["root_labels"][1]),
    }
    root_records: list[dict[str, Any]] = []
    for momentum_index, factors in ((0, first_factors), (2, soft_factors)):
        for label in GLOBAL_ROOT_LABELS:
            if (momentum_index, label) in selected_keys:
                continue
            if (
                momentum_index == 0
                and label == "plus_u"
                and configuration["role"] == "representative"
            ):
                separation_lower = (
                    M5381.modulus_lower(1 + q_value)
                    * M5381.modulus_lower(selected_root)
                )
                bound = {
                    "method": "same_momentum_root_relation_plus_u_equals_minus_q_z",
                    "chart": "exact_q_relation",
                    "translated_numerator_modulus_lower": separation_lower,
                    "projective_denominator_modulus_upper": 1.0,
                    "separation_modulus_lower": separation_lower,
                }
            elif momentum_index == 0 and label == "plus_v":
                if configuration["role"] == "representative":
                    denominator_upper = (
                        M5381.modulus_upper(external_root)
                        * M5381.modulus_upper(holomorphic)
                    )
                    separation_lower = (
                        2 * M5381.modulus_lower(first_energy)
                        / denominator_upper
                        if denominator_upper > 0
                        else math.inf
                    )
                    bound = {
                        "method": "factorized_null_identity_2E_over_eH",
                        "chart": "exact_null_reduction",
                        "translated_numerator_modulus_lower": 2
                        * M5381.modulus_lower(first_energy),
                        "projective_denominator_modulus_upper": denominator_upper,
                        "separation_modulus_lower": separation_lower,
                    }
                else:
                    q_upper = M5381.modulus_upper(q_value)
                    separation_lower = (
                        M5381.modulus_lower(selected_root)
                        * M5381.modulus_lower(1 + q_value)
                        / q_upper
                    )
                    bound = {
                        "method": "same_momentum_root_relation_plus_v_equals_minus_z_over_q",
                        "chart": "exact_q_relation",
                        "translated_numerator_modulus_lower": M5381.modulus_lower(
                            selected_root
                        )
                        * M5381.modulus_lower(1 + q_value),
                        "projective_denominator_modulus_upper": q_upper,
                        "separation_modulus_lower": separation_lower,
                    }
            else:
                bound = projective_separation_bound(
                    factors, label, external_root, selected_root
                )
            clearance_margin = (
                bound["separation_modulus_lower"] - global_radius_upper
            )
            root_records.append(
                {
                    "root_id": f"g{momentum_index + 1}:{label}",
                    **bound,
                    "clearance_margin_lower": clearance_margin,
                    "root_clears_global_contour": clearance_margin > 0,
                }
            )
    selected_numerator = (
        holomorphic
        if configuration["role"] == "representative"
        else antiholomorphic
    )
    collision_cross_residual = (
        soft_sine * first_factors[0]
        + q_value * (1 + soft_cosine) * selected_numerator
    )
    first_null_residual = (
        first_factors[0] * first_factors[1]
        - holomorphic * antiholomorphic
    )
    primitive_denominators = (
        64 + epsilon_squared,
        energy_recoil_radicand,
        decay_sine,
        1 + soft_cosine,
        soft_sine,
        factor_f2,
        representative_denominator,
        representative,
        relative,
        external_root,
        *selected_root_denominators,
        selected_root,
    )
    minimum_primitive_denominator_lower = min(
        M5381.modulus_lower(value) for value in primitive_denominators
    )
    worst_root = min(
        root_records, key=lambda row: row["clearance_margin_lower"]
    )
    return {
        "event_pole_energy": event_pole_energy,
        "energy": energy,
        "energy_recoil_radicand": energy_recoil_radicand,
        "q_value": q_value,
        "relative_root": relative,
        "selected_global_root": selected_root,
        "global_contour_radius_upper": global_radius_upper,
        "minimum_primitive_denominator_modulus_lower": minimum_primitive_denominator_lower,
        "collision_cross_residual": collision_cross_residual,
        "collision_cross_residual_contains_zero": M5381.contains_zero(
            collision_cross_residual
        ),
        "first_null_residual": first_null_residual,
        "first_null_residual_contains_zero": M5381.contains_zero(
            first_null_residual
        ),
        "root_records": root_records,
        "worst_root": worst_root,
        "all_six_nonselected_roots_clear": len(root_records) == 6
        and all(row["root_clears_global_contour"] for row in root_records),
    }


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5384 — Y5/R2FR D4 nested global-contour root-clearance certificate",
        "",
        "## Result",
        "",
        f"Decision: `{result['decision']}`.",
        "",
        "The 5380 complex event boxes are now carried around the checkpoint-5383 parent-energy contour. On each certified energy arc, the intended colliding pair is fixed by an exact algebraic collision identity and all six nonselected projective global roots are proved to remain outside the inner Cauchy contour.",
        "",
        f"- certified event/epsilon boxes: `{result['certified_event_epsilon_box_count']}/{result['required_event_epsilon_box_count']}`;",
        f"- certified energy-contour arcs: `{result['certified_energy_arc_count']}/{result['required_energy_arc_count']}`;",
        f"- nonselected root checks: `{result['nonselected_root_check_count']}`;",
        f"- minimum certified nonselected-root separation: `{result['minimum_nonselected_root_separation_lower']}`;",
        f"- maximum inner global-contour radius: `{result['maximum_global_contour_radius_upper']}`;",
        f"- minimum separation-minus-radius margin: `{result['minimum_global_contour_clearance_margin_lower']}`.",
        "",
        "## Exact identities",
        "",
        "With `D_+=E_1+p_z`, `D_-=E_1-p_z`, `H=p_x+i p_y`, and `A=p_x-i p_y`, exact polynomial reduction modulo `s^2+c^2=1` and `t^2+d^2=1` gives `D_+D_--HA=0`. The parent relative-root formula also gives `s D_+ + q(1+c)H=0`; under the reciprocal chart `A(1/y)=H(y)`. These identities own the selected double root and the chart changes used by the projective clearance bounds.",
        "",
        "## Scope",
        "",
        "This certifies isolation of the inner global double pole while the outer energy variable traverses its Cauchy contour. It does not yet enclose the finite-plus contour integrand, prove that the parent energy pole is the only energy-plane singularity inside the outer contour, or establish endpoint C, H3, the uniform remainder, the D4 outer limit, local GR, or the full MTS theory.",
        "",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    temporary.replace(DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    M5380.set_below_normal_priority()
    iv.dps = INTERVAL_DIGITS
    preflight_result = preflight()
    if not preflight_result["all_pass"]:
        raise RuntimeError(f"preflight failed: {preflight_result}")
    algebra = exact_algebra_audit()
    references, _ = M5380.M5379.M5378.M5359.reference_rows()
    events = read_csv(EVENTS_5358)
    event_lookup = {row["event_id"]: row for row in events}
    arc_rows: list[dict[str, Any]] = []
    root_aggregate: dict[tuple[str, str, str], dict[str, Any]] = {}
    certified_boxes: set[tuple[str, str]] = set()
    for source in read_csv(BOXES_5380):
        configuration = M5380.M5379.M5378.M5359.event_configuration(
            event_lookup[source["event_id"]], references
        )
        epsilon = iv.mpc(
            iv.mpf(
                [source["epsilon_real_lower"], source["epsilon_real_upper"]]
            ),
            iv.mpf(
                [
                    source["epsilon_imaginary_lower"],
                    source["epsilon_imaginary_upper"],
                ]
            ),
        )
        state_boxes = [
            M5381.parse_complex_box(text)
            for text in source["complex_state_boxes"].split("|")
        ]
        source_box_passes = True
        for arc_index in range(ENERGY_PHASE_ARC_COUNT):
            phase_interval = (
                2
                * iv.pi
                * iv.mpf([arc_index, arc_index + 1])
                / ENERGY_PHASE_ARC_COUNT
            )
            certificate = contour_certificate(
                configuration, epsilon, state_boxes, phase_interval
            )
            event_energy_upper = M5381.modulus_upper(
                certificate["event_pole_energy"]
            )
            radicand_real_lower = M5380.real_lower(
                certificate["energy_recoil_radicand"]
            )
            arc_passes = (
                event_energy_upper < 1
                and radicand_real_lower > 0
                and certificate[
                    "minimum_primitive_denominator_modulus_lower"
                ]
                > 0
                and certificate["collision_cross_residual_contains_zero"]
                and certificate["first_null_residual_contains_zero"]
                and certificate["all_six_nonselected_roots_clear"]
            )
            source_box_passes = source_box_passes and arc_passes
            worst_root = certificate["worst_root"]
            arc_rows.append(
                {
                    "event_id": configuration["event_id"],
                    "event_type": configuration["event_type"],
                    "epsilon_bin_index": source["epsilon_bin_index"],
                    "epsilon_real_lower": source["epsilon_real_lower"],
                    "epsilon_real_upper": source["epsilon_real_upper"],
                    "epsilon_imaginary_lower": source[
                        "epsilon_imaginary_lower"
                    ],
                    "epsilon_imaginary_upper": source[
                        "epsilon_imaginary_upper"
                    ],
                    "energy_phase_arc_index": arc_index,
                    "energy_phase_lower": M5380.real_lower(phase_interval),
                    "energy_phase_upper": M5380.real_upper(phase_interval),
                    "selected_role": configuration["role"],
                    "selected_root_labels": "|".join(
                        configuration["root_labels"]
                    ),
                    "event_pole_energy_modulus_upper": event_energy_upper,
                    "energy_contour_radius": ENERGY_CONTOUR_RELATIVE_RADIUS,
                    "energy_recoil_radicand_real_lower": radicand_real_lower,
                    "selected_global_root_box": M5380.complex_interval_text(
                        certificate["selected_global_root"]
                    ),
                    "global_contour_radius_upper": certificate[
                        "global_contour_radius_upper"
                    ],
                    "minimum_primitive_denominator_modulus_lower": certificate[
                        "minimum_primitive_denominator_modulus_lower"
                    ],
                    "worst_nonselected_root_id": worst_root["root_id"],
                    "worst_nonselected_root_method": worst_root["method"],
                    "worst_nonselected_root_chart": worst_root["chart"],
                    "minimum_nonselected_root_separation_lower": worst_root[
                        "separation_modulus_lower"
                    ],
                    "minimum_global_contour_clearance_margin_lower": worst_root[
                        "clearance_margin_lower"
                    ],
                    "collision_cross_residual_modulus_upper": M5381.modulus_upper(
                        certificate["collision_cross_residual"]
                    ),
                    "collision_cross_residual_contains_zero": certificate[
                        "collision_cross_residual_contains_zero"
                    ],
                    "first_null_residual_modulus_upper": M5381.modulus_upper(
                        certificate["first_null_residual"]
                    ),
                    "first_null_residual_contains_zero": certificate[
                        "first_null_residual_contains_zero"
                    ],
                    "six_nonselected_roots_checked": len(
                        certificate["root_records"]
                    )
                    == 6,
                    "energy_arc_passes": arc_passes,
                    CLAIM_CLEARANCE: False,
                    **open_claims(),
                }
            )
            for root in certificate["root_records"]:
                key = (
                    configuration["event_id"],
                    source["epsilon_bin_index"],
                    root["root_id"],
                )
                aggregate = root_aggregate.get(key)
                if aggregate is None:
                    root_aggregate[key] = {
                        "event_id": configuration["event_id"],
                        "event_type": configuration["event_type"],
                        "epsilon_bin_index": source["epsilon_bin_index"],
                        "root_id": root["root_id"],
                        "minimum_separation_modulus_lower": root[
                            "separation_modulus_lower"
                        ],
                        "minimum_clearance_margin_lower": root[
                            "clearance_margin_lower"
                        ],
                        "worst_energy_phase_arc_index": arc_index,
                        "methods": {root["method"]},
                        "charts": {root["chart"]},
                        "all_energy_arcs_clear": root[
                            "root_clears_global_contour"
                        ],
                    }
                else:
                    aggregate["methods"].add(root["method"])
                    aggregate["charts"].add(root["chart"])
                    aggregate["all_energy_arcs_clear"] = aggregate[
                        "all_energy_arcs_clear"
                    ] and root["root_clears_global_contour"]
                    if root["clearance_margin_lower"] < aggregate[
                        "minimum_clearance_margin_lower"
                    ]:
                        aggregate["minimum_separation_modulus_lower"] = root[
                            "separation_modulus_lower"
                        ]
                        aggregate["minimum_clearance_margin_lower"] = root[
                            "clearance_margin_lower"
                        ]
                        aggregate["worst_energy_phase_arc_index"] = arc_index
        if source_box_passes:
            certified_boxes.add(
                (configuration["event_id"], source["epsilon_bin_index"])
            )
        print(
            f"completed {configuration['event_id']} epsilon-bin={source['epsilon_bin_index']} passes={source_box_passes}",
            flush=True,
        )
    root_rows: list[dict[str, Any]] = []
    for key in sorted(root_aggregate):
        aggregate = root_aggregate[key]
        root_rows.append(
            {
                **{
                    name: value
                    for name, value in aggregate.items()
                    if name not in {"methods", "charts"}
                },
                "methods": "|".join(sorted(aggregate["methods"])),
                "charts": "|".join(sorted(aggregate["charts"])),
                CLAIM_CLEARANCE: False,
                **open_claims(),
            }
        )
    required_box_count = len(EVENT_IDS) * M5380.EPSILON_BIN_COUNT
    required_arc_count = required_box_count * ENERGY_PHASE_ARC_COUNT
    certified_arc_count = sum(
        parse_bool(row["energy_arc_passes"]) for row in arc_rows
    )
    nonselected_root_check_count = required_arc_count * 6
    minimum_separation = min(
        float(row["minimum_nonselected_root_separation_lower"])
        for row in arc_rows
    )
    maximum_global_radius = max(
        float(row["global_contour_radius_upper"]) for row in arc_rows
    )
    minimum_clearance_margin = min(
        float(row["minimum_global_contour_clearance_margin_lower"])
        for row in arc_rows
    )
    minimum_primitive = min(
        float(row["minimum_primitive_denominator_modulus_lower"])
        for row in arc_rows
    )
    validations = [
        validation_row(
            "preflight_passes",
            preflight_result["all_pass"],
            preflight_result["checks"],
        ),
        validation_row(
            "exact_null_collision_and_reciprocal_identities_reduce_to_zero",
            algebra["all_exact_remainders_are_zero"],
            algebra,
        ),
        validation_row(
            "all_required_event_epsilon_boxes_are_certified",
            len(certified_boxes) == required_box_count,
            f"certified={len(certified_boxes)};required={required_box_count}",
        ),
        validation_row(
            "all_required_energy_phase_arcs_are_certified",
            certified_arc_count == required_arc_count,
            f"certified={certified_arc_count};required={required_arc_count}",
        ),
        validation_row(
            "every_arc_checks_exactly_six_nonselected_roots",
            all(
                parse_bool(row["six_nonselected_roots_checked"])
                for row in arc_rows
            ),
            f"checks={nonselected_root_check_count}",
        ),
        validation_row(
            "all_384_box_root_summaries_are_present",
            len(root_rows) == required_box_count * 6,
            f"rows={len(root_rows)};required={required_box_count * 6}",
        ),
        validation_row(
            "all_nonselected_roots_clear_the_global_contour",
            minimum_clearance_margin > 0
            and all(
                parse_bool(row["all_energy_arcs_clear"])
                for row in root_rows
            ),
            minimum_clearance_margin,
        ),
        validation_row(
            "all_event_pole_centers_keep_fixed_energy_radius",
            all(
                float(row["event_pole_energy_modulus_upper"]) < 1
                for row in arc_rows
            ),
            max(
                float(row["event_pole_energy_modulus_upper"])
                for row in arc_rows
            ),
        ),
        validation_row(
            "energy_recoil_square_root_chart_excludes_its_cut",
            all(
                float(row["energy_recoil_radicand_real_lower"]) > 0
                for row in arc_rows
            ),
            min(
                float(row["energy_recoil_radicand_real_lower"])
                for row in arc_rows
            ),
        ),
        validation_row(
            "all_primitive_contour_denominators_exclude_zero",
            minimum_primitive > 0,
            minimum_primitive,
        ),
        validation_row(
            "all_interval_collision_and_null_residuals_enclose_zero",
            all(
                parse_bool(row["collision_cross_residual_contains_zero"])
                and parse_bool(row["first_null_residual_contains_zero"])
                for row in arc_rows
            ),
            f"arcs={len(arc_rows)}",
        ),
        validation_row(
            "integrand_energy_pole_H3_and_downstream_claims_remain_false",
            all(value is False for value in open_claims().values()),
            open_claims(),
        ),
        validation_row(
            "formal_workbench_remains_unchanged",
            M5380.M5379.M5378.M5359.M5342.M5283.formal_inventory_digest()
            == M5380.M5379.M5378.M5359.M5342.FORMAL_DIGEST,
            M5380.M5379.M5378.M5359.M5342.M5283.formal_inventory_digest(),
        ),
        validation_row(
            "scripts_cache_remains_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    for row in arc_rows:
        row[CLAIM_CLEARANCE] = passed
    for row in root_rows:
        row[CLAIM_CLEARANCE] = passed
    registered_sources = source_rows()
    for row in registered_sources:
        row[CLAIM_CLEARANCE] = passed
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "decision": (
            "D4_NESTED_GLOBAL_CONTOUR_ROOT_CLEARANCE_CERTIFIED__ENCLOSE_FACTORIZED_FINITE_PLUS_INTEGRAND"
            if passed
            else "D4_NESTED_GLOBAL_CONTOUR_ROOT_CLEARANCE_BLOCKED"
        ),
        "required_event_epsilon_box_count": required_box_count,
        "certified_event_epsilon_box_count": len(certified_boxes),
        "required_energy_arc_count": required_arc_count,
        "certified_energy_arc_count": certified_arc_count,
        "nonselected_root_check_count": nonselected_root_check_count,
        "minimum_nonselected_root_separation_lower": minimum_separation,
        "maximum_global_contour_radius_upper": maximum_global_radius,
        "minimum_global_contour_clearance_margin_lower": minimum_clearance_margin,
        "minimum_primitive_denominator_modulus_lower": minimum_primitive,
        "exact_algebra_audit": algebra,
        "claim_boundary": {CLAIM_CLEARANCE: passed, **open_claims()},
        "remaining_obstruction": "factor the finite-plus amplitude around the certified selected double root so interval evaluation preserves pole cancellation; then enclose the outer energy contour and derive an H3 Cauchy bound",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(
        output / "D4_nested_global_contour_root_clearance_arcs.csv", arc_rows
    )
    atomic_csv(
        output / "D4_nested_global_contour_root_clearance_roots.csv", root_rows
    )
    atomic_csv(
        output / "D4_nested_global_contour_root_clearance_validation.csv",
        validations,
    )
    atomic_csv(output / "source_register.csv", registered_sources)
    atomic_csv(VALIDATION, validations)
    atomic_json(
        output / "D4_nested_global_contour_root_clearance_result.json", result
    )
    atomic_json(
        output / "status.json",
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if passed else "blocked",
            "decision": result["decision"],
            "updated_utc": result["updated_utc"],
        },
    )
    render_document(result)
    return result


def self_test() -> dict[str, Any]:
    iv.dps = 30
    factors = (iv.mpc(2), iv.mpc(3), iv.mpc(4), iv.mpc(1.5))
    external_root = iv.mpc(1.2)
    selected_root = iv.mpc(0.5)
    bound = projective_separation_bound(
        factors, "plus_u", external_root, selected_root
    )
    return {
        "projective_bound_is_positive": bound["separation_modulus_lower"] > 0,
        "six_global_labels_are_declared": len(GLOBAL_ROOT_LABELS) == 4,
        "phase_arc_count_is_positive": ENERGY_PHASE_ARC_COUNT > 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=MARKER)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        tests = self_test()
        print(json.dumps(tests, indent=2, sort_keys=True))
        return 0 if all(tests.values()) else 1
    if arguments.dry_run:
        result = preflight()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["all_pass"] else 1
    result = run(arguments.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
