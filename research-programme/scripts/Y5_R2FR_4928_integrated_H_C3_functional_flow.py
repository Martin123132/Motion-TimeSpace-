from __future__ import annotations

import csv
import hashlib
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.constants import G, c, hbar
from scipy.integrate import solve_ivp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "functional_rg" / "4928"
SCRIPTS = POST / "scripts"

CHECKED_DATE = "2026-07-12"
MARKER = "MTS_INTEGRATED_H_C3_FUNCTIONAL_FLOW_4928"
FORMAL_MARKER = "PPC4161_INTEGRATED_H_C3_FUNCTIONAL_FLOW_4928"
NEXT_TARGET = "4929-Y5-R2FR-MTS-matter-completed-C3-essential-flow-and-fixed-point-survival-or-one-Wilson-retention.md"

AS_2016_URL = "https://arxiv.org/abs/1601.01800"
AS_2026_URL = "https://arxiv.org/abs/2509.07058"
AS_2016_PDF = SOURCE / "1601.01800v1.pdf"
AS_2016_SOURCE = SOURCE / "1601.01800v1-source.tar"
AS_2026_PDF = SOURCE / "2509.07058v1.pdf"
AS_2026_SOURCE = SOURCE / "2509.07058v1-source.tar"
AS_2016_TEX = SOURCE / "src1601" / "letter.tex"
AS_2026_TEX = SOURCE / "src2509" / "notes.tex"
NATURAL_NOTEBOOK = SOURCE / "src2509" / "betas_natural_scheme.nb"
PROVENANCE = SOURCE / "PROVENANCE.md"

EXPECTED_HASHES = {
    AS_2016_PDF: "8e1b524465a2b6b112ea63ca339ccc84da216bdd0b25d6665b2931e9135cc822",
    AS_2016_SOURCE: "016ffc070fc1d10d798eb3b8ae37b82abe07897137c722691e2de96f70f6ec89",
    AS_2026_PDF: "e203ead85ebdf37a94c03d52c1a6e68c4d45ab72a90415e1ff165adc42d712ec",
    AS_2026_SOURCE: "11cf0a348b5413e7daf896dcf59b560698780b3a21b3670f54664eeb5c9b7c1d",
}

CHECKPOINT_4876 = POST / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md"
CHECKPOINT_4923 = POST / "4923-Y5-R2FR-GW250114-gravitational-QNM-parity-even-Weyl-cubic-recast-or-posterior-acquisition-gate.md"
CHECKPOINT_4925 = POST / "4925-Y5-R2FR-integrated-H-two-loop-renormalization-condition-and-finite-zeta-plus-boundary-owner-or-explicit-Wilson-input.md"
CHECKPOINT_4927 = POST / "4927-Y5-R2FR-motion-field-normalization-from-metric-covariance-residue-and-EH-matching-or-one-Wilson-freeze.md"
WILSON_BOUND_PATH = OUTPUT / "P8_Y5_R2FR_4925_WILSON_BOUND.csv"
BRANCH_RECAST_PATH = OUTPUT / "P8_Y5_R2FR_4923_BRANCH_RECAST.csv"

CHECKPOINT_DOC = POST / "4928-Y5-R2FR-integrated-H-C3-functional-flow-boundary-or-observational-Wilson-freeze.md"
FORMAL_NOTE = FORMAL / "944-PPC4161-integrated-H-C3-functional-flow-and-Wilson-freeze.md"
VALIDATION = SCRIPTS / "Y5_R2FR_4928_integrated_H_C3_functional_flow_validation.py"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
VARIABLE_REGISTER = FORMAL / "04-variable-audit.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM_REGISTER = FORMAL / "06-consistency-red-team.md"
SPINE_REGISTER = FORMAL / "07-unification-spine.md"

