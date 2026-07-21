from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4978"
VALIDATION_DIR = POST / "source-intake" / "mts_residuals"
VALIDATION = VALIDATION_DIR / "P8_Y5_BRR545_4978_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RUNNER = POST / "scripts" / "Y5_R2FR_4978_scalar_massless_metric_TTT_assembler.py"
VALIDATOR = POST / "scripts" / "Y5_R2FR_4978_scalar_massless_metric_TTT_validation.py"
CHECKPOINT_DOC = POST / "4978-Y5-R2FR-complete-massless-scalar-metric-TTT-and-direct-log-residue-match.md"
FORMAL_NOTE = FORMAL / "994-PPC4161-complete-massless-scalar-metric-TTT-and-direct-log-residue.md"
CURRENT_RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CURRENT_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
VARIABLE_AUDIT = FORMAL / "04-variable-audit.csv"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION_SPINE = FORMAL / "07-unification-spine.md"

QUADRATIC = SOURCE / "scalar_TTT_quadratic_log_response.csv"
CUBIC = SOURCE / "scalar_TTT_cubic_channel_response.csv"
ASSEMBLY = SOURCE / "scalar_TTT_assembled_response.csv"
WARD = SOURCE / "scalar_TTT_scale_mu_Ward_identity.csv"
DIRECT_UV = SOURCE / "scalar_TTT_direct_determinant_UV_log_residue.csv"
GATE = SOURCE / "scalar_TTT_assembly_gate.csv"
RESULT = SOURCE / "scalar_TTT_assembly_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
PREDECESSOR_RESULT = POST / "source-intake" / "functional_rg" / "4977" / "C3_massless_scalar_nonlocal_results.json"

MARKER = "MTS_4978_SCALAR_MASSLESS_METRIC_TTT_VALIDATION"
FORMAL_MARKER = "PPC4161_COMPLETE_MASSLESS_SCALAR_METRIC_TTT_4978"
EXPECTED_INDICES = {1, 4, 5, 6, 9, 10, 11, 15, 16, 17, 22, 23, 24, 25, 26, 27, 28, 29}
ACTION_PREFACTOR = 1.0 / (2.0 * (4.0 * math.pi) ** 2)


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
    return path.exists() and text in path.read_text(encoding="utf-8", errors="replace")


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError):
        return False
    return True


def finite_rows(rows: list[dict[str, str]], fields: tuple[str, ...]) -> bool:
    try:
        return all(math.isfinite(float(row[field])) for row in rows for field in fields)
    except (KeyError, TypeError, ValueError):
        return False


def no_claim_rows(rows: list[dict[str, str]]) -> bool:
    return all(row.get("valid_for_full_MTS_claim", "").lower() == "false" for row in rows)


