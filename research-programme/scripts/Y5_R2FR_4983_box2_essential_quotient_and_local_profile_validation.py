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
SOURCE = POST / "source-intake" / "functional_rg" / "4983"
VALIDATION_DIR = POST / "source-intake" / "mts_residuals"
VALIDATION = VALIDATION_DIR / "P8_Y5_BRR545_4983_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RUNNER = POST / "scripts" / "Y5_R2FR_4983_box2_essential_quotient_and_local_profile.py"
VALIDATOR = POST / "scripts" / "Y5_R2FR_4983_box2_essential_quotient_and_local_profile_validation.py"
CHECKPOINT_DOC = POST / "4983-Y5-R2FR-box2-essential-quotient-running-frame-and-local-profile-theorem.md"
FORMAL_NOTE = FORMAL / "999-PPC4161-box2-essential-quotient-and-local-profile.md"
CURRENT_RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CURRENT_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
VARIABLE_AUDIT = FORMAL / "04-variable-audit.csv"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION_SPINE = FORMAL / "07-unification-spine.md"

PREDECESSOR_RESULT = POST / "source-intake" / "functional_rg" / "4982" / "covariant_orderX_essential_results.json"
TRUNCATION_SOURCE = POST / "source-intake" / "functional_rg" / "4937" / "src-2110.09566v1" / "SSTwAS.tex"
EFT_SOURCE = POST / "source-intake" / "functional_rg" / "4930" / "src1908" / "GravityEFTv2_final.tex"
SIX_DERIVATIVE_BASIS = POST / "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md"
SIX_DERIVATIVE_PROJECTOR = POST / "4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-full-invariant-amplitude-or-curvature-route-rejection.md"
SOURCE_SELECTION = POST / "source-intake" / "functional_rg" / "4943" / "matter_source_selection_rules.csv"
JUNCTION_SOURCE = POST / "source-intake" / "functional_rg" / "4943" / "junction_scalar_charge_and_fifth_force.csv"
INTERIOR_BENCHMARKS = POST / "source-intake" / "functional_rg" / "4943" / "interior_stability_benchmarks.csv"

NOTATION = SOURCE / "box2_operator_notation_and_source_scope.csv"
HESSIAN = SOURCE / "box2_covariant_hessian_contract.csv"
JET = SOURCE / "box2_local_jet_crosscheck.csv"
QUOTIENT = SOURCE / "box2_four_derivative_essential_quotient.csv"
RUNNING_FRAME = SOURCE / "box2_running_frame_and_projector.csv"
PROFILE = SOURCE / "box2_sourced_local_profile_response.csv"
JUNCTION = SOURCE / "box2_junction_and_local_GR_gate.csv"
GATE = SOURCE / "box2_essential_local_profile_gate.csv"
RESULT = SOURCE / "box2_essential_local_profile_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4983_BOX2_ESSENTIAL_LOCAL_PROFILE_VALIDATION"
RUNNER_MARKER = "MTS_4983_BOX2_ESSENTIAL_QUOTIENT_LOCAL_PROFILE"
FORMAL_MARKER = "PPC4161_BOX2_ESSENTIAL_LOCAL_PROFILE_4983"
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


def relative_residual(value: float, expected: float) -> float:
    return abs(value - expected) / max(abs(value), abs(expected), 1.0e-300)


def trapezoid(values: list[float], step: float) -> float:
    return step * (0.5 * (values[0] + values[-1]) + math.fsum(values[1:-1]))