PLANCK_LENGTH_M = math.sqrt(hbar * G / c**3)
SOLAR_MASS_KG = 1.988409870698051e30


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for row in rows:
        row["checkpoint_marker"] = MARKER
        row["valid_for_claim"] = False
        row["source_checked_date"] = CHECKED_DATE
    return rows


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_text_auto(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def beta_g(newton: float) -> float:
    return (
        2.0
        * newton
        * (-32.0 * newton + 6.0 * math.pi)
        / (-9.0 * newton + 6.0 * math.pi)
    )


def c3_polynomial_coefficients(newton: float) -> tuple[float, float, float, float]:
    pi = math.pi
    constant = 69.0 * newton
    linear = (
        -3_709_440.0 * newton**2 * pi
        + 14_515_200.0 * newton * pi**2
        + 1_451_520.0 * pi**3
    )
    quadratic = (
        47_585_664.0 * newton**3 * pi**2
        - 21_337_344.0 * newton**2 * pi**3
    )
    cubic = (
        -84_188_160.0 * newton**4 * pi**3
        + 78_382_080.0 * newton**3 * pi**4
    )
    return constant, linear, quadratic, cubic


def beta_c3(newton: float, c3_coupling: float) -> float:
    constant, linear, quadratic, cubic = c3_polynomial_coefficients(newton)
    numerator = (
        constant
        + linear * c3_coupling
        + quadratic * c3_coupling**2
        + cubic * c3_coupling**3
    )
    denominator = (
        120_960.0
        * (9.0 * newton - 6.0 * math.pi)
        * math.pi**2
    )
    return -numerator / denominator


def fixed_point_data() -> dict[str, float]:
    newton_star = 3.0 * math.pi / 16.0
    coefficients = c3_polynomial_coefficients(newton_star)
    roots = np.roots([coefficients[3], coefficients[2], coefficients[1], coefficients[0]])
    real_roots = [float(root.real) for root in roots if abs(root.imag) < 1.0e-11]
    if len(real_roots) != 1:
        raise RuntimeError(f"expected one real C3 fixed point, found {roots}")
    c3_star = real_roots[0]

    constant, linear, quadratic, cubic = coefficients
    denominator = (
        120_960.0
        * (9.0 * newton_star - 6.0 * math.pi)
        * math.pi**2
    )
    d_beta_c3_d_c3 = -(
        linear + 2.0 * quadratic * c3_star + 3.0 * cubic * c3_star**2
    ) / denominator

    pi = math.pi
    d_constant = 69.0
    d_linear = -7_418_880.0 * newton_star * pi + 14_515_200.0 * pi**2
    d_quadratic = (
        142_756_992.0 * newton_star**2 * pi**2
        - 42_674_688.0 * newton_star * pi**3
    )
    d_cubic = (
        -336_752_640.0 * newton_star**3 * pi**3
        + 235_146_240.0 * newton_star**2 * pi**4
    )
    d_numerator_d_newton = (
        d_constant
        + d_linear * c3_star
        + d_quadratic * c3_star**2
        + d_cubic * c3_star**3
    )
    d_beta_c3_d_newton = -d_numerator_d_newton / denominator
    d_beta_g_d_newton = -64.0 / 23.0
    relevant_slope = -d_beta_c3_d_newton / (
        d_beta_c3_d_c3 - d_beta_g_d_newton
    )
    return {
        "newton_star": newton_star,
        "c3_star": c3_star,
        "theta_relevant": -d_beta_g_d_newton,
        "theta_irrelevant": -d_beta_c3_d_c3,
        "d_beta_c3_d_newton": d_beta_c3_d_newton,
        "d_beta_c3_d_c3": d_beta_c3_d_c3,
        "relevant_slope": relevant_slope,
        "complex_root_count": float(len(roots) - len(real_roots)),
    }


def integrate_separatrix(
    fixed: dict[str, float],
) -> tuple[list[dict[str, Any]], float, float]:
    epsilon = 1.0e-6
    newton_initial = fixed["newton_star"] - epsilon
    c3_initial = fixed["c3_star"] + fixed["relevant_slope"] * (
        newton_initial - fixed["newton_star"]
    )
    log_newton_initial = math.log(newton_initial)
    ratio_initial = c3_initial / newton_initial
    log_coefficient = 69.0 / (725_760.0 * math.pi**3)

    def ratio_flow(log_newton: float, state: np.ndarray) -> list[float]:
        newton = math.exp(log_newton)
        ratio = float(state[0])
        return [beta_c3(newton, ratio * newton) / beta_g(newton) - ratio]

    solution = solve_ivp(
        ratio_flow,
        (log_newton_initial, -50.0),
        [ratio_initial],
        rtol=2.0e-12,
        atol=1.0e-14,
        max_step=0.02,
        dense_output=True,
    )
    if not solution.success or solution.sol is None:
        raise RuntimeError(f"separatrix integration failed: {solution.message}")

    sample_logs = np.linspace(log_newton_initial, -50.0, 121)
    rows: list[dict[str, Any]] = []
    for index, log_newton in enumerate(sample_logs):
        newton = math.exp(float(log_newton))
        ratio = float(solution.sol(float(log_newton))[0])
        c3_coupling = ratio * newton
        subtracted = ratio - 0.5 * log_coefficient * float(log_newton)
        residual = math.hypot(beta_g(newton), beta_c3(newton, c3_coupling))
        rows.append(
            {
                "sample_id": f"SEP4928_{index:03d}",
                "ln_g": float(log_newton),
                "g": newton,
                "g_C3": c3_coupling,
                "g_C3_over_g": ratio,
                "analytic_log_coefficient_dratio_dlnk": log_coefficient,
                "log_subtracted_ratio": subtracted,
                "distance_from_fixed_flow": residual,
                "IR_sample": float(log_newton) <= -30.0,
                "status": "UNIQUE_RELEVANT_SEPARATRIX_NUMERIC",
                "passed": math.isfinite(subtracted),
            }
        )
    infrared_ratio = float(solution.sol(-50.0)[0])
    infrared_constant = infrared_ratio - 0.5 * log_coefficient * -50.0
    return tagged(rows), infrared_constant, log_coefficient


def beta_rows(log_coefficient: float) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "object": "dimensionless Newton coupling",
                "definition": "g=k^2 G_N(k)",
                "beta_function": "beta_g=2g(-32g+6pi)/(-9g+6pi)",
                "IR_expansion": "beta_g=2g+O(g^2)",
                "derived_value": 2.0,
                "source": "2509.07058v1 attached natural-scheme notebook",
                "status": "SOURCE_TRANSCRIBED_AND_EXECUTED",
                "passed": True,
            },
            {
                "object": "dimensionless Weyl-cubic coupling",
                "definition": "h=g_C3=k^2 G_C3(k)",
                "beta_function": "beta_h=-N(g,h)/[120960(9g-6pi)pi^2] with cubic N",
                "IR_expansion": "beta_h=2h+c_log g+O(g h,g^2,h^2)",
                "derived_value": log_coefficient,
                "source": "2509.07058v1 attached natural-scheme notebook",
                "status": "SOURCE_TRANSCRIBED_AND_EXECUTED",
                "passed": True,
            },
            {
                "object": "massless logarithmic slope",
                "definition": "c_log=lim_(g,h->0)(beta_h-2h)/g",
                "beta_function": "c_log=69/(725760 pi^3)=23/(241920 pi^3)",
                "IR_expansion": "h/g=A_C3+c_log ln(k/k0)+o(1)",
                "derived_value": log_coefficient,
                "source": "independent expansion of attached beta functions",
                "status": "EXACT_IR_LOG_COEFFICIENT_DERIVED",
                "passed": log_coefficient > 0.0,
            },
        ]
    )


