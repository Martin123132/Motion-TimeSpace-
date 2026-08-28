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
OUTPUT = FUNCTIONAL_RG / "5382"
DOCUMENT = POST / "5382-Y5-R2FR-D4-Cauchy-double-pole-coefficient-extraction.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5382_VALIDATION.csv"

SCRIPT_5381 = SCRIPTS / "Y5_R2FR_5381_D4_parent_residue_geometric_denominator_enclosure.py"
RESULT_5381 = FUNCTIONAL_RG / "5381" / "D4_parent_residue_geometric_denominator_result.json"
VALIDATION_5381 = FUNCTIONAL_RG / "5381" / "D4_parent_residue_geometric_denominator_validation.csv"
EVENTS_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
ENDPOINTS_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_coefficients.csv"

CHECKPOINT = 5382
MARKER = "MTS_5382_D4_CAUCHY_DOUBLE_POLE_COEFFICIENT_EXTRACTION"
REVISION = "D4-Cauchy-double-pole-coefficient-extraction-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
MP_DIGITS = 110
ENERGY_INITIAL_STEP = "1e-6"
ENERGY_LEVELS = 8
ENERGY_EXTRAPOLATION_ORDER = 5
CONTOUR_PRIMARY_RELATIVE_RADIUS = "1e-7"
CONTOUR_SECONDARY_RELATIVE_RADIUS = "5e-8"
CONTOUR_PRIMARY_POINTS = 48
CONTOUR_ANGULAR_CROSSCHECK_POINTS = 72
RADIUS_SAFETY_FACTOR = 8
CAUCHY_RELATIVE_STABILITY_LIMIT = 2.0e-8
C0_RELATIVE_AGREEMENT_LIMIT = 2.0e-5

CLAIM_CAUCHY = "valid_for_D4_numerical_Cauchy_double_pole_coefficient_extraction"
CLAIM_C0 = "valid_for_D4_Cauchy_parent_energy_residue_crosscheck"
OPEN_CLAIMS = (
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


M5381 = load_module("mts_5381_for_5382", SCRIPT_5381)
M5378 = M5381.M5380.M5379.M5378
mp = M5378.mp


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


def mp_text(value: Any, digits: int = 40) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


def complex_fields(prefix: str, value: Any) -> dict[str, str]:
    return {
        f"{prefix}_real": mp_text(mp.re(value)),
        f"{prefix}_imaginary": mp_text(mp.im(value)),
    }


def complex_from_row(row: dict[str, str], prefix: str) -> Any:
    return mp.mpc(row[f"{prefix}_real"], row[f"{prefix}_imaginary"])


def relative_difference(first: Any, second: Any) -> float:
    return float(
        abs(first - second) / max(abs(first), abs(second), mp.mpf("1e-300"))
    )


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
        EVENTS_5358,
        ENDPOINTS_5359,
        Path(M5378.__file__).resolve(),
        Path(M5378.AMP.__file__).resolve(),
    )
    return tuple(dict.fromkeys(path.resolve() for path in paths))


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "MISSING",
            CLAIM_CAUCHY: False,
            CLAIM_C0: False,
            **open_claims(),
        }
        for path in source_paths()
    ]


def preflight() -> dict[str, Any]:
    paths = source_paths()
    result_5381 = read_json(RESULT_5381)
    checks = {
        "all_direct_sources_exist": all(path.is_file() for path in paths),
        "checkpoint_5381_passes": result_5381.get("validation_passed") is True
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5381)),
        "geometric_denominator_enclosure_is_claimed": result_5381.get(
            "claim_boundary", {}
        ).get("valid_for_D4_parent_residue_geometric_denominator_enclosure")
        is True,
        "eight_zero_events_are_present": [
            row["event_id"] for row in read_csv(EVENTS_5358)
        ]
        == list(EVENT_IDS),
        "formal_workbench_inventory_is_unchanged": M5378.M5359.M5342.M5283.formal_inventory_digest()
        == M5378.M5359.M5342.FORMAL_DIGEST,
        "scripts_cache_is_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {"checks": checks, "all_pass": all(checks.values())}


