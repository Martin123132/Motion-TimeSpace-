from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
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
OUTPUT = FUNCTIONAL_RG / "5383"
DOCUMENT = POST / "5383-Y5-R2FR-D4-double-Cauchy-parent-C0-residue.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5383_VALIDATION.csv"

SCRIPT_5382 = SCRIPTS / "Y5_R2FR_5382_D4_cauchy_double_pole_coefficient_extraction.py"
RESULT_5382 = FUNCTIONAL_RG / "5382" / "D4_Cauchy_double_pole_result.json"
VALIDATION_5382 = FUNCTIONAL_RG / "5382" / "D4_Cauchy_double_pole_validation.csv"
SUMMARY_5382 = FUNCTIONAL_RG / "5382" / "D4_Cauchy_double_pole_event_summary.csv"
EVENTS_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
ENDPOINTS_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_coefficients.csv"

CHECKPOINT = 5383
MARKER = "MTS_5383_D4_DOUBLE_CAUCHY_PARENT_C0_RESIDUE"
REVISION = "D4-double-Cauchy-parent-C0-residue-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
MP_DIGITS = 110
ENERGY_PRIMARY_RELATIVE_RADIUS = "1e-6"
ENERGY_SECONDARY_RELATIVE_RADIUS = "5e-7"
ENERGY_PRIMARY_POINTS = 16
ENERGY_ANGULAR_CROSSCHECK_POINTS = 24
GLOBAL_CONTOUR_RELATIVE_RADIUS = "1e-7"
GLOBAL_CONTOUR_POINTS = 24
DOUBLE_CAUCHY_RELATIVE_STABILITY_LIMIT = 2.0e-9
C0_RELATIVE_AGREEMENT_LIMIT = 2.0e-8

CLAIM_DOUBLE_CAUCHY = "valid_for_D4_numerical_double_Cauchy_parent_C0_residue"
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


M5382 = load_module("mts_5382_for_5383", SCRIPT_5382)
M5378 = M5382.M5378
mp = M5382.mp


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
        SCRIPT_5382,
        RESULT_5382,
        VALIDATION_5382,
        SUMMARY_5382,
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
            CLAIM_DOUBLE_CAUCHY: False,
            **open_claims(),
        }
        for path in source_paths()
    ]


def preflight() -> dict[str, Any]:
    paths = source_paths()
    result_5382 = read_json(RESULT_5382)
    checks = {
        "all_direct_sources_exist": all(path.is_file() for path in paths),
        "checkpoint_5382_passes": result_5382.get("validation_passed") is True
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5382)),
        "Cauchy_global_pole_extraction_is_claimed": result_5382.get(
            "claim_boundary", {}
        ).get("valid_for_D4_numerical_Cauchy_double_pole_coefficient_extraction")
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


def energy_integrand(
    configuration: dict[str, Any],
    energy: Any,
    epsilon: Any,
    component: dict[str, Any],
) -> Any:
    geometry = M5382.collision_geometry(configuration, energy, epsilon)
    geometry["energy"] = energy
    double_pole_coefficient = M5382.contour_coefficient(
        geometry,
        mp.mpf(GLOBAL_CONTOUR_RELATIVE_RADIUS),
        GLOBAL_CONTOUR_POINTS,
    )
    winding = M5378.M5359.M5342.M5312.M5280.M5277.source_winding_delta(
        component, configuration["role"]
    )
    return (
        winding
        * configuration["trace_orientation"]
        * double_pole_coefficient
        / (
            geometry["relative_root"]
            * geometry["selected_global_root"]
            * geometry["collision_jacobian"]
        )
    )


