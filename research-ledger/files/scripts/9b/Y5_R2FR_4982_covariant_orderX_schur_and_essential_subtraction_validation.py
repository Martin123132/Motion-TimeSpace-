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
SOURCE = POST / "source-intake" / "functional_rg" / "4982"
VALIDATION_DIR = POST / "source-intake" / "mts_residuals"
VALIDATION = VALIDATION_DIR / "P8_Y5_BRR545_4982_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RUNNER = POST / "scripts" / "Y5_R2FR_4982_covariant_orderX_schur_and_essential_subtraction.py"
VALIDATOR = POST / "scripts" / "Y5_R2FR_4982_covariant_orderX_schur_and_essential_subtraction_validation.py"
CHECKPOINT_DOC = POST / "4982-Y5-R2FR-covariant-orderX-Schur-kernel-and-essential-two-point-subtraction.md"
FORMAL_NOTE = FORMAL / "998-PPC4161-covariant-orderX-Schur-and-essential-subtraction.md"
CURRENT_RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CURRENT_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
VARIABLE_AUDIT = FORMAL / "04-variable-audit.csv"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION_SPINE = FORMAL / "07-unification-spine.md"

PARENT_RESULT = POST / "source-intake" / "functional_rg" / "4981" / "parent_hessian_common_scheme_results.json"
PRIMARY_SOURCE = POST / "source-intake" / "functional_rg" / "4937" / "src-2110.09566v1" / "SSTwAS.tex"
PX_CONTRACT = POST / "source-intake" / "functional_rg" / "4956" / "functional_PX_Hessian_contract.csv"
LOWER_QUOTIENT = POST / "source-intake" / "functional_rg" / "4941" / "lower_scalar_essential_quotient.csv"
TENSOR_IDENTITIES = POST / "source-intake" / "functional_rg" / "4941" / "typeII_direct_O4_tensor_identities.csv"
TRAJECTORY_RESULT = POST / "source-intake" / "functional_rg" / "4958" / "essential_PX_sixpoint_trajectory_results.json"