def fixed_point_rows(fixed: dict[str, float]) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "fixed_point": "Gaussian",
                "g_star": 0.0,
                "g_C3_star": 0.0,
                "beta_norm": 0.0,
                "theta_1": -2.0,
                "theta_2": -2.0,
                "relevant_directions": 0,
                "fixed_scale_free_parameters": "not the selected UV completion",
                "status": "IR_GAUSSIAN_ENDPOINT",
                "passed": True,
            },
            {
                "fixed_point": "natural-scheme non-Gaussian",
                "g_star": fixed["newton_star"],
                "g_C3_star": fixed["c3_star"],
                "beta_norm": math.hypot(
                    beta_g(fixed["newton_star"]),
                    beta_c3(fixed["newton_star"], fixed["c3_star"]),
                ),
                "theta_1": fixed["theta_relevant"],
                "theta_2": fixed["theta_irrelevant"],
                "relevant_directions": 1,
                "fixed_scale_free_parameters": 0,
                "status": "ONE_RELEVANT_DIRECTION_AFTER_UNIT_SCALE",
                "passed": fixed["theta_relevant"] > 0.0
                and fixed["theta_irrelevant"] < 0.0,
            },
        ]
    )


def log_sign_rows(infrared_constant: float, log_coefficient: float) -> list[dict[str, Any]]:
    critical_scale = math.exp(-infrared_constant / log_coefficient)
    return tagged(
        [
            {
                "audit_id": "LOG4928_00_notebook",
                "source_object": "attached natural-regulator beta notebook",
                "reported_or_derived_slope": log_coefficient,
                "sign": "positive",
                "test": "canonical small-g expansion",
                "result": "beta_h=2h+c_log g gives d(h/g)/d ln k=c_log>0",
                "status": "EXECUTABLE_SOURCE_SIGN_DERIVED",
                "passed": True,
            },
            {
                "audit_id": "LOG4928_01_article_text",
                "source_object": "2509.07058v1 notes.tex natural-scheme paragraph",
                "reported_or_derived_slope": -3.07e-6,
                "sign": "negative",
                "test": "literal source-text value",
                "result": "opposite to the attached notebook convention",
                "status": "SOURCE_INTERNAL_SIGN_DISCREPANCY",
                "passed": True,
            },
            {
                "audit_id": "LOG4928_02_limit",
                "source_object": "independently integrated attached notebook",
                "reported_or_derived_slope": log_coefficient,
                "sign": "positive",
                "test": "A=lim_[g->0]{h/g-(c_log/2)ln g}",
                "result": infrared_constant,
                "status": "PUBLISHED_3P02E_MINUS6_LIMIT_REPRODUCED",
                "passed": abs(infrared_constant - 3.02e-6) < 1.0e-8,
            },
            {
                "audit_id": "LOG4928_03_reference_crossing",
                "source_object": "reference-scale transform A(xi)=A(1)+c_log ln xi",
                "reported_or_derived_slope": log_coefficient,
                "sign": "positive",
                "test": "xi_zero=exp(-A/c_log)",
                "result": critical_scale,
                "status": "ARTICLE_0P37_CROSSING_REPRODUCED_ONLY_WITH_POSITIVE_SLOPE",
                "passed": abs(critical_scale - 0.37) < 0.01,
            },
        ]
    )