def collision_geometry(
    configuration: dict[str, Any], energy: Any, epsilon: Any
) -> dict[str, Any]:
    target, q_value = M5378.target_and_q(epsilon)
    external_root = -1j * mp.sqrt(-q_value)
    soft_cosine = configuration["soft_cosine"]
    decay_cosine = configuration["decay_cosine"]
    representative_root = M5378.representative_relative_root(
        energy, soft_cosine, decay_cosine, q_value
    )
    relative_root = (
        1 / representative_root
        if configuration["role"] == "reciprocal"
        else representative_root
    )

    def collision_roots(varied_relative_root: Any) -> tuple[Any, Any]:
        _, _, local_internal = M5378.complex_event_geometry(
            energy, soft_cosine, decay_cosine, varied_relative_root
        )
        directions = [
            [
                local_internal[index][component_index]
                / local_internal[index][0]
                for component_index in range(1, 4)
            ]
            for index in (0, 2)
        ]
        return (
            M5378.global_root(
                directions[0], configuration["root_labels"][0], external_root
            ),
            M5378.global_root(
                directions[1], configuration["root_labels"][1], external_root
            ),
        )

    soft_direction, decay_direction, internal = M5378.complex_event_geometry(
        energy, soft_cosine, decay_cosine, relative_root
    )
    roots = collision_roots(relative_root)
    selected_global_root = (roots[0] + roots[1]) / 2
    collision_jacobian = mp.diff(
        lambda value: collision_roots(value)[0] - collision_roots(value)[1],
        relative_root,
    )
    return {
        "target": target,
        "relative_root": relative_root,
        "soft_direction": soft_direction,
        "decay_direction": decay_direction,
        "internal": internal,
        "selected_global_root": selected_global_root,
        "collision_root_difference": roots[0] - roots[1],
        "collision_jacobian": collision_jacobian,
    }


def contour_coefficient(
    geometry: dict[str, Any], relative_radius: Any, point_count: int
) -> Any:
    selected_global_root = geometry["selected_global_root"]
    radius = relative_radius * max(mp.mpf(1), abs(selected_global_root))
    total = mp.mpc(0)
    for index in range(point_count):
        phase = 2 * mp.pi * index / point_count
        displacement = radius * mp.exp(1j * phase)
        direct, subtraction = M5378.complex_finite_plus_components(
            geometry["internal"],
            geometry["energy"],
            geometry["soft_direction"],
            geometry["decay_direction"],
            geometry["target"],
            selected_global_root + displacement,
        )
        total += (direct + subtraction) * displacement**2
    return total / point_count