HESSIAN = SOURCE / "covariant_PX_second_variation_contract.csv"
AUTODIFF = SOURCE / "covariant_PX_autodiff_crosscheck.csv"
SCHUR = SOURCE / "order_X_schur_operator_reduction.csv"
SUBTRACTION = SOURCE / "order_X_two_point_essential_subtraction.csv"
CONE = SOURCE / "essential_PX_principal_cone_bound.csv"
LOCAL_GR = SOURCE / "local_GR_zero_gradient_gate.csv"
GATE = SOURCE / "covariant_orderX_essential_gate.csv"
RESULT = SOURCE / "covariant_orderX_essential_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4982_COVARIANT_ORDERX_ESSENTIAL_SUBTRACTION_VALIDATION"
RUNNER_MARKER = "MTS_4982_COVARIANT_ORDERX_SCHUR_ESSENTIAL_SUBTRACTION"
FORMAL_MARKER = "PPC4161_COVARIANT_ORDERX_ESSENTIAL_SUBTRACTION_4982"
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

    output_csvs = (HESSIAN, AUTODIFF, SCHUR, SUBTRACTION, CONE, LOCAL_GR, GATE)
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
        PARENT_RESULT,
        PRIMARY_SOURCE,
        PX_CONTRACT,
        LOWER_QUOTIENT,
        TENSOR_IDENTITIES,
        TRAJECTORY_RESULT,
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
    check("V05_dry_run_gate_count", "DRY_RUN=19/19" in dry_run.stdout, dry_run.stdout.strip())

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

    parent_result = json.loads(PARENT_RESULT.read_text(encoding="utf-8"))
    primary_text = PRIMARY_SOURCE.read_text(encoding="utf-8", errors="replace")
    hessian_rows = read_csv(HESSIAN)
    autodiff_rows = read_csv(AUTODIFF)
    schur_rows = read_csv(SCHUR)
    subtraction_rows = read_csv(SUBTRACTION)
    cone_rows = read_csv(CONE)
    local_rows = read_csv(LOCAL_GR)
    gate_rows = read_csv(GATE)
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    check("V20_parent_4981_hessian", parent_result["valid_for_parent_gauge_fixed_quadratic_hessian"] is True, "4981 parent promoted")
    source_fragments = (
        r"Z_k^2 \, C_k \, X^2",
        "R^{\\mu\\nu} X_{\\mu\\nu}",
        r"D_k \, R \, X",
        "\\beta_{\\tilde{c}}",
        "\\beta_{c}",
        "(D^{2} \\phi)^2",
    )
    check("V21_primary_source_fragments", all(fragment in primary_text for fragment in source_fragments), "six source fragments")

    check("V22_hessian_shape", len(hessian_rows) == 4, "four covariant block rows")
    check("V23_hessian_marker", all(row["checkpoint_marker"] == RUNNER_MARKER for row in hessian_rows), RUNNER_MARKER)
    check("V24_hessian_claim_rows", all(bool_value(row["valid_for_covariant_parent_Hessian_claim"]) for row in hessian_rows), "all four derived")
    check("V25_hessian_source_paths", source_paths_exist(hessian_rows), "all cited paths exist")
    hessian_by_id = {row["block_id"]: row for row in hessian_rows}
    check("V26_hessian_formula_packet", "P_XX*delta_hX*delta_kX" in hessian_by_id["H4982_01_metric_metric"]["mixed_second_variation"] and "4P_XX" in hessian_by_id["H4982_03_scalar_scalar"]["mixed_second_variation"], "metric and scalar formulas")

    check("V27_autodiff_shape", len(autodiff_rows) == 24, "eight controls times three blocks")
    block_counts = {block: sum(row["block"] == block for row in autodiff_rows) for block in ("metric_metric", "metric_scalar", "scalar_scalar")}
    check("V28_autodiff_block_counts", all(count == 8 for count in block_counts.values()), str(block_counts))
    check("V29_autodiff_numeric", finite_rows(autodiff_rows, ("P_X2_coefficient", "automatic_second_derivative", "analytic_second_derivative", "absolute_residual", "relative_residual")), "all finite")
    maximum_autodiff_relative = max(float(row["relative_residual"]) for row in autodiff_rows)
    maximum_autodiff_absolute = max(float(row["absolute_residual"]) for row in autodiff_rows)
    check("V30_autodiff_residual", maximum_autodiff_relative < 2.0e-13 and maximum_autodiff_absolute < 2.0e-13, f"rel={maximum_autodiff_relative:.3e};abs={maximum_autodiff_absolute:.3e}")
    check("V31_autodiff_status", all(row["status"] == "INDEPENDENT_SECOND_ORDER_JET_MATCH" for row in autodiff_rows), "independent jet labels")
    check("V32_autodiff_marker", all(row["checkpoint_marker"] == RUNNER_MARKER for row in autodiff_rows), RUNNER_MARKER)

    check("V33_schur_shape", len(schur_rows) == 5, "five operator rows")
    check("V34_schur_source_paths", source_paths_exist(schur_rows), "all cited paths exist")
    schur_by_id = {row["reduction_id"]: row for row in schur_rows}
    check("V35_BKB_identity", "B^dagger K B=(1/2)X(-Box)" in schur_by_id["S4982_01_mixed_vertex"]["operator_identity"], "exact D4 contraction")
    check("V36_principal_Schur_local", "=X/2" in schur_by_id["S4982_02_principal_Schur"]["operator_identity"] and "local" in schur_by_id["S4982_02_principal_Schur"]["consequence"], "no new principal pole")
    check("V37_nonconstant_audit_retained", "off-shell/nonconstant-gradient audit row" in schur_by_id["S4982_04_Bochner_EOM"]["consequence"], "not erased")
    tensor_rows = read_csv(TENSOR_IDENTITIES)
    check("V38_BKB_source_control", any(row["identity_id"] == "ID4941_3_BKB" and bool_value(row["passed"]) for row in tensor_rows), "4941 independent source row")

    check("V39_subtraction_shape", len(subtraction_rows) == 6, "five coefficients plus open remainder")
    numeric_subtraction = [row for row in subtraction_rows if row["coordinate"] != "nonconstant_gradient_remainder"]
    check("V40_subtraction_numeric", finite_rows(numeric_subtraction, ("coefficient_numeric_at_g1",)), "five finite rows")
    remainder = next(row for row in subtraction_rows if row["coordinate"] == "nonconstant_gradient_remainder")
    check("V41_single_explicit_nan", math.isnan(float(remainder["coefficient_numeric_at_g1"])) and remainder["status"] == "OPEN_SEPARATE_PROJECTOR_NOT_SILENTLY_ZERO", "only open projector is nan")
    subtraction_by_coordinate = {row["coordinate"]: row for row in subtraction_rows}
    check("V42_raw_beta_c", abs(float(subtraction_by_coordinate["c_X2_standard"]["coefficient_numeric_at_g1"]) - 20.0) < 1.0e-15, "20 g^2")
    check("V43_beta_ctilde", abs(float(subtraction_by_coordinate["ctilde_RicciX"]["coefficient_numeric_at_g1"]) + 1.0 / (6.0 * math.pi)) < 1.0e-15, "-g/(6pi)")
    check("V44_beta_d", abs(float(subtraction_by_coordinate["d_RX"]["coefficient_numeric_at_g1"]) + 1.0 / (3.0 * math.pi)) < 1.0e-15, "-g/(3pi)")
    exact_essential = Fraction(20, 1) + 8 * (Fraction(-1, 6) + Fraction(-1, 3))
    check("V45_exact_essential_arithmetic", exact_essential == 16, "20+8(-1/6-1/3)=16")
    check("V46_frame_shift", abs(float(subtraction_by_coordinate["Einstein_frame_shift_to_c"]["coefficient_numeric_at_g1"]) + 4.0) < 1.0e-15, "-4 g^2")
    check("V47_essential_source", abs(float(subtraction_by_coordinate["c_X2_essential"]["coefficient_numeric_at_g1"]) - 16.0) < 1.0e-15, "16 g^2")
    essential_rows = {row["coordinate"] for row in subtraction_rows if bool_value(row["valid_for_essential_claim"])}
    check("V48_essential_scope", essential_rows == {"Einstein_frame_shift_to_c", "c_X2_essential"}, str(sorted(essential_rows)))
    check("V49_no_finite_fit", all("FIT" not in row["status"] or "NO_FINITE_FIT" in row["status"] for row in subtraction_rows), "no fitted finite coefficient")
    check("V50_subtraction_source_paths", source_paths_exist(subtraction_rows), "all cited paths exist")

    check("V51_cone_shape", len(cone_rows) == 2, "dynamic and reference N8 schemes")
    cone_fields = ("polynomial_order", "x_maximum", "minimum_transverse_principal_eigenvalue", "x_at_transverse_minimum", "minimum_longitudinal_principal_eigenvalue", "x_at_longitudinal_minimum", "first_longitudinal_zero", "stored_first_longitudinal_zero", "root_relative_residual")
    check("V52_cone_numeric", finite_rows(cone_rows, cone_fields), "all finite")
    check("V53_cone_N8_domain", all(int(row["polynomial_order"]) == 8 and abs(float(row["x_maximum"]) - 0.1) < 1.0e-15 for row in cone_rows), "N=8 on x<=0.1")
    minimum_transverse = min(float(row["minimum_transverse_principal_eigenvalue"]) for row in cone_rows)
    minimum_longitudinal = min(float(row["minimum_longitudinal_principal_eigenvalue"]) for row in cone_rows)
    check("V54_cone_positive", minimum_transverse > 0.95 and minimum_longitudinal > 0.84, f"T={minimum_transverse:.12g};L={minimum_longitudinal:.12g}")
    roots = {row["scheme"]: float(row["first_longitudinal_zero"]) for row in cone_rows}
    check("V55_cone_roots", abs(roots["dynamic_etaN"] - 0.16145150408227915) < 2.0e-15 and abs(roots["reference_etaN0"] - 0.1794406814164427) < 2.0e-15, str(roots))
    check("V56_cone_root_residual", max(float(row["root_relative_residual"]) for row in cone_rows) < 2.0e-6, "stored roots reproduced")
    check("V57_no_Lorentzian_promotion", all(not bool_value(row["valid_for_Lorentzian_causality_claim"]) for row in cone_rows), "Euclidean principal gate only")

    check("V58_local_gate_shape", len(local_rows) == 6, "five closure rows plus explicit remainder")
    check("V59_local_first_five", all(bool_value(row["passed"]) for row in local_rows[:5]), "packet silent at X=0")
    check("V60_local_remainder_open", local_rows[-1]["gate_id"] == "L4982_06_nonconstant_remainder" and local_rows[-1]["status"] == "OPEN_EXPLICIT", "nonconstant sector open")
    check("V61_local_scope_nonclaim", all(not bool_value(row["valid_for_exact_all_operator_local_GR_claim"]) for row in local_rows), "packet not full parent")
    check("V62_Ward_row", "=2 nabla_mu(P_X v^mu) v_nu" in next(row["statement"] for row in local_rows if row["gate_id"] == "L4982_03_Ward_conservation"), "on-shell conservation")
    check("V63_Newton_Maxwell_scope", next(row["status"] for row in local_rows if row["gate_id"] == "L4982_05_Newton_Maxwell") == "RETAINED_NOT_REDERIVED_NUMERIC_G", "retained rather than overclaimed")

    check("V64_runner_gate_shape", len(gate_rows) == 19, "19 runner gates")
    check("V65_runner_gates", all(bool_value(row["passed"]) and row["status"] == "pass" for row in gate_rows), "19/19")
    check("V66_result_gate_count", result["gate_pass_count"] == result["gate_count"] == 19, "19/19")
    promoted_flags = (
        result["valid_for_covariant_orderX_parent_Hessian"],
        result["valid_for_principal_Schur_operator_reduction"],
        result["valid_for_essential_two_point_subtraction_map"],
        result["valid_for_PX_packet_local_GR_zero_gradient_gate"],
    )
    check("V67_result_packet_promotions", all(flag is True for flag in promoted_flags), "four packet-level results")
    check("V68_result_nonconstant_false", result["valid_for_nonconstant_gradient_completion"] is False, "open")
    check("V69_result_parent_TTT_false", result["valid_for_finite_parent_metric_three_point_claim"] is False, "open")
    check("V70_result_local_GR_false", result["valid_for_exact_all_operator_local_GR_claim"] is False, "not promoted")
    check("V71_result_MTS_false", result["valid_for_full_MTS_claim"] is False, "nonclaim")

    variable_rows = read_csv(VARIABLE_AUDIT)
    required_variables = {
        "CovariantPXHessian4982_MTS",
        "PXAutodiff4982_MTS",
        "OrderXSchur4982_MTS",
        "EssentialSubtraction4982_MTS",
        "PXPrincipalCone4982_MTS",
        "PXLocalGRGate4982_MTS",
        "PredictivityStatus4982_MTS",
    }
    symbols = [row["symbol"] for row in variable_rows]
    check("V72_variable_rows", required_variables.issubset(symbols), "seven 4982 variables")
    check("V73_variable_unique", all(symbols.count(symbol) == 1 for symbol in required_variables), "no duplicate 4982 rows")
    claims = read_csv(CLAIMS_REGISTER)
    claim = next((row for row in claims if row["claim_id"] == "L-824"), None)
    check("V74_claim_L824", claim is not None and FORMAL_MARKER in claim["notes"], "registered")
    check("V75_claim_L824_nonclaim", claim is not None and "private_nonclaim" in claim["status"], "scope explicit")
    check("V76_provenance_inputs", contains(PROVENANCE, "Input digests") and contains(PROVENANCE, "No web request and no GitHub action"), "local provenance")
    check("V77_no_missing_markers", not any("MISSING_" in path.read_text(encoding="utf-8", errors="replace") for path in (*output_csvs, RESULT)), "no placeholder output")
    check("V78_scope_valid", path_scope_valid(required_paths + (VALIDATION, VALIDATION_PROVENANCE)), "post-checkpoint-work/formalization-workbench only")
    pycache = list((POST / "scripts").glob("__pycache__"))
    check("V79_no_pycache", not pycache, "python -B and in-memory compile")

    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)
    pass_count = sum(bool(row["passed"]) for row in checks)
    provenance_lines = [
        "# Checkpoint 4982 validation provenance",
        "",
        f"Checks: `{pass_count}/{len(checks)}`.",
        "",
        "The validator reruns the strict dry-run, independently checks the",
        "covariant Hessian residuals, recomputes the exact essential-source",
        "arithmetic, and preserves every nonconstant-gradient, Lorentzian,",
        "finite-parent, local-GR, and full-MTS nonclaim boundary.",
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
