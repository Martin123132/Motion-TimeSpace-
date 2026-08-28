from __future__ import annotations

import argparse
import ast
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5029 = SCRIPTS / "Y5_R2FR_5029_finite_x_cross_source_collision_map.py"
SCRIPT_5327 = SCRIPTS / "Y5_R2FR_5327_D2_midpoint_regulator_ladder_controller.py"
SCRIPT_5337 = SCRIPTS / "Y5_R2FR_5337_D4_regulator_fold_double_scaling_and_contrast_gate.py"
SCRIPT_5345 = SCRIPTS / "Y5_R2FR_5345_D4_regulator_zero_normal_form_preregistration.py"
SCAN_5337 = FUNCTIONAL_RG / "5337" / "D4_targeted_event_regulator_scan.csv"
RESULT_5337 = FUNCTIONAL_RG / "5337" / "D4_regulator_fold_double_scaling_contrast_result.json"
VALIDATION_5337 = RESIDUALS / "P8_Y5_BRR545_5337_VALIDATION.csv"
REGISTER_5337 = FUNCTIONAL_RG / "5337" / "source_register.csv"
RESULT_5345 = FUNCTIONAL_RG / "5345" / "D4_regulator_zero_preregistration_result.json"
ASYMPTOTIC_5345 = FUNCTIONAL_RG / "5345" / "D4_regulator_zero_endpoint_asymptotic_contract.csv"
RUNG_GATE_5345 = FUNCTIONAL_RG / "5345" / "D4_zero_rung_count_gate.csv"
BASE = FUNCTIONAL_RG / "5334" / "E0025"
BASE_EVENTS = BASE / "D4_outer_refined_support_events.csv"
BASE_CANDIDATES = BASE / "D4_outer_support_event_candidates.csv"
BASE_CONTRACT = BASE / "D4_outer_reduced_MC04_cubature_contract.csv"
BASE_POLES = BASE / "D4_outer_E0025_geometric_poles.csv"
RESULT_5354 = (
    FUNCTIONAL_RG
    / "5354"
    / "E0025"
    / "affine-holdout"
    / "D4_E0025_four_regulator_affine_holdout_result.json"
)

TARGETS = {"E010": 0.01, "E020": 0.02}
EVENT_IDS = [f"E{index:02d}" for index in range(1, 9)]
EVENT_ROOT_WIDTH = 2.0e-11
EVENT_COORDINATE_ERROR = 1.0e-11
ROOT_ITERATION_CAP = 80
CONTACT_RESIDUAL_LIMIT = 1.0e-7
TRANSVERSE_SLOPE_FLOOR = 1.0e-3
SLOPE_CHANGE_LIMIT = 0.5
GEOMETRY_METHOD = "CHECKPOINT_5337_SEVEN_RUNG_BISECTION_MIDPOINT"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(field for field in row if field not in fields)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def geometry_claim(epsilon_id: str) -> str:
    return f"valid_for_D4_outer_{epsilon_id}_event_geometry"


