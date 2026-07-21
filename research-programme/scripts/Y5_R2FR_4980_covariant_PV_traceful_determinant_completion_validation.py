from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4980"
VALIDATION_DIR = POST / "source-intake" / "mts_residuals"
VALIDATION = VALIDATION_DIR / "P8_Y5_BRR545_4980_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RUNNER = POST / "scripts" / "Y5_R2FR_4980_covariant_PV_traceful_determinant_completion.py"
VALIDATOR = POST / "scripts" / "Y5_R2FR_4980_covariant_PV_traceful_determinant_completion_validation.py"
CHECKPOINT_DOC = POST / "4980-Y5-R2FR-covariant-PV-traceful-determinant-completion.md"
FORMAL_NOTE = FORMAL / "996-PPC4161-covariant-PV-traceful-scalar-determinant-completion.md"
CURRENT_RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CURRENT_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
VARIABLE_AUDIT = FORMAL / "04-variable-audit.csv"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION_SPINE = FORMAL / "07-unification-spine.md"

CONTRACT = SOURCE / "covariant_PV_regulator_contract.csv"
SOURCE_TARGETS = SOURCE / "traceful_source_targets.csv"
Q4_CROSSCHECK = SOURCE / "massive_scalar_q4_extraction_crosscheck.csv"
SCHEME = SOURCE / "PV_two_point_common_scheme_map.csv"
TRACEFUL = SOURCE / "PV_traceful_finite_completion.csv"
INDEPENDENCE = SOURCE / "PV_regulator_independence.csv"
GATE = SOURCE / "PV_traceful_completion_gate.csv"
RESULT = SOURCE / "PV_traceful_completion_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
PREDECESSOR = POST / "source-intake" / "functional_rg" / "4979" / "massless_scalar_finite_determinant_results.json"

MARKER = "MTS_4980_COVARIANT_PV_TRACEFUL_DETERMINANT_COMPLETION_VALIDATION"
FORMAL_MARKER = "PPC4161_COVARIANT_PV_TRACEFUL_SCALAR_COMPLETION_4980"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_width_valid(path: Path) -> bool:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    return bool(rows) and all(len(row) == len(rows[0]) for row in rows)


def contains(path: Path, text: str) -> bool:
    return path.exists() and text in path.read_text(
        encoding="utf-8", errors="replace"
    )


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError):
        return False
    return True


def finite_rows(rows: list[dict[str, str]], fields: tuple[str, ...]) -> bool:
    try:
        return all(
            math.isfinite(float(row[field])) for row in rows for field in fields
        )
    except (KeyError, TypeError, ValueError):
        return False


def false_value(value: str) -> bool:
    return value.strip().lower() == "false"


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-30)


def path_scope_valid() -> bool:
    completed = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 0:
        return all(
            line[3:].strip().replace("\\", "/").startswith(
                ("post-checkpoint-work/", "formalization-workbench/")
            )
            for line in completed.stdout.splitlines()
        )
    allowed = (
        RUNNER,
        VALIDATOR,
        CHECKPOINT_DOC,
        FORMAL_NOTE,
        CURRENT_RESUME,
        CURRENT_SPINE,
        VARIABLE_AUDIT,
        CLAIMS_REGISTER,
        EQUATION_REGISTER,
        RED_TEAM,
        UNIFICATION_SPINE,
        SOURCE,
        VALIDATION,
    )
    roots = (POST.resolve(), FORMAL.resolve())
    return all(
        any(path.resolve().is_relative_to(root) for root in roots)
        for path in allowed
    )


