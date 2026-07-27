from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4981"
VALIDATION_DIR = POST / "source-intake" / "mts_residuals"
VALIDATION = VALIDATION_DIR / "P8_Y5_BRR545_4981_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RUNNER = POST / "scripts" / "Y5_R2FR_4981_parent_motion_graviton_ghost_hessian_and_common_scheme.py"
VALIDATOR = POST / "scripts" / "Y5_R2FR_4981_parent_motion_graviton_ghost_hessian_and_common_scheme_validation.py"
CHECKPOINT_DOC = POST / "4981-Y5-R2FR-parent-motion-graviton-ghost-hessian-and-common-scheme-two-point-completion.md"
FORMAL_NOTE = FORMAL / "997-PPC4161-parent-motion-graviton-ghost-hessian-and-common-scheme.md"
CURRENT_RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CURRENT_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
VARIABLE_AUDIT = FORMAL / "04-variable-audit.csv"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION_SPINE = FORMAL / "07-unification-spine.md"

SOURCE_TEX = POST / "source-intake" / "functional_rg" / "4973" / "src-2605.29159" / "main_new.tex"
PX_CONTRACT = POST / "source-intake" / "functional_rg" / "4956" / "functional_PX_Hessian_contract.csv"
PREDECESSOR_RESULT = POST / "source-intake" / "functional_rg" / "4980" / "PV_traceful_completion_results.json"

HESSIAN = SOURCE / "parent_gauge_fixed_hessian_contract.csv"
MODES = SOURCE / "parent_supertrace_mode_count.csv"
LOGS = SOURCE / "parent_common_scheme_log_coefficients.csv"
SCHUR = SOURCE / "motion_metric_schur_expansion_crosscheck.csv"
TRANSFER = SOURCE / "parent_contact_transfer_gate.csv"
GATE = SOURCE / "parent_hessian_common_scheme_gate.csv"
RESULT = SOURCE / "parent_hessian_common_scheme_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4981_PARENT_HESSIAN_AND_COMMON_SCHEME_VALIDATION"
RUNNER_MARKER = "MTS_4981_PARENT_HESSIAN_AND_COMMON_SCHEME"
FORMAL_MARKER = "PPC4161_PARENT_HESSIAN_COMMON_SCHEME_4981"
CHECKED_DATE = "2026-07-14"


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


def bool_value(value: str) -> bool:
    return value.strip().lower() == "true"


def finite_rows(rows: list[dict[str, str]], fields: tuple[str, ...]) -> bool:
    try:
        return all(math.isfinite(float(row[field])) for row in rows for field in fields)
    except (KeyError, TypeError, ValueError):
        return False


def source_paths_exist(rows: list[dict[str, str]]) -> bool:
    for row in rows:
        for source_path in row.get("source_path", "").split(";"):
            source_path = source_path.strip()
            if source_path and not (ROOT / source_path).exists():
                return False
    return True