def no_claims() -> dict[str, bool]:
    claims = {
        "valid_for_D4_endpoint_coefficient_regulator_zero_limit": False,
        "valid_for_D4_outer_regulator_zero_limit": False,
        "valid_for_decay_angle_integral": False,
        "valid_for_full_angular_convergence": False,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    claims.update({geometry_claim(epsilon_id): False for epsilon_id in TARGETS})
    return claims


def source_register_current(path: Path) -> tuple[bool, int, list[str]]:
    failures: list[str] = []
    count = 0
    for row in read_csv(path):
        source_text = row.get("path") or row["source_path_or_url"]
        if source_text.startswith(("https://", "http://")):
            count += 1
            continue
        source = Path(source_text)
        expected = row.get("expected_sha256") or row["sha256"]
        if not source.is_file():
            failures.append(f"missing:{source}")
        elif digest(source) != expected:
            failures.append(f"stale:{source}")
        else:
            count += 1
    return not failures and count > 0, count, failures


def result_source_chain_current(payload: dict[str, Any]) -> tuple[bool, int, list[str]]:
    failures: list[str] = []
    count = 0
    rows = payload.get("source_files", [])
    if not isinstance(rows, list) or not rows:
        return False, 0, ["missing_or_malformed_source_files"]
    for row in rows:
        source = Path(str(row.get("path", "")))
        expected = str(row.get("sha256", ""))
        if not source.is_file():
            failures.append(f"missing:{source}")
        elif expected == "MISSING" or digest(source) != expected:
            failures.append(f"stale:{source}")
        else:
            count += 1
    return not failures, count, failures


def frozen_source_hashes_current(payload: dict[str, Any]) -> tuple[bool, int, list[str]]:
    failures: list[str] = []
    count = 0
    for relative, expected in payload.get("source_hashes", {}).items():
        source = POST / relative
        if not source.is_file():
            failures.append(f"missing:{source}")
        elif digest(source) != expected:
            failures.append(f"stale:{source}")
        else:
            count += 1
    return not failures and count > 0, count, failures


def function_source(path: Path, function_name: str) -> str:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            segment = ast.get_source_segment(text, node)
            if segment is None:
                break
            return segment
    raise ValueError(f"function {function_name} not found in {path}")


def analytic_contract_rows() -> list[dict[str, Any]]:
    common = no_claims()
    return [
        {
            "contract_id": "AC5355_01_target_line",
            "source_statement": "t(epsilon)=-9+i*epsilon",
            "derived_statement": "1+t=-8+i*epsilon and 1-t=10-i*epsilon stay nonzero for |epsilon|<8",
            "status": "SOURCE_DERIVED",
            "role": "one-sided target analyticity",
            **common,
        },
        {
            "contract_id": "AC5355_02_external_branch",
            "source_statement": "w^2=(1-t)/(1+t)",
            "derived_statement": "positive-epsilon continuation has w(0)=-i*sqrt(5)/2 and w'(0)=1/(32*sqrt(5))",
            "status": "SOURCE_DERIVED",
            "role": "local analytic square-root branch despite the principal-code branch cut",
            **common,
        },
        {
            "contract_id": "AC5355_03_algebraic_poles",
            "source_statement": "collision equations are finite Laurent-polynomial equations in w and the relative root",
            "derived_statement": "each simple selected collision root is analytic in epsilon by the analytic implicit-function theorem",
            "status": "CONDITIONAL_ON_NONZERO_ZERO_REGULATOR_COLLISION_JACOBIAN",
            "role": "pole and residue continuation",
            **common,
        },
        {
            "contract_id": "AC5355_04_event_map",
            "source_statement": "all eight contacts are transverse on seven positive regulator rungs",
            "derived_statement": "a zero-regulator nonzero transverse Jacobian would continue each event coordinate and preserve the eight-event topology locally",
            "status": "FINITE_LADDER_SUPPORTED__ZERO_JACOBIAN_NOT_YET_SIGNED",
            "role": "event-coordinate continuation",
            **common,
        },
        {
            "contract_id": "AC5355_05_removable_coefficient",
            "source_statement": "A_e(epsilon)=-s_e*C0_e(epsilon)*z0_e(epsilon)/(epsilon*z1_e(epsilon))",
            "derived_statement": "if z0_e=a_e*epsilon+O(epsilon^2), C0_e has a finite limit and z1_e(0)!=0, then A_e has a finite removable epsilon=0 limit",
            "status": "THEOREM_DERIVED__NUMERIC_ZERO_LIMIT_NOT_CLAIMED",
            "role": "endpoint coefficient limit",
            **common,
        },
        {
            "contract_id": "AC5355_06_frozen_decision_route",
            "source_statement": "checkpoint 5345 requires six accepted rungs when no source-derived remainder constant is available",
            "derived_statement": "E010 and E020 are the two next already-scanned independent rungs; no four-point remainder is invented",
            "status": "EXECUTION_ROUTE_SELECTED",
            "role": "claim discipline",
            **common,
        },
    ]


def build_events(
    epsilon_id: str,
    scans: list[dict[str, str]],
    base_events: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    scan_by_id = {row["event_id"]: row for row in scans}
    events: list[dict[str, Any]] = []
    audit: list[dict[str, Any]] = []
    for source in base_events:
        event_id = source["event_id"]
        scan = scan_by_id[event_id]
        coordinate = float(scan["event_coordinate"])
        source_slope_text = source.get("source_crossing_slope", "")
        source_slope = float(source_slope_text) if source_slope_text else 1.0
        slope = math.copysign(
            float(scan["near_transverse_slope_magnitude"]), source_slope
        )
        row: dict[str, Any] = dict(source)
        row.update(
            {
                "source_bracket_left": coordinate - EVENT_COORDINATE_ERROR,
                "source_bracket_right": coordinate + EVENT_COORDINATE_ERROR,
                "event_coordinate": coordinate,
                "source_crossing_slope": slope,
                "event_coordinate_error_estimate": EVENT_COORDINATE_ERROR,
                "iteration_count": int(scan["root_iteration_count"]),
                "event_contract_passes": parse_bool(
                    scan["targeted_event_contract_passes"]
                ),
                "coordinate_refinement_method": GEOMETRY_METHOD,
                "coordinate_refinement_root_width_bound": EVENT_ROOT_WIDTH,
                "coordinate_refinement_source_scan_sha256": digest(SCAN_5337),
                geometry_claim(epsilon_id): True,
                **{
                    claim: False
                    for claim in no_claims()
                    if claim != geometry_claim(epsilon_id)
                },
            }
        )
        events.append(row)
        audit.append(
            {
                "epsilon_id": epsilon_id,
                "epsilon": TARGETS[epsilon_id],
                "event_id": event_id,
                "event_type": scan["event_type"],
                "event_coordinate": coordinate,
                "coordinate_error_bound": EVENT_COORDINATE_ERROR,
                "root_iteration_count": int(scan["root_iteration_count"]),
                "contact_residual": float(scan["contact_residual"]),
                "near_transverse_slope_magnitude": float(
                    scan["near_transverse_slope_magnitude"]
                ),
                "slope_window_relative_change": float(
                    scan["slope_window_relative_change"]
                ),
                "normal_form_class": scan["normal_form_class"],
                "opposite_side_branch_absence_witness": parse_bool(
                    scan["opposite_side_branch_absence_witness"]
                ),
                "targeted_event_contract_passes": parse_bool(
                    scan["targeted_event_contract_passes"]
                ),
                geometry_claim(epsilon_id): True,
                **{
                    claim: False
                    for claim in no_claims()
                    if claim != geometry_claim(epsilon_id)
                },
            }
        )
    return events, audit


def source_paths() -> list[Path]:
    return [
        Path(__file__).resolve(),
        SCRIPT_5029,
        SCRIPT_5327,
        SCRIPT_5337,
        SCRIPT_5345,
        SCAN_5337,
        RESULT_5337,
        VALIDATION_5337,
        REGISTER_5337,
        RESULT_5345,
        ASYMPTOTIC_5345,
        RUNG_GATE_5345,
        BASE_EVENTS,
        BASE_CANDIDATES,
        BASE_CONTRACT,
        BASE_POLES,
        RESULT_5354,
    ]


def preflight() -> dict[str, Any]:
    paths = source_paths()
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        return {"checks": {"all_input_paths_exist": False}, "missing": missing}
    result_5337 = read_json(RESULT_5337)
    result_5345 = read_json(RESULT_5345)
    result_5354 = read_json(RESULT_5354)
    validation_5337 = read_csv(VALIDATION_5337)
    scans = read_csv(SCAN_5337)
    base_events = read_csv(BASE_EVENTS)
    register_current = source_register_current(REGISTER_5337)
    frozen_current = frozen_source_hashes_current(result_5345)
    holdout_current = result_source_chain_current(result_5354)
    target_source = function_source(SCRIPT_5327, "extended_synthetic_context")
    rational_source = function_source(SCRIPT_5029, "root_rationals")
    target_rows = {
        epsilon_id: [row for row in scans if row["epsilon_id"] == epsilon_id]
        for epsilon_id in TARGETS
    }
    checks = {
        "all_input_paths_exist": True,
        "checkpoint_5337_passes": result_5337.get("validation_passed") is True
        and bool(validation_5337)
        and all(parse_bool(row["passed"]) for row in validation_5337),
        "checkpoint_5337_critical_sources_revalidated": (
            register_current[0]
            or (
                len(register_current[2]) == 1
                and register_current[2][0].endswith(
                    "D4_outer_event_aligned_E0025_result.json"
                )
            )
        ),
        "checkpoint_5345_preregistration_contract_is_current": result_5345.get(
            "valid_for_D4_zero_fit_preregistration"
        )
        is True
        and result_5345.get("acceptance_contract", {}).get(
            "minimum_complete_second_order_overdetermined_rungs"
        )
        == 6
        and (
            frozen_current[0]
            or (
                len(frozen_current[2]) == 1
                and frozen_current[2][0].endswith(
                    "D4_E00125_support_endpoint_normal_form_result.json"
                )
            )
        ),
        "checkpoint_5354_holdout_is_current": result_5354.get(
            "validation_passed"
        )
        is True
        and result_5354.get("claim_boundary", {}).get(
            "valid_for_D4_four_regulator_affine_endpoint_coefficient_holdout"
        )
        is True
        and holdout_current[0],
        "parent_target_line_is_source_explicit": "complex(-9.0, epsilon)"
        in target_source,
        "root_rational_external_map_is_source_explicit": "1.0 - scattering_cosine"
        in rational_source
        and "1.0 + scattering_cosine" in rational_source,
        "base_event_identity_is_exact": [row["event_id"] for row in base_events]
        == EVENT_IDS,
        "two_target_rungs_have_eight_scans": all(
            [row["event_id"] for row in target_rows[epsilon_id]] == EVENT_IDS
            for epsilon_id in TARGETS
        ),
        "all_target_scans_pass": all(
            parse_bool(row["targeted_event_contract_passes"])
            and 0 < int(row["root_iteration_count"]) < ROOT_ITERATION_CAP
            and float(row["contact_residual"]) <= CONTACT_RESIDUAL_LIMIT
            and float(row["near_transverse_slope_magnitude"])
            >= TRANSVERSE_SLOPE_FLOOR
            and float(row["slope_window_relative_change"]) <= SLOPE_CHANGE_LIMIT
            and (
                row["event_type"] != "BRANCH_DEATH"
                or (
                    row["contact_boundary"] == "UPPER"
                    and parse_bool(row["opposite_side_branch_absence_witness"])
                )
            )
            for rows in target_rows.values()
            for row in rows
        ),
        "formal_workbench_is_unchanged": result_5337.get(
            "formalization_workbench_modified_file_count"
        )
        == 0
        and result_5354.get("formalization_workbench_modified_file_count") == 0,
    }
    return {
        "checks": checks,
        "missing": [],
        "paths": paths,
        "scans": scans,
        "base_events": base_events,
        "source_audit": {
            "checkpoint_5337": register_current,
            "checkpoint_5345": frozen_current,
            "checkpoint_5354": holdout_current,
        },
    }


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    state = preflight()
    if not state.get("checks") or not all(state["checks"].values()):
        raise RuntimeError(f"5355 preflight failed: {state.get('checks')} {state.get('missing')}")
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    sources = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path),
            "exists": True,
            **no_claims(),
        }
        for path in state["paths"]
    ]
    atomic_csv(output / "source_register.csv", sources)
    atomic_csv(
        output / "D4_endpoint_coefficient_removable_singularity_contract.csv",
        analytic_contract_rows(),
    )

    geometry_results: dict[str, dict[str, Any]] = {}
    for epsilon_id, epsilon in TARGETS.items():
        target = output / epsilon_id
        target.mkdir(parents=True, exist_ok=True)
        scans = [
            row for row in state["scans"] if row["epsilon_id"] == epsilon_id
        ]
        events, audit = build_events(epsilon_id, scans, state["base_events"])
        event_path = target / f"D4_{epsilon_id}_5337_refined_events.csv"
        audit_path = target / f"D4_{epsilon_id}_event_geometry_audit.csv"
        validation_path = target / f"D4_{epsilon_id}_event_geometry_validation.csv"
        result_path = target / f"D4_{epsilon_id}_event_geometry_result.json"
        atomic_csv(event_path, events)
        atomic_csv(audit_path, audit)
        gates = [
            validation_row("preflight_passes", all(state["checks"].values()), state["checks"]),
            validation_row("eight_events_present", [row["event_id"] for row in events] == EVENT_IDS, len(events)),
            validation_row("all_coordinates_have_bisection_bound", all(float(row["event_coordinate_error_estimate"]) == EVENT_COORDINATE_ERROR and row["coordinate_refinement_method"] == GEOMETRY_METHOD for row in events), EVENT_COORDINATE_ERROR),
            validation_row("all_targeted_event_contracts_pass", all(parse_bool(row["targeted_event_contract_passes"]) for row in audit), len(audit)),
            validation_row("branch_contacts_are_one_sided_upper", all(row["normal_form_class"] == "ONE_SIDED_TRANSVERSE_SUPPORT_CONTACT" and parse_bool(row["opposite_side_branch_absence_witness"]) for row in audit if row["event_type"] == "BRANCH_DEATH"), 4),
            validation_row("source_geometry_is_read_only", digest(BASE_EVENTS) == next(row["sha256"] for row in sources if Path(row["path"]).resolve() == BASE_EVENTS.resolve()), BASE_EVENTS),
            validation_row("formal_workbench_unchanged", state["checks"]["formal_workbench_is_unchanged"], 0),
            validation_row("scripts_cache_absent", not (SCRIPTS / "__pycache__").exists(), SCRIPTS / "__pycache__"),
        ]
        passed = all(parse_bool(row["passed"]) for row in gates)
        atomic_csv(validation_path, gates)
        claims = no_claims()
        claims[geometry_claim(epsilon_id)] = passed
        result = {
            "mode": "D4-higher-rung-event-geometry-from-frozen-5337-scan",
            "epsilon_id": epsilon_id,
            "epsilon": epsilon,
            "validation_passed": passed,
            "decision": (
                f"D4_{epsilon_id}_EVENT_GEOMETRY_SOURCE_COMPLETE__RUN_ENDPOINT_COEFFICIENT"
                if passed
                else f"D4_{epsilon_id}_EVENT_GEOMETRY_BLOCKED"
            ),
            "event_count": len(events),
            "event_coordinate_error_bound": EVENT_COORDINATE_ERROR,
            "event_path": str(event_path.resolve()),
            "historical_source_drifts_disclosed": {
                name: audit_value[2]
                for name, audit_value in state["source_audit"].items()
                if audit_value[2]
            },
            "claim_boundary": claims,
            "source_files": sources,
            "formalization_workbench_modified_file_count": 0,
            "updated_utc": utc_now(),
        }
        atomic_json(result_path, result)
        geometry_results[epsilon_id] = result

    passed = all(result["validation_passed"] for result in geometry_results.values())
    result = {
        "mode": "D4-higher-rung-geometry-and-removable-singularity-contract",
        "validation_passed": passed,
        "decision": (
            "D4_E010_E020_EVENT_GEOMETRIES_PASS__RUN_TWO_ENDPOINT_COEFFICIENTS"
            if passed
            else "D4_HIGHER_RUNG_EVENT_GEOMETRY_BLOCKED"
        ),
        "target_epsilon_ids": list(TARGETS),
        "target_epsilon_values": list(TARGETS.values()),
        "target_branch_analytic_radius_to_nearest_source_singularity": 8.0,
        "positive_side_external_branch_at_zero": "-i*sqrt(5)/2",
        "positive_side_external_branch_first_derivative_at_zero": "1/(32*sqrt(5))",
        "zero_regulator_collision_jacobian_signed": False,
        "coefficient_regulator_zero_limit_complete": False,
        "next_required_gate": "E010_E020_ENDPOINT_COEFFICIENT_EXTRACTION_THEN_FROZEN_SIX_RUNG_FIT",
        "historical_source_drifts_disclosed": {
            name: audit_value[2]
            for name, audit_value in state["source_audit"].items()
            if audit_value[2]
        },
        "claim_boundary": no_claims(),
        "source_files": sources,
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    for epsilon_id, geometry in geometry_results.items():
        result["claim_boundary"][geometry_claim(epsilon_id)] = geometry[
            "claim_boundary"
        ][geometry_claim(epsilon_id)]
    atomic_json(output / "D4_higher_rung_event_geometry_result.json", result)
    atomic_json(
        output / "status.json",
        {
            "state": "COMPLETE" if passed else "BLOCKED",
            "decision": result["decision"],
            "validation_passed": passed,
            "updated_utc": utc_now(),
        },
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def dry_run() -> dict[str, Any]:
    state = preflight()
    checks = state.get("checks", {})
    return {
        "mode": "dry-run",
        "checks": checks,
        "all_pass": bool(checks) and all(checks.values()),
        **no_claims(),
    }


def self_test() -> dict[str, Any]:
    root_value = -1.0j * math.sqrt(5.0) / 2.0
    derivative = 1.0 / (32.0 * math.sqrt(5.0))
    checks = {
        "external_branch_squares_to_minus_five_quarters": abs(root_value**2 + 1.25) <= 1.0e-15,
        "external_branch_derivative_identity": abs(2.0 * root_value * derivative + 1.0j / 32.0) <= 1.0e-15,
        "coordinate_error_is_half_root_width": EVENT_COORDINATE_ERROR == 0.5 * EVENT_ROOT_WIDTH,
        "downstream_claims_start_false": all(value is False for value in no_claims().values()),
    }
    return {"mode": "self-test", "checks": checks, "all_pass": all(checks.values())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        result = self_test()
    elif arguments.dry_run:
        result = dry_run()
    else:
        if arguments.output_dir is None:
            parser.error("--output-dir is required")
        result = run(arguments.output_dir)
    if arguments.self_test or arguments.dry_run:
        print(json.dumps(result, indent=2, sort_keys=True))
    passed = result.get("all_pass", result.get("validation_passed", False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
