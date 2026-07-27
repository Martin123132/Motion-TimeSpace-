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
SOURCE = POST / "source-intake" / "functional_rg" / "4984"
VALIDATION_DIR = POST / "source-intake" / "mts_residuals"
VALIDATION = VALIDATION_DIR / "P8_Y5_BRR545_4984_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RUNNER = POST / "scripts" / "Y5_R2FR_4984_running_frame_six_derivative_spillover_and_nonlocal_silence.py"
VALIDATOR = POST / "scripts" / "Y5_R2FR_4984_running_frame_six_derivative_spillover_and_nonlocal_silence_validation.py"
CHECKPOINT_DOC = POST / "4984-Y5-R2FR-running-essential-frame-six-derivative-spillover-and-nonlocal-source-silence.md"
FORMAL_NOTE = FORMAL / "1000-PPC4161-running-frame-p6-and-nonlocal-source-silence.md"
CURRENT_RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CURRENT_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
VARIABLE_AUDIT = FORMAL / "04-variable-audit.csv"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION_SPINE = FORMAL / "07-unification-spine.md"

RESULT_4983 = POST / "source-intake" / "functional_rg" / "4983" / "box2_essential_local_profile_results.json"
BASIS_4930 = POST / "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md"
EFT_SOURCE = POST / "source-intake" / "functional_rg" / "4930" / "src1908" / "GravityEFTv2_final.tex"
QUOTIENT_4958 = POST / "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md"
PROJECTOR_4959 = POST / "4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-full-invariant-amplitude-or-curvature-route-rejection.md"
RESULT_4959 = POST / "source-intake" / "functional_rg" / "4959" / "curvature_sixpoint_projector_results.json"
SOURCE_SELECTION = POST / "source-intake" / "functional_rg" / "4943" / "matter_source_selection_rules.csv"
JUNCTION_SOURCE = POST / "source-intake" / "functional_rg" / "4943" / "junction_scalar_charge_and_fifth_force.csv"
PARENT_HESSIAN_RESULT = POST / "source-intake" / "functional_rg" / "4981" / "parent_hessian_common_scheme_results.json"