def cauchy_relative_residue(
    configuration: dict[str, Any],
    energy: Any,
    epsilon: Any,
    component: dict[str, Any],
) -> dict[str, Any]:
    geometry = collision_geometry(configuration, energy, epsilon)
    geometry["energy"] = energy
    primary_radius = mp.mpf(CONTOUR_PRIMARY_RELATIVE_RADIUS)
    secondary_radius = mp.mpf(CONTOUR_SECONDARY_RELATIVE_RADIUS)
    primary = contour_coefficient(
        geometry, primary_radius, CONTOUR_PRIMARY_POINTS
    )
    angular_crosscheck = contour_coefficient(
        geometry, primary_radius, CONTOUR_ANGULAR_CROSSCHECK_POINTS
    )
    radius_crosscheck = contour_coefficient(
        geometry, secondary_radius, CONTOUR_PRIMARY_POINTS
    )
    displacement_state = M5378.analytic_parent_relative_residue(
        configuration,
        energy,
        epsilon,
        component,
        M5378.GLOBAL_EXPONENT,
        mp.mpf(M5378.GLOBAL_PHASE),
    )
    coefficient_radius = RADIUS_SAFETY_FACTOR * max(
        abs(primary - angular_crosscheck),
        abs(primary - radius_crosscheck),
        abs(angular_crosscheck - radius_crosscheck),
        mp.mpf("1e-80"),
    )
    winding = M5378.M5359.M5342.M5312.M5280.M5277.source_winding_delta(
        component, configuration["role"]
    )
    residue = (
        winding
        * configuration["trace_orientation"]
        * primary
        / (
            geometry["relative_root"]
            * geometry["selected_global_root"]
            * geometry["collision_jacobian"]
        )
    )
    residue_radius = coefficient_radius * abs(
        winding
        * configuration["trace_orientation"]
        / (
            geometry["relative_root"]
            * geometry["selected_global_root"]
            * geometry["collision_jacobian"]
        )
    )
    return {
        **geometry,
        "double_pole_coefficient": primary,
        "double_pole_coefficient_radius": coefficient_radius,
        "angular_crosscheck": angular_crosscheck,
        "radius_crosscheck": radius_crosscheck,
        "displacement_coefficient": displacement_state[
            "double_pole_coefficient"
        ] if "double_pole_coefficient" in displacement_state else None,
        "displacement_residue": displacement_state["residue"],
        "residue": residue,
        "residue_radius": residue_radius,
        "winding": int(winding),
    }


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5382 — Y5/R2FR D4 Cauchy double-pole coefficient extraction",
        "",
        "## Result",
        "",
        f"Decision: `{result['decision']}`.",
        "",
        "The parent finite-plus double-pole coefficient is extracted as the Laurent coefficient",
        "",
        "`K=(2 pi i)^(-1) integral F(zeta)(zeta-z) d zeta`,",
        "",
        "implemented as the circular average of `F(z+r exp(i theta)) r^2 exp(2 i theta)`. This replaces the earlier single tiny displacement by a phase-complete contour projection.",
        "",
        f"- maximum angular/radius contour relative spread: `{result['maximum_contour_relative_spread']}`;",
        f"- maximum Cauchy-versus-displacement relative difference: `{result['maximum_Cauchy_vs_displacement_relative_difference']}`;",
        f"- maximum Cauchy-C0 versus checkpoint-5359 relative difference: `{result['maximum_Cauchy_C0_relative_difference']}`.",
        "",
        "## Scope",
        "",
        "This is a high-precision independent numerical Laurent extraction and parent-energy-residue crosscheck. It is not yet an interval enclosure over the 5380 complex strip, so endpoint C, H3, the uniform remainder, the D4 outer limit, and broader claims remain false.",
        "",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    temporary.replace(DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    M5378.set_below_normal_priority()
    mp.mp.dps = MP_DIGITS
    M5378.AMP.mp.mp.dps = MP_DIGITS
    preflight_result = preflight()
    if not preflight_result["all_pass"]:
        raise RuntimeError(f"preflight failed: {preflight_result}")
    references, _ = M5378.M5359.reference_rows()
    events = read_csv(EVENTS_5358)
    endpoint_rows = {row["event_id"]: row for row in read_csv(ENDPOINTS_5359)}
    sequence_rows: list[dict[str, Any]] = []
    event_rows: list[dict[str, Any]] = []
    old_kernel = M5378.M5359.M5342.configure()
    try:
        context = M5378.M5359.M5342.M5312.M5303.synthetic_context()
        epsilon_id = M5378.M5359.M5342.M5312.EPSILON_ID
        component = context["inventories"][epsilon_id]["components"]["MC04"]
        physical_multiplier = mp.mpf(
            str(M5378.M5359.M5342.M5312.M5309.physical_multiplier())
        )
        for event in events:
            configuration = M5378.M5359.event_configuration(event, references)
            source_endpoint = endpoint_rows[configuration["event_id"]]
            orientations = [
                int(value)
                for value in source_endpoint["parent_orientations"].split("|")
                if value
            ]
            if orientations != [1]:
                raise RuntimeError(
                    f"unexpected trace orientation for {configuration['event_id']}: {orientations}"
                )
            configuration["trace_orientation"] = orientations[0]
            points: list[tuple[Any, Any, Any]] = []
            contour_spreads: list[float] = []
            displacement_differences: list[float] = []
            for level in range(ENERGY_LEVELS):
                step = mp.mpf(ENERGY_INITIAL_STEP) / mp.power(2, level)
                signed_displacement = configuration["energy_approach_sign"] * step
                energy = configuration["energy"] + signed_displacement
                state = cauchy_relative_residue(
                    configuration, energy, mp.mpf(0), component
                )
                estimator = physical_multiplier * signed_displacement * state["residue"]
                estimator_radius = (
                    abs(physical_multiplier * signed_displacement)
                    * state["residue_radius"]
                )
                points.append((step, estimator, estimator_radius))
                contour_spread = max(
                    relative_difference(
                        state["double_pole_coefficient"], state["angular_crosscheck"]
                    ),
                    relative_difference(
                        state["double_pole_coefficient"], state["radius_crosscheck"]
                    ),
                )
                displacement_difference = relative_difference(
                    state["residue"], state["displacement_residue"]
                )
                contour_spreads.append(contour_spread)
                displacement_differences.append(displacement_difference)
                sequence_rows.append(
                    {
                        "event_id": configuration["event_id"],
                        "event_type": configuration["event_type"],
                        "level": level,
                        "positive_energy_step": mp_text(step),
                        "signed_energy_displacement": mp_text(signed_displacement),
                        "sample_energy": mp_text(energy),
                        "contour_primary_relative_radius": CONTOUR_PRIMARY_RELATIVE_RADIUS,
                        "contour_secondary_relative_radius": CONTOUR_SECONDARY_RELATIVE_RADIUS,
                        "contour_primary_points": CONTOUR_PRIMARY_POINTS,
                        "contour_angular_crosscheck_points": CONTOUR_ANGULAR_CROSSCHECK_POINTS,
                        **complex_fields(
                            "Cauchy_double_pole_coefficient",
                            state["double_pole_coefficient"],
                        ),
                        "Cauchy_double_pole_coefficient_radius": mp_text(
                            state["double_pole_coefficient_radius"]
                        ),
                        **complex_fields(
                            "Cauchy_angular_crosscheck", state["angular_crosscheck"]
                        ),
                        **complex_fields(
                            "Cauchy_radius_crosscheck", state["radius_crosscheck"]
                        ),
                        "contour_relative_spread": contour_spread,
                        "Cauchy_vs_displacement_relative_difference": displacement_difference,
                        **complex_fields("Cauchy_energy_residue_estimator", estimator),
                        "Cauchy_energy_residue_estimator_radius": mp_text(
                            estimator_radius
                        ),
                        **complex_fields(
                            "collision_root_difference",
                            state["collision_root_difference"],
                        ),
                        **complex_fields(
                            "collision_jacobian", state["collision_jacobian"]
                        ),
                        CLAIM_CAUCHY: False,
                        CLAIM_C0: False,
                        **open_claims(),
                    }
                )
            c0_result = M5378.extrapolated_value(
                points, ENERGY_EXTRAPOLATION_ORDER
            )
            source_c0 = complex_from_row(source_endpoint, "C0_zero")
            c0_difference = relative_difference(c0_result["value"], source_c0)
            event_rows.append(
                {
                    "event_id": configuration["event_id"],
                    "event_type": configuration["event_type"],
                    **complex_fields("Cauchy_C0", c0_result["value"]),
                    "Cauchy_C0_radius": mp_text(c0_result["radius"]),
                    **complex_fields("source_5359_C0", source_c0),
                    "Cauchy_C0_relative_difference": c0_difference,
                    "maximum_contour_relative_spread": max(contour_spreads),
                    "maximum_Cauchy_vs_displacement_relative_difference": max(
                        displacement_differences
                    ),
                    CLAIM_CAUCHY: False,
                    CLAIM_C0: False,
                    **open_claims(),
                }
            )
    finally:
        M5378.M5359.M5342.M5326.restore_kernel(old_kernel)
    maximum_contour_spread = max(
        float(row["maximum_contour_relative_spread"]) for row in event_rows
    )
    maximum_displacement_difference = max(
        float(row["maximum_Cauchy_vs_displacement_relative_difference"])
        for row in event_rows
    )
    maximum_c0_difference = max(
        float(row["Cauchy_C0_relative_difference"]) for row in event_rows
    )
    cauchy_passes = maximum_contour_spread <= CAUCHY_RELATIVE_STABILITY_LIMIT
    c0_passes = cauchy_passes and maximum_c0_difference <= C0_RELATIVE_AGREEMENT_LIMIT
    validations = [
        validation_row(
            "preflight_passes", preflight_result["all_pass"], preflight_result["checks"]
        ),
        validation_row(
            "all_eight_event_sequences_are_complete",
            len(sequence_rows) == len(EVENT_IDS) * ENERGY_LEVELS,
            len(sequence_rows),
        ),
        validation_row(
            "Cauchy_coefficients_are_angular_and_radius_stable",
            cauchy_passes,
            maximum_contour_spread,
        ),
        validation_row(
            "Cauchy_energy_residues_match_source_C0",
            c0_passes,
            maximum_c0_difference,
        ),
        validation_row(
            "interval_H3_and_downstream_claims_remain_false",
            all(value is False for value in open_claims().values()),
            open_claims(),
        ),
        validation_row(
            "formal_workbench_remains_unchanged",
            M5378.M5359.M5342.M5283.formal_inventory_digest()
            == M5378.M5359.M5342.FORMAL_DIGEST,
            M5378.M5359.M5342.M5283.formal_inventory_digest(),
        ),
        validation_row(
            "scripts_cache_remains_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    for row in sequence_rows + event_rows:
        row[CLAIM_CAUCHY] = cauchy_passes
        row[CLAIM_C0] = c0_passes
    registered_sources = source_rows()
    for row in registered_sources:
        row[CLAIM_CAUCHY] = cauchy_passes
        row[CLAIM_C0] = c0_passes
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "decision": (
            "D4_CAUCHY_DOUBLE_POLE_COEFFICIENT_AND_ENERGY_RESIDUE_CROSSCHECK_CERTIFIED__INTERVALIZE_COEFFICIENT"
            if passed
            else "D4_CAUCHY_DOUBLE_POLE_COEFFICIENT_EXTRACTION_BLOCKED"
        ),
        "event_count": len(event_rows),
        "sequence_row_count": len(sequence_rows),
        "maximum_contour_relative_spread": maximum_contour_spread,
        "maximum_Cauchy_vs_displacement_relative_difference": maximum_displacement_difference,
        "maximum_Cauchy_C0_relative_difference": maximum_c0_difference,
        "claim_boundary": {
            CLAIM_CAUCHY: cauchy_passes,
            CLAIM_C0: c0_passes,
            **open_claims(),
        },
        "remaining_obstruction": "convert the phase-complete Cauchy extraction into an interval contour enclosure on the certified complex event strip, then bound endpoint H derivatives",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_Cauchy_double_pole_energy_sequence.csv", sequence_rows)
    atomic_csv(output / "D4_Cauchy_double_pole_event_summary.csv", event_rows)
    atomic_csv(output / "D4_Cauchy_double_pole_validation.csv", validations)
    atomic_csv(output / "source_register.csv", registered_sources)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_Cauchy_double_pole_result.json", result)
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
    mp.mp.dps = 60
    center = mp.mpc("1.2", "-0.3")
    coefficient = mp.mpc("2.5", "0.75")
    radius = mp.mpf("0.01")
    point_count = 48
    recovered = mp.mpc(0)
    for index in range(point_count):
        phase = 2 * mp.pi * index / point_count
        displacement = radius * mp.exp(1j * phase)
        value = coefficient / displacement**2 + 3 / displacement + 4 + displacement
        recovered += value * displacement**2
    recovered /= point_count
    checks = {
        "Cauchy_projection_recovers_double_pole_coefficient": abs(
            recovered - coefficient
        )
        <= mp.mpf("1e-50"),
        "relative_difference_is_zero_for_equal_values": relative_difference(
            coefficient, coefficient
        )
        == 0,
        "center_is_finite": math.isfinite(float(abs(center))),
    }
    return {"checks": checks, "all_pass": all(checks.values())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    if arguments.self_test:
        result = self_test()
    elif arguments.dry_run:
        result = preflight()
    else:
        result = run(arguments.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("all_pass", result.get("validation_passed", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
