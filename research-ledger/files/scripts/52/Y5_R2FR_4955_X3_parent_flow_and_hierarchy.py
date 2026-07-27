from __future__ import annotations

import csv
import hashlib
import json
import math
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

RESULT_JSON = SOURCE / "X3_parent_flow_results.json"
GRAVITY_CSV = SOURCE / "minimal_gravity_X2_X3_source_projection.csv"
HIERARCHY_CSV = SOURCE / "PX_coefficient_hierarchy.csv"
OPERATORS_CSV = SOURCE / "six_derivative_operator_flow_roles.csv"
TRAJECTORY_CSV = SOURCE / "GR_gaussian_X3_forced_trajectory.csv"
SPARC_CSV = SOURCE / "SPARC_parent_forced_X3_coordinate_gate.csv"
DECISION_CSV = SOURCE / "X3_parent_flow_decision.csv"

BASIS_TEX = POST / "source-intake" / "functional_rg" / "4930" / "src1908" / "GravityEFTv2_final.tex"
SCALAR_TEX = POST / "source-intake" / "functional_rg" / "4937" / "src-2110.09566v1" / "SSTwAS.tex"
O4_4941 = POST / "4941-Y5-R2FR-natural-TypeII-direct-metric-scalar-O4-zero-proof-and-minimal-O4-parent-completion-gate.md"
LOWER_4941 = POST / "source-intake" / "functional_rg" / "4941" / "lower_scalar_essential_quotient.csv"
NUMBER_CHANGE_4954 = POST / "4954-Y5-R2FR-finite-time-off-shell-X2-number-changing-2PI-kernel-and-formation-source-efficiency-or-nonequilibrium-route-rejection.md"
RESULT_4954 = POST / "source-intake" / "functional_rg" / "4954" / "offshell_X2_X3_number_change_results.json"
SPARC_4954 = POST / "source-intake" / "functional_rg" / "4954" / "SPARC_finite_time_and_controlled_24_gate.csv"

MARKER = "MTS_4955_X3_PARENT_FLOW_AND_HIERARCHY"
CHECKED_DATE = "2026-07-13"
PLANCK_MASS_EV = Decimal("1.2208901285838957e28")
PI_DECIMAL = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286")

EXPECTED_HASHES = {
    BASIS_TEX: "e234ab07031885f79030529bb3dcabc7e928cc4283774f26ebc5dac6b8a226dc",
    SCALAR_TEX: "09e4775df76bf3e2024be7f2ec655a125436dbb6042779bc71fe03f6f7e5d778",
    O4_4941: "f4c6f83668c5f904706747dcafb3d538068a038307ffc062e13fe3234a6b9543",
    LOWER_4941: "62f83d1e254709fa6dd5141ad9132a3d9aac89894a30684f804bae508646e89f",
    NUMBER_CHANGE_4954: "3f4d4c09ca97d88327246b9c0ef91b63f98931b2ef467b14b3b7ab57c6cbec69",
    RESULT_4954: "523339dd40a835f84c2bbd24a20b7977710f5a71b826dbb3d830089b7445ab45",
    SPARC_4954: "8fc7c934cb35fb9e7a6316d6d0407273ab6cded64a8d4daa95ca43dcb454382b",
}