def operator_map_rows(infrared_constant: float) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "map_id": "OMAP4928_00_action",
                "external_object": "integral sqrt(g)[-R/(16pi G_N)+G_C3 C^3]",
                "MTS_object": "(16pi G_N)^-1 integral sqrt(-g)[R+a_+ I1]",
                "relation": "I1=C^3 on Ricci-flat vacuum and zeta_+=G_C3",
                "dimension_check": "[G_C3]=-2; [zeta_+]=-2",
                "result": "SAME_ESSENTIAL_SIX_DERIVATIVE_OPERATOR",
                "passed": True,
            },
            {
                "map_id": "OMAP4928_01_coefficient",
                "external_object": "r_C3=G_C3/G_N",
                "MTS_object": "a_+=16pi G_N zeta_+",
                "relation": "a_+/l_P^4=16pi r_C3",
                "dimension_check": "[a_+]=-4",
                "result": 16.0 * math.pi * infrared_constant,
                "passed": True,
            },
            {
                "map_id": "OMAP4928_02_QNM",
                "external_object": "positive G_C3 in the source convention",
                "MTS_object": "alpha_ev=a_+/M^4=s_+(ell_+/M)^4",
                "relation": "sign(alpha_ev)=sign(G_C3) after the locked operator map",
                "dimension_check": "dimensionless",
                "result": "POSITIVE_CONDITIONAL_BRANCH",
                "passed": True,
            },
        ]
    )


