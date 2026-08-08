from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4968"
RESIDUAL = POST / "source-intake" / "mts_residuals"
OUTPUT = RESIDUAL / "P8_Y5_BRR545_4968_VALIDATION.csv"
MARKER = "MTS_4968_CFF_P8_COMPLETED_VALIDATION"
CHECKPOINT_MARKER = "PPC4161_CFF_P8_HELICITY_TRAJECTORY_BOUND_4968"
CHECKED_DATE = "2026-07-13"
AMPLITUDE_SCRIPT = POST / "scripts" / "Y5_R2FR_4968_CFF_p8_helicity_source.py"
TRAJECTORY_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_4968_CFF_p8_trajectory_and_static_bound.py"
)
VALIDATION_SCRIPT = POST / "scripts" / "Y5_R2FR_4968_CFF_p8_completed_validation.py"
AMPLITUDE_JSON = SOURCE / "CFF_squared_p8_helicity_source_results.json"
TRAJECTORY_JSON = SOURCE / "p8_CFF_completed_trajectory_and_static_bound_results.json"
AMPLITUDE_CSV = SOURCE / "CFF_tree_helicity_amplitudes.csv"
PROJECTION_CSV = SOURCE / "CFF_squared_p8_partial_wave_projection.csv"
FIXED_CSV = SOURCE / "p8_CFF_completed_fixed_point.csv"
TRAJECTORY_CSV = SOURCE / "p8_CFF_completed_GR_connected_trajectory.csv"
CONVERGENCE_CSV = SOURCE / "p8_CFF_completed_IR_endpoint_convergence.csv"
STATIC_CSV = SOURCE / "p8_CFF_completed_static_compact_response.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = (
    POST
    / "4968-Y5-R2FR-CFF-squared-four-graviton-p8-helicity-source-GR-trajectory-and-static-bound-or-three-loop-Einstein-residual.md"
)
FORMAL_NOTE = FORMAL / "984-PPC4161-CFF-p8-helicity-source-and-completed-trajectory.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
VARIABLES = FORMAL / "04-variable-audit.csv"
CLAIMS = FORMAL / "02-claims-register.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION = FORMAL / "07-unification-spine.md"
EXPECTED_HASHES = {
    AMPLITUDE_JSON: "ce728a854ffb92fbdb3ffeb16727357a6c69433fb4e6edc1a66bd1b952f2a19d",
    TRAJECTORY_JSON: "495e12c4441cda77776b8c39cf1aa7d5b9252b3cec4bf1e8d742ce212668d964",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, Any]]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "check_id",
        "requirement",
        "observed",
        "detail",
        "passed",
        "checkpoint_marker",
        "valid_for_full_MTS_claim",
        "source_checked_date",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def validation_row(
    index: int,
    requirement: str,
    observed: str,
    detail: object,
    passed: bool,
) -> dict[str, Any]:
    return {
        "check_id": f"VAL4968_{index:02d}",
        "requirement": requirement,
        "observed": observed,
        "detail": json.dumps(detail, sort_keys=True, default=str),
        "passed": bool(passed),
        "checkpoint_marker": MARKER,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    required_paths = [
        AMPLITUDE_SCRIPT,
        TRAJECTORY_SCRIPT,
        VALIDATION_SCRIPT,
        AMPLITUDE_JSON,
        TRAJECTORY_JSON,
        AMPLITUDE_CSV,
        PROJECTION_CSV,
        FIXED_CSV,
        TRAJECTORY_CSV,
        CONVERGENCE_CSV,
        STATIC_CSV,
        PROVENANCE,
        CHECKPOINT,
        FORMAL_NOTE,
        RESUME,
        SPINE,
        VARIABLES,
        CLAIMS,
        EQUATIONS,
        RED_TEAM,
        UNIFICATION,
    ]
    missing_paths = [str(path) for path in required_paths if not path.exists()]
    rows: list[dict[str, Any]] = []
    rows.append(
        validation_row(
            len(rows),
            "all checkpoint source result document and register paths exist",
            f"{len(missing_paths)} missing paths",
            missing_paths,
            not missing_paths,
        )
    )
    compile_failures: list[str] = []
    for script in (AMPLITUDE_SCRIPT, TRAJECTORY_SCRIPT, VALIDATION_SCRIPT):
        try:
            compile(script.read_text(encoding="utf-8"), str(script), "exec")
        except Exception as error:
            compile_failures.append(f"{script}: {error}")
    rows.append(
        validation_row(
            len(rows),
            "all 4968 scripts compile without executing or writing bytecode",
            f"{len(compile_failures)} compile failures",
            compile_failures,
            not compile_failures,
        )
    )
    hash_results = {
        str(path.relative_to(ROOT)): digest(path) for path in EXPECTED_HASHES
    }
    hash_failures = {
        str(path.relative_to(ROOT)): {
            "expected": expected,
            "actual": digest(path),
        }
        for path, expected in EXPECTED_HASHES.items()
        if digest(path) != expected
    }
    rows.append(
        validation_row(
            len(rows),
            "both authoritative result JSON files match locked hashes",
            f"{len(hash_failures)} hash mismatches",
            hash_results,
            not hash_failures,
        )
    )
    amplitude = json.loads(AMPLITUDE_JSON.read_text(encoding="utf-8"))
    trajectory = json.loads(TRAJECTORY_JSON.read_text(encoding="utf-8"))
    rows.append(
        validation_row(
            len(rows),
            "the covariant amplitude generator passes every internal check",
            f"all={amplitude['all_checks_pass']}; maxWard={amplitude['maximum_ward_residual']:.12g}",
            amplitude["ward_residuals"],
            amplitude["all_checks_pass"]
            and amplitude["maximum_ward_residual"] <= 5.0e-8,
        )
    )
    normalization = amplitude["amplitude_normalization"]
    rows.append(
        validation_row(
            len(rows),
            "action and independent all-plus amplitude fix Lambda^-2=2c",
            normalization["Trott_coupling_map"],
            normalization,
            normalization["Trott_coupling_map"] == "Lambda^-2=2c"
            and normalization["dimensionless_q"] == "q=M_P^2*c=2 W_C",
        )
    )
    partial = amplitude["partial_wave_projection"]
    rows.append(
        validation_row(
            len(rows),
            "the complete photon cut has exact same-helicity zero and mixed source",
            partial["gamma_C_R4prime_q"],
            partial,
            partial["gamma_C_R4"] == "0"
            and partial["gamma_C_R4prime_q"] == "-79*q**2/(280*pi**2)"
            and partial["beta_B_plus_running"]
            == "-79*g_CFF**2/(140*pi*g**2)",
        )
    )
    amplitude_rows = read_csv(AMPLITUDE_CSV)
    amplitude_failures = [row for row in amplitude_rows if row["status"] != "PASS"]
    rows.append(
        validation_row(
            len(rows),
            "all fifteen sampled helicity amplitudes match exact formulas",
            f"rows={len(amplitude_rows)}; failures={len(amplitude_failures)}",
            amplitude_failures,
            len(amplitude_rows) == 15 and not amplitude_failures,
        )
    )
    projection_rows = read_csv(PROJECTION_CSV)
    rows.append(
        validation_row(
            len(rows),
            "partial-wave ledger contains direct crossed zero and total rows",
            f"rows={len(projection_rows)}",
            [row["row_id"] for row in projection_rows],
            len(projection_rows) == 5
            and sum(
                row["status"] == "DERIVED_COMPLETE_ONE_LOOP_CFF_SQUARED"
                for row in projection_rows
            )
            == 1
            and sum(row["status"] == "EXACT_HELICITY_ZERO" for row in projection_rows)
            == 1,
        )
    )
    rows.append(
        validation_row(
            len(rows),
            "all four CFF-completed GR-connected trajectory runs succeed",
            f"runs={len(trajectory['completed_N8_endpoints'])} N8; all={trajectory['all_checks_pass']}",
            trajectory["completed_N8_endpoints"],
            trajectory["all_checks_pass"]
            and len(trajectory["completed_N8_endpoints"]) == 2,
        )
    )
    fixed_rows = read_csv(FIXED_CSV)
    trajectory_rows = read_csv(TRAJECTORY_CSV)
    rows.append(
        validation_row(
            len(rows),
            "fixed and sampled trajectory row counts are complete",
            f"fixed={len(fixed_rows)}; trajectory={len(trajectory_rows)}",
            {"fixed": len(fixed_rows), "trajectory": len(trajectory_rows)},
            len(fixed_rows) == 4 and len(trajectory_rows) == 4 * 121,
        )
    )
    rows.append(
        validation_row(
            len(rows),
            "the p8 extension retains two irrelevant directions and zero new relevant parameters",
            f"eigenvalues={trajectory['p8_subblock_eigenvalues']}; new={trajectory['new_relevant_directions']}",
            trajectory["p8_subblock_eigenvalues"],
            trajectory["p8_subblock_eigenvalues"] == [4.0, 4.0]
            and trajectory["new_relevant_directions"] == 0,
        )
    )
    endpoints = trajectory["completed_N8_endpoints"]
    b_c_values = [float(row["B_C_endpoint"]) for row in endpoints]
    b_t_values = [float(row["B_t_endpoint"]) for row in endpoints]
    rows.append(
        validation_row(
            len(rows),
            "the completed N8 endpoint matches the recorded source bracket",
            f"BC=[{min(b_c_values):.13g},{max(b_c_values):.13g}]; Bt=[{min(b_t_values):.13g},{max(b_t_values):.13g}]",
            endpoints,
            math.isclose(min(b_c_values), 0.013876928742365074, rel_tol=0, abs_tol=2e-15)
            and math.isclose(max(b_c_values), 0.013877796048066918, rel_tol=0, abs_tol=2e-15)
            and math.isclose(min(b_t_values), -0.01223564291729139, rel_tol=0, abs_tol=2e-15)
            and math.isclose(max(b_t_values), -0.012235315742706605, rel_tol=0, abs_tol=2e-15),
        )
    )
    increments = trajectory["increment_over_4967"]
    rows.append(
        validation_row(
            len(rows),
            "the direct CFF source shifts Bplus while leaving Bminus invariant within tolerance",
            str(increments),
            increments,
            all(abs(value["B_minus_endpoint"]) <= 2.0e-8 for value in increments.values())
            and all(abs(value["B_plus_endpoint"]) > 1.0e-4 for value in increments.values()),
        )
    )
    convergence_rows = read_csv(CONVERGENCE_CSV)
    n6_n8 = [row for row in convergence_rows if row["comparison"] == "N6_to_N8"]
    rows.append(
        validation_row(
            len(rows),
            "N6 to N8 convergence passes the 1e-3 gate",
            f"max={trajectory['maximum_N6_to_N8_relative_shift']:.12g}",
            {row["scheme"] + ":" + row["coordinate"]: row["relative_difference"] for row in n6_n8},
            len(convergence_rows) == 12
            and len(n6_n8) == 8
            and all(float(row["relative_difference"]) <= 1.0e-3 for row in n6_n8),
        )
    )
    static_rows = read_csv(STATIC_CSV)
    static_max = max(float(row["max_abs_metric_residual"]) for row in static_rows)
    rows.append(
        validation_row(
            len(rows),
            "all twenty-two compact rows remain below their metric gate",
            f"rows={len(static_rows)}; max={static_max:.12g}",
            {"recorded_max": trajectory["maximum_static_metric_residual"]},
            len(static_rows) == 22
            and all(
                float(row["max_abs_metric_residual"]) <= float(row["epsilon_gate"])
                for row in static_rows
            )
            and math.isclose(
                static_max,
                trajectory["maximum_static_metric_residual"],
                rel_tol=1.0e-14,
            ),
        )
    )
    rows.append(
        validation_row(
            len(rows),
            "full source completeness and full MTS remain explicitly false",
            f"full={trajectory['full_source_complete']}; remaining={trajectory['remaining_p8_sources']}",
            trajectory["remaining_p8_sources"],
            trajectory["full_source_complete"] is False
            and trajectory["valid_for_full_MTS_claim"] is False
            and "three-loop pure-Einstein p8 source" in trajectory["remaining_p8_sources"],
        )
    )
    marker_paths = [
        CHECKPOINT,
        FORMAL_NOTE,
        RESUME,
        SPINE,
        EQUATIONS,
        RED_TEAM,
        UNIFICATION,
    ]
    marker_missing = [
        str(path) for path in marker_paths if CHECKPOINT_MARKER not in path.read_text(encoding="utf-8")
    ]
    rows.append(
        validation_row(
            len(rows),
            "checkpoint formal handoff spine and registers contain the 4968 marker",
            f"{len(marker_missing)} missing markers",
            marker_missing,
            not marker_missing,
        )
    )
    variable_rows = read_csv(VARIABLES)
    required_variable_ids = (
        "q_CFF4968",
        "gamma_R4prime_CFF4968",
        "B_plus4968_MTS",
        "B_C4968_MTS",
        "PredictivityStatus4968_MTS",
    )
    variable_counts = {
        variable_id: sum(row["symbol"] == variable_id for row in variable_rows)
        for variable_id in required_variable_ids
    }
    rows.append(
        validation_row(
            len(rows),
            "all five canonical 4968 variable rows occur exactly once",
            str(variable_counts),
            variable_counts,
            all(count == 1 for count in variable_counts.values()),
        )
    )
    claim_rows = read_csv(CLAIMS)
    claim_count = sum(row["claim_id"] == "L-810" for row in claim_rows)
    rows.append(
        validation_row(
            len(rows),
            "claim L-810 occurs exactly once and remains private nonclaim",
            f"count={claim_count}",
            [row for row in claim_rows if row["claim_id"] == "L-810"],
            claim_count == 1
            and all(
                "private_nonclaim" in row["status"]
                for row in claim_rows
                if row["claim_id"] == "L-810"
            ),
        )
    )
    authored_docs = [CHECKPOINT, FORMAL_NOTE, PROVENANCE]
    placeholder_docs = [
        str(path)
        for path in authored_docs
        if "MISSING_" in path.read_text(encoding="utf-8")
    ]
    rows.append(
        validation_row(
            len(rows),
            "new authored documents contain no MISSING placeholder tokens",
            f"{len(placeholder_docs)} placeholder documents",
            placeholder_docs,
            not placeholder_docs,
        )
    )
    csv_paths = [
        AMPLITUDE_CSV,
        PROJECTION_CSV,
        FIXED_CSV,
        TRAJECTORY_CSV,
        CONVERGENCE_CSV,
        STATIC_CSV,
        VARIABLES,
        CLAIMS,
    ]
    malformed = []
    for path in csv_paths:
        parsed = read_csv(path)
        if not parsed or any(None in row for row in parsed):
            malformed.append(str(path))
    rows.append(
        validation_row(
            len(rows),
            "all generated and canonical CSV files parse cleanly",
            f"{len(malformed)} malformed CSV files",
            malformed,
            not malformed,
        )
    )
    cache_paths = [
        str(path) for path in POST.rglob("__pycache__") if path.is_dir()
    ]
    rows.append(
        validation_row(
            len(rows),
            "no Python bytecode cache directories remain under post-checkpoint-work",
            f"{len(cache_paths)} cache directories",
            cache_paths,
            not cache_paths,
        )
    )
    rows.append(
        validation_row(
            len(rows),
            "every prior validation row passes while claim promotion remains false",
            f"prior_passed={all(row['passed'] for row in rows)}; rows={len(rows)}",
            {"valid_for_full_MTS_claim": False},
            all(row["passed"] for row in rows),
        )
    )
    write_csv(rows)
    failures = [row["check_id"] for row in rows if not row["passed"]]
    print(f"{MARKER}_CHECKS={len(rows)}", flush=True)
    print(f"{MARKER}_FAILURES={failures}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    if failures:
        raise RuntimeError(f"4968 validation failed: {failures}")
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