HIGH_FREQUENCY_CASES = {
    "white_dwarf_fundamental_pair_quantum",
    "neutron_star_fundamental_pair_quantum",
    "one_GeV_quantum",
    "UHE_1e20_eV_quantum",
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


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def symmetric_tensor_basis(dimension: int = 4) -> list[sp.Matrix]:
    basis: list[sp.Matrix] = []
    for first in range(dimension):
        tensor = sp.zeros(dimension)
        tensor[first, first] = 1
        basis.append(tensor)
    for first in range(dimension):
        for second in range(first + 1, dimension):
            tensor = sp.zeros(dimension)
            tensor[first, second] = 1 / sp.sqrt(2)
            tensor[second, first] = 1 / sp.sqrt(2)
            basis.append(tensor)
    return basis


def angular_average_s3(expression: sp.Expr, cosine: sp.Symbol) -> sp.Expr:
    polynomial = sp.Poly(sp.expand(expression), cosine)
    result = sp.Integer(0)
    for (power,), coefficient in polynomial.terms():
        if power % 2:
            continue
        half_power = power // 2
        moment = sp.rf(sp.Rational(1, 2), half_power) / sp.rf(sp.Integer(2), half_power)
        result += coefficient * moment
    return sp.simplify(result)


def minimal_gravity_projection() -> tuple[dict[str, sp.Expr], list[dict[str, Any]]]:
    cosine, radial = sp.symbols("z q", real=True)
    basis = symmetric_tensor_basis()
    trace_vector = sp.Matrix([sp.trace(tensor) for tensor in basis])
    dewitt = sp.eye(10) - sp.Rational(1, 2) * trace_vector * trace_vector.T

    gradient = sp.Matrix([1, 0, 0, 0])
    momentum_hat = sp.Matrix([cosine, sp.sqrt(1 - cosine**2), 0, 0])
    gradient_tensor = gradient * gradient.T
    gradient_components = sp.Matrix([sp.trace(tensor * gradient_tensor) for tensor in basis])

    mixed = sp.Matrix(
        [
            sp.Rational(1, 2) * gradient.dot(momentum_hat) * sp.trace(tensor)
            - (gradient.T * tensor * momentum_hat)[0]
            for tensor in basis
        ]
    )
    symmetrized_gradient_action = sp.Matrix(
        10,
        10,
        lambda first, second: sp.trace(
            basis[first]
            * (gradient_tensor * basis[second] + basis[second] * gradient_tensor)
        )
        / 2,
    )
    metric_vertex = (
        -sp.Rational(1, 4) * dewitt
        - sp.Rational(1, 4)
        * (trace_vector * gradient_components.T + gradient_components * trace_vector.T)
        + symmetrized_gradient_action
    )

    mixed_matrix = sp.zeros(11)
    metric_matrix = sp.zeros(11)
    mixed_matrix[:10, 10] = radial * dewitt * mixed
    mixed_matrix[10, :10] = radial * mixed.T
    metric_matrix[:10, :10] = dewitt * metric_vertex

    trace_metric = sp.simplify(sp.trace(dewitt * metric_vertex))
    mixed_norm = sp.simplify((mixed.T * dewitt * mixed)[0])
    coefficient_x2 = sp.simplify(
        sp.trace(metric_matrix**2)
        - 3 * sp.trace(mixed_matrix**2 * metric_matrix)
        + sp.trace(mixed_matrix**4)
    )
    coefficient_x3 = sp.simplify(
        -sp.trace(metric_matrix**3)
        + 4 * sp.trace(mixed_matrix**2 * metric_matrix**2)
        + 2 * sp.trace(mixed_matrix * metric_matrix * mixed_matrix * metric_matrix)
        - 5 * sp.trace(mixed_matrix**4 * metric_matrix)
        + sp.trace(mixed_matrix**6)
    )
    angular_x2 = angular_average_s3(coefficient_x2, cosine)
    angular_x3 = angular_average_s3(coefficient_x3, cosine)
    radial_x2 = sp.integrate(radial**3 * angular_x2, (radial, 0, 1))
    radial_x3 = sp.integrate(radial**3 * angular_x3, (radial, 0, 1))
    flow_x2_prefactor = sp.simplify(radial_x2 / (8 * sp.pi**2))
    flow_x3_prefactor = sp.simplify(radial_x3 / (8 * sp.pi**2))
    beta_c_source = sp.simplify(flow_x2_prefactor * (32 * sp.pi) ** 2)
    beta_e_source = sp.simplify(flow_x3_prefactor * (32 * sp.pi) ** 3)

    expected = {
        "trace_metric": sp.Integer(0),
        "mixed_norm": sp.Rational(1, 2),
        "angular_x2": (8 * radial**4 - 9 * radial**2 + 12) / 16,
        "angular_x3": (8 * radial**6 - 15 * radial**4 + 9 * radial**2 - 3) / 32,
        "radial_x2": sp.Rational(5, 32),
        "radial_x3": -sp.Rational(13, 1280),
        "beta_c_source": sp.Integer(20),
        "beta_e_source": -sp.Rational(208, 5) * sp.pi,
    }
    actual = {
        "trace_metric": trace_metric,
        "mixed_norm": mixed_norm,
        "coefficient_x2_before_angular_average": sp.factor(coefficient_x2),
        "coefficient_x3_before_angular_average": sp.factor(coefficient_x3),
        "angular_x2": sp.factor(angular_x2),
        "angular_x3": sp.factor(angular_x3),
        "radial_x2": radial_x2,
        "radial_x3": radial_x3,
        "flow_x2_prefactor": flow_x2_prefactor,
        "flow_x3_prefactor": flow_x3_prefactor,
        "beta_c_source": beta_c_source,
        "beta_e_source": beta_e_source,
    }
    for key, expected_value in expected.items():
        if sp.simplify(actual[key] - expected_value) != 0:
            raise AssertionError(f"minimal-gravity projection mismatch for {key}: {actual[key]}")

    rows: list[dict[str, Any]] = []
    descriptions = {
        "trace_metric": "The one-insertion X term cancels in the DeWitt trace.",
        "mixed_norm": "The kinetic mixed h-phi vertex has exact DeWitt norm one half.",
        "coefficient_x2_before_angular_average": "Order-X2 inverse-Hessian trace before the S3 angular average.",
        "coefficient_x3_before_angular_average": "Order-X3 inverse-Hessian trace before the S3 angular average.",
        "angular_x2": "S3-averaged order-X2 kernel as a function of radial q.",
        "angular_x3": "S3-averaged order-X3 kernel as a function of radial q.",
        "radial_x2": "Litim-ball radial integral of the X2 kernel.",
        "radial_x3": "Litim-ball radial integral of the X3 kernel.",
        "flow_x2_prefactor": "Momentum-measure coefficient multiplying s4 X2.",
        "flow_x3_prefactor": "Momentum-measure coefficient multiplying s6 X3.",
        "beta_c_source": "Additive gravity source for source-convention c at zero matter couplings.",
        "beta_e_source": "Additive gravity source for source-convention e at zero matter couplings.",
    }
    for key, value in actual.items():
        rows.append(
            {
                "quantity": key,
                "exact_expression": sp.sstr(value),
                "numeric_value": f"{float(sp.N(value, 16)):.16g}" if not value.has(radial, cosine) else "",
                "derivation": descriptions[key],
                "projection": "flat_Euclidean_harmonic_gauge_Litim_eta0_lambda0_Gaussian_matter",
                "status": "EXACT_SYMBOLIC_DERIVATION",
                "passed": True,
            }
        )
    return actual, rows


def pure_scalar_hierarchy() -> tuple[dict[str, sp.Expr], list[dict[str, Any]]]:
    x, radial, cosine = sp.symbols("x q z", real=True)
    c, e, f, h5 = sp.symbols("c e f h5", real=True)
    lagrangian = x / 2 + c * x**2 + e * x**3 + f * x**4 + h5 * x**5
    inverse_denominator_shift = radial**2 * (
        2 * sp.diff(lagrangian, x) - 1
        + 4 * x * sp.diff(lagrangian, x, 2) * cosine**2
    )
    inverse_series = sp.series(1 / (1 + inverse_denominator_shift), x, 0, 5).removeO()
    angular_series = angular_average_s3(inverse_series, cosine)
    quantum_flow = sp.expand(
        sp.integrate(radial**3 * angular_series, (radial, 0, 1)) / (8 * sp.pi**2)
    )
    quantum_c = sp.simplify(quantum_flow.coeff(x, 2))
    quantum_e = sp.simplify(quantum_flow.coeff(x, 3))
    quantum_f = sp.simplify(quantum_flow.coeff(x, 4))
    beta_c = sp.simplify(4 * c + quantum_c)
    beta_e = sp.simplify(8 * e + quantum_e)
    beta_f = sp.simplify(12 * f + quantum_f)

    expected_beta_c = 4 * c - e / (4 * sp.pi**2) + 5 * c**2 / (8 * sp.pi**2)
    expected_beta_e = (
        8 * e
        - 5 * f / (12 * sp.pi**2)
        + 21 * c * e / (8 * sp.pi**2)
        - 37 * c**3 / (10 * sp.pi**2)
    )
    expected_beta_f = (
        12 * f
        + 25 * c**4 / sp.pi**2
        - 243 * c**2 * e / (10 * sp.pi**2)
        + 9 * c * f / (2 * sp.pi**2)
        + 45 * e**2 / (16 * sp.pi**2)
        - 5 * h5 / (8 * sp.pi**2)
    )
    if sp.simplify(beta_c - expected_beta_c) != 0:
        raise AssertionError(f"pure-scalar beta_c mismatch: {beta_c}")
    if sp.simplify(beta_e - expected_beta_e) != 0:
        raise AssertionError(f"pure-scalar beta_e mismatch: {beta_e}")
    if sp.simplify(beta_f - expected_beta_f) != 0:
        raise AssertionError(f"pure-scalar beta_f mismatch: {beta_f}")

    values = {
        "inverse_denominator_shift": sp.factor(inverse_denominator_shift),
        "angular_inverse_series_to_X3": sp.factor(angular_series),
        "quantum_flow_to_X3": sp.factor(quantum_flow),
        "quantum_beta_c": quantum_c,
        "quantum_beta_e": quantum_e,
        "quantum_beta_f": quantum_f,
        "beta_c": beta_c,
        "beta_e": beta_e,
        "beta_f": beta_f,
        "general_next_coordinate_feed": "partial beta_a_n / partial a_(n+1)=-(n+1)(n+2)/(48*pi^2)",
        "X2_X3_closed": sp.false,
    }
    rows = [
        {
            "coordinate": "c_X2",
            "beta_function": sp.sstr(beta_c),
            "canonical_term": "4*c",
            "lower_or_same_order_terms": "5*c**2/(8*pi**2)",
            "next_coordinate_feed": "-e/(4*pi**2)",
            "closure_requirement": "X3 must be retained even for beta_c beyond the X2 projection",
            "status": "EXACT_FLAT_PX_PROJECTION",
            "passed": True,
        },
        {
            "coordinate": "e_X3",
            "beta_function": sp.sstr(beta_e),
            "canonical_term": "8*e",
            "lower_or_same_order_terms": "21*c*e/(8*pi**2)-37*c**3/(10*pi**2)",
            "next_coordinate_feed": "-5*f/(12*pi**2)",
            "closure_requirement": "the independent X4 coordinate f is mandatory",
            "status": "EXACT_FLAT_PX_PROJECTION",
            "passed": True,
        },
        {
            "coordinate": "f_X4",
            "beta_function": sp.sstr(beta_f),
            "canonical_term": "12*f",
            "lower_or_same_order_terms": "25*c**4/pi**2-243*c**2*e/(10*pi**2)+9*c*f/(2*pi**2)+45*e**2/(16*pi**2)",
            "next_coordinate_feed": "-5*h5/(8*pi**2)",
            "closure_requirement": "the next X5 coordinate enters beta_f; adding X4 does not terminate the hierarchy",
            "status": "EXACT_FLAT_PX_PROJECTION",
            "passed": True,
        },
        {
            "coordinate": "finite_X2_X3_truncation",
            "beta_function": "not autonomous because partial(beta_e)/partial(f)=-5/(12*pi**2)",
            "canonical_term": "",
            "lower_or_same_order_terms": "",
            "next_coordinate_feed": "nonzero X4 feed",
            "closure_requirement": "derive a controlled P(X) tower or a convergence bound; do not set f=0 as a parent result",
            "status": "NONCLOSURE_PROVED",
            "passed": True,
        },
        {
            "coordinate": "general_PX_tower",
            "beta_function": "partial beta_a_n/partial a_(n+1)=-(n+1)(n+2)/(48*pi**2) for n>=2",
            "canonical_term": "4(n-1)a_n",
            "lower_or_same_order_terms": "polynomial in a_2 through a_n",
            "next_coordinate_feed": "nonzero for every finite n",
            "closure_requirement": "solve P_k(X) functionally or prove a controlled convergence/error bound",
            "status": "FINITE_POLYNOMIAL_NONCLOSURE_THEOREM",
            "passed": True,
        },
    ]
    return values, rows


def operator_rows() -> list[dict[str, Any]]:
    return [
        {
            "operator_id": "O1",
            "operator": "[(nabla phi)^2]^3 = X^3",
            "derivative_order": 6,
            "constant_gradient_flat_projection": "nonzero",
            "role_in_beta_e": "direct projected coordinate e",
            "source_location": "GravityEFTv2_final.tex:699",
            "status": "BASIS_SIGNED_AND_PROJECTED",
            "passed": True,
        },
        {
            "operator_id": "O2",
            "operator": "X (nabla_rho nabla_sigma phi)^2",
            "derivative_order": 6,
            "constant_gradient_flat_projection": "zero on the selected linear background",
            "role_in_beta_e": "independent momentum-dependent scalar coordinate outside the constant-gradient projector",
            "source_location": "GravityEFTv2_final.tex:699",
            "status": "BASIS_SIGNED_FLOW_UNPROJECTED",
            "passed": True,
        },
        {
            "operator_id": "O3",
            "operator": "C_mu nu^rho sigma C^mu nu alpha beta C_alpha beta rho sigma",
            "derivative_order": 6,
            "constant_gradient_flat_projection": "zero on flat background",
            "role_in_beta_e": "independent pure-gravity coordinate; mixed gravity flow can feed away from the Gaussian point",
            "source_location": "GravityEFTv2_final.tex:699",
            "status": "BASIS_SIGNED_FLOW_UNPROJECTED",
            "passed": True,
        },
        {
            "operator_id": "O4",
            "operator": "C^2 X",
            "derivative_order": 6,
            "constant_gradient_flat_projection": "zero on flat background",
            "role_in_beta_e": "independent curvature-motion coordinate already isolated by checkpoint 4941",
            "source_location": "GravityEFTv2_final.tex:700; checkpoint 4941",
            "status": "BASIS_SIGNED_FLAT_ZERO_ONLY",
            "passed": True,
        },
        {
            "operator_id": "O5",
            "operator": "C_mu nu rho sigma nabla^mu phi nabla^rho phi nabla^nu nabla^sigma phi",
            "derivative_order": 6,
            "constant_gradient_flat_projection": "zero on flat linear background",
            "role_in_beta_e": "independent curvature-gradient coordinate outside the flat projector",
            "source_location": "GravityEFTv2_final.tex:700",
            "status": "BASIS_SIGNED_FLOW_UNPROJECTED",
            "passed": True,
        },
        {
            "operator_id": "X4",
            "operator": "[(nabla phi)^2]^4 = X^4",
            "derivative_order": 8,
            "constant_gradient_flat_projection": "nonzero",
            "role_in_beta_e": "feeds beta_e linearly as -5 f/(12 pi^2)",
            "source_location": "GravityEFTv2_final.tex:706-712",
            "status": "BASIS_SIGNED_AND_NONCLOSURE_FEED_DERIVED",
            "passed": True,
        },
    ]


def trajectory_rows(beta_e_source: sp.Expr) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    forced_e_coefficient = sp.simplify(-beta_e_source / 2)
    forced_v_coefficient = sp.simplify(8 * forced_e_coefficient)
    rows = [
        {
            "quantity": "beta_g_GR_Gaussian",
            "equation_or_solution": "beta_g=2g",
            "derivation": "canonical IR scaling on the GR-connected Gaussian branch",
            "status": "DECLARED_LEADING_GR_COMPARATOR",
            "passed": True,
        },
        {
            "quantity": "beta_c_essential_leading",
            "equation_or_solution": "beta_c_ess=4 c_ess+16 g^2",
            "derivation": "checkpoint 4941 essential quotient",
            "status": "SOURCE_LOCKED_LOWER_FLOW",
            "passed": True,
        },
        {
            "quantity": "beta_e_Gaussian_matter",
            "equation_or_solution": "beta_e=8e-(208*pi/5)g^3",
            "derivation": "4955 exact minimal kinetic Hessian projection",
            "status": "EXACT_ADDITIVE_SOURCE_AT_DECLARED_BASEPOINT",
            "passed": True,
        },
        {
            "quantity": "g_solution",
            "equation_or_solution": "g(k)=g0 (k/k0)^2",
            "derivation": "integral of beta_g=2g",
            "status": "EXACT_IN_LEADING_SYSTEM",
            "passed": True,
        },
        {
            "quantity": "c_essential_solution",
            "equation_or_solution": "c_ess(k)=g(k)^2[C_c+16 ln(k/k0)]",
            "derivation": "resonant forced solution of beta_c_ess",
            "status": "EXACT_IN_LEADING_SYSTEM",
            "passed": True,
        },
        {
            "quantity": "e_solution",
            "equation_or_solution": f"e(k)=({sp.sstr(forced_e_coefficient)})g(k)^3+C_e g(k)^4",
            "derivation": "forced plus homogeneous solution of beta_e",
            "status": "EXACT_IN_LEADING_SYSTEM",
            "passed": True,
        },
        {
            "quantity": "recent_convention_map",
            "equation_or_solution": "X_recent=X_source/2; u_X2=4c; v_X3=8e; r3=e/(2c^2)",
            "derivation": "coefficient equality under the two X conventions",
            "status": "EXACT_CONVENTION_MAP",
            "passed": True,
        },
        {
            "quantity": "v_X3_forced",
            "equation_or_solution": f"v_X3,forced=({sp.sstr(forced_v_coefficient)})g^3",
            "derivation": "recent-convention minimal gravity-forced coordinate with C_e=0",
            "status": "LEADING_COMPARATOR_NOT_COMPLETE_PARENT_PREDICTION",
            "passed": True,
        },
        {
            "quantity": "r3_fixed_ratio_gate",
            "equation_or_solution": "r3=e/(2c^2) is scale dependent and behaves as O[1/(g ln(k/k0)^2)] on the forced branch",
            "derivation": "c scales as g^2 ln k while e scales as g^3",
            "status": "FINITE_FIXED_RATIO_NOT_DERIVED",
            "passed": True,
        },
        {
            "quantity": "beta_r3_leading",
            "equation_or_solution": "beta_r3=-(104*pi/5)g^3/c^2-32 r3 g^2/c",
            "derivation": "beta[e/(2c^2)] using beta_c=4c+16g^2 and beta_e=8e-(208*pi/5)g^3",
            "status": "EXACT_IN_LEADING_SYSTEM",
            "passed": True,
        },
        {
            "quantity": "forced_r3_solution_Cc_Ce_zero",
            "equation_or_solution": "r3(k)=13*pi/[320 g(k) ln(k/k0)^2]",
            "derivation": "substitution of c=16g^2 ln(k/k0) and e=(104*pi/5)g^3",
            "status": "SCALE_DEPENDENT_NOT_A_FIXED_RATIO",
            "passed": True,
        },
    ]
    result = {
        "beta_e_additive_source": sp.sstr(beta_e_source),
        "forced_e_coefficient": sp.sstr(forced_e_coefficient),
        "forced_v_recent_coefficient": sp.sstr(forced_v_coefficient),
        "beta_r3_leading": "-(104*pi/5)g^3/c^2-32 r3 g^2/c",
        "forced_r3_Cc_Ce_zero": "13*pi/[320 g ln(k/k0)^2]",
        "finite_fixed_r3": False,
        "complete_parent_trajectory": False,
    }
    return result, rows


def decimal_log10(value: Decimal) -> float:
    if value <= 0:
        return -math.inf
    return float(value.log10())


def sparc_forced_rows(coefficient_v: Decimal, coefficient_c2: Decimal) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_row in read_csv(SPARC_4954):
        energy = Decimal(source_row["injection_energy_eV"])
        density = Decimal(source_row["required_density_eV4"])
        g_value = (energy / PLANCK_MASS_EV) ** 2
        v_value = coefficient_v * g_value**3
        if density == 0:
            background_coordinate = Decimal(0)
        else:
            background_coordinate = abs(v_value) * (density / energy**4) ** 2
        contact_sigma_e2 = coefficient_c2 * v_value**2
        unit_gain = Decimal(source_row["unit_six_point_controlled_log_gain_envelope"])
        forced_contact_gain = unit_gain * v_value**2
        required_gain = Decimal(source_row["required_log_multiplicity_after_Amax"])
        positive_target = source_row["positive_outer_residual_target"] == "True"
        high_frequency = source_row["injection_case"] in HIGH_FREQUENCY_CASES
        can_close = forced_contact_gain >= required_gain
        if not positive_target:
            status = "NO_POSITIVE_OUTER_RESIDUAL_TARGET"
        elif source_row["injection_case"] in {"direct_profile_quantum", "minimum_4952_supported_profile_pair"}:
            status = "NUMBER_MULTIPLICATION_NOT_REQUIRED_DIRECT_SOURCE_AMPLITUDE_OPEN"
        elif high_frequency and not can_close:
            status = "MINIMAL_GR_FORCED_X3_CONTACT_COMPARATOR_FAILS"
        else:
            status = "MINIMAL_GR_FORCED_X3_COMPARATOR_ONLY"
        rows.append(
            {
                "galaxy": source_row["galaxy"],
                "injection_case": source_row["injection_case"],
                "positive_outer_residual_target": positive_target,
                "injection_energy_eV": str(energy),
                "required_density_eV4": str(density),
                "g_E_GN_E2": f"{g_value:.18E}",
                "v_X3_forced_recent": f"{v_value:.18E}",
                "log10_abs_v_X3_forced": decimal_log10(abs(v_value)),
                "background_coordinate_abs_v_rho_over_E4_sq": f"{background_coordinate:.18E}",
                "log10_background_coordinate": decimal_log10(background_coordinate),
                "contact_sigmaE2_C2_v2": f"{contact_sigma_e2:.18E}",
                "log10_contact_sigmaE2": decimal_log10(contact_sigma_e2),
                "unit_six_point_log_gain_envelope_4954": str(unit_gain),
                "minimal_forced_X3_contact_log_gain_comparator": f"{forced_contact_gain:.18E}",
                "required_log_multiplicity_after_Amax": str(required_gain),
                "minimal_forced_X3_can_close_deficit": can_close,
                "background_derivative_expansion_controlled": background_coordinate < 1,
                "status": status,
            }
        )

    positive_high = [
        row
        for row in rows
        if row["positive_outer_residual_target"] and row["injection_case"] in HIGH_FREQUENCY_CASES
    ]
    failed_high = sum(not row["minimal_forced_X3_can_close_deficit"] for row in positive_high)
    max_v = max(Decimal(row["v_X3_forced_recent"]) for row in rows)
    max_background = max(Decimal(row["background_coordinate_abs_v_rho_over_E4_sq"]) for row in rows)
    max_contact = max(Decimal(row["contact_sigmaE2_C2_v2"]) for row in rows)
    max_gain_high = max(Decimal(row["minimal_forced_X3_contact_log_gain_comparator"]) for row in positive_high)
    min_required_high = min(Decimal(row["required_log_multiplicity_after_Amax"]) for row in positive_high)
    summary = {
        "rows": len(rows),
        "positive_high_frequency_rows": len(positive_high),
        "failed_high_frequency_rows": failed_high,
        "max_v_X3_forced": f"{max_v:.18E}",
        "max_background_coordinate": f"{max_background:.18E}",
        "max_contact_sigmaE2": f"{max_contact:.18E}",
        "max_forced_contact_log_gain_high_frequency": f"{max_gain_high:.18E}",
        "min_required_log_gain_high_frequency": f"{min_required_high:.18E}",
        "all_background_rows_controlled": all(row["background_derivative_expansion_controlled"] for row in rows),
    }
    return rows, summary


def decision_rows(sparc_summary: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4955_01_basis",
            "question": "Is the CP-even six-derivative shift-symmetric scalar-gravity basis known?",
            "answer": "yes: O1 through O5 are source complete",
            "status": "SIX_DERIVATIVE_BASIS_SOURCE_SIGNED",
            "next_action": "retain every operator when leaving the flat constant-gradient projector",
        },
        {
            "decision_id": "DEC4955_02_gravity_source",
            "question": "Does minimal gravity generate X3 when e is zero?",
            "answer": "yes: beta_e|0=-(208*pi/5)g^3",
            "status": "X3_ZERO_SURFACE_NOT_INVARIANT",
            "next_action": "carry e as a parent coordinate",
        },
        {
            "decision_id": "DEC4955_03_calibration",
            "question": "Does the same projector reproduce the known X2 source?",
            "answer": "yes: beta_c|0=20g^2 before the essential quotient",
            "status": "X3_PROJECTION_NORMALIZATION_CALIBRATED",
            "next_action": "use the X3 coefficient only within the declared basepoint",
        },
        {
            "decision_id": "DEC4955_04_PX_closure",
            "question": "Is a finite X2-X3 P(X) truncation autonomous?",
            "answer": "no: beta_c depends on e and beta_e depends linearly on f_X4",
            "status": "FINITE_X2_X3_TRUNCATION_NONCLOSURE_PROVED",
            "next_action": "derive a controlled P(X) tower or a quantitative convergence bound",
        },
        {
            "decision_id": "DEC4955_05_full_basis",
            "question": "Does the flat X3 projection complete the parent six-derivative flow?",
            "answer": "no: O2 O3 O4 O5 and gravitational mixed terms remain outside this projector",
            "status": "COMPLETE_SIX_DERIVATIVE_PARENT_FLOW_OPEN",
            "next_action": "construct the coupled derivative-expansion Hessian rather than set omitted coordinates to zero",
        },
        {
            "decision_id": "DEC4955_06_trajectory",
            "question": "Does the leading GR Gaussian system fix a finite r3=d3/c_ess^2?",
            "answer": "no: absolute e is forced but r3 remains scale dependent and the full trajectory is not closed",
            "status": "FINITE_R3_FIXED_RATIO_NOT_DERIVED",
            "next_action": "solve the completed coupled flow before using the 4954 cross section as a prediction",
        },
        {
            "decision_id": "DEC4955_07_SPARC",
            "question": "Can the minimal GR-forced X3 contact comparator close the executed high-frequency galaxy deficits?",
            "answer": f"no: {sparc_summary['failed_high_frequency_rows']}/{sparc_summary['positive_high_frequency_rows']} fail",
            "status": "MINIMAL_GR_FORCED_X3_COMPARATOR_REJECTED",
            "next_action": "do not mistake this leading comparator for the complete parent trajectory",
        },
        {
            "decision_id": "DEC4955_08_2PI",
            "question": "Is an expensive strong unequal-time 2PI solve now parent warranted?",
            "answer": "not yet: the complete derivative trajectory has not produced a controlled broad state",
            "status": "STRONG_2PI_DEFERRED_PENDING_PARENT_TRAJECTORY",
            "next_action": "close or bound the derivative hierarchy first",
        },
        {
            "decision_id": "DEC4955_09_direct_source",
            "question": "Is direct profile-frequency formation emission rejected?",
            "answer": "no: its source amplitude remains underived",
            "status": "DIRECT_PROFILE_FORMATION_AMPLITUDE_OPEN",
            "next_action": "derive the formation stress spectrum only after the parent motion trajectory is controlled",
        },
        {
            "decision_id": "DEC4955_10_local",
            "question": "Does this hierarchy result alter the stationary local limit?",
            "answer": "no",
            "status": "4947_LOCAL_GR_NEWTON_MAXWELL_RETAINED",
            "next_action": "continue to carry compact and radiative residual gates",
        },
        {
            "decision_id": "DEC4955_11_full_MTS",
            "question": "Does checkpoint 4955 establish full MTS unification?",
            "answer": "no",
            "status": "FULL_MTS_PROMOTION_BLOCKED",
            "next_action": "advance to the complete derivative-hierarchy flow",
        },
    ]