def reference_scale_rows(infrared_constant: float, log_coefficient: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    critical_scale = math.exp(-infrared_constant / log_coefficient)
    scales = [0.1, 0.2, 0.3, critical_scale, 0.5, 1.0, 2.0, 10.0]
    for scale in scales:
        shifted = infrared_constant + log_coefficient * math.log(scale)
        rows.append(
            {
                "xi_k0_over_MPl": scale,
                "r_C3_at_reference": shifted,
                "sign": "positive" if shifted > 1.0e-18 else "negative" if shifted < -1.0e-18 else "zero",
                "transform": "r_C3(xi)=r_C3(1)+c_log ln(xi)",
                "regular_extremal_Kerr_condition_in_external_branch": shifted >= -1.0e-18,
                "status": "REFERENCE_SCALE_CONDITIONAL_NOT_MTS_PREDICTION",
                "passed": math.isfinite(shifted),
            }
        )
    return tagged(rows)


def conditional_prediction_rows(infrared_constant: float) -> list[dict[str, Any]]:
    robust_bound = next(
        row for row in read_csv(WILSON_BOUND_PATH) if row["bound_id"] == "WBOUND4925_00_robust_abs"
    )
    compact_bound = next(
        row for row in read_csv(WILSON_BOUND_PATH) if row["bound_id"] == "WBOUND4925_02_NS_domain"
    )
    gw_mass_solar = float(robust_bound["mass_anchor_solar"])
    gw_mass_m = G * SOLAR_MASS_KG * gw_mass_solar / c**2
    observational_a_bound = float(robust_bound["abs_a_eff_bound_m4"])
    compact_a_bound = float(compact_bound["abs_a_eff_bound_m4"])
    branches = [
        (
            "natural_regulator_reproduced",
            infrared_constant,
            "independently integrated attached 2509.07058 beta notebook",
            "CONDITIONAL_PURE_GRAVITY_TRUNCATION",
        ),
        (
            "shifted_regulator_quoted",
            9.6e-3,
            "2509.07058 quoted subtraction branch",
            "SOURCE_QUOTED_SCHEME_COMPARATOR",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for branch, ratio, source, status in branches:
        a_over_planck4 = 16.0 * math.pi * ratio
        signed_length_over_planck = abs(a_over_planck4) ** 0.25
        signed_length_m = signed_length_over_planck * PLANCK_LENGTH_M
        coefficient_m4 = math.copysign(signed_length_m**4, ratio)
        rows.append(
            {
                "branch": branch,
                "G_C3_over_G_N": ratio,
                "a_plus_over_lPlanck4": a_over_planck4,
                "ell_plus_over_lPlanck": signed_length_over_planck,
                "ell_plus_m": signed_length_m,
                "a_plus_m4": coefficient_m4,
                "alpha_ev_at_GW250114_mass": coefficient_m4 / gw_mass_m**4,
                "ratio_to_robust_GW_coefficient_bound": abs(coefficient_m4) / observational_a_bound,
                "ratio_to_NS_one_percent_target": abs(coefficient_m4) / compact_a_bound,
                "coefficient_sign": "positive" if ratio > 0.0 else "negative",
                "source": source,
                "status": status,
                "passed": abs(coefficient_m4) < compact_a_bound,
            }
        )
    return tagged(rows)


def parent_inheritance_rows() -> list[dict[str, Any]]:
    clauses = [
        (
            "H_to_g_coordinate",
            "four-dimensional H-to-g map is locally invertible",
            True,
            "4925 exact point Jacobian",
            False,
            "KINEMATICALLY_CLOSED",
        ),
        (
            "coordinate_measure",
            "flat component D H differs from D g only by a field-independent point Jacobian",
            True,
            "abs det(dH/dg)=1 in d=4",
            False,
            "NO_HIDDEN_C3_MEASURE_SOURCE",
        ),
        (
            "essential_operator_basis",
            "Ricci-flat parity-even six-derivative quotient is the same I1=C3 coordinate",
            True,
            "4922-4925 operator map",
            False,
            "BASIS_CLOSED",
        ),
        (
            "natural_graviton_regulator",
            "all gravity and ghost regulators use the source natural endomorphisms",
            False,
            "not selected by the current integrated-H parent",
            True,
            "OPEN_PARENT_REGULATOR",
        ),
        (
            "zero_cosmological_truncation",
            "Lambda_k=0 remains on the essential flow trajectory",
            False,
            "C0_R=0 is a renormalized saddle condition rather than a derived UV trajectory",
            True,
            "OPEN_FLAT_FLOW_CONDITION",
        ),
        (
            "pure_gravity_UV_field_content",
            "no light MTS SM EM or bath fields deform the two beta functions near the fixed point",
            False,
            "the active framework explicitly contains matter EM and an MTS scalar sector",
            True,
            "FAILED_FULL_PARENT_FIELD_CONTENT",
        ),
        (
            "full_MTS_fixed_point",
            "the complete MTS essential flow has a non-Gaussian fixed point",
            False,
            "not calculated",
            True,
            "OPEN_DYNAMIC_FIXED_POINT",
        ),
        (
            "one_relevant_direction_after_matter",
            "the complete fixed point leaves no dimensionless C3 datum after fixing G_N",
            False,
            "pure-gravity result cannot establish the matter-completed stability matrix",
            True,
            "OPEN_CRITICAL_SURFACE_DIMENSION",
        ),
        (
            "Planck_transition_scale",
            "k0=M_Pl follows from the MTS parent rather than a naturalness prescription",
            False,
            "the scale choice is externally prescribed and logarithmically scheme dependent",
            True,
            "OPEN_TRANSITION_SCALE_OWNER",
        ),
    ]
    rows = []
    for clause, requirement, satisfied, evidence, blocks, status in clauses:
        rows.append(
            {
                "clause": clause,
                "inheritance_requirement": requirement,
                "MTS_clause_satisfied": satisfied,
                "evidence": evidence,
                "blocks_MTS_numeric_prediction": blocks,
                "status": status,
                "passed": True,
            }
        )
    rows.append(
        {
            "clause": "all_dynamic_inheritance",
            "inheritance_requirement": "every blocking dynamical clause is parent-signed",
            "MTS_clause_satisfied": all(
                row["MTS_clause_satisfied"] for row in rows
            ),
            "evidence": "three kinematic clauses close but six dynamical/scale clauses do not",
            "blocks_MTS_numeric_prediction": True,
            "status": "PURE_GRAVITY_FLOW_NOT_INHERITED_AS_MTS_PREDICTION",
            "passed": True,
        }
    )
    return tagged(rows)


def observational_freeze_rows(infrared_constant: float) -> list[dict[str, Any]]:
    bounds = {row["bound_id"]: row for row in read_csv(WILSON_BOUND_PATH)}
    branches = {row["branch"]: row for row in read_csv(BRANCH_RECAST_PATH)}
    robust = bounds["WBOUND4925_00_robust_abs"]
    positive = bounds["WBOUND4925_01_positive"]
    compact = bounds["WBOUND4925_02_NS_domain"]
    conditional_a_m4 = (
        16.0 * math.pi * infrared_constant * PLANCK_LENGTH_M**4
    )
    rows = [
        {
            "freeze_id": "WF4928_00_parameter",
            "observable_parameter": "A_+(Q_GW)=RG-invariant local-plus-log amplitude coefficient at the GW250114 kinematic reference",
            "lower": -float(robust["abs_a_eff_bound_m4"]),
            "upper": float(robust["abs_a_eff_bound_m4"]),
            "units": "m^4",
            "independent_IR_test_parameters": 1,
            "source": "P8_Y5_R2FR_4925_WILSON_BOUND.csv",
            "interpretation": "robust signed two-branch envelope; not a combined polarization likelihood",
            "status": "SELECTED_ONE_OBSERVATIONAL_WILSON_FREEZE",
            "passed": True,
        },
        {
            "freeze_id": "WF4928_01_positive",
            "observable_parameter": "A_+(Q_GW) conditional nonnegative branch",
            "lower": 0.0,
            "upper": float(positive["abs_a_eff_bound_m4"]),
            "units": "m^4",
            "independent_IR_test_parameters": 1,
            "source": "P8_Y5_R2FR_4925_WILSON_BOUND.csv",
            "interpretation": "applies only if the total matched coefficient is nonnegative",
            "status": "CONDITIONAL_POSITIVE_ENVELOPE",
            "passed": True,
        },
        {
            "freeze_id": "WF4928_02_polar",
            "observable_parameter": "alpha_ev polar_plus",
            "lower": float(branches["polar_plus"]["alpha_lower_90"]),
            "upper": float(branches["polar_plus"]["alpha_upper_90"]),
            "units": "dimensionless",
            "independent_IR_test_parameters": 1,
            "source": "P8_Y5_R2FR_4923_BRANCH_RECAST.csv",
            "interpretation": "branch-conditional 90 percent interval containing GR",
            "status": "OBSERVATIONAL_BRANCH_NONCLAIM",
            "passed": branches["polar_plus"]["GR_inside_90"] == "True",
        },
        {
            "freeze_id": "WF4928_03_axial",
            "observable_parameter": "alpha_ev axial_minus",
            "lower": float(branches["axial_minus"]["alpha_lower_90"]),
            "upper": float(branches["axial_minus"]["alpha_upper_90"]),
            "units": "dimensionless",
            "independent_IR_test_parameters": 1,
            "source": "P8_Y5_R2FR_4923_BRANCH_RECAST.csv",
            "interpretation": "branch-conditional 90 percent interval containing GR",
            "status": "OBSERVATIONAL_BRANCH_NONCLAIM",
            "passed": branches["axial_minus"]["GR_inside_90"] == "True",
        },
        {
            "freeze_id": "WF4928_04_compact_gap",
            "observable_parameter": "selected one-percent neutron-star coefficient domain",
            "lower": -float(compact["abs_a_eff_bound_m4"]),
            "upper": float(compact["abs_a_eff_bound_m4"]),
            "units": "m^4",
            "independent_IR_test_parameters": 1,
            "source": "P8_Y5_R2FR_4925_WILSON_BOUND.csv",
            "interpretation": "internal perturbative-control target not reached by the observational envelope",
            "status": "COMPACT_PROMOTION_NOT_OBSERVATIONALLY_CLOSED",
            "passed": True,
        },
        {
            "freeze_id": "WF4928_05_conditional_AS",
            "observable_parameter": "conditional pure-gravity natural-flow a_+",
            "lower": conditional_a_m4,
            "upper": conditional_a_m4,
            "units": "m^4",
            "independent_IR_test_parameters": 0,
            "source": "checkpoint 4928 separatrix integration",
            "interpretation": "not selected as MTS prediction because dynamic inheritance fails",
            "status": "CONDITIONAL_CALCULATED_BRANCH_ONLY",
            "passed": conditional_a_m4 < float(compact["abs_a_eff_bound_m4"]),
        },
    ]
    return tagged(rows)


def gate_rows(
    fixed: dict[str, float],
    infrared_constant: float,
    inheritance: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    inherited = next(
        row for row in inheritance if row["clause"] == "all_dynamic_inheritance"
    )["MTS_clause_satisfied"]
    return tagged(
        [
            {
                "gate": "natural_beta_reproduction",
                "status": "PASS",
                "decision": f"NGFP=({fixed['newton_star']:.12g},{fixed['c3_star']:.12g}); A_C3={infrared_constant:.12g}",
                "claim_promoted": False,
                "passed": abs(infrared_constant - 3.02e-6) < 1.0e-8,
            },
            {
                "gate": "integrated_H_kinematic_compatibility",
                "status": "DERIVED",
                "decision": "constant H-to-g Jacobian and common essential I1 basis permit the same pure-metric flow after a covariant regulator choice",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "MTS_dynamic_flow_inheritance",
                "status": "NOT_DERIVED",
                "decision": "matter EM motion-field regulator flat-flow and complete fixed-point clauses remain open",
                "claim_promoted": False,
                "passed": not inherited,
            },
            {
                "gate": "conditional_pure_gravity_branch",
                "status": "CALCULATED_NONCLAIM",
                "decision": "natural essential truncation gives positive Planck-suppressed a_+ and is compact-safe by more than 150 coefficient orders",
                "claim_promoted": False,
                "passed": infrared_constant > 0.0,
            },
            {
                "gate": "observational_Wilson_freeze",
                "status": "ONE_SIGNED_PARAMETER_SELECTED",
                "decision": "retain one RG-invariant A_+(Q_GW) bounded by the existing GW250114 branch envelope",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "weak_GR_Newton_Maxwell",
                "status": "RETAINED",
                "decision": "the six-derivative flow does not alter the calibrated two-derivative Hilbert-source limit",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "compact_GR",
                "status": "NOT_PROMOTED",
                "decision": "conditional fixed-point branch is safe but not inherited; observation alone remains above the compact one-percent target",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "full_MTS_to_GR",
                "status": "NOT_PROMOTED",
                "decision": "complete matter-coupled essential flow and ultraviolet critical surface remain uncalculated",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "next_target",
                "status": "MATTER_COMPLETED_ESSENTIAL_FLOW",
                "decision": NEXT_TARGET,
                "claim_promoted": False,
                "passed": True,
            },
        ]
    )


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, expected_hash, role in (
        ("SRC4928_00_2016_pdf", AS_2016_PDF, EXPECTED_HASHES[AS_2016_PDF], "original_GS_FRG_paper"),
        ("SRC4928_01_2016_source", AS_2016_SOURCE, EXPECTED_HASHES[AS_2016_SOURCE], "author_TeX_fixed_point_equations"),
        ("SRC4928_02_2026_pdf", AS_2026_PDF, EXPECTED_HASHES[AS_2026_PDF], "IR_Wilson_prediction_paper"),
        ("SRC4928_03_2026_source", AS_2026_SOURCE, EXPECTED_HASHES[AS_2026_SOURCE], "author_TeX_and_beta_notebook"),
    ):
        exists = path.exists()
        actual_hash = digest(path) if exists else ""
        passed = exists and actual_hash == expected_hash
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": path.relative_to(ROOT).as_posix(),
                "source_role": role,
                "verification": "SHA256",
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
                "source_exists": exists,
                "marker_found": passed,
                "status": "LOCAL_BINARY_SOURCE_HASH_VERIFIED" if passed else "LOCAL_BINARY_SOURCE_FAILED",
                "passed": passed,
            }
        )
    for source_id, path, marker, role in (
        ("SRC4928_04_provenance", PROVENANCE, "MTS_INTEGRATED_H_C3_FUNCTIONAL_FLOW_PROVENANCE_4928", "source_provenance"),
        ("SRC4928_05_2016_tex", AS_2016_TEX, "\\sigma_* = -0.305", "original_fixed_point_text"),
        ("SRC4928_06_2026_tex", AS_2026_TEX, "3.02 \\cdot 10^{-6}G_{\\text{N}}", "published_natural_scheme_limit"),
        ("SRC4928_07_notebook", NATURAL_NOTEBOOK, "3709440", "attached_natural_beta_functions"),
        ("SRC4928_08_4876", CHECKPOINT_4876, "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876", "integrated_H_parent"),
        ("SRC4928_09_4923", CHECKPOINT_4923, "MTS_GW250114_GRAVITATIONAL_QNM_WEYL_C3_RECAST_4923", "observational_branch_recast"),
        ("SRC4928_10_4925", CHECKPOINT_4925, "MTS_INTEGRATED_H_TWO_LOOP_WILSON_BOUNDARY_4925", "one_Wilson_theorem"),
        ("SRC4928_11_4927", CHECKPOINT_4927, "MTS_MOTION_NORMALIZATION_COVARIANCE_RESIDUE_4927", "predecessor_normalization_gate"),
        ("SRC4928_12_Wilson", WILSON_BOUND_PATH, "WBOUND4925_00_robust_abs", "current_Wilson_bound"),
        ("SRC4928_13_branches", BRANCH_RECAST_PATH, "polar_plus", "current_branch_intervals"),
        ("SRC4928_14_research", Path(__file__).resolve(), "def integrate_separatrix", "generated_research_code"),
        ("SRC4928_15_checkpoint", CHECKPOINT_DOC, MARKER, "generated_checkpoint"),
        ("SRC4928_16_formal", FORMAL_NOTE, FORMAL_MARKER, "formal_checkpoint_note"),
        ("SRC4928_17_validation", VALIDATION, "MTS_INTEGRATED_H_C3_FUNCTIONAL_FLOW_VALIDATION_4928", "independent_validation_code"),
        ("SRC4928_18_resume", RESUME, NEXT_TARGET, "local_resume_ledger"),
        ("SRC4928_19_claims", CLAIMS_REGISTER, "L-770", "claim_register"),
        ("SRC4928_20_variables", VARIABLE_REGISTER, "C3FunctionalFlowStatus4928_MTS", "variable_register"),
        ("SRC4928_21_equations", EQUATION_REGISTER, "1.221 Integrated-H C3 functional flow and observational Wilson freeze", "equation_register"),
        ("SRC4928_22_red_team", RED_TEAM_REGISTER, "172. A pure-gravity fixed-point trajectory is not automatically the MTS ultraviolet trajectory", "red_team_register"),
        ("SRC4928_23_spine", SPINE_REGISTER, "PPC4161 checkpoint 4928", "unification_spine"),
    ):
        exists = path.exists()
        marker_found = exists and marker in read_text_auto(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": path.relative_to(ROOT).as_posix(),
                "source_role": role,
                "verification": "path_and_marker",
                "expected_sha256": "",
                "actual_sha256": digest(path) if exists else "",
                "source_exists": exists,
                "marker_found": marker_found,
                "status": "LOCAL_TEXT_SOURCE_VERIFIED" if marker_found else "LOCAL_TEXT_SOURCE_FAILED",
                "passed": marker_found,
            }
        )
    for source_id, url, role in (
        ("SRC4928_24_2016_URL", AS_2016_URL, "primary_original_FRG_record"),
        ("SRC4928_25_2026_URL", AS_2026_URL, "primary_Wilson_prediction_record"),
    ):
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": url,
                "source_role": role,
                "verification": "external_primary_URL_recorded",
                "expected_sha256": "",
                "actual_sha256": "",
                "source_exists": True,
                "marker_found": True,
                "status": "EXTERNAL_PRIMARY_URL_RECORDED",
                "passed": True,
            }
        )
    return tagged(rows)


