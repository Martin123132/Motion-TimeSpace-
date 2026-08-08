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
SOURCE = POST / "source-intake" / "functional_rg" / "4935"
OUTPUT_DIR = POST / "source-intake" / "mts_residuals"
OUTPUT = OUTPUT_DIR / "P8_Y5_BRR545_4935_VALIDATION.csv"

CHECKPOINT = POST / "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md"
FORMAL_NOTE = FORMAL / "951-PPC4161-GR-connected-minimal-trajectory-and-motion-entry.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

TRAJECTORY_SCRIPT = POST / "scripts" / "Y5_R2FR_4935_completed_fixed_point_trajectory.py"
MOTION_SCRIPT = POST / "scripts" / "Y5_R2FR_4935_motion_sector_entry.py"
TRAJECTORY_JSON = SOURCE / "completed_fixed_point_trajectory_results.json"
TRACE_CSV = SOURCE / "completed_fixed_point_GR_branch_trace.csv"
MOTION_JSON = SOURCE / "motion_sector_entry_results.json"
MOTION_TABLE = SOURCE / "motion_sector_entry_operator_table.csv"
PARENT_4934 = POST / "source-intake" / "functional_rg" / "4934" / "completed_combined_flow_results.json"

MARKER = "MTS_GR_CONNECTED_MINIMAL_TRAJECTORY_MOTION_ENTRY_4935"
FORMAL_MARKER = "PPC4161_GR_CONNECTED_MINIMAL_TRAJECTORY_MOTION_ENTRY_4935"
VALIDATION_MARKER = "MTS_GR_CONNECTED_MINIMAL_TRAJECTORY_MOTION_ENTRY_VALIDATION_4935"
NEXT_TARGET = "4936-Y5-R2FR-motion-1PI-mass-and-O4-functional-trace-projection-or-two-scale-predictivity-gate.md"
CHECKED_DATE = "2026-07-12"