def main() -> int:
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check": name,
                "passed": bool(passed),
                "detail": detail,
                "checkpoint_marker": MARKER,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": "2026-07-14",
            }
        )

    output_csvs = (
        CONTRACT,
        SOURCE_TARGETS,
        Q4_CROSSCHECK,
        SCHEME,
        TRACEFUL,
        INDEPENDENCE,
        GATE,
    )
    required_paths = (
        RUNNER,
        VALIDATOR,
        CHECKPOINT_DOC,
        FORMAL_NOTE,
        CURRENT_RESUME,
        CURRENT_SPINE,
        VARIABLE_AUDIT,
        CLAIMS_REGISTER,
        EQUATION_REGISTER,
        RED_TEAM,
        UNIFICATION_SPINE,
        RESULT,
        PROVENANCE,
        PREDECESSOR,
        *output_csvs,
    )
    check("V01_required_paths_exist", all(path.exists() for path in required_paths), f"{len(required_paths)} paths")
    check("V02_runner_compiles", compiles(RUNNER), str(RUNNER))
    check("V03_validator_compiles", compiles(VALIDATOR), str(VALIDATOR))
    for index, path in enumerate(
        (
            CHECKPOINT_DOC,
            FORMAL_NOTE,
            CURRENT_RESUME,
            CURRENT_SPINE,
            EQUATION_REGISTER,
            RED_TEAM,
            UNIFICATION_SPINE,
        ),
        start=4,
    ):
        check(f"V{index:02d}_formal_marker_{path.stem}", contains(path, FORMAL_MARKER), FORMAL_MARKER)

    predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
    check("V11_predecessor_TT_closed", predecessor["valid_for_TT_common_scheme_finite_determinant_match"] is True, "4979 TT match true")
    check("V12_predecessor_trace_open", predecessor["valid_for_complete_traceful_common_scheme_finite_determinant_match"] is False, "4980 begins from open trace contact")

    for index, path in enumerate(output_csvs, start=13):
        check(f"V{index:02d}_csv_width_{path.stem}", csv_width_valid(path), path.name)

    contract_rows = read_csv(CONTRACT)
    source_rows = read_csv(SOURCE_TARGETS)
    q4_rows = read_csv(Q4_CROSSCHECK)
    scheme_rows = read_csv(SCHEME)
    trace_rows = read_csv(TRACEFUL)
    independence_rows = read_csv(INDEPENDENCE)
    gate_rows = read_csv(GATE)
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    all_rows = (
        contract_rows
        + source_rows
        + q4_rows
        + scheme_rows
        + trace_rows
        + independence_rows
        + gate_rows
    )
    check("V20_no_full_MTS_rows", all(false_value(row["valid_for_full_MTS_claim"]) for row in all_rows), f"rows={len(all_rows)}")
    check("V21_no_missing_markers", all("MISSING_" not in " ".join(row.values()) for row in all_rows), "no placeholder markers")

    check("V22_contract_shape", len(contract_rows) == 7, "four fields plus three moments")
    moment_rows = [row for row in contract_rows if row["field_role"] == "PV_moment_cancellation"]
    check("V23_PV_moments_zero", len(moment_rows) == 3 and all(float(row["coefficient"]) == 0.0 for row in moment_rows), "sum c r^p=0 p=0,1,2")

    check("V24_source_shape", len(source_rows) == 8, "G03-G06 at two grids")
    check("V25_source_ids", {row["geometry_id"] for row in source_rows} == {"G03", "G04", "G05", "G06"}, "four traceful controls")
    check("V26_fresh_source_rows", sum(row["control_class"] == "fresh_withheld_traceful" for row in source_rows) == 4, "G05/G06 grids 4/6")
    check("V27_source_numeric", finite_rows(source_rows, ("scalar_local_response", "ricci_local_response", "anomaly_local_response", "source_minus_W_density")), "all finite")

    check("V28_q4_shape", len(q4_rows) == 2, "G05/G06")
    check("V29_q4_numeric", finite_rows(q4_rows, ("analytic_q4", "direct_fit_q4_xmax_0p04", "direct_fit_q4_xmax_0p07", "maximum_relative_q4_residual")), "all finite")
    max_q4 = max(float(row["maximum_relative_q4_residual"]) for row in q4_rows)
    check("V30_q4_crosscheck", max_q4 < 2.0e-8, f"max={max_q4:.17g}")

    check("V31_scheme_shape", len(scheme_rows) == 24, "six masses times four coefficients")
    check("V32_scheme_no_three_point_fit", all(false_value(row["fit_uses_three_point_data"]) for row in scheme_rows), "two-point only")
    check("V33_scheme_numeric", finite_rows(scheme_rows, ("regulator_mass_M", "fitted_bare_PV_value", "exact_bare_PV_value", "target_common_scheme_value", "covariant_fit_residual")), "all finite")
    max_fit = max(float(row["covariant_fit_residual"]) for row in scheme_rows)
    max_exact = max(float(row["fitted_minus_exact_bare_residual"]) for row in scheme_rows)
    check("V34_scheme_covariant_fit", max_fit < 2.0e-13, f"max={max_fit:.17g}")
    check("V35_scheme_exact_formula", max_exact < 1.0e-10, f"max={max_exact:.17g}")
    exact_formula_valid = True
    for row in scheme_rows:
        mass = float(row["regulator_mass_M"])
        shift = math.log(3.0 * mass**2 / 8.0)
        expected = {
            "Ricci_log_q2_over_mu2": 1.0 / 60.0,
            "Ricci_finite_local": -23.0 / 450.0 - shift / 60.0,
            "R_log_q2_over_mu2": 1.0 / 120.0,
            "R_finite_local": -1.0 / 1800.0 - shift / 120.0,
        }[row["coefficient"]]
        exact_formula_valid &= relative_error(float(row["exact_bare_PV_value"]), expected) < 1.0e-14
    check("V36_exact_scheme_identity", exact_formula_valid, "log(3M^2/8) rule")

    check("V37_trace_shape", len(trace_rows) == 24, "four geometries times six masses")
    counts = {geometry: sum(row["geometry_id"] == geometry for row in trace_rows) for geometry in ("G03", "G04", "G05", "G06")}
    check("V38_trace_counts", all(count == 6 for count in counts.values()), str(counts))
    check("V39_trace_no_fit", all(false_value(row["fit_uses_this_geometry"]) for row in trace_rows), "all withheld")
    check("V40_trace_promoted_rows", all(row["valid_for_complete_free_scalar_traceful_match"].lower() == "true" for row in trace_rows), "free scalar only")
    check("V41_trace_numeric", finite_rows(trace_rows, ("renormalized_PV_W", "source_target_W", "absolute_residual", "relative_residual", "exact_vs_fitted_counterterm_residual")), "all finite")
    max_old = max(float(row["relative_residual"]) for row in trace_rows if row["geometry_id"] in ("G03", "G04"))
    max_fresh = max(float(row["relative_residual"]) for row in trace_rows if row["geometry_id"] in ("G05", "G06"))
    max_absolute = max(float(row["absolute_residual"]) for row in trace_rows)
    check("V42_old_trace_match", max_old < 1.0e-8, f"max={max_old:.17g}")
    check("V43_fresh_trace_match", max_fresh < 2.0e-8, f"max={max_fresh:.17g}")
    check("V44_trace_absolute", max_absolute < 3.0e-13, f"max={max_absolute:.17g}")

    check("V45_independence_shape", len(independence_rows) == 6, "two slopes plus four contacts")
    slope_rows = [row for row in independence_rows if "slope" in row["identity"]]
    contact_rows = [row for row in independence_rows if row["identity"] == "renormalized_traceful_regulator_independence"]
    check("V46_slope_count", len(slope_rows) == 2, "Ricci and R")
    check("V47_slope_precision", max(float(row["relative_residual"]) for row in slope_rows) < 1.0e-12, "exact logarithmic slopes")
    check("V48_contact_count", len(contact_rows) == 4, "four geometries")
    max_spread = max(float(row["regulator_mass_spread"]) for row in contact_rows)
    check("V49_regulator_independence", max_spread < 2.0e-12, f"max={max_spread:.17g}")

    check("V50_gate_shape", len(gate_rows) == 16, "16 runner gates")
    check("V51_all_runner_gates", all(row["passed"].lower() == "true" and row["status"] == "pass" for row in gate_rows), "16/16")
    check("V52_result_gate_count", result["gate_pass_count"] == result["gate_count"] == 16, "16/16")
    check("V53_result_q4_flag", result["valid_for_covariant_PV_q4_contact_derivation"] is True, "derived")
    check("V54_result_trace_flag", result["valid_for_complete_free_scalar_traceful_common_scheme_finite_determinant_match"] is True, "free scalar traceful closed")
    check("V55_result_parent_false", result["valid_for_interacting_motion_graviton_ghost_kernel"] is False, "parent interaction open")
    check("V56_result_MTS_false", result["valid_for_full_MTS_claim"] is False, "nonclaim")

    variable_text = VARIABLE_AUDIT.read_text(encoding="utf-8")
    required_variables = (
        "PVRegulator4980_MTS",
        "MassiveQ4Contact4980_MTS",
        "PVSchemeCounterterm4980_MTS",
        "ScalarTraceCompletion4980_MTS",
        "RegulatorIndependence4980_MTS",
        "PredictivityStatus4980_MTS",
    )
    check("V57_variable_rows", all(symbol in variable_text for symbol in required_variables), "six 4980 variables")
    claims = read_csv(CLAIMS_REGISTER)
    claim = next((row for row in claims if row["claim_id"] == "L-822"), None)
    check("V58_claim_L822", claim is not None and FORMAL_MARKER in claim["notes"], "registered")
    check("V59_provenance_inputs", contains(PROVENANCE, "checkpoint 4978") and contains(PROVENANCE, "checkpoint 4979"), "predecessor digests")
    check("V60_scope_valid", path_scope_valid(), "post-checkpoint-work/formalization-workbench only")

    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)
    pass_count = sum(bool(row["passed"]) for row in checks)
    provenance_lines = [
        "# Checkpoint 4980 validation provenance",
        "",
        f"Checks: `{pass_count}/{len(checks)}`.",
        "",
        "## Digests",
    ]
    for path in required_paths:
        if path.is_file():
            provenance_lines.append(
                f"- `{path.relative_to(ROOT).as_posix()}` sha256 `{digest(path)}`"
            )
    VALIDATION_PROVENANCE.write_text(
        "\n".join(provenance_lines) + "\n", encoding="utf-8"
    )
    print(
        f"{MARKER}_PASS={pass_count}/{len(checks)} output={VALIDATION}",
        flush=True,
    )
    return 0 if pass_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