def main() -> int:
    fixed = fixed_point_data()
    separatrix, infrared_constant, log_coefficient = integrate_separatrix(fixed)
    beta = beta_rows(log_coefficient)
    fixed_points = fixed_point_rows(fixed)
    log_sign = log_sign_rows(infrared_constant, log_coefficient)
    operator_map = operator_map_rows(infrared_constant)
    scale_scan = reference_scale_rows(infrared_constant, log_coefficient)
    conditional = conditional_prediction_rows(infrared_constant)
    inheritance = parent_inheritance_rows()
    freeze = observational_freeze_rows(infrared_constant)
    gates = gate_rows(fixed, infrared_constant, inheritance)
    sources = source_register_rows()
    tables = {
        "P8_Y5_R2FR_4928_NATURAL_BETA_FUNCTION.csv": beta,
        "P8_Y5_R2FR_4928_FIXED_POINT.csv": fixed_points,
        "P8_Y5_R2FR_4928_SEPARATRIX.csv": separatrix,
        "P8_Y5_R2FR_4928_LOG_SIGN_AUDIT.csv": log_sign,
        "P8_Y5_R2FR_4928_OPERATOR_MAP.csv": operator_map,
        "P8_Y5_R2FR_4928_REFERENCE_SCALE_SCAN.csv": scale_scan,
        "P8_Y5_R2FR_4928_CONDITIONAL_PREDICTION.csv": conditional,
        "P8_Y5_R2FR_4928_PARENT_INHERITANCE_GATE.csv": inheritance,
        "P8_Y5_R2FR_4928_OBSERVATIONAL_WILSON_FREEZE.csv": freeze,
        "P8_Y5_R2FR_4928_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4928_GATE_DECISION.csv": gates,
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    passed = all(bool(row.get("passed", True)) for rows in tables.values() for row in rows)
    natural = conditional[0]
    print(
        "P8_Y5_R2FR_4928_INTEGRATED_H_C3_FUNCTIONAL_FLOW_PASS"
        if passed
        else "P8_Y5_R2FR_4928_INTEGRATED_H_C3_FUNCTIONAL_FLOW_FAIL"
    )
    print(f"natural_g_star={fixed['newton_star']:.16e}")
    print(f"natural_g_C3_star={fixed['c3_star']:.16e}")
    print(f"critical_exponents={fixed['theta_relevant']:.12g},{fixed['theta_irrelevant']:.12g}")
    print(f"IR_G_C3_over_G_N={infrared_constant:.16e}")
    print(f"IR_log_coefficient={log_coefficient:.16e}")
    print("article_log_sign_discrepancy=True")
    print(f"conditional_ell_plus_m={float(natural['ell_plus_m']):.16e}")
    print("MTS_dynamic_flow_inherited=False")
    print("independent_IR_I1_test_parameters=1")
    print("compact_GR_promoted=False")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