GRADING = SOURCE / "running_frame_derivative_grading.csv"
SPILLOVER = SOURCE / "running_frame_six_derivative_spillover.csv"
IBP = SOURCE / "running_frame_IBP_jet_crosscheck.csv"
PROJECTOR = SOURCE / "running_frame_flat_onshell_projector.csv"
NONLOCAL = SOURCE / "nonlocal_two_point_source_silence_theorem.csv"
BRANCH = SOURCE / "selected_branch_six_derivative_silence_gate.csv"
GATE = SOURCE / "running_frame_nonlocal_silence_gate.csv"
RESULT = SOURCE / "running_frame_nonlocal_silence_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4984_RUNNING_FRAME_P6_NONLOCAL_SILENCE_VALIDATION"
RUNNER_MARKER = "MTS_4984_RUNNING_FRAME_P6_NONLOCAL_SILENCE"
FORMAL_MARKER = "PPC4161_RUNNING_FRAME_P6_NONLOCAL_SILENCE_4984"
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

    output_csvs = (GRADING, SPILLOVER, IBP, PROJECTOR, NONLOCAL, BRANCH, GATE)
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
        RESULT_4983,
        BASIS_4930,
        EFT_SOURCE,
        QUOTIENT_4958,
        PROJECTOR_4959,
        RESULT_4959,
        SOURCE_SELECTION,
        JUNCTION_SOURCE,
        PARENT_HESSIAN_RESULT,
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
    check("V05_dry_run_gate_count", "DRY_RUN=32/32" in dry_run.stdout, dry_run.stdout.strip())

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

    predecessor = json.loads(RESULT_4983.read_text(encoding="utf-8"))
    projector_source = json.loads(RESULT_4959.read_text(encoding="utf-8"))
    grading_rows = read_csv(GRADING)
    spillover_rows = read_csv(SPILLOVER)
    ibp_rows = read_csv(IBP)
    projector_rows = read_csv(PROJECTOR)
    nonlocal_rows = read_csv(NONLOCAL)
    branch_rows = read_csv(BRANCH)
    gate_rows = read_csv(GATE)
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    check("V20_predecessor", predecessor["valid_for_selected_parent_Box2_zero_motion_local_branch"] is True, "4983 branch")
    check("V21_projector_source", projector_source["gates"]["O2_projector"] == "DERIVED_GAUGE_COMPLETE", "4959 O2")
    check("V22_source_basis", all(fragment in BASIS_4930.read_text(encoding="utf-8", errors="replace") for fragment in ("O2=(nabla phi)^2", "O3=C_mn^rs C^mnab C_abrs", "O4=(C_abrs C^abrs)(nabla phi)^2")), "O2/O3/O4")

    check("V23_grading_shape", len(grading_rows) == 10, "ten rows")
    check("V24_grading_sources", source_paths_exist(grading_rows), "all source paths")
    grading_by_id = {row["grading_id"]: row for row in grading_rows}
    check("V25_kinetic_shift", "b_new=b-2Zs" in grading_by_id["DG4984_01_kinetic"]["six_derivative_effect"], "factor two")
    check("V26_Box2_surface", "O(dt^2)" in grading_by_id["DG4984_02_Box2_surface"]["six_derivative_effect"], "no first-order p6 term")
    check("V27_X2_map", "-4cs X Y^2-8cs" in grading_by_id["DG4984_03_X2"]["frame_variation"], "raw connection")
    check("V28_curvature_surface", grading_by_id["DG4984_04_RicciX"]["essential_O2_shift"] == "0 on ctilde=0" and grading_by_id["DG4984_05_RX"]["essential_O2_shift"] == "0 on d=0", "minimal surface")
    check("V29_six_to_eight", grading_by_id["DG4984_06_O2"]["output_derivative_order"] == "8" and grading_by_id["DG4984_08_O4"]["output_derivative_order"] == "8", "triangular grading")
    check("V30_O3_scalar_trivial", grading_by_id["DG4984_07_O3"]["frame_variation"] == "classical scalar substitution acts trivially", "pure metric")
    check("V31_source_map", "J_new=J+s Box J" in grading_by_id["DG4984_09_source"]["frame_variation"], "source connection")
    check("V32_Jacobian_open", grading_by_id["DG4984_10_Jacobian"]["quantum_measure_status"] == "PURE_METRIC_JACOBIAN_OPEN", "not dropped")

    check("V33_spillover_shape", len(spillover_rows) == 9, "nine p6 coordinates")
    check("V34_spillover_sources", source_paths_exist(spillover_rows), "all source paths")
    spillover_by_id = {row["spillover_id"]: row for row in spillover_rows}
    check("V35_A6_beta", spillover_by_id["SP4984_01_A6"]["connection_beta"] == "-4 c gamma_Box", "-4c gamma")
    check("V36_B6_beta", spillover_by_id["SP4984_02_B6"]["connection_beta"] == "-8 c gamma_Box", "-8c gamma")
    check("V37_A6_B6_EOM", bool_value(spillover_by_id["SP4984_01_A6"]["contains_explicit_leading_EOM"]) and bool_value(spillover_by_id["SP4984_02_B6"]["contains_explicit_leading_EOM"]), "explicit Box psi")
    check("V38_essential_shifts_numeric", finite_rows(spillover_rows, ("essential_six_derivative_shift",)) and all(float(row["essential_six_derivative_shift"]) == 0.0 for row in spillover_rows), "all zero")
    check("V39_O2_genuine_open", spillover_by_id["SP4984_06_O2"]["status"] == "ESSENTIAL_O2_NOT_CONTAMINATED_GENUINE_BETA_OPEN", "connection versus genuine beta")
    check("V40_O3_quantum_open", spillover_by_id["SP4984_07_O3"]["status"] == "CLASSICAL_ZERO_QUANTUM_MEASURE_OPEN", "measure retained")
    check("V41_O5_reflection", spillover_by_id["SP4984_09_O5"]["status"].startswith("REFLECTION_ODD_EXCLUDED"), "selected parent")

    check("V42_IBP_shape", len(ibp_rows) == 24, "24 controls")
    signature_counts = {signature: sum(row["signature"] == signature for row in ibp_rows) for signature in ("Euclidean", "Lorentzian_local_jet")}
    check("V43_IBP_signatures", signature_counts == {"Euclidean": 12, "Lorentzian_local_jet": 12}, str(signature_counts))
    ibp_fields = ("X", "Y_Box_psi", "vvH", "v_dot_nablaY", "coefficient_c", "gamma_Box", "direct_delta_cX2", "boundary_divergence", "reduced_EOM_bulk", "reconstructed_delta_cX2", "absolute_residual", "relative_residual")
    check("V44_IBP_numeric", finite_rows(ibp_rows, ibp_fields), "all finite")
    maximum_ibp_relative = max(float(row["relative_residual"]) for row in ibp_rows)
    maximum_ibp_absolute = max(float(row["absolute_residual"]) for row in ibp_rows)
    check("V45_IBP_residual", maximum_ibp_relative < 2.0e-13 and maximum_ibp_absolute < 2.0e-13, f"rel={maximum_ibp_relative:.3e};abs={maximum_ibp_absolute:.3e}")
    direct_residuals = []
    reconstruction_residuals = []
    for row in ibp_rows:
        kinetic = float(row["X"])
        box_psi = float(row["Y_Box_psi"])
        vv_hessian = float(row["vvH"])
        v_gradient = float(row["v_dot_nablaY"])
        coefficient = float(row["coefficient_c"])
        gamma_box = float(row["gamma_Box"])
        expected_direct = 4.0 * coefficient * gamma_box * kinetic * v_gradient
        expected_divergence = 4.0 * coefficient * gamma_box * (
            2.0 * box_psi * vv_hessian + kinetic * v_gradient + kinetic * box_psi**2
        )
        expected_bulk = -4.0 * coefficient * gamma_box * kinetic * box_psi**2 - 8.0 * coefficient * gamma_box * box_psi * vv_hessian
        direct_residuals.append(abs(expected_direct - float(row["direct_delta_cX2"])))
        reconstruction_residuals.append(abs(expected_direct - expected_divergence - expected_bulk))
    check("V46_IBP_formula_recomputed", max(direct_residuals) < 2.0e-14 and max(reconstruction_residuals) < 2.0e-13, f"direct={max(direct_residuals):.3e};identity={max(reconstruction_residuals):.3e}")
    check("V47_IBP_status", all(row["status"] == "COVARIANT_LOCAL_JET_IBP_IDENTITY_MATCH" for row in ibp_rows), "all matched")

    check("V48_projector_shape", len(projector_rows) == 14, "14 events")
    projector_fields = ("scattering_angle_radians", "maximum_external_mass_shell_residual", "momentum_conservation_residual", "s_plus_t_plus_u_residual", "s", "t", "u", "P_A_XBox2", "P_B_BoxvvH", "P_O2_minus3stu", "induced_running_frame_projector", "absolute_induced_to_O2_ratio")
    check("V49_projector_numeric", finite_rows(projector_rows, projector_fields), "all finite")
    maximum_shell = max(max(float(row["maximum_external_mass_shell_residual"]), float(row["momentum_conservation_residual"]), float(row["s_plus_t_plus_u_residual"])) for row in projector_rows)
    check("V50_projector_shell", maximum_shell < 2.0e-14, f"{maximum_shell:.3e}")
    o2_residual = max(abs(float(row["P_O2_minus3stu"]) + 3.0 * float(row["s"]) * float(row["t"]) * float(row["u"])) for row in projector_rows)
    check("V51_O2_formula", o2_residual < 2.0e-14, f"{o2_residual:.3e}")
    induced_residual = max(abs(float(row["induced_running_frame_projector"]) - (-4.0 * 0.731 * float(row["P_A_XBox2"]) - 8.0 * 0.731 * float(row["P_B_BoxvvH"]))) for row in projector_rows)
    check("V52_induced_formula", induced_residual < 2.0e-28, f"{induced_residual:.3e}")
    maximum_ratio = max(float(row["absolute_induced_to_O2_ratio"]) for row in projector_rows)
    minimum_o2 = min(abs(float(row["P_O2_minus3stu"])) for row in projector_rows)
    check("V53_induced_zero", maximum_ratio < 2.0e-13, f"{maximum_ratio:.3e}")
    check("V54_O2_nonzero", minimum_o2 > 1.0, f"{minimum_o2:.6g}")
    check("V55_projector_status", all(row["status"] == "MASSLESS_ONSHELL_REDUNDANT_PACKET_ZERO_O2_NONZERO" for row in projector_rows), "all events")

    check("V56_nonlocal_shape", len(nonlocal_rows) == 10, "ten theorem rows")
    check("V57_nonlocal_sources", source_paths_exist(nonlocal_rows), "all source paths")
    check("V58_nonlocal_scope", all(bool_value(row["valid_for_selected_nonlocal_source_silence_claim"]) for row in nonlocal_rows[:7]) and all(not bool_value(row["valid_for_selected_nonlocal_source_silence_claim"]) for row in nonlocal_rows[7:]), "seven theorem rows, three boundaries")
    nonlocal_by_id = {row["theorem_id"]: row for row in nonlocal_rows}
    check("V59_kernel_generality", "F_H(-Box)" in nonlocal_by_id["NL4984_01_kernel"]["assumption_or_identity"] and "ANALYTIC_OR_NONANALYTIC" in nonlocal_by_id["NL4984_01_kernel"]["status"], "covariant kernel")
    check("V60_classical_stress", nonlocal_by_id["NL4984_02_metric"]["consequence_at_psi_zero"] == "classical T_mn[Gamma2]=0", "psi bilinear")
    check("V61_matter_descent", nonlocal_by_id["NL4984_04_matter"]["consequence_at_psi_zero"] == "J_psi=0 in every scalar coordinate", "public metric only")
    check("V62_source_fixed_point", nonlocal_by_id["NL4984_05_source_map"]["consequence_at_psi_zero"] == "J=0 maps exactly to J_new=0", "zero invariant")
    check("V63_boundary_domain", "every normal derivative vanish" in nonlocal_by_id["NL4984_06_boundary"]["consequence_at_psi_zero"], "global zero")
    check("V64_Ward_silence", nonlocal_by_id["NL4984_07_Ward"]["consequence_at_psi_zero"] == "no independent classical one-scalar force current", "covariant Ward")
    check("V65_uniqueness_open", nonlocal_by_id["NL4984_08_uniqueness"]["status"] == "EXPLICIT_NONCLAIM_UNIQUENESS_OPEN", "existence only")
    check("V66_determinant_open", nonlocal_by_id["NL4984_09_determinant"]["status"] == "QUANTUM_METRIC_DETERMINANT_RETAINED_OPEN", "quantum response")
    check("V67_pure_metric_open", nonlocal_by_id["NL4984_10_scope"]["status"] == "PURE_METRIC_OBSTRUCTION_RETAINED", "not exact GR")

    check("V68_branch_shape", len(branch_rows) == 10, "ten branch rows")
    check("V69_branch_sources", source_paths_exist(branch_rows), "all source paths")
    check("V70_branch_validity", all(bool_value(row["valid_for_selected_branch_claim"]) for row in branch_rows), "declared branch")
    branch_by_id = {row["sector_id"]: row for row in branch_rows}
    check("V71_O2_branch", branch_by_id["BR4984_03_O2"]["status"] == "MOTION_OPERATOR_SILENT_FOR_ARBITRARY_wO2", "coefficient independent")
    check("V72_O3_branch", branch_by_id["BR4984_04_O3"]["classical_metric_stress_at_psi_zero"] == "GENERALLY_NONZERO_ON_CURVED_BACKGROUND", "pure metric remains")
    check("V73_O4_branch", branch_by_id["BR4984_05_O4"]["status"] == "MOTION_CURVATURE_PORTAL_SILENT", "C2X zero")
    check("V74_source_branch", branch_by_id["BR4984_07_source"]["classical_metric_stress_at_psi_zero"] == "VISIBLE_T_MN_REMAINS", "GR source retained")
    check("V75_frame_branch", branch_by_id["BR4984_08_frame"]["one_scalar_source_at_psi_zero"] == "J=0 maps to 0", "zero fixed")
    check("V76_Jacobian_branch", branch_by_id["BR4984_09_Jacobian"]["flat_metric_quadratic_Hessian"] == "REGULATOR_DEPENDENT", "not calculated")
    check("V77_Newton_branch", branch_by_id["BR4984_10_Newton"]["flat_metric_quadratic_Hessian"] == "0 at p2 Newton order", "leading classical")

    check("V78_gate_shape", len(gate_rows) == 32, "32 gates")
    check("V79_gate_pass", all(bool_value(row["passed"]) and row["status"] == "pass" for row in gate_rows), "32/32")
    check("V80_gate_marker", all(row["checkpoint_marker"] == RUNNER_MARKER for row in gate_rows), RUNNER_MARKER)
    check("V81_gate_full_claim_false", all(not bool_value(row["valid_for_full_MTS_claim"]) for row in gate_rows), "no full claim")

    check("V82_result_marker", result["checkpoint_marker"] == RUNNER_MARKER, RUNNER_MARKER)
    check("V83_result_counts", result["massless_projector_event_count"] == 14 and result["gate_pass_count"] == result["gate_count"] == 32, "14 events, 32 gates")
    check("V84_result_IBP", abs(result["maximum_IBP_jet_relative_residual"] - maximum_ibp_relative) < 1.0e-30, f"{maximum_ibp_relative:.3e}")
    check("V85_result_projector", abs(result["maximum_running_frame_induced_to_O2_projector_ratio"] - maximum_ratio) < 1.0e-30, f"{maximum_ratio:.3e}")
    raw_vector = result["scalar_running_frame_raw_p6_connection_vector"]
    check("V86_result_raw_vector", raw_vector == {"A6": "-4 c gamma_Box", "B6": "-8 c gamma_Box"}, str(raw_vector))
    essential_vector = result["scalar_running_frame_essential_p6_shift_vector"]
    check("V87_result_essential_vector", all(float(value) == 0.0 for value in essential_vector.values()), str(essential_vector))
    check("V88_beta_b_not_required", result["numeric_beta_bBox_required_for_zero_essential_O2_shift"] is False, "coefficient independent")
    true_flags = (
        "valid_for_classical_running_frame_six_derivative_map",
        "valid_for_zero_essential_O2_shift_from_beta_bBox_connection",
        "valid_for_selected_parent_nonlocal_two_point_source_silence",
        "valid_for_leading_flat_Newton_silence_of_six_derivative_scalar_packet",
    )
    false_flags = (
        "valid_for_numeric_beta_bBox_claim",
        "valid_for_complete_parent_O2_beta_claim",
        "valid_for_quantum_field_redefinition_Jacobian_coefficient_claim",
        "valid_for_nonlocal_zero_solution_uniqueness_claim",
        "valid_for_finite_parent_metric_three_point_claim",
        "valid_for_exact_all_operator_local_GR_claim",
        "valid_for_full_MTS_claim",
    )
    check("V89_result_positive_flags", all(result[field] is True for field in true_flags), ",".join(true_flags))
    check("V90_result_negative_flags", all(result[field] is False for field in false_flags), ",".join(false_flags))
    check("V91_next_target", result["next_target"].startswith("4985") and "genuine parent O2" in result["next_target"], result["next_target"])

    variables = {row["symbol"] for row in read_csv(VARIABLE_AUDIT)}
    expected_variables = {
        "RunningFrameDerivativeGrading4984_MTS",
        "RunningFrameP6Spillover4984_MTS",
        "RunningFrameO2Projector4984_MTS",
        "NonlocalSourceSilence4984_MTS",
        "SourceBoundaryFrameFixedPoint4984_MTS",
        "LeadingNewtonP6Silence4984_MTS",
        "PredictivityStatus4984_MTS",
    }
    check("V92_variable_rows", expected_variables.issubset(variables), str(sorted(expected_variables)))
    claims = [row for row in read_csv(CLAIMS_REGISTER) if row["claim_id"] == "L-826"]
    check("V93_claim_row", len(claims) == 1 and "private_nonclaim" in claims[0]["status"] and FORMAL_MARKER in claims[0]["notes"], "L-826")

    all_outputs = (*output_csvs, RESULT, PROVENANCE, CHECKPOINT_DOC, FORMAL_NOTE)
    missing_markers = [str(path) for path in all_outputs if "MISSING_" in path.read_text(encoding="utf-8", errors="replace")]
    check("V94_no_missing_placeholders", not missing_markers, str(missing_markers))
    row_sets = (grading_rows, spillover_rows, ibp_rows, projector_rows, nonlocal_rows, branch_rows, gate_rows)
    check("V95_all_output_full_claim_false", all(not bool_value(row.get("valid_for_full_MTS_claim", "false")) for rows in row_sets for row in rows), "all CSV rows false")
    permitted_roots = (POST.resolve(), FORMAL.resolve())
    scope_paths = (*required_paths, VALIDATION, VALIDATION_PROVENANCE)
    check("V96_path_scope", all(any(path.resolve().is_relative_to(root) for root in permitted_roots) for path in scope_paths), "post and formal only")
    pycache = list(POST.rglob("__pycache__"))
    check("V97_no_pycache", not pycache, str(pycache))
    check("V98_provenance", contains(PROVENANCE, "No GitHub action") and contains(PROVENANCE, "does not assign beta_bBox"), "nonclaim provenance")

    passed = sum(bool(row["passed"]) for row in checks)
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    provenance_lines = [
        "# Checkpoint 4984 independent validation provenance",
        "",
        "Generated locally. No GitHub action.",
        "",
        f"Result: {passed}/{len(checks)} independent checks pass.",
        "",
        "The validator independently reconstructs the covariant IBP map and all",
        "massless projector formulae, checks source paths, claim boundaries, and",
        "formal integration. It does not assign beta_bBox, beta_wO2, a Jacobian",
        "coefficient, uniqueness, exact local GR, or full MTS.",
        "",
        "## Input digests",
    ]
    for path in required_paths:
        provenance_lines.append(
            f"- {path.relative_to(ROOT).as_posix()} sha256 {digest(path)}"
        )
    VALIDATION_PROVENANCE.write_text("\n".join(provenance_lines) + "\n", encoding="utf-8")

    print(
        f"{MARKER}={passed}/{len(checks)} "
        f"IBP={maximum_ibp_relative:.3e} projector_ratio={maximum_ratio:.3e} "
        f"output={VALIDATION}",
        flush=True,
    )
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