def energy_contour_residue(
    configuration: dict[str, Any],
    epsilon: Any,
    component: dict[str, Any],
    physical_multiplier: Any,
    relative_radius: Any,
    point_count: int,
) -> Any:
    pole_energy = configuration["energy"]
    radius = relative_radius * max(mp.mpf(1), abs(pole_energy))
    total = mp.mpc(0)
    for index in range(point_count):
        phase = 2 * mp.pi * index / point_count
        displacement = radius * mp.exp(1j * phase)
        total += energy_integrand(
            configuration,
            pole_energy + displacement,
            epsilon,
            component,
        ) * displacement
    return physical_multiplier * total / point_count


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5383 — Y5/R2FR D4 double-Cauchy parent C0 residue",
        "",
        "## Result",
        "",
        f"Decision: `{result['decision']}`.",
        "",
        "The global double pole and parent energy pole are now projected by nested Cauchy integrals. The resulting `C0` requires neither a tiny one-phase global displacement nor a one-sided polynomial energy extrapolation.",
        "",
        f"- maximum energy-contour angular/radius spread: `{result['maximum_energy_contour_relative_spread']}`;",
        f"- maximum double-Cauchy versus checkpoint-5359 C0 difference: `{result['maximum_source_C0_relative_difference']}`;",
        f"- maximum double-Cauchy versus checkpoint-5382 C0 difference: `{result['maximum_5382_C0_relative_difference']}`.",
        "",
        "## Scope",
        "",
        "This closes an independent high-precision numerical residue construction. It is not an interval contour theorem over the common complex regulator strip, so endpoint C, H3, the uniform remainder, D4 outer limit, and broader claims remain open.",
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
    summary_5382 = {row["event_id"]: row for row in read_csv(SUMMARY_5382)}
    rows: list[dict[str, Any]] = []
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
            primary = energy_contour_residue(
                configuration,
                mp.mpf(0),
                component,
                physical_multiplier,
                mp.mpf(ENERGY_PRIMARY_RELATIVE_RADIUS),
                ENERGY_PRIMARY_POINTS,
            )
            angular_crosscheck = energy_contour_residue(
                configuration,
                mp.mpf(0),
                component,
                physical_multiplier,
                mp.mpf(ENERGY_PRIMARY_RELATIVE_RADIUS),
                ENERGY_ANGULAR_CROSSCHECK_POINTS,
            )
            radius_crosscheck = energy_contour_residue(
                configuration,
                mp.mpf(0),
                component,
                physical_multiplier,
                mp.mpf(ENERGY_SECONDARY_RELATIVE_RADIUS),
                ENERGY_PRIMARY_POINTS,
            )
            contour_spread = max(
                relative_difference(primary, angular_crosscheck),
                relative_difference(primary, radius_crosscheck),
                relative_difference(angular_crosscheck, radius_crosscheck),
            )
            source_c0 = complex_from_row(source_endpoint, "C0_zero")
            c0_5382 = complex_from_row(summary_5382[configuration["event_id"]], "Cauchy_C0")
            rows.append(
                {
                    "event_id": configuration["event_id"],
                    "event_type": configuration["event_type"],
                    "energy_primary_relative_radius": ENERGY_PRIMARY_RELATIVE_RADIUS,
                    "energy_secondary_relative_radius": ENERGY_SECONDARY_RELATIVE_RADIUS,
                    "energy_primary_points": ENERGY_PRIMARY_POINTS,
                    "energy_angular_crosscheck_points": ENERGY_ANGULAR_CROSSCHECK_POINTS,
                    "global_contour_relative_radius": GLOBAL_CONTOUR_RELATIVE_RADIUS,
                    "global_contour_points": GLOBAL_CONTOUR_POINTS,
                    **complex_fields("double_Cauchy_C0", primary),
                    **complex_fields("energy_angular_crosscheck_C0", angular_crosscheck),
                    **complex_fields("energy_radius_crosscheck_C0", radius_crosscheck),
                    **complex_fields("source_5359_C0", source_c0),
                    **complex_fields("source_5382_C0", c0_5382),
                    "energy_contour_relative_spread": contour_spread,
                    "source_5359_C0_relative_difference": relative_difference(
                        primary, source_c0
                    ),
                    "source_5382_C0_relative_difference": relative_difference(
                        primary, c0_5382
                    ),
                    CLAIM_DOUBLE_CAUCHY: False,
                    **open_claims(),
                }
            )
            print(
                f"completed {configuration['event_id']} contour_spread={contour_spread:.3e}",
                flush=True,
            )
    finally:
        M5378.M5359.M5342.M5326.restore_kernel(old_kernel)
    maximum_spread = max(
        float(row["energy_contour_relative_spread"]) for row in rows
    )
    maximum_source_difference = max(
        float(row["source_5359_C0_relative_difference"]) for row in rows
    )
    maximum_5382_difference = max(
        float(row["source_5382_C0_relative_difference"]) for row in rows
    )
    double_cauchy_passes = (
        maximum_spread <= DOUBLE_CAUCHY_RELATIVE_STABILITY_LIMIT
        and maximum_source_difference <= C0_RELATIVE_AGREEMENT_LIMIT
        and maximum_5382_difference <= C0_RELATIVE_AGREEMENT_LIMIT
    )
    validations = [
        validation_row(
            "preflight_passes", preflight_result["all_pass"], preflight_result["checks"]
        ),
        validation_row(
            "all_eight_double_Cauchy_residues_are_present",
            len(rows) == len(EVENT_IDS),
            len(rows),
        ),
        validation_row(
            "energy_contours_are_angular_and_radius_stable",
            maximum_spread <= DOUBLE_CAUCHY_RELATIVE_STABILITY_LIMIT,
            maximum_spread,
        ),
        validation_row(
            "double_Cauchy_residues_match_checkpoint_5359",
            maximum_source_difference <= C0_RELATIVE_AGREEMENT_LIMIT,
            maximum_source_difference,
        ),
        validation_row(
            "double_Cauchy_residues_match_checkpoint_5382",
            maximum_5382_difference <= C0_RELATIVE_AGREEMENT_LIMIT,
            maximum_5382_difference,
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
    for row in rows:
        row[CLAIM_DOUBLE_CAUCHY] = double_cauchy_passes
    registered_sources = source_rows()
    for row in registered_sources:
        row[CLAIM_DOUBLE_CAUCHY] = double_cauchy_passes
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "decision": (
            "D4_DOUBLE_CAUCHY_PARENT_C0_RESIDUE_CERTIFIED__INTERVALIZE_NESTED_CONTOURS"
            if passed
            else "D4_DOUBLE_CAUCHY_PARENT_C0_RESIDUE_BLOCKED"
        ),
        "event_count": len(rows),
        "maximum_energy_contour_relative_spread": maximum_spread,
        "maximum_source_C0_relative_difference": maximum_source_difference,
        "maximum_5382_C0_relative_difference": maximum_5382_difference,
        "claim_boundary": {CLAIM_DOUBLE_CAUCHY: double_cauchy_passes, **open_claims()},
        "remaining_obstruction": "interval-enclose the nested global/energy contour integrand on the certified complex regulator boxes, then apply Cauchy derivative bounds to H",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_double_Cauchy_parent_C0_events.csv", rows)
    atomic_csv(output / "D4_double_Cauchy_parent_C0_validation.csv", validations)
    atomic_csv(output / "source_register.csv", registered_sources)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_double_Cauchy_parent_C0_result.json", result)
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
    first_residue = mp.mpc("2.5", "0.75")
    second_residue = mp.mpc("-1.2", "0.4")
    radius_first = mp.mpf("0.01")
    radius_second = mp.mpf("0.02")
    point_count = 24
    recovered = mp.mpc(0)
    for first_index in range(point_count):
        first_phase = 2 * mp.pi * first_index / point_count
        first_displacement = radius_first * mp.exp(1j * first_phase)
        inner = mp.mpc(0)
        for second_index in range(point_count):
            second_phase = 2 * mp.pi * second_index / point_count
            second_displacement = radius_second * mp.exp(1j * second_phase)
            value = (
                first_residue
                * second_residue
                / first_displacement
                / second_displacement**2
            )
            inner += value * second_displacement**2
        recovered += inner / point_count * first_displacement
    recovered /= point_count
    checks = {
        "nested_Cauchy_projection_recovers_product_residue": abs(
            recovered - first_residue * second_residue
        )
        <= mp.mpf("1e-50"),
        "relative_difference_is_zero_for_equal_values": relative_difference(
            recovered, recovered
        )
        == 0,
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