def independent_bump_form_factors() -> tuple[float, dict[float, float]]:
    intervals = 20_000
    step = 1.0 / intervals
    radii = [index * step for index in range(intervals + 1)]
    raw_profile = [
        math.exp(-1.0 / (1.0 - radius * radius)) if radius < 1.0 else 0.0
        for radius in radii
    ]
    raw_charge = trapezoid(
        [radius * radius * value for radius, value in zip(radii, raw_profile)],
        step,
    )
    normalized_profile = [value / raw_charge for value in raw_profile]
    normalized_charge = trapezoid(
        [radius * radius * value for radius, value in zip(radii, normalized_profile)],
        step,
    )
    factors: dict[float, float] = {}
    for ell in (0.1, 0.3, 1.0):
        mass = 1.0 / ell
        integrand = [
            radius * value * math.sinh(mass * radius)
            for radius, value in zip(radii, normalized_profile)
        ]
        factors[ell] = trapezoid(integrand, step) / mass
    return normalized_charge, factors


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

    output_csvs = (NOTATION, HESSIAN, JET, QUOTIENT, RUNNING_FRAME, PROFILE, JUNCTION, GATE)
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
        PREDECESSOR_RESULT,
        TRUNCATION_SOURCE,
        EFT_SOURCE,
        SIX_DERIVATIVE_BASIS,
        SIX_DERIVATIVE_PROJECTOR,
        SOURCE_SELECTION,
        JUNCTION_SOURCE,
        INTERIOR_BENCHMARKS,
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
    check("V05_dry_run_gate_count", "DRY_RUN=27/27" in dry_run.stdout, dry_run.stdout.strip())

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

    predecessor = json.loads(PREDECESSOR_RESULT.read_text(encoding="utf-8"))
    truncation_text = TRUNCATION_SOURCE.read_text(encoding="utf-8", errors="replace")
    eft_text = EFT_SOURCE.read_text(encoding="utf-8", errors="replace")
    notation_rows = read_csv(NOTATION)
    hessian_rows = read_csv(HESSIAN)
    jet_rows = read_csv(JET)
    quotient_rows = read_csv(QUOTIENT)
    frame_rows = read_csv(RUNNING_FRAME)
    profile_rows = read_csv(PROFILE)
    junction_rows = read_csv(JUNCTION)
    gate_rows = read_csv(GATE)
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    check("V21_predecessor_essential_map", predecessor["valid_for_essential_two_point_subtraction_map"] is True, "4982 promoted")
    source_fragments = (
        "(D^{2} \\phi)^2",
        "momentum-dependent form factor",
    )
    check("V22_truncation_source_fragments", all(fragment in truncation_text for fragment in source_fragments), "omission and form-factor statements")
    eft_fragments = (
        "operators proportional to the free field equation of motion",
        "we already imposed the scalar's EOM",
    )
    check("V23_EFT_source_fragments", all(fragment in eft_text for fragment in eft_fragments), "field-redefinition and EOM statements")

    check("V24_notation_shape", len(notation_rows) == 3, "three disambiguation rows")
    notation_by_id = {row["operator_id"]: row for row in notation_rows}
    split_valid = (
        notation_by_id["OBOX4_4983"]["derivative_order"] == "4"
        and notation_by_id["OBOX4_4983"]["scalar_field_degree"] == "2"
        and notation_by_id["O2SIX_4930_4959"]["derivative_order"] == "6"
        and notation_by_id["O2SIX_4930_4959"]["scalar_field_degree"] == "4"
        and not bool_value(notation_by_id["OBOX4_4983"]["same_as_six_derivative_O2"])
        and bool_value(notation_by_id["O2SIX_4930_4959"]["same_as_six_derivative_O2"])
    )
    check("V25_operator_identity_split", split_valid, "four-derivative bilinear differs from six-derivative O2")
    check("V26_notation_sources", source_paths_exist(notation_rows), "all notation sources exist")
    check("V27_notation_nonclaim", all(not bool_value(row["valid_for_full_MTS_claim"]) for row in notation_rows), "no full claim")

    check("V28_hessian_shape", len(hessian_rows) == 8, "eight covariant contract rows")
    check("V29_hessian_sources", source_paths_exist(hessian_rows), "all Hessian sources exist")
    check("V30_hessian_claim_rows", all(bool_value(row["valid_for_covariant_Box2_Hessian_claim"]) for row in hessian_rows), "8/8 derived")
    hessian_by_id = {row["contract_id"]: row for row in hessian_rows}
    check("V31_scalar_variation", "Box^2 psi" in hessian_by_id["BH4983_02_scalar_variation"]["equation"] and "surface" in hessian_by_id["BH4983_02_scalar_variation"]["equation"], "bulk plus boundary")
    check("V32_metric_box_definition", "D_h f:=delta_h(Box f)" in hessian_by_id["BH4983_04_metric_box"]["equation"] and "nabla_m h^{m lambda}" in hessian_by_id["BH4983_04_metric_box"]["equation"], "connection variation retained")
    check("V33_mixed_hessian", "(D_h psi)Box chi" in hessian_by_id["BH4983_05_metric_scalar"]["equation"] and "Y(D_h chi)" in hessian_by_id["BH4983_05_metric_scalar"]["equation"], "complete mixed block")
    check("V34_zero_background_blocks", "H_hh^Box2=0" in hessian_by_id["BH4983_06_zero_background"]["equation"] and "H_psipsi^Box2=b_Box Box^2" in hessian_by_id["BH4983_06_zero_background"]["equation"], "metric silent, scalar p4 retained")
    check("V35_flat_projector", "(1/2) d^2 Gamma_psipsi^(2)" in hessian_by_id["BH4983_07_projector"]["equation"], "normalization fixed")

    check("V36_jet_shape", len(jet_rows) == 32, "32 local-jet controls")
    block_counts = {block: sum(row["block"] == block for row in jet_rows) for block in ("metric_scalar", "scalar_scalar", "metric_metric_at_psi0")}
    check("V37_jet_block_counts", block_counts == {"metric_scalar": 16, "scalar_scalar": 8, "metric_metric_at_psi0": 8}, str(block_counts))
    jet_fields = ("automatic_mixed_second_derivative", "analytic_mixed_second_derivative", "absolute_residual", "relative_residual")
    check("V38_jet_numeric", finite_rows(jet_rows, jet_fields), "all jet values finite")
    maximum_jet_relative = max(float(row["relative_residual"]) for row in jet_rows)
    maximum_jet_absolute = max(float(row["absolute_residual"]) for row in jet_rows)
    check("V39_jet_residual", maximum_jet_relative < 2.0e-13 and maximum_jet_absolute < 2.0e-13, f"rel={maximum_jet_relative:.3e};abs={maximum_jet_absolute:.3e}")
    expected_statuses = {"LOCAL_NORMAL_COORDINATE_JET_MATCH", "QUADRATIC_BOX_OPERATOR_JET_MATCH", "ZERO_BACKGROUND_METRIC_BLOCK_MATCH"}
    check("V40_jet_statuses", {row["status"] for row in jet_rows} == expected_statuses, str(sorted(expected_statuses)))
    check("V41_jet_marker", all(row["checkpoint_marker"] == RUNNER_MARKER for row in jet_rows), RUNNER_MARKER)

    check("V42_quotient_shape", len(quotient_rows) == 6, "six quotient rows")
    quotient_by_id = {row["quotient_id"]: row for row in quotient_rows}
    nan_ids = {row["quotient_id"] for row in quotient_rows if math.isnan(float(row["coefficient_value"]))}
    check("V43_quotient_nan_scope", nan_ids == {"Q4983_01_IBP_Bochner", "Q4983_02_scalar_redefinition"}, str(sorted(nan_ids)))
    check("V44_Bochner_identity", "I_Box-I_Hessian-I_RicciX" in quotient_by_id["Q4983_01_IBP_Bochner"]["raw_direction"] and "=boundary" in quotient_by_id["Q4983_01_IBP_Bochner"]["redefinition_or_identity"], "covariant IBP identity")
    check("V45_scalar_redefinition", "b_Box/(2Z)" in quotient_by_id["Q4983_02_scalar_redefinition"]["redefinition_or_identity"] and "b_Box_new=b_Box-2Zs=0" in quotient_by_id["Q4983_02_scalar_redefinition"]["result"], "factor and sign fixed")
    ctilde = float(quotient_by_id["Q4983_03_metric_disformal"]["coefficient_value"])
    d_value = float(quotient_by_id["Q4983_04_metric_conformal"]["coefficient_value"])
    essential = float(quotient_by_id["Q4983_05_essential_X2"]["coefficient_value"])
    check("V46_metric_redefinition_values", abs(ctilde + 1.0 / (6.0 * math.pi)) < 1.0e-15 and abs(d_value + 1.0 / (3.0 * math.pi)) < 1.0e-15, f"ctilde={ctilde:.16g};d={d_value:.16g}")
    exact_essential = 20.0 + 8.0 * (-1.0 / 6.0 - 1.0 / 3.0)
    check("V47_essential_source", abs(essential - 16.0) < 1.0e-15 and abs(exact_essential - essential) < 1.0e-15, "20+8(-1/6-1/3)=16")
    check("V48_essential_dimension", float(quotient_by_id["Q4983_06_rank"]["coefficient_value"]) == 1.0 and "redundant rank 3" in quotient_by_id["Q4983_06_rank"]["result"], "5-1-3=1")
    check("V49_quotient_claim_scope", all(bool_value(row["valid_for_local_essential_basis_claim"]) for row in quotient_rows) and not bool_value(quotient_by_id["Q4983_02_scalar_redefinition"]["valid_for_numeric_offshell_form_factor_claim"]), "basis yes, raw b numeric no")
    check("V50_quotient_sources", source_paths_exist(quotient_rows), "all quotient sources exist")

    check("V51_running_frame_shape", len(frame_rows) == 7, "seven frame/projector rows")
    frame_by_id = {row["frame_id"]: row for row in frame_rows}
    check("V52_running_frame_sources", source_paths_exist(frame_rows), "all frame sources exist")
    check("V53_running_projector", "Z p^2+b_Box p^4" in frame_by_id["RF4983_01_flat_projector"]["equation"], "analytic p4 coordinate")
    check("V54_running_connection", "gamma_Box=beta_bBox/(2Z)" in frame_by_id["RF4983_02_running_reduction"]["equation"], "essential-frame connection law")
    check("V55_invertibility_condition", "epsilon_Box=abs(b_Box)p_max^2/(2Z)<1" in frame_by_id["RF4983_03_invertibility"]["equation"], "IR perturbative domain")
    check("V56_massive_shift", "Z-b_Box m_gap^2" in frame_by_id["RF4983_04_massive_lower_terms"]["equation"], "lower two-point rematching")
    check("V57_propagator_contact", "-b_Box/Z^2" in frame_by_id["RF4983_05_propagator_expansion"]["equation"], "first EFT correction is contact")
    check("V58_exact_resummation_not_promoted", not bool_value(frame_by_id["RF4983_06_exact_resummation"]["valid_for_essential_flow_claim"]) and "CONTROL_ONLY" in frame_by_id["RF4983_06_exact_resummation"]["status"], "heavy mode is control only")
    check("V59_nonlocal_completion_open", not bool_value(frame_by_id["RF4983_07_nonlocal_form_factor"]["valid_for_essential_flow_claim"]) and frame_by_id["RF4983_07_nonlocal_form_factor"]["status"] == "NONLOCAL_COMPLETION_OPEN", "nonanalytic tail not inferred")
    check("V60_numeric_beta_not_claimed", result["numeric_beta_bBox_available"] is False and result["valid_for_numeric_beta_bBox_claim"] is False, "beta value remains open")

    generic_profiles = [row for row in profile_rows if row["profile_id"].startswith("GENERIC_")]
    selected_profiles = [row for row in profile_rows if row["profile_id"].startswith("MTS_JZERO_")]
    check("V61_profile_shape", len(profile_rows) == 23, "15 generic plus 8 selected")
    check("V62_profile_split", len(generic_profiles) == 15 and len(selected_profiles) == 8, f"generic={len(generic_profiles)};selected={len(selected_profiles)}")
    check("V63_profile_sources", source_paths_exist(profile_rows), "all profile sources exist")
    generic_fields = (
        "ell_over_source_radius",
        "radius_over_source_radius",
        "compact_source_form_factor",
        "exact_resummed_potential_correction_fraction",
        "exact_resummed_force_correction_fraction",
        "order_reduced_exterior_correction",
        "massless_charge_residue_ratio",
    )
    check("V64_generic_profile_numeric", finite_rows(generic_profiles, generic_fields), "all generic controls finite")
    formula_residuals: list[float] = []
    for row in generic_profiles:
        ell = float(row["ell_over_source_radius"])
        radius = float(row["radius_over_source_radius"])
        form_factor = float(row["compact_source_form_factor"])
        potential = float(row["exact_resummed_potential_correction_fraction"])
        force = float(row["exact_resummed_force_correction_fraction"])
        expected_potential = -form_factor * math.exp(-radius / ell)
        expected_force = expected_potential * (1.0 + radius / ell)
        formula_residuals.extend((relative_residual(potential, expected_potential), relative_residual(force, expected_force)))
    check("V65_profile_formula", max(formula_residuals) < 2.0e-14, f"max relative={max(formula_residuals):.3e}")
    independent_charge, independent_factors = independent_bump_form_factors()
    factor_residuals = [
        relative_residual(float(row["compact_source_form_factor"]), independent_factors[float(row["ell_over_source_radius"])])
        for row in generic_profiles
    ]
    check("V66_profile_independent_quadrature", abs(independent_charge - 1.0) < 2.0e-13 and max(factor_residuals) < 2.0e-12, f"charge={independent_charge:.16g};max factor={max(factor_residuals):.3e}")
    monotonic = True
    for ell in (0.1, 0.3, 1.0):
        group = sorted((row for row in generic_profiles if float(row["ell_over_source_radius"]) == ell), key=lambda row: float(row["radius_over_source_radius"]))
        forces = [abs(float(row["exact_resummed_force_correction_fraction"])) for row in group]
        monotonic = monotonic and all(left > right for left, right in zip(forces, forces[1:]))
    check("V67_profile_radial_decay", monotonic, "absolute Yukawa correction decreases outside each source")
    check("V68_order_reduced_exterior", all(float(row["order_reduced_exterior_correction"]) == 0.0 and float(row["massless_charge_residue_ratio"]) == 1.0 for row in generic_profiles), "contact support and unit residue")
    check("V69_generic_nonclaim", all(not bool_value(row["valid_for_declared_integrated_H_local_branch"]) and "NO_PHYSICAL_BBOX_OR_CHARGE" in row["source_status"] for row in generic_profiles), "dimensionless controls only")
    selected_zero_fields = ("exact_resummed_potential_correction_fraction", "exact_resummed_force_correction_fraction", "order_reduced_exterior_correction", "massless_charge_residue_ratio")
    check("V70_selected_profiles_zero", finite_rows(selected_profiles, selected_zero_fields) and all(float(row[field]) == 0.0 for row in selected_profiles for field in selected_zero_fields), "eight exact zero-source rows")
    expected_sources = {"Earth", "Sun", "one_solar_mass_white_dwarf", "1.4_solar_mass_12km_neutron_star"}
    selected_pairs = {(row["source_case"], float(row["density_multiplier_over_mean"])) for row in selected_profiles}
    check("V71_selected_source_grid", selected_pairs == {(source, density) for source in expected_sources for density in (1.0, 10.0)}, str(sorted(selected_pairs)))
    check("V72_selected_branch_validity", all(bool_value(row["valid_for_declared_integrated_H_local_branch"]) and row["source_status"] == "SELECTED_PARENT_JPSI_ZERO_PSI_ZERO_BOUNDARY_ALL_BBOX" for row in selected_profiles), "declared branch only")
    check("V73_profile_full_claim_false", all(not bool_value(row["valid_for_full_MTS_claim"]) for row in profile_rows), "no profile promotes full MTS")

    check("V74_junction_shape", len(junction_rows) == 12, "nine local rows plus three explicit boundaries")
    check("V75_junction_passed", all(bool_value(row["passed"]) for row in junction_rows), "12/12 statements internally satisfied")
    check("V76_junction_sources", source_paths_exist(junction_rows), "all junction sources exist")
    check("V77_junction_scope", all(bool_value(row["valid_for_declared_integrated_H_local_branch"]) for row in junction_rows[:9]) and all(not bool_value(row["valid_for_declared_integrated_H_local_branch"]) for row in junction_rows[9:]), "nine promoted, three retained open/nonclaim")
    junction_by_id = {row["gate_id"]: row for row in junction_rows}
    check("V78_parent_source_zero", "J_psi=delta S_SM/delta psi=0" in junction_by_id["JL4983_01_parent_source"]["statement"], "ordinary matter source theorem")
    check("V79_bulk_zero", "psi=0" in junction_by_id["JL4983_03_bulk_zero"]["statement"] and "arbitrary" in junction_by_id["JL4983_03_bulk_zero"]["status"].lower(), "zero solution for any local b_Box")
    junction_statement = junction_by_id["JL4983_04_finite_action_junction"]["statement"]
    check("V80_four_junction_conditions", all(fragment in junction_statement for fragment in ("[psi]", "[n.nabla psi]", "[b_Box Box psi]", "[Z n.nabla psi-b_Box n.nabla Box psi]")), "four conditions retained")
    check("V81_zero_stress", "T_Box2=0 at psi=0" in junction_by_id["JL4983_06_stress"]["statement"], "metric correction silent")
    check("V82_Ward_identity", "nabla_mu T_Box2" in junction_by_id["JL4983_07_Ward"]["statement"] and "E_Box2 nabla_nu psi" in junction_by_id["JL4983_07_Ward"]["statement"], "diffeomorphism identity")
    check("V83_exterior_theorem", "-b_Box J/Z^2" in junction_by_id["JL4983_08_order_reduced_exterior"]["statement"], "compact-support correction")
    check("V84_charge_residue", "massless residue remains 1/Z" in junction_by_id["JL4983_09_charge_residue"]["statement"], "Gauss charge unchanged")
    check("V85_heavy_mode_open", junction_by_id["JL4983_10_exact_heavy_mode"]["status"].startswith("OPEN_EXPLICIT"), "not promoted from truncation")
    check("V86_nonlocal_tail_open", junction_by_id["JL4983_11_nonlocal_tail"]["status"] == "OPEN_EXPLICIT", "nonanalytic tail remains open")
    check("V87_scope_boundary", junction_by_id["JL4983_12_scope"]["status"] == "NONCLAIM_BOUNDARY_RETAINED", "packet-level result")

    check("V88_gate_shape", len(gate_rows) == 27, "27 runner gates")
    check("V89_gate_pass", all(bool_value(row["passed"]) and row["status"] == "pass" for row in gate_rows), "27/27")
    check("V90_gate_marker", all(row["checkpoint_marker"] == RUNNER_MARKER for row in gate_rows), RUNNER_MARKER)
    check("V91_gate_full_claim_false", all(not bool_value(row["valid_for_full_MTS_claim"]) for row in gate_rows), "no full claim")

    check("V92_result_marker", result["checkpoint_marker"] == RUNNER_MARKER, RUNNER_MARKER)
    count_packet = (
        result["four_derivative_raw_operator_count"],
        result["IBP_identity_count"],
        result["post_IBP_coordinate_count"],
        result["redundant_field_redefinition_rank"],
        result["essential_four_derivative_dimension"],
    )
    check("V93_result_quotient_counts", count_packet == (5, 1, 4, 3, 1), str(count_packet))
    check("V94_result_numerics", abs(result["maximum_local_jet_relative_residual"] - maximum_jet_relative) < 1.0e-30 and result["quotient_invariant_orthogonality_residual"] < 2.0e-15, "jet and quotient residuals reproduced")
    check("V95_result_profile_counts", result["generic_profile_row_count"] == 15 and result["selected_parent_zero_source_profile_row_count"] == 8, "15+8")
    true_flags = (
        "valid_for_operator_name_disambiguation",
        "valid_for_covariant_local_Box2_Hessian",
        "valid_for_local_four_derivative_essential_quotient",
        "valid_for_order_reduced_compact_source_exterior_theorem",
        "valid_for_selected_parent_Box2_zero_motion_local_branch",
    )
    false_flags = (
        "valid_for_numeric_beta_bBox_claim",
        "valid_for_nonperturbative_resummed_heavy_mode_claim",
        "valid_for_nonlocal_motion_form_factor_completion",
        "valid_for_finite_parent_metric_three_point_claim",
        "valid_for_exact_all_operator_local_GR_claim",
        "valid_for_full_MTS_claim",
    )
    check("V96_result_positive_flags", all(result[field] is True for field in true_flags), ",".join(true_flags))
    check("V97_result_negative_flags", all(result[field] is False for field in false_flags), ",".join(false_flags))
    check("V98_result_next_target", result["next_target"].startswith("4984") and "six-derivative spillover" in result["next_target"], result["next_target"])

    variable_rows = read_csv(VARIABLE_AUDIT)
    variable_symbols = {row["symbol"] for row in variable_rows}
    expected_variables = {
        "Box2OperatorIdentity4983_MTS",
        "CovariantBox2Hessian4983_MTS",
        "Box2EssentialQuotient4983_MTS",
        "Box2RunningFrame4983_MTS",
        "Box2ProfileTheorem4983_MTS",
        "Box2JunctionGate4983_MTS",
        "PredictivityStatus4983_MTS",
    }
    check("V99_variable_audit_rows", expected_variables.issubset(variable_symbols), str(sorted(expected_variables)))
    claim_rows = read_csv(CLAIMS_REGISTER)
    claim_4983 = [row for row in claim_rows if row["claim_id"] == "L-825"]
    check("V100_claim_register_row", len(claim_4983) == 1 and "private_nonclaim" in claim_4983[0]["status"] and FORMAL_MARKER in claim_4983[0]["notes"], "L-825")

    all_outputs = (*output_csvs, RESULT, PROVENANCE, CHECKPOINT_DOC, FORMAL_NOTE)
    missing_markers = [str(path) for path in all_outputs if "MISSING_" in path.read_text(encoding="utf-8", errors="replace")]
    check("V101_no_missing_placeholders", not missing_markers, str(missing_markers))
    check("V102_all_output_full_claim_false", all(not bool_value(row.get("valid_for_full_MTS_claim", "false")) for rows in (notation_rows, hessian_rows, jet_rows, quotient_rows, frame_rows, profile_rows, junction_rows, gate_rows) for row in rows), "all CSV rows false")
    permitted_roots = (POST.resolve(), FORMAL.resolve())
    scope_paths = (*required_paths, VALIDATION, VALIDATION_PROVENANCE)
    check("V103_path_scope", all(any(path.resolve().is_relative_to(root) for root in permitted_roots) for path in scope_paths), "post-checkpoint-work and formalization-workbench only")
    pycache = list(POST.rglob("__pycache__"))
    check("V104_no_pycache", not pycache, str(pycache))
    check("V105_provenance_present", contains(PROVENANCE, "No GitHub action") and contains(PROVENANCE, "No numeric `beta_bBox`"), "runner provenance and nonclaim")

    passed = sum(bool(row["passed"]) for row in checks)
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    provenance_lines = [
        "# Checkpoint 4983 independent validation provenance",
        "",
        "Generated locally. No GitHub action.",
        "",
        f"Result: `{passed}/{len(checks)}` independent checks pass.",
        "",
        "The validator independently recomputes the compact bump normalization,",
        "Yukawa form factors, profile equations, quotient arithmetic, source-path",
        "closure, claim boundaries, and corpus integration. It does not assign a",
        "numeric beta_bBox, resum a physical heavy pole, or promote full MTS.",
        "",
        "## Input digests",
    ]
    for path in required_paths:
        provenance_lines.append(f"- `{path.relative_to(ROOT).as_posix()}` sha256 `{digest(path)}`")
    VALIDATION_PROVENANCE.write_text("\n".join(provenance_lines) + "\n", encoding="utf-8")

    print(
        f"{MARKER}={passed}/{len(checks)} "
        f"jet={maximum_jet_relative:.3e} profiles={len(profile_rows)} "
        f"output={VALIDATION}",
        flush=True,
    )
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