def main() -> int:
    SOURCE.mkdir(parents=True, exist_ok=True)
    source_hashes = {str(path): digest(path) for path in EXPECTED_HASHES}
    source_hashes_match = all(source_hashes[str(path)] == expected for path, expected in EXPECTED_HASHES.items())
    if not source_hashes_match:
        mismatches = {
            str(path): {"expected": expected, "actual": source_hashes[str(path)]}
            for path, expected in EXPECTED_HASHES.items()
            if source_hashes[str(path)] != expected
        }
        raise RuntimeError(f"source hash mismatch: {mismatches}")

    basis_text = BASIS_TEX.read_text(encoding="utf-8", errors="replace")
    scalar_text = SCALAR_TEX.read_text(encoding="utf-8", errors="replace")
    lower_text = LOWER_4941.read_text(encoding="utf-8-sig")
    source_clause_checks = {
        "six_derivative_O1_X3": "\\mathcal{O}_1 = \\big[(\\nabla_\\mu \\phi)^2\\big]^3" in basis_text,
        "six_derivative_O2": "\\mathcal{O}_2 = (\\nabla_\\mu \\phi)^2" in basis_text,
        "six_derivative_O3_O4_O5": all(token in basis_text for token in ("\\mathcal{O}_3 =", "\\mathcal{O}_4 =", "\\mathcal{O}_5 =")),
        "eight_derivative_X4": "d\\phi^8" in basis_text,
        "scalar_action_X2_convention": "Z_k^2 \\, C_k \\, X^2" in scalar_text,
        "flat_beta_c_source": "\\frac{5}{8\\pi^2} c^2" in scalar_text,
        "kinetic_hh_vertex": "- \\frac{1}{4}  X" in scalar_text,
        "kinetic_hphi_vertex": "\\frac{1}{2} g_{\\alpha\\beta} \\phi^{; \\lambda} D_\\lambda" in scalar_text,
        "essential_X2_source": "16 g^2" in lower_text,
    }
    if not all(source_clause_checks.values()):
        raise RuntimeError(f"source clause check failed: {source_clause_checks}")

    gravity, gravity_rows = minimal_gravity_projection()
    hierarchy, hierarchy_rows = pure_scalar_hierarchy()
    trajectory, trajectory_table = trajectory_rows(gravity["beta_e_source"])

    result_4954 = json.loads(RESULT_4954.read_text(encoding="utf-8"))
    coefficient_c2 = Decimal(str(result_4954["on_shell_24"]["C2"]))
    coefficient_v = Decimal(832) * PI_DECIMAL / Decimal(5)
    sparc_rows, sparc_summary = sparc_forced_rows(coefficient_v, coefficient_c2)
    decisions = decision_rows(sparc_summary)

    write_csv(GRAVITY_CSV, tagged(gravity_rows))
    write_csv(HIERARCHY_CSV, tagged(hierarchy_rows))
    write_csv(OPERATORS_CSV, tagged(operator_rows()))
    write_csv(TRAJECTORY_CSV, tagged(trajectory_table))
    write_csv(SPARC_CSV, tagged(sparc_rows))
    write_csv(DECISION_CSV, tagged(decisions))

    result = {
        "checkpoint_marker": MARKER,
        "source_hashes": source_hashes,
        "source_hashes_match": source_hashes_match,
        "source_clause_checks": source_clause_checks,
        "conventions": {
            "source_X": "X_source=(nabla phi)^2",
            "recent_X": "X_recent=X_source/2",
            "source_action": "P(X_source)=X_source/2+c X_source^2+e X_source^3+f X_source^4+...",
            "recent_coordinates": "u_X2=4c; v_X3=8e; r3=e/(2c^2)",
            "Newton_coordinate": "g=G_N k^2=(k/M_Pl)^2",
            "regulator_projection": "flat Euclidean harmonic gauge; natural Type I/Litim; eta_N=eta_s=lambda=0",
        },
        "minimal_gravity_projection": {key: sp.sstr(value) for key, value in gravity.items()},
        "pure_scalar_hierarchy": {key: sp.sstr(value) for key, value in hierarchy.items()},
        "leading_GR_trajectory": trajectory,
        "SPARC_execution": sparc_summary,
        "decision": {
            "gravity_generates_X3": True,
            "X3_zero_surface_invariant": False,
            "finite_X2_X3_truncation_closed": False,
            "complete_six_derivative_parent_flow": False,
            "finite_r3_fixed_by_leading_system": False,
            "minimal_forced_X3_high_frequency_failures": sparc_summary["failed_high_frequency_rows"],
            "strong_2PI_parent_warranted": False,
            "direct_profile_formation_amplitude": "OPEN",
            "local_GR_Newton_Maxwell_4947": "RETAINED",
            "full_MTS": False,
        },
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"wrote {RESULT_JSON}")
    print(f"beta_c|0 = {gravity['beta_c_source']} g^2")
    print(f"beta_e|0 = {gravity['beta_e_source']} g^3")
    print(f"SPARC minimal-forced failures = {sparc_summary['failed_high_frequency_rows']}/{sparc_summary['positive_high_frequency_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
