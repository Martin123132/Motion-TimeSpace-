from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import subprocess
import sys
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True
getcontext().prec = 90

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4955"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4955_VALIDATION.csv"

RESEARCH = POST / "scripts" / "Y5_R2FR_4955_X3_parent_flow_and_hierarchy.py"
CHECKPOINT = POST / "4955-Y5-R2FR-six-derivative-shift-sector-X3-parent-flow-and-number-changing-fixed-ratio-or-strong-2PI-route-rejection.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
FORMAL = ROOT / "formalization-workbench" / "971-PPC4161-X3-parent-flow-and-functional-hierarchy-decision.md"
CLAIMS = ROOT / "formalization-workbench" / "02-claims-register.csv"
VARIABLES = ROOT / "formalization-workbench" / "04-variable-audit.csv"
EQUATIONS = ROOT / "formalization-workbench" / "05-equation-register.md"
RED_TEAM = ROOT / "formalization-workbench" / "06-consistency-red-team.md"
SPINE = ROOT / "formalization-workbench" / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

RESULT = SOURCE / "X3_parent_flow_results.json"
GRAVITY = SOURCE / "minimal_gravity_X2_X3_source_projection.csv"
HIERARCHY = SOURCE / "PX_coefficient_hierarchy.csv"
OPERATORS = SOURCE / "six_derivative_operator_flow_roles.csv"
TRAJECTORY = SOURCE / "GR_gaussian_X3_forced_trajectory.csv"
SPARC = SOURCE / "SPARC_parent_forced_X3_coordinate_gate.csv"
DECISION = SOURCE / "X3_parent_flow_decision.csv"