SCRIPTS = (TRAJECTORY_SCRIPT, MOTION_SCRIPT, Path(__file__))
HASH_LOCKS = {
    PARENT_4934: "c70583d03ec773fb31aca0cb0ac73e662c66c6146ee8bfcdeb07598ddfe43978",
    TRAJECTORY_SCRIPT: "ad3199770b67210d14748c5b88c4b9c1cee0796318281adcfe8adb16f1c80f48",
    MOTION_SCRIPT: "1256616f44aaea6c443b3c09d6ce265803ca59b97b7fe3312ed20ae6c185c8e9",
    TRAJECTORY_JSON: "8793e369ba0a9726c43dc64fe454ba87f88876832eca0ba9b79f07b171d1e222",
    TRACE_CSV: "9244de9c6414ea78bc0c72a12010aca273831417f76e97c54212faf5337ea643",
    MOTION_JSON: "ba3dfdaacfb1e3d00282d82c4b4656a937e033cb9145e94c71b81e9c42a54240",
    MOTION_TABLE: "50f6a5481e3e1a94df12469ce13fa0a88450770a5930226eec928f8e9bafc3d6",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def add_check(
    checks: list[dict[str, Any]],
    check_id: str,
    requirement: str,
    expected: str,
    actual: str,
    passed: bool,
) -> None:
    checks.append(
        {
            "validation_id": check_id,
            "requirement": requirement,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "checkpoint_marker": VALIDATION_MARKER,
            "valid_for_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []
    required = [
        *SCRIPTS,
        *HASH_LOCKS,
        CHECKPOINT,
        FORMAL_NOTE,
        PROVENANCE,
        CLAIMS,
        VARIABLES,
        EQUATIONS,
        RED_TEAM,
        SPINE,
        RESUME,
    ]
    missing = sorted(str(path) for path in set(required) if not path.exists())
    add_check(
        checks,
        "VAL4935_00_paths",
        "all generators results trace documents and registers exist",
        "0 missing paths",
        str(missing),
        not missing,
    )

    syntax_errors = []
    for path in SCRIPTS:
        try:
            compile(read_text(path), str(path), "exec")
        except SyntaxError as error:
            syntax_errors.append(f"{path.name}:{error}")
    add_check(
        checks,
        "VAL4935_01_compile",
        "all three checkpoint scripts compile without writing bytecode",
        "0 syntax errors",
        str(syntax_errors),
        not syntax_errors,
    )

    hash_failures = []
    for path, expected in HASH_LOCKS.items():
        actual = digest(path) if path.exists() else "MISSING"
        if actual != expected:
            hash_failures.append(f"{path.name}:{actual}")
    add_check(
        checks,
        "VAL4935_02_hashes",
        "the parent result both generators and four executed artifacts match locked hashes",
        "7 matches",
        "OK" if not hash_failures else str(hash_failures),
        not hash_failures,
    )

    trajectory = load_json(TRAJECTORY_JSON)
    trajectory_checks = trajectory["checks"]
    add_check(
        checks,
        "VAL4935_03_trajectory_internal",
        "every internal trajectory existence scaling convergence and solve check passes",
        "all true",
        str(trajectory_checks),
        all(trajectory_checks.values()),
    )

    physical = trajectory["physical_branch_seed_runs"]
    branch_ok = (
        len(physical) == 5
        and [run["relative_seed_amplitude"] for run in physical]
        == [1.0e-4, 3.0e-5, 1.0e-5, 3.0e-6, 1.0e-6]
        and all(run["termination"] == "IR_G_TARGET" for run in physical)
        and all(abs(run["endpoint"][0] - 1.0e-10) < 2.0e-20 for run in physical)
        and all(run["positive_Newton_through_stored_steps"] for run in physical)
    )
    add_check(
        checks,
        "VAL4935_04_physical_branches",
        "five declared negative relevant seeds reach g=1e-10 with positive Newton coupling",
        "5 seeds; all IR_G_TARGET; g=1e-10; positive",
        str([(run["relative_seed_amplitude"], run["termination"], run["endpoint"][0]) for run in physical]),
        branch_ok,
    )

    opposite = trajectory["opposite_branch_run"]
    opposite_ok = (
        opposite["termination"] == "SCALED_NORM_LIMIT"
        and opposite["endpoint"][0] > trajectory["flow_contract"]["fixed_point"][0]
        and opposite["endpoint"][1] > 30.0
        and opposite["endpoint"][2] > 200.0
    )
    add_check(
        checks,
        "VAL4935_05_opposite_branch",
        "the opposite relevant sign runs away rather than reaching the Gaussian target",
        "SCALED_NORM_LIMIT; increasing g; large four-photon coordinates",
        f"termination={opposite['termination']}; endpoint={opposite['endpoint']}",
        opposite_ok,
    )

    gaussian = trajectory["gaussian_source_extraction"]
    gaussian_ok = (
        abs(gaussian["ray_rows"][0]["beta_g_over_g"] - 2.0) < 2.0e-7
        and abs(gaussian["plus_source_limit"]) < 1.0e-8
        and abs(gaussian["minus_source_limit"] + 1096.0 / 15.0) < 1.0e-10
        and abs(gaussian["c3_source_limit"] + 3.669491731602941e-5) < 1.0e-14
    )
    add_check(
        checks,
        "VAL4935_06_gaussian",
        "the Gaussian Newton plus photon-log and completed C3 source limits are recovered",
        "2; 0; -1096/15; -3.669491731602941e-5",
        f"g={gaussian['ray_rows'][0]['beta_g_over_g']}; plus={gaussian['plus_source_limit']}; minus={gaussian['minus_source_limit']}; c3={gaussian['c3_source_limit']}",
        gaussian_ok,
    )

    representative = trajectory["representative_branch"]
    wilsons = representative["endpoint_wilson_coordinates"]
    expected_wilsons = {
        "W_plus": 0.007916337891619754,
        "W_minus_cl16pi": 0.09472565630613844,
        "W_C": 0.000550951486900825,
        "A_C3": -2.1700910782992792e-5,
    }
    wilson_ok = all(
        math.isclose(wilsons[name], value, rel_tol=2.0e-12, abs_tol=2.0e-15)
        for name, value in expected_wilsons.items()
    )
    add_check(
        checks,
        "VAL4935_07_wilsons",
        "the log-subtracted minimal Wilson endpoint matches the executed reference",
        str(expected_wilsons),
        str(wilsons),
        wilson_ok,
    )

    convergence = trajectory["seed_convergence"]
    convergence_ok = (
        convergence["W_plus"]["max_relative_difference"] < 1.0e-8
        and convergence["W_minus_cl16pi"]["max_relative_difference"] < 1.0e-8
        and convergence["W_C"]["max_relative_difference"] < 2.0e-9
        and convergence["A_C3"]["max_relative_difference"] < 1.0e-5
    )
    add_check(
        checks,
        "VAL4935_08_seed_convergence",
        "all four infrared coordinates are stable across five relevant-direction seed distances",
        "photon<1e-8; C3<1e-5 relative",
        str(convergence),
        convergence_ok,
    )

    numerical_ok = (
        representative["maximum_raw_projection_condition_number"] > 1.0e20
        and representative["maximum_equilibrated_projection_condition_number"] < 211.0
        and representative["maximum_backward_relative_linear_residual"] < 1.4e-16
    )
    add_check(
        checks,
        "VAL4935_09_numerics",
        "raw scaling warning equilibration and backward residual are all retained",
        "raw>1e20; equilibrated<211; residual<1.4e-16",
        str(representative),
        numerical_ok,
    )

    trace_rows = read_csv(TRACE_CSV)
    trace_ok = (
        len(trace_rows) == 241
        and all(row["checkpoint_marker"] == "MTS_4935_COMPLETED_FIXED_POINT_TRAJECTORY" for row in trace_rows)
        and all(row["valid_for_claim"] == "False" for row in trace_rows)
        and float(trace_rows[0]["g"]) > float(trace_rows[-1]["g"])
        and math.isclose(float(trace_rows[-1]["g"]), 1.0e-10, rel_tol=2.0e-12)
        and all(
            math.isfinite(float(row[field]))
            for row in trace_rows
            for field in (
                "g",
                "g_plus",
                "g_minus",
                "g_CFF",
                "h_C3",
                "equilibrated_projection_condition_number",
                "backward_relative_linear_residual",
            )
        )
    )
    add_check(
        checks,
        "VAL4935_10_trace",
        "the 241-row representative trace parses is finite remains private and reaches the target",
        "241 finite private rows; decreasing g; endpoint 1e-10",
        f"rows={len(trace_rows)}; g0={trace_rows[0]['g']}; g1={trace_rows[-1]['g']}",
        trace_ok,
    )

    trajectory_boundary = trajectory["claim_boundary"]
    trajectory_boundary_ok = (
        trajectory_boundary["GR_connected_minimal_trajectory_derived"]
        and trajectory_boundary["source_complete_minimal_point_has_Gaussian_IR_branch"]
        and not trajectory_boundary["full_MTS_trajectory_derived"]
        and not trajectory_boundary["motion_sector_included"]
        and not trajectory_boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add_check(
        checks,
        "VAL4935_11_trajectory_boundary",
        "minimal GR connectivity is true while full MTS motion and local promotion remain false",
        "minimal=true; full=false; motion=false; local=false",
        str(trajectory_boundary),
        trajectory_boundary_ok,
    )

    motion = load_json(MOTION_JSON)
    add_check(
        checks,
        "VAL4935_12_motion_internal",
        "every exact motion variation dimension threshold and quotient check passes",
        "all true",
        str(motion["checks"]),
        all(motion["checks"].values()),
    )

    motion_parent = motion["parent_motion_action"]
    motion_hessian_ok = (
        motion_parent["vacuum"] == "psi_0=0 is the only classical stationary point"
        and motion_parent["bare_vacuum_Hessian_limit"] == "oo"
        and not motion["claim_boundary"]["bare_zero_background_Hessian_usable"]
        and motion["claim_boundary"]["renormalized_1PI_entry_required"]
    )
    add_check(
        checks,
        "VAL4935_13_motion_hessian",
        "the only bare vacuum has an infinite Hessian and the result requires a renormalized 1PI entry",
        "vacuum=0; Hessian=oo; bare usable=false; 1PI=true",
        str(motion_parent),
        motion_hessian_ok,
    )

    renormalized = motion["renormalized_entry"]
    relevance_ok = (
        renormalized["canonical_critical_exponents"]
        == {"g_tilde_psi": 8.0 / 3.0, "w_psi": 2.0}
        and renormalized["canonical_beta_g_tilde"] == "-8*g_tilde/3"
        and renormalized["canonical_beta_w"] == "-2*c_m**2*g_tilde**(3/4)"
    )
    add_check(
        checks,
        "VAL4935_14_motion_relevance",
        "the invariant potential and equivalent mass coordinate are canonically relevant before mixing",
        "theta=8/3 and 2",
        str(renormalized),
        relevance_ok,
    )

    threshold = motion["minimal_optimized_trace"]
    threshold_ok = (
        threshold["decoupling_factor"] == "1/(w + 1)"
        and "6*pi*(w + 1)" in threshold["Delta_beta_g"]
        and "eta_psi" in threshold["Delta_beta_h"]
        and threshold["eta_zero_result"].startswith("Delta beta_h=0")
    )
    add_check(
        checks,
        "VAL4935_15_threshold",
        "the optimized massive scalar threshold and eta-zero C3 result are explicit",
        "D=1/(1+w); Delta beta_g; eta-weighted Delta beta_h; eta=0 zero",
        str(threshold),
        threshold_ok,
    )

    motion_rows = read_csv(MOTION_TABLE)
    o4_rows = [row for row in motion_rows if row["entry_id"] == "ME4935_03_O4_portal"]
    operator_ok = (
        len(motion_rows) == 4
        and len(o4_rows) == 1
        and "-2u_O4" in o4_rows[0]["quadratic_Hessian"]
        and all(row["checkpoint_marker"] == "MTS_4935_MOTION_SECTOR_ENTRY" for row in motion_rows)
        and all(row["valid_for_claim"] == "False" for row in motion_rows)
        and motion["six_derivative_entry"]["motion_rows_with_nonzero_quadratic_Hessian"]
        == ["S6_O4"]
    )
    add_check(
        checks,
        "VAL4935_16_O4",
        "the four-row motion interface isolates O4 as the unique six-derivative quadratic motion portal",
        "4 private rows; unique O4; Hessian=-2u_O4...",
        str(motion_rows),
        operator_ok,
    )

    motion_boundary = motion["claim_boundary"]
    motion_boundary_ok = (
        motion_boundary["motion_parent_Hessian_form_derived"]
        and motion_boundary["minimal_mass_threshold_derived"]
        and motion_boundary["motion_relevant_scale_identified"]
        and not motion_boundary["motion_fixed_point_calculated"]
        and not motion_boundary["full_MTS_trajectory_calculated"]
        and not motion_boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add_check(
        checks,
        "VAL4935_17_motion_boundary",
        "motion entry and relevance are derived while its fixed point full trajectory and local promotion remain false",
        "entry=true; relevance=true; fixed/full/local=false",
        str(motion_boundary),
        motion_boundary_ok,
    )

    documents = {
        "checkpoint": read_text(CHECKPOINT),
        "formal": read_text(FORMAL_NOTE),
        "provenance": read_text(PROVENANCE),
        "claims": read_text(CLAIMS),
        "variables": read_text(VARIABLES),
        "equations": read_text(EQUATIONS),
        "red_team": read_text(RED_TEAM),
        "spine": read_text(SPINE),
        "resume": read_text(RESUME),
    }
    markers = {
        "checkpoint": MARKER,
        "formal": FORMAL_MARKER,
        "provenance": "MTS_GR_CONNECTED_MINIMAL_TRAJECTORY_MOTION_ENTRY_PROVENANCE_4935",
        "claims": "L-777",
        "variables": "TrajectoryStatus4935_MTS",
        "equations": "## 1.228 GR-connected minimal trajectory and motion entry",
        "red_team": "## 179. A minimal GR separatrix is not the enlarged MTS trajectory",
        "spine": "## PPC4161 checkpoint 4935 - GR-connected minimal trajectory and motion entry",
        "resume": NEXT_TARGET,
    }
    missing_markers = [name for name, marker in markers.items() if marker not in documents[name]]
    add_check(
        checks,
        "VAL4935_18_registers",
        "checkpoint provenance formal note registers and resume contain the 4935 markers",
        "0 missing markers",
        str(missing_markers),
        not missing_markers,
    )

    with CLAIMS.open("r", encoding="utf-8-sig", newline="") as handle:
        claim_rows = [row for row in csv.DictReader(handle) if row.get("claim_id") == "L-777"]
    claim_ok = (
        len(claim_rows) == 1
        and "full_MTS_trajectory_false" in claim_rows[0]["status"]
        and "local GR" in claim_rows[0]["risk"]
        and NEXT_TARGET in claim_rows[0]["next_test"]
    )
    add_check(
        checks,
        "VAL4935_19_claim_policy",
        "the single L-777 row blocks full MTS and local-GR promotion and selects the motion beta projection",
        "one row; full=false; local prohibited; next=4936",
        str(claim_rows),
        claim_ok,
    )

    cache_paths = sorted(str(path) for path in POST.rglob("__pycache__"))
    add_check(
        checks,
        "VAL4935_20_cache",
        "no Python bytecode cache directories remain under post-checkpoint-work",
        "0 __pycache__ directories",
        str(cache_paths),
        not cache_paths,
    )

    placeholders = [
        path.name
        for path in (CHECKPOINT, FORMAL_NOTE, PROVENANCE)
        if "MISSING_" in read_text(path)
    ]
    add_check(
        checks,
        "VAL4935_21_placeholders",
        "authored checkpoint documents contain no MISSING_ placeholder tokens",
        "0 documents",
        str(placeholders),
        not placeholders,
    )

    all_prior_pass = all(bool(row["passed"]) for row in checks)
    add_check(
        checks,
        "VAL4935_22_gate",
        "all prior 4935 checks pass and every generated evidence row remains private nonclaim",
        "all prior true; valid_for_claim=false",
        f"prior_passed={all_prior_pass}; prior_rows={len(checks)}",
        all_prior_pass,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fields = [
        "validation_id",
        "requirement",
        "expected",
        "actual",
        "passed",
        "checkpoint_marker",
        "valid_for_claim",
        "source_checked_date",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(checks)

    failed = [row["validation_id"] for row in checks if not row["passed"]]
    print(f"Wrote {OUTPUT}")
    print(f"Checks: {len(checks)}; failed: {failed}")
    print(f"Minimal Wilson endpoint: {wilsons}")
    print(f"Motion critical exponents: {renormalized['canonical_critical_exponents']}")
    print(f"Full MTS trajectory: {trajectory_boundary['full_MTS_trajectory_derived']}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