def path_scope_valid() -> bool:
    completed = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 0:
        for line in completed.stdout.splitlines():
            path = line[3:].strip().replace("\\", "/")
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            if not (
                path.startswith("post-checkpoint-work/")
                or path.startswith("formalization-workbench/")
            ):
                return False
        return True
    allowlisted = (
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
        for path in allowlisted
    )


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-30)


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
                "source_checked_date": "2026-07-13",
            }
        )

    output_csvs = (QUADRATIC, CUBIC, ASSEMBLY, WARD, DIRECT_UV, GATE)
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
        PREDECESSOR_RESULT,
        *output_csvs,
    )
    check("V01_required_paths_exist", all(path.exists() for path in required_paths), f"{len(required_paths)} paths")
    check("V02_runner_compiles", compiles(RUNNER), str(RUNNER))
    check("V03_validator_compiles", compiles(VALIDATOR), str(VALIDATOR))
    check("V04_checkpoint_marker", contains(CHECKPOINT_DOC, FORMAL_MARKER), FORMAL_MARKER)
    check("V05_formal_note_marker", contains(FORMAL_NOTE, FORMAL_MARKER), FORMAL_MARKER)
    check("V06_resume_marker", contains(CURRENT_RESUME, FORMAL_MARKER), FORMAL_MARKER)
    check("V07_local_spine_marker", contains(CURRENT_SPINE, FORMAL_MARKER), FORMAL_MARKER)
    check("V08_equation_marker", contains(EQUATION_REGISTER, FORMAL_MARKER), FORMAL_MARKER)
    check("V09_red_team_marker", contains(RED_TEAM, FORMAL_MARKER), FORMAL_MARKER)
    check("V10_unification_marker", contains(UNIFICATION_SPINE, FORMAL_MARKER), FORMAL_MARKER)

    predecessor = json.loads(PREDECESSOR_RESULT.read_text(encoding="utf-8"))
    check("V11_predecessor_form_factors", predecessor["valid_for_complete_free_scalar_cubic_curvature_form_factors"] is True, "4977 source form factors valid")
    check("V12_predecessor_full_MTS_false", predecessor["valid_for_full_MTS_claim"] is False, "4977 nonclaim retained")

    quadratic_rows = read_csv(QUADRATIC)
    cubic_rows = read_csv(CUBIC)
    assembly_rows = read_csv(ASSEMBLY)
    ward_rows = read_csv(WARD)
    direct_rows = read_csv(DIRECT_UV)
    gate_rows = read_csv(GATE)
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    check("V13_assembly_shape", len(assembly_rows) == 4, "2 geometries x 2 grids")
    assembly_keys = {(row["geometry_id"], int(row["grid_size"])) for row in assembly_rows}
    check("V14_assembly_keys", assembly_keys == {("G03", 6), ("G03", 8), ("G04", 6), ("G04", 8)}, str(sorted(assembly_keys)))
    check("V15_assembly_numeric", finite_rows(assembly_rows, ("quadratic_total", "cubic_total", "braces_total", "minus_W_mixed_density", "anomaly_local_response")), "all finite")
    check("V16_assembly_sum", all(math.isclose(float(row["braces_total"]), float(row["quadratic_total"]) + float(row["cubic_total"]), rel_tol=1.0e-13, abs_tol=1.0e-15) for row in assembly_rows), "total=quadratic+cubic")
    check("V17_action_prefactor", all(math.isclose(float(row["minus_W_mixed_density"]), ACTION_PREFACTOR * float(row["braces_total"]), rel_tol=1.0e-13, abs_tol=1.0e-16) for row in assembly_rows), "1/[2(4pi)^2]")

    check("V18_quadratic_shape", len(quadratic_rows) == 8, "4 responses x 2 invariants")
    check("V19_quadratic_coefficients", all((row["sector"] == "scalar_R2" and math.isclose(float(row["log_coefficient"]), -1 / 120) and math.isclose(float(row["finite_coefficient"]), -29 / 1800)) or (row["sector"] == "Ricci2" and math.isclose(float(row["log_coefficient"]), -1 / 60) and math.isclose(float(row["finite_coefficient"]), 4 / 225)) for row in quadratic_rows), "exact minimal-scalar coefficients")
    check("V20_quadratic_weighted_sum", all(math.isclose(float(row["weighted_response"]), float(row["log_coefficient"]) * float(row["log_functional_response"]) + float(row["finite_coefficient"]) * float(row["local_functional_response"]), rel_tol=1.0e-13, abs_tol=1.0e-15) for row in quadratic_rows), "weighted source form factors")

    check("V21_cubic_shape", len(cubic_rows) == 72, "4 responses x 18 source terms")
    cubic_groups: dict[tuple[str, int], set[int]] = {}
    for row in cubic_rows:
        cubic_groups.setdefault((row["geometry_id"], int(row["grid_size"])), set()).add(int(row["form_factor_index"]))
    check("V22_cubic_index_completeness", len(cubic_groups) == 4 and all(indices == EXPECTED_INDICES for indices in cubic_groups.values()), "all 18 indices per response")
    check("V23_cubic_numeric", finite_rows(cubic_rows, ("summed_six_assignment_response", "fraction_of_cubic_sum")), "all finite")
    assembly_map = {(row["geometry_id"], int(row["grid_size"])): row for row in assembly_rows}
    check("V24_cubic_sums", all(math.isclose(sum(float(row["summed_six_assignment_response"]) for row in cubic_rows if (row["geometry_id"], int(row["grid_size"])) == key), float(value["cubic_total"]), rel_tol=1.0e-13, abs_tol=1.0e-15) for key, value in assembly_map.items()), "18-term sum equals cubic total")

    grid_rows = [row for row in ward_rows if row["identity"].startswith("grid_convergence")]
    mu_rows = [row for row in ward_rows if row["identity"] == "mu_rescaling_quadratic_action"]
    permutation_rows = [row for row in ward_rows if row["identity"].startswith("cyclic_source_permutation")]
    check("V25_Ward_shape", len(ward_rows) == 13 and len(grid_rows) == 6 and len(mu_rows) == 4 and len(permutation_rows) == 3, "6 grid + 4 mu + 3 permutation")
    max_grid = max(float(row["relative_residual"]) for row in grid_rows)
    max_mu = max(float(row["relative_residual"]) for row in mu_rows)
    max_permutation = max(float(row["relative_residual"]) for row in permutation_rows)
    check("V26_grid_precision", max_grid < 1.0e-12, f"max={max_grid:.17g}")
    check("V27_mu_precision", max_mu < 1.0e-12, f"max={max_mu:.17g}")
    check("V28_permutation_precision", max_permutation < 1.0e-12, f"max={max_permutation:.17g}")
    check("V29_zero_mode_precision", max(float(row["maximum_zero_mode_residual"]) for row in assembly_rows) < 1.0e-12, "no log zero-mode leakage")
    check("V30_imaginary_precision", max(float(row["maximum_imaginary_residual"]) for row in assembly_rows) < 1.0e-12, "real mixed response")
    check("V31_metric_inverse_precision", max(float(row["metric_inverse_residual"]) for row in assembly_rows) < 1.0e-12, "metric inverse")
    check("V32_logBox_variation_retained", all(max(abs(float(row["scalar_delta_logBox_response"])), abs(float(row["ricci_delta_logBox_response"]))) > 1.0e-3 for row in assembly_rows), "nonzero operator variation on every row")

    finite_direct = [row for row in direct_rows if row["status"] == "finite_radius_UV_shell"]
    extrapolated_direct = [row for row in direct_rows if row["status"] == "quadratic_fit_in_inverse_radius_squared"]
    check("V33_direct_shape", len(direct_rows) == 12 and len(finite_direct) == 10 and len(extrapolated_direct) == 2, "2 geometries x (5 radii + infinity)")
    check("V34_direct_numeric", finite_rows(direct_rows, ("direct_determinant_dW_dlnLambda_q4", "expected_source_log_residue", "relative_difference_at_radius")), "all finite")
    recomputed_fits: dict[str, float] = {}
    for geometry_id in ("G03", "G04"):
        selected = sorted((row for row in finite_direct if row["geometry_id"] == geometry_id), key=lambda row: float(row["radius"]))
        radii = np.asarray([float(row["radius"]) for row in selected])
        values = np.asarray([float(row["direct_determinant_dW_dlnLambda_q4"]) for row in selected])
        recomputed_fits[geometry_id] = float(np.polyfit(1.0 / radii**2, values, 2)[-1])
    check("V35_direct_fit_recomputed", all(math.isclose(recomputed_fits[row["geometry_id"]], float(row["direct_determinant_dW_dlnLambda_q4"]), rel_tol=1.0e-13, abs_tol=1.0e-16) for row in extrapolated_direct), str(recomputed_fits))
    high_grid = {row["geometry_id"]: row for row in assembly_rows if int(row["grid_size"]) == 8}
    check("V36_direct_expected_recomputed", all(math.isclose(float(row["expected_source_log_residue"]), 2.0 * ACTION_PREFACTOR * float(high_grid[row["geometry_id"]]["anomaly_local_response"]), rel_tol=1.0e-13, abs_tol=1.0e-16) for row in extrapolated_direct), "2 prefactor A_local")
    max_direct = max(float(row["relative_difference_at_radius"]) for row in extrapolated_direct)
    check("V37_direct_log_precision", max_direct < 1.0e-8, f"max={max_direct:.17g}")
    check("V38_direct_sign_opposition", float(next(row for row in extrapolated_direct if row["geometry_id"] == "G03")["expected_source_log_residue"]) > 0.0 and float(next(row for row in extrapolated_direct if row["geometry_id"] == "G04")["expected_source_log_residue"]) < 0.0, "positive and negative independent rows")

    check("V39_runner_gates", len(gate_rows) == 14 and all(row["passed"].lower() == "true" for row in gate_rows), "14/14")
    check("V40_result_counts", result["response_count"] == 4 and result["gate_pass_count"] == result["gate_count"] == 14, "production result")
    check("V41_source_TTT_true", result["valid_for_complete_free_scalar_source_metric_TTT"] is True, "source-side complete")
    check("V42_direct_log_true", result["valid_for_direct_determinant_UV_log_match"] is True, "UV logarithm independently matched")
    check("V43_finite_direct_false", result["valid_for_independent_renormalized_determinant_match"] is False, "finite scheme comparator open")
    check("V44_full_MTS_false", result["valid_for_full_MTS_claim"] is False, "full MTS false")

    all_output_rows = [read_csv(path) for path in output_csvs]
    check("V45_all_rows_nonclaim", all(no_claim_rows(rows) for rows in all_output_rows), "valid_for_full_MTS_claim=false")
    check("V46_csv_widths", all(csv_width_valid(path) for path in (*output_csvs, VARIABLE_AUDIT, CLAIMS_REGISTER)), "scientific and formal CSV widths")
    check("V47_no_missing_markers", not any("MISSING_" in path.read_text(encoding="utf-8", errors="replace") for path in (*output_csvs, RESULT, CHECKPOINT_DOC, FORMAL_NOTE)), "no placeholders")

    expected_variables = {
        "LogFrechet4978_MTS",
        "ScalarQuadraticTTT4978_MTS",
        "ScalarCubicTTT4978_MTS",
        "ScalarTTTAssembled4978_MTS",
        "DirectUVLogResidue4978_MTS",
        "PredictivityStatus4978_MTS",
    }
    variable_rows = read_csv(VARIABLE_AUDIT)
    present_variables = {row["symbol"] for row in variable_rows if row["symbol"] in expected_variables}
    check("V48_variable_rows", present_variables == expected_variables, str(sorted(present_variables)))
    claim_rows = read_csv(CLAIMS_REGISTER)
    check("V49_claim_row", sum(row["claim_id"] == "L-820" for row in claim_rows) == 1, "L-820 exactly once")
    check("V50_path_scope", path_scope_valid(), "git diff or explicit local allowlist")
    check("V51_no_script_pycache", not (POST / "scripts" / "__pycache__").exists(), "bytecode cache absent")

    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)
    passed = sum(bool(row["passed"]) for row in checks)
    VALIDATION_PROVENANCE.write_text(
        f"""# Checkpoint 4978 validation provenance

Marker: `{MARKER}`

- checks passed: `{passed}/{len(checks)}`
- validation CSV: `{VALIDATION.relative_to(ROOT).as_posix()}`
- validation CSV SHA256: `{digest(VALIDATION)}`
- runner SHA256: `{digest(RUNNER)}`
- validator SHA256: `{digest(VALIDATOR)}`
- maximum N6/N8 residual: `{max_grid:.17g}`
- maximum mu-identity residual: `{max_mu:.17g}`
- maximum source-permutation residual: `{max_permutation:.17g}`
- maximum direct determinant log-residue residual: `{max_direct:.17g}`
- complete source-side free-scalar metric TTT: `true`
- independently renormalized finite determinant match: `false`
- full MTS: `false`
""",
        encoding="utf-8",
    )
    print(f"{MARKER} {passed}/{len(checks)}")
    print(f"validation_sha256={digest(VALIDATION)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