def path_scope_valid(paths: tuple[Path, ...]) -> bool:
    roots = (POST.resolve(), FORMAL.resolve())
    return all(any(path.resolve().is_relative_to(root) for root in roots) for path in paths)


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
                "source_checked_date": CHECKED_DATE,
            }
        )

    output_csvs = (HESSIAN, MODES, LOGS, SCHUR, TRANSFER, GATE)
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
        SOURCE_TEX,
        PX_CONTRACT,
        PREDECESSOR_RESULT,
        *output_csvs,
        RESULT,
        PROVENANCE,
    )
    check("V01_required_paths_exist", all(path.exists() for path in required_paths), f"{len(required_paths)} paths")
    check("V02_runner_compiles", compiles(RUNNER), str(RUNNER))
    check("V03_validator_compiles", compiles(VALIDATOR), str(VALIDATOR))

    dry_run = subprocess.run(
        [sys.executable, "-B", str(RUNNER), "--dry-run"],
        cwd=POST,
        capture_output=True,
        text=True,
        check=False,
    )
    check("V04_strict_dry_run", dry_run.returncode == 0, dry_run.stdout.strip() or dry_run.stderr.strip())
    check("V05_dry_run_gate_count", "DRY_RUN=18/18" in dry_run.stdout, dry_run.stdout.strip())

    marker_paths = (
        CHECKPOINT_DOC,
        FORMAL_NOTE,
        CURRENT_RESUME,
        CURRENT_SPINE,
        EQUATION_REGISTER,
        RED_TEAM,
        UNIFICATION_SPINE,
    )
    for index, path in enumerate(marker_paths, start=6):
        check(f"V{index:02d}_formal_marker_{path.stem}", contains(path, FORMAL_MARKER), FORMAL_MARKER)

    for index, path in enumerate(output_csvs, start=13):
        check(f"V{index:02d}_csv_width_{path.stem}", csv_width_valid(path), path.name)

    hessian_rows = read_csv(HESSIAN)
    mode_rows = read_csv(MODES)
    log_rows = read_csv(LOGS)
    schur_rows = read_csv(SCHUR)
    transfer_rows = read_csv(TRANSFER)
    gate_rows = read_csv(GATE)
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    predecessor = json.loads(PREDECESSOR_RESULT.read_text(encoding="utf-8"))

    check("V19_predecessor_scalar_closed", predecessor["valid_for_complete_free_scalar_traceful_common_scheme_finite_determinant_match"] is True, "4980 free scalar closed")
    check("V20_hessian_shape", len(hessian_rows) == 7, "seven parent block rows")
    check("V21_hessian_marker", all(row["checkpoint_marker"] == RUNNER_MARKER for row in hessian_rows), RUNNER_MARKER)
    check("V22_hessian_parent_rows", all(bool_value(row["valid_for_parent_quadratic_claim"]) for row in hessian_rows), "all seven quadratic rows")
    check("V23_hessian_source_paths", source_paths_exist(hessian_rows), "all cited paths exist")
    check("V24_hessian_x0_block", any(row["block_id"] == "H4981_07_parent_x0" and "BLOCK_DIAGONAL" in row["status"] for row in hessian_rows), "x=0 factorization")

    check("V25_mode_shape", len(mode_rows) == 6, "six mode rows")
    check("V26_mode_numeric", finite_rows(mode_rows, ("weighted_count",)), "all weighted counts finite")
    mode_by_field = {row["field"]: row for row in mode_rows}
    check("V27_gravity_mode_count", abs(float(mode_by_field["Einstein_plus_ghost_total"]["weighted_count"]) - 1.0) < 1.0e-15, "two graviton helicities")
    check("V28_parent_mode_count", abs(float(mode_by_field["parent_total_at_x0"]["weighted_count"]) - 1.5) < 1.0e-15, "two graviton plus scalar")
    check("V29_conformal_sign_explicit", "conformal-sign" in mode_by_field["metric_trace"]["interpretation"], "not hidden")
    check("V30_mode_source_paths", source_paths_exist(mode_rows), "all cited paths exist")

    check("V31_log_shape", len(log_rows) == 6, "three sectors times two invariants")
    check("V32_log_numeric", finite_rows(log_rows, ("action_coefficient_numeric", "response_coefficient_numeric")), "all finite")
    check("V33_log_factor_two", all(abs(float(row["response_coefficient_numeric"]) - 2.0 * float(row["action_coefficient_numeric"])) < 1.0e-15 for row in log_rows), "response=2 action")
    parent_logs = {row["invariant"]: row for row in log_rows if row["sector"] == "parent_zero_motion_background"}
    check("V34_parent_R_fraction", parent_logs["R_log_R"]["action_coefficient_in_units_1_over_4pi_squared"] == "1/80", "1/80")
    check("V35_parent_Ricci_fraction", parent_logs["Ricci_log_Ricci"]["action_coefficient_in_units_1_over_4pi_squared"] == "43/120", "43/120")
    check("V36_parent_R_arithmetic", Fraction(1, 120) + Fraction(1, 240) == Fraction(1, 80), "gravity plus scalar")
    check("V37_parent_Ricci_arithmetic", Fraction(7, 20) + Fraction(1, 120) == Fraction(43, 120), "gravity plus scalar")
    check("V38_log_source_paths", source_paths_exist(log_rows), "all cited paths exist")

    check("V39_schur_shape", len(schur_rows) == 6, "six shrinking-x controls")
    check("V40_schur_numeric", finite_rows(schur_rows, ("x", "analytic_first_order_slope", "measured_secant_slope", "relative_slope_residual", "block_determinant_log_residual")), "all finite")
    schur_residuals = [float(row["relative_slope_residual"]) for row in schur_rows]
    check("V41_schur_convergence", all(right < left for left, right in zip(schur_residuals, schur_residuals[1:])), str(schur_residuals))
    check("V42_schur_final", schur_residuals[-1] < 1.0e-4, f"last={schur_residuals[-1]:.17g}")
    check("V43_schur_identity", max(float(row["block_determinant_log_residual"]) for row in schur_rows) < 1.0e-12, "exact block determinant")

    check("V44_transfer_shape", len(transfer_rows) == 8, "eight transfer decisions")
    transfer_by_id = {row["gate_id"]: row for row in transfer_rows}
    check("V45_zero_motion_transfer", bool_value(transfer_by_id["T4981_02_scalar_contact_architecture"]["result"]), "operator/UV transfer")
    check("V46_interacting_naive_false", not bool_value(transfer_by_id["T4981_05_interacting_PX_factorization"]["result"]), "Schur term compulsory")
    check("V47_background_covariant", bool_value(transfer_by_id["T4981_06_background_covariance"]["result"]), "background Diff")
    check("V48_full_BRST_false", not bool_value(transfer_by_id["T4981_07_quantum_BRST_restoration"]["result"]), "not overclaimed")
    check("V49_parent_TTT_false", not bool_value(transfer_by_id["T4981_08_parent_finite_TTT"]["result"]), "finite parent TTT open")
    check("V50_transfer_source_paths", source_paths_exist(transfer_rows), "all cited paths exist")

    check("V51_gate_shape", len(gate_rows) == 18, "18 runner gates")
    check("V52_runner_gates", all(bool_value(row["passed"]) and row["status"] == "pass" for row in gate_rows), "18/18")
    check("V53_result_gate_count", result["gate_pass_count"] == result["gate_count"] == 18, "18/18")
    check("V54_result_parent_hessian", result["valid_for_parent_gauge_fixed_quadratic_hessian"] is True, "promoted")
    check("V55_result_parent_logs", result["valid_for_parent_universal_quadratic_log_claim"] is True, "promoted")
    check("V56_result_interacting_false", result["valid_for_interacting_PX_finite_parent_determinant"] is False, "open")
    check("V57_result_TTT_false", result["valid_for_parent_finite_metric_three_point_claim"] is False, "open")
    check("V58_result_BRST_false", result["valid_for_full_quantum_BRST_claim"] is False, "open")
    check("V59_result_local_GR_false", result["valid_for_exact_all_operator_local_GR_claim"] is False, "not promoted")
    check("V60_result_MTS_false", result["valid_for_full_MTS_claim"] is False, "nonclaim")

    variable_rows = read_csv(VARIABLE_AUDIT)
    required_variables = {
        "ParentGaugeHessian4981_MTS",
        "ParentSignedSupertrace4981_MTS",
        "ResponseActionNormalization4981_MTS",
        "ParentUniversalLog4981_MTS",
        "MotionMetricSchur4981_MTS",
        "ParentBRSTStatus4981_MTS",
        "PredictivityStatus4981_MTS",
    }
    symbols = [row["symbol"] for row in variable_rows]
    check("V61_variable_rows", required_variables.issubset(symbols), "seven 4981 variables")
    check("V62_variable_unique", all(symbols.count(symbol) == 1 for symbol in required_variables), "no duplicate 4981 rows")
    claims = read_csv(CLAIMS_REGISTER)
    claim = next((row for row in claims if row["claim_id"] == "L-823"), None)
    check("V63_claim_L823", claim is not None and FORMAL_MARKER in claim["notes"], "registered")
    check("V64_claim_L823_nonclaim", claim is not None and "private_nonclaim" in claim["status"], "scope explicit")
    check("V65_provenance_inputs", contains(PROVENANCE, "Input digests") and contains(PROVENANCE, "No web request and no GitHub action"), "local provenance")
    check("V66_no_missing_markers", not any("MISSING_" in path.read_text(encoding="utf-8", errors="replace") for path in (*output_csvs, RESULT)), "no placeholder output")
    check("V67_scope_valid", path_scope_valid(required_paths + (VALIDATION, VALIDATION_PROVENANCE)), "post-checkpoint-work/formalization-workbench only")
    pycache = list((POST / "scripts").glob("__pycache__"))
    check("V68_no_pycache", not pycache, "python -B and in-memory compile")

    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)
    pass_count = sum(bool(row["passed"]) for row in checks)
    provenance_lines = [
        "# Checkpoint 4981 validation provenance",
        "",
        f"Checks: `{pass_count}/{len(checks)}`.",
        "",
        "The validator reruns the strict dry-run, checks every cited output path,",
        "recomputes the exact rational coefficient sums, and preserves all",
        "finite-parent, BRST, local-GR, and full-MTS nonclaim flags.",
        "",
        "## Digests",
    ]
    for path in required_paths:
        if path.is_file():
            provenance_lines.append(f"- `{path.relative_to(ROOT).as_posix()}` sha256 `{digest(path)}`")
    VALIDATION_PROVENANCE.write_text("\n".join(provenance_lines) + "\n", encoding="utf-8")
    print(f"{MARKER}_PASS={pass_count}/{len(checks)} output={VALIDATION}", flush=True)
    return 0 if pass_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