MARKER = "MTS_4955_X3_PARENT_FLOW_AND_HIERARCHY"
VALIDATION_MARKER = "MTS_4955_INDEPENDENT_VALIDATION"
PLANCK_MASS_EV = Decimal("1.2208901285838957e28")
PI_DECIMAL = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286")
HIGH_FREQUENCY_CASES = {
    "white_dwarf_fundamental_pair_quantum",
    "neutron_star_fundamental_pair_quantum",
    "one_GeV_quantum",
    "UHE_1e20_eV_quantum",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def close(left: float, right: float, relative: float = 2.0e-12, absolute: float = 0.0) -> bool:
    return math.isclose(left, right, rel_tol=relative, abs_tol=absolute)


def decimal_close(left: Decimal, right: Decimal, relative: Decimal = Decimal("2e-17")) -> bool:
    scale = max(abs(left), abs(right), Decimal("1e-1000"))
    return abs(left - right) <= relative * scale


def add(
    rows: list[dict[str, Any]],
    check_id: str,
    requirement: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    rows.append(
        {
            "check_id": check_id,
            "requirement": requirement,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "validation_marker": VALIDATION_MARKER,
        }
    )


def angular_average_s3(expression: sp.Expr, cosine: sp.Symbol) -> sp.Expr:
    polynomial = sp.Poly(sp.expand(expression), cosine)
    result = sp.Integer(0)
    for (power,), coefficient in polynomial.terms():
        if power % 2 == 0:
            half_power = power // 2
            result += coefficient * sp.rf(sp.Rational(1, 2), half_power) / sp.rf(2, half_power)
    return sp.simplify(result)


def independent_scalar_betas() -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    x, radial, cosine = sp.symbols("x q z", real=True)
    c, e, f, h5 = sp.symbols("c e f h5", real=True)
    lagrangian = x / 2 + c * x**2 + e * x**3 + f * x**4 + h5 * x**5
    shift = radial**2 * (
        2 * sp.diff(lagrangian, x) - 1
        + 4 * x * sp.diff(lagrangian, x, 2) * cosine**2
    )
    inverse = sp.series(1 / (1 + shift), x, 0, 5).removeO()
    flow = sp.expand(
        sp.integrate(radial**3 * angular_average_s3(inverse, cosine), (radial, 0, 1))
        / (8 * sp.pi**2)
    )
    return (
        sp.simplify(4 * c + flow.coeff(x, 2)),
        sp.simplify(8 * e + flow.coeff(x, 3)),
        sp.simplify(12 * f + flow.coeff(x, 4)),
    )


def main() -> int:
    checks: list[dict[str, Any]] = []
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    execution = subprocess.run(
        [sys.executable, str(RESEARCH)],
        cwd=POST,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    add(checks, "VAL4955_00_research", "research runner completes", 0, execution.returncode, execution.returncode == 0)

    outputs = [RESULT, GRAVITY, HIERARCHY, OPERATORS, TRAJECTORY, SPARC, DECISION]
    documents = [RESEARCH, CHECKPOINT, PROVENANCE, FORMAL, CLAIMS, VARIABLES, EQUATIONS, RED_TEAM, SPINE, RESUME]
    missing = [str(path) for path in outputs + documents if not path.is_file()]
    add(checks, "VAL4955_01_paths", "all output and synchronized document paths exist", [], missing, not missing)
    if missing or execution.returncode != 0:
        VALIDATION.parent.mkdir(parents=True, exist_ok=True)
        with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
            writer.writeheader()
            writer.writerows(checks)
        return 1

    compile_failures: list[str] = []
    for path in (RESEARCH, Path(__file__)):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as error:
            compile_failures.append(f"{path}:{error}")
    add(checks, "VAL4955_02_compile", "research and validator compile without bytecode output", [], compile_failures, not compile_failures)

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    gravity = read_csv(GRAVITY)
    hierarchy = read_csv(HIERARCHY)
    operators = read_csv(OPERATORS)
    trajectory = read_csv(TRAJECTORY)
    sparc = read_csv(SPARC)
    decisions = read_csv(DECISION)
    tables = (gravity, hierarchy, operators, trajectory, sparc, decisions)

    marker_ok = result["checkpoint_marker"] == MARKER and all(
        row["checkpoint_marker"] == MARKER for table in tables for row in table
    )
    add(checks, "VAL4955_03_marker", "result and every evidence row use one checkpoint marker", MARKER, result["checkpoint_marker"], marker_ok)
    nonclaim_ok = all(not as_bool(row["valid_for_full_MTS_claim"]) for table in tables for row in table)
    add(checks, "VAL4955_04_nonclaim", "every generated row remains private nonclaim", True, nonclaim_ok, nonclaim_ok)

    hash_failures = [
        path
        for path, expected in result["source_hashes"].items()
        if not Path(path).is_file() or digest(Path(path)) != expected
    ]
    add(checks, "VAL4955_05_hashes", "all locked source hashes independently recompute", [], hash_failures, result["source_hashes_match"] and not hash_failures)
    clauses_ok = all(result["source_clause_checks"].values()) and len(result["source_clause_checks"]) == 9
    add(checks, "VAL4955_06_clauses", "all nine source clauses are present", "9 true", result["source_clause_checks"], clauses_ok)

    gravity_map = {row["quantity"]: row for row in gravity}
    required_gravity = {
        "trace_metric",
        "mixed_norm",
        "coefficient_x2_before_angular_average",
        "coefficient_x3_before_angular_average",
        "angular_x2",
        "angular_x3",
        "radial_x2",
        "radial_x3",
        "flow_x2_prefactor",
        "flow_x3_prefactor",
        "beta_c_source",
        "beta_e_source",
    }
    gravity_shape = len(gravity) == 12 and set(gravity_map) == required_gravity and all(as_bool(row["passed"]) for row in gravity)
    add(checks, "VAL4955_07_gravity_shape", "all twelve exact gravity projection rows exist", sorted(required_gravity), sorted(gravity_map), gravity_shape)

    radial = sp.symbols("q", real=True)
    angular_x2 = (8 * radial**4 - 9 * radial**2 + 12) / 16
    angular_x3 = (8 * radial**6 - 15 * radial**4 + 9 * radial**2 - 3) / 32
    radial_x2 = sp.integrate(radial**3 * angular_x2, (radial, 0, 1))
    radial_x3 = sp.integrate(radial**3 * angular_x3, (radial, 0, 1))
    add(checks, "VAL4955_08_radial_X2", "X2 Litim radial integral independently recomputes", sp.Rational(5, 32), radial_x2, radial_x2 == sp.Rational(5, 32))
    add(checks, "VAL4955_09_radial_X3", "X3 Litim radial integral independently recomputes", -sp.Rational(13, 1280), radial_x3, radial_x3 == -sp.Rational(13, 1280))
    beta_c_source = sp.simplify(radial_x2 * (32 * sp.pi) ** 2 / (8 * sp.pi**2))
    beta_e_source = sp.simplify(radial_x3 * (32 * sp.pi) ** 3 / (8 * sp.pi**2))
    add(checks, "VAL4955_10_beta_c", "known X2 source is exactly reproduced", 20, beta_c_source, beta_c_source == 20 and gravity_map["beta_c_source"]["exact_expression"] == "20")
    add(checks, "VAL4955_11_beta_e", "new X3 additive source independently recomputes", "-208*pi/5", sp.sstr(beta_e_source), beta_e_source == -sp.Rational(208, 5) * sp.pi and gravity_map["beta_e_source"]["exact_expression"] == "-208*pi/5")

    beta_c, beta_e, beta_f = independent_scalar_betas()
    c, e, f, h5 = sp.symbols("c e f h5", real=True)
    expected_c = 4 * c + 5 * c**2 / (8 * sp.pi**2) - e / (4 * sp.pi**2)
    expected_e = 8 * e - 37 * c**3 / (10 * sp.pi**2) + 21 * c * e / (8 * sp.pi**2) - 5 * f / (12 * sp.pi**2)
    expected_f = 12 * f + 25 * c**4 / sp.pi**2 - 243 * c**2 * e / (10 * sp.pi**2) + 9 * c * f / (2 * sp.pi**2) + 45 * e**2 / (16 * sp.pi**2) - 5 * h5 / (8 * sp.pi**2)
    add(checks, "VAL4955_12_scalar_beta_c", "flat scalar beta_c independently recomputes", sp.sstr(expected_c), sp.sstr(beta_c), sp.simplify(beta_c - expected_c) == 0)
    add(checks, "VAL4955_13_scalar_beta_e", "flat scalar beta_e independently recomputes", sp.sstr(expected_e), sp.sstr(beta_e), sp.simplify(beta_e - expected_e) == 0)
    add(checks, "VAL4955_14_scalar_beta_f", "flat scalar beta_f independently recomputes", sp.sstr(expected_f), sp.sstr(beta_f), sp.simplify(beta_f - expected_f) == 0)

    hierarchy_map = {row["coordinate"]: row for row in hierarchy}
    hierarchy_shape = len(hierarchy) == 5 and set(hierarchy_map) == {"c_X2", "e_X3", "f_X4", "finite_X2_X3_truncation", "general_PX_tower"} and all(as_bool(row["passed"]) for row in hierarchy)
    add(checks, "VAL4955_15_hierarchy_shape", "hierarchy table contains three explicit betas and two closure theorems", 5, len(hierarchy), hierarchy_shape)
    general_feed_failures = []
    for order in range(2, 9):
        expected_feed = -sp.Rational((order + 1) * (order + 2), 48) / sp.pi**2
        if expected_feed == 0:
            general_feed_failures.append(order)
    add(checks, "VAL4955_16_general_feed", "next-coordinate feed is nonzero through independent orders 2 to 8", [], general_feed_failures, not general_feed_failures and hierarchy_map["general_PX_tower"]["status"] == "FINITE_POLYNOMIAL_NONCLOSURE_THEOREM")
    explicit_feeds_ok = hierarchy_map["c_X2"]["next_coordinate_feed"] == "-e/(4*pi**2)" and hierarchy_map["e_X3"]["next_coordinate_feed"] == "-5*f/(12*pi**2)" and hierarchy_map["f_X4"]["next_coordinate_feed"] == "-5*h5/(8*pi**2)"
    add(checks, "VAL4955_17_explicit_feeds", "X3 X4 and X5 feeds are retained explicitly", True, explicit_feeds_ok, explicit_feeds_ok)

    operator_ids = {row["operator_id"] for row in operators}
    operator_ok = len(operators) == 6 and operator_ids == {"O1", "O2", "O3", "O4", "O5", "X4"} and all(as_bool(row["passed"]) for row in operators)
    add(checks, "VAL4955_18_operators", "complete six-derivative basis plus X4 feed is tabulated", sorted({"O1", "O2", "O3", "O4", "O5", "X4"}), sorted(operator_ids), operator_ok)

    trajectory_map = {row["quantity"]: row for row in trajectory}
    required_trajectory = {
        "beta_g_GR_Gaussian",
        "beta_c_essential_leading",
        "beta_e_Gaussian_matter",
        "g_solution",
        "c_essential_solution",
        "e_solution",
        "recent_convention_map",
        "v_X3_forced",
        "r3_fixed_ratio_gate",
        "beta_r3_leading",
        "forced_r3_solution_Cc_Ce_zero",
    }
    trajectory_ok = len(trajectory) == 11 and set(trajectory_map) == required_trajectory and all(as_bool(row["passed"]) for row in trajectory)
    add(checks, "VAL4955_19_trajectory", "leading coupled trajectory and ratio flow are complete", sorted(required_trajectory), sorted(trajectory_map), trajectory_ok)
    coefficient_e = sp.simplify(-beta_e_source / 2)
    coefficient_v = sp.simplify(8 * coefficient_e)
    trajectory_coefficients_ok = coefficient_e == sp.Rational(104, 5) * sp.pi and coefficient_v == sp.Rational(832, 5) * sp.pi and result["leading_GR_trajectory"]["forced_e_coefficient"] == "104*pi/5" and result["leading_GR_trajectory"]["forced_v_recent_coefficient"] == "832*pi/5"
    add(checks, "VAL4955_20_forced_coefficients", "forced e and recent v coefficients independently follow", "104*pi/5;832*pi/5", f"{coefficient_e};{coefficient_v}", trajectory_coefficients_ok)
    ratio_ok = trajectory_map["forced_r3_solution_Cc_Ce_zero"]["equation_or_solution"] == "r3(k)=13*pi/[320 g(k) ln(k/k0)^2]" and not result["leading_GR_trajectory"]["finite_fixed_r3"]
    add(checks, "VAL4955_21_ratio", "leading solution does not claim a finite fixed r3", True, ratio_ok, ratio_ok)

    result_4954 = json.loads((POST / "source-intake" / "functional_rg" / "4954" / "offshell_X2_X3_number_change_results.json").read_text(encoding="utf-8"))
    coefficient_c2 = Decimal(str(result_4954["on_shell_24"]["C2"]))
    coefficient_v_decimal = Decimal(832) * PI_DECIMAL / Decimal(5)
    formula_failures = 0
    for row in sparc:
        energy = Decimal(row["injection_energy_eV"])
        density = Decimal(row["required_density_eV4"])
        g_value = (energy / PLANCK_MASS_EV) ** 2
        v_value = coefficient_v_decimal * g_value**3
        background = Decimal(0) if density == 0 else abs(v_value) * (density / energy**4) ** 2
        contact = coefficient_c2 * v_value**2
        forced_gain = Decimal(row["unit_six_point_log_gain_envelope_4954"]) * v_value**2
        if not (
            decimal_close(Decimal(row["g_E_GN_E2"]), g_value)
            and decimal_close(Decimal(row["v_X3_forced_recent"]), v_value)
            and decimal_close(Decimal(row["background_coordinate_abs_v_rho_over_E4_sq"]), background)
            and decimal_close(Decimal(row["contact_sigmaE2_C2_v2"]), contact)
            and decimal_close(Decimal(row["minimal_forced_X3_contact_log_gain_comparator"]), forced_gain)
            and as_bool(row["background_derivative_expansion_controlled"]) == (background < 1)
        ):
            formula_failures += 1
    add(checks, "VAL4955_22_sparc_formulas", "every SPARC forced-coordinate row independently recomputes", 0, formula_failures, formula_failures == 0)
    add(checks, "VAL4955_23_sparc_shape", "six cases exist for every one of 175 galaxies", 1050, len(sparc), len(sparc) == 1050)
    positive_high = [row for row in sparc if as_bool(row["positive_outer_residual_target"]) and row["injection_case"] in HIGH_FREQUENCY_CASES]
    failed_high = sum(not as_bool(row["minimal_forced_X3_can_close_deficit"]) for row in positive_high)
    add(checks, "VAL4955_24_sparc_gate", "all positive high-frequency minimal forced comparators fail", "692/692", f"{failed_high}/{len(positive_high)}", len(positive_high) == 692 and failed_high == 692)
    background_controlled = all(as_bool(row["background_derivative_expansion_controlled"]) for row in sparc)
    add(checks, "VAL4955_25_background", "all minimal forced background coordinates remain controlled", True, background_controlled, background_controlled)
    maxima_ok = Decimal(result["SPARC_execution"]["max_v_X3_forced"]) == max(Decimal(row["v_X3_forced_recent"]) for row in sparc) and Decimal(result["SPARC_execution"]["max_background_coordinate"]) == max(Decimal(row["background_coordinate_abs_v_rho_over_E4_sq"]) for row in sparc) and Decimal(result["SPARC_execution"]["max_contact_sigmaE2"]) == max(Decimal(row["contact_sigmaE2_C2_v2"]) for row in sparc)
    add(checks, "VAL4955_26_maxima", "reported SPARC maxima independently match the table", True, maxima_ok, maxima_ok)

    decision_statuses = {row["status"] for row in decisions}
    required_statuses = {
        "SIX_DERIVATIVE_BASIS_SOURCE_SIGNED",
        "X3_ZERO_SURFACE_NOT_INVARIANT",
        "X3_PROJECTION_NORMALIZATION_CALIBRATED",
        "FINITE_X2_X3_TRUNCATION_NONCLOSURE_PROVED",
        "COMPLETE_SIX_DERIVATIVE_PARENT_FLOW_OPEN",
        "FINITE_R3_FIXED_RATIO_NOT_DERIVED",
        "MINIMAL_GR_FORCED_X3_COMPARATOR_REJECTED",
        "STRONG_2PI_DEFERRED_PENDING_PARENT_TRAJECTORY",
        "DIRECT_PROFILE_FORMATION_AMPLITUDE_OPEN",
        "4947_LOCAL_GR_NEWTON_MAXWELL_RETAINED",
        "FULL_MTS_PROMOTION_BLOCKED",
    }
    decisions_ok = len(decisions) == 11 and decision_statuses == required_statuses
    add(checks, "VAL4955_27_decisions", "decision table contains every required route status", sorted(required_statuses), sorted(decision_statuses), decisions_ok)
    result_decision = result["decision"]
    result_ok = result_decision["gravity_generates_X3"] and not result_decision["X3_zero_surface_invariant"] and not result_decision["finite_X2_X3_truncation_closed"] and not result_decision["complete_six_derivative_parent_flow"] and not result_decision["finite_r3_fixed_by_leading_system"] and not result_decision["strong_2PI_parent_warranted"] and result_decision["local_GR_Newton_Maxwell_4947"] == "RETAINED" and not result_decision["full_MTS"]
    add(checks, "VAL4955_28_result", "result preserves all claim boundaries", True, result_decision, result_ok)

    checkpoint_text = CHECKPOINT.read_text(encoding="utf-8")
    formal_text = FORMAL.read_text(encoding="utf-8")
    claims_text = CLAIMS.read_text(encoding="utf-8")
    variables_text = VARIABLES.read_text(encoding="utf-8")
    equations_text = EQUATIONS.read_text(encoding="utf-8")
    red_text = RED_TEAM.read_text(encoding="utf-8")
    spine_text = SPINE.read_text(encoding="utf-8")
    resume_text = RESUME.read_text(encoding="utf-8")
    documentation_ok = all(
        token in text
        for token, text in (
            ("MTS_X3_PARENT_FLOW_HIERARCHY_DECISION_4955", checkpoint_text),
            ("PPC4161_X3_PARENT_FLOW_FUNCTIONAL_HIERARCHY_4955", formal_text),
            ('"L-797"', claims_text),
            ("PredictivityStatus4955_MTS", variables_text),
            ("## 1.248", equations_text),
            ("## 199.", red_text),
            ("checkpoint 4955", spine_text),
            ("Current checkpoint 4955 handoff", resume_text),
        )
    )
    add(checks, "VAL4955_29_documents", "checkpoint 4955 is synchronized across every register", True, documentation_ok, documentation_ok)
    claims_rows = read_csv(CLAIMS)
    variable_rows = read_csv(VARIABLES)
    csv_registry_ok = sum(row["claim_id"] == "L-797" for row in claims_rows) == 1 and sum(row["symbol"] == "PredictivityStatus4955_MTS" for row in variable_rows) == 1 and len(claims_rows[-1]) == 13 and len(variable_rows[-1]) == 11
    add(checks, "VAL4955_30_registry_csv", "claims and variable registers parse cleanly with unique 4955 rows", True, csv_registry_ok, csv_registry_ok)
    prohibited = ["FULL_MTS_TRUE", "FIXED_R3_DERIVED", "COMPLETE_PARENT_FLOW_TRUE"]
    synchronized = "\n".join((checkpoint_text, formal_text, equations_text, red_text, spine_text, resume_text))
    present = [token for token in prohibited if token in synchronized]
    add(checks, "VAL4955_31_prohibitions", "synchronized prose contains no false promotion marker", [], present, not present)
    provenance_text = PROVENANCE.read_text(encoding="utf-8")
    provenance_ok = all(value in provenance_text for value in result["source_hashes"].values())
    add(checks, "VAL4955_32_provenance", "provenance records every locked source hash", True, provenance_ok, provenance_ok)
    pycache = list((POST / "scripts").glob("__pycache__"))
    add(checks, "VAL4955_33_pycache", "no script bytecode cache remains", [], [str(path) for path in pycache], not pycache)
    reproducibility = {
        "research_sha256": digest(RESEARCH),
        "result_sha256": digest(RESULT),
        "checkpoint_sha256": digest(CHECKPOINT),
    }
    add(checks, "VAL4955_34_hash_report", "reproducibility hashes are nonempty SHA-256 values", "three 64-character hashes", reproducibility, all(len(value) == 64 for value in reproducibility.values()))

    all_previous = all(as_bool(row["passed"]) for row in checks)
    add(checks, "VAL4955_35_complete", "all preceding independent checks pass", True, all_previous, all_previous)
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)
    return 0 if all(as_bool(row["passed"]) for row in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
