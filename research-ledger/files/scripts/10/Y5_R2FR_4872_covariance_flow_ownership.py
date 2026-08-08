from __future__ import annotations

import json
from typing import Any

import sympy as sp


def damping_variation() -> dict[str, Any]:
    time = sp.symbols("t", real=True)
    gamma = sp.symbols("gamma", real=True)
    psi = sp.Function("psi")(time)
    psi_dot = sp.diff(psi, time)
    lagrangian = -gamma * psi * psi_dot
    euler = sp.simplify(
        sp.diff(sp.diff(lagrangian, psi_dot), time)
        - sp.diff(lagrangian, psi)
    )
    boundary_identity = sp.simplify(
        lagrangian + sp.diff(gamma * psi**2 / 2, time)
    )
    return {
        "lagrangian": str(lagrangian),
        "boundary_form": "-(gamma/2) d_t(psi^2)",
        "euler_derivative": str(euler),
        "boundary_identity_residual": str(boundary_identity),
        "bulk_damping_generated": euler != 0,
        "passed": euler == 0 and boundary_identity == 0,
    }


def metric_map_identities() -> dict[str, Any]:
    p, q = sp.symbols("p q", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    unit_flow = sp.Matrix([1, 0, 0, 0])
    unit_covector = eta * unit_flow

    public_inverse = eta + p * unit_flow * unit_flow.T
    public_metric = sp.simplify(public_inverse.inv())
    expected_public_metric = (
        eta - p * unit_covector * unit_covector.T / (1 - p)
    )

    core_metric = eta + q * unit_covector * unit_covector.T
    core_inverse = sp.simplify(core_metric.inv())
    expected_core_inverse = eta - q * unit_flow * unit_flow.T / (1 - q)

    public_inverse_residual = sp.simplify(
        public_metric - expected_public_metric
    )
    core_inverse_residual = sp.simplify(core_inverse - expected_core_inverse)
    determinant_ratio = sp.simplify(public_metric.det() / eta.det())
    core_p = sp.simplify(-q / (1 - q))

    return {
        "public_inverse_residual_zero": public_inverse_residual == sp.zeros(4),
        "public_determinant_ratio": str(determinant_ratio),
        "core_covariant_rank_one_p": str(core_p),
        "core_inverse_residual_zero": core_inverse_residual == sp.zeros(4),
        "core_branch_sign_for_0_le_q_lt_1": "p_core<=0",
        "inverse_covariance_branch": "gHat^munu=eta^munu+C^munu; p=q>=0",
        "lorentzian_gate": "0<=q<1",
        "passed": (
            public_inverse_residual == sp.zeros(4)
            and core_inverse_residual == sp.zeros(4)
            and sp.simplify(determinant_ratio - 1 / (1 - p)) == 0
        ),
    }


def coframe_redundancy_identity() -> dict[str, Any]:
    rapidity = sp.symbols("chi", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    boost = sp.Matrix(
        [
            [sp.cosh(rapidity), sp.sinh(rapidity), 0, 0],
            [sp.sinh(rapidity), sp.cosh(rapidity), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    residual = sp.simplify(boost.T * eta * boost - eta)
    return {
        "lorentz_residual_zero": residual == sp.zeros(4),
        "metric_factorization": "gHat=e^T eta e",
        "redundancy": "e -> Lambda(x)e with Lambda^T eta Lambda=eta",
        "translation_compensator_forced": False,
        "passed": residual == sp.zeros(4),
    }


def rank_one_frobenius_identity() -> dict[str, Any]:
    normalization = sp.symbols("N", real=True)
    gradient = sp.symbols("p0:3", real=True)
    normalization_gradient = sp.symbols("N0:3", real=True)
    hessian_symbols = {
        (0, 0): sp.symbols("p00", real=True),
        (0, 1): sp.symbols("p01", real=True),
        (0, 2): sp.symbols("p02", real=True),
        (1, 1): sp.symbols("p11", real=True),
        (1, 2): sp.symbols("p12", real=True),
        (2, 2): sp.symbols("p22", real=True),
    }

    def hessian(first: int, second: int) -> sp.Expr:
        return hessian_symbols[tuple(sorted((first, second)))]

    def flow(index: int) -> sp.Expr:
        return normalization * gradient[index]

    def derivative(derivative_index: int, flow_index: int) -> sp.Expr:
        return (
            normalization_gradient[derivative_index] * gradient[flow_index]
            + normalization * hessian(derivative_index, flow_index)
        )

    wedge = sp.expand(
        flow(0) * (derivative(1, 2) - derivative(2, 1))
        + flow(1) * (derivative(2, 0) - derivative(0, 2))
        + flow(2) * (derivative(0, 1) - derivative(1, 0))
    )
    wedge = sp.simplify(wedge)
    return {
        "flow": "u_mu=N partial_mu psi",
        "frobenius_component": str(wedge),
        "vorticity_sector": "identically_zero",
        "spin1_mode_owned": False,
        "passed": wedge == 0,
    }


def multimode_vorticity_example() -> dict[str, Any]:
    x, y, epsilon = sp.symbols("x y epsilon", real=True)
    weight_one = 1 + y
    weight_two = 1 + x
    weight_sum = sp.simplify(weight_one + weight_two)

    velocity_x = sp.simplify(-epsilon * weight_one / weight_sum)
    velocity_y = sp.simplify(-epsilon * weight_two / weight_sum)
    curl = sp.factor(sp.diff(velocity_y, x) - sp.diff(velocity_x, y))
    expected = sp.factor(epsilon * (x - y) / weight_sum**2)

    return {
        "realizations": "dphi1=dt+epsilon dx; dphi2=dt+epsilon dy",
        "weights": "w1=1+y; w2=1+x",
        "landau_velocity_x_Oepsilon": str(velocity_x),
        "landau_velocity_y_Oepsilon": str(velocity_y),
        "vorticity_Oepsilon": str(curl),
        "vorticity_nonzero_generically": sp.simplify(curl) != 0,
        "passed": sp.simplify(curl - expected) == 0 and curl != 0,
    }


def public_surface_identities() -> dict[str, Any]:
    p, d, r = sp.symbols("p d r", positive=True)
    capital_d = d + p - d * p
    c1 = capital_d / 2
    c3 = -capital_d / 2
    c2 = 2 * p**2 / (3 * (d + p) * (1 - p))
    c4 = 2 * d * p / (d + p) - capital_d / 2
    c14 = sp.simplify(c1 + c4)
    c123 = sp.simplify(c1 + c2 + c3)
    ctheta = sp.simplify(c1 + c3 + 3 * c2)

    alpha1 = sp.factor(
        -8 * (c3**2 + c1 * c4) / (2 * c1 - c1**2 + c3**2)
    )
    alpha2 = sp.factor(
        alpha1 / 2
        - (c1 + 2 * c3 - c4)
        * (2 * c1 + 3 * c2 + c3 + c4)
        / ((c1 + c2 + c3) * (2 - c1 - c4))
    )
    cosmology_to_newton = sp.factor(
        (1 - c14 / 2) / (1 + ctheta / 2)
    )

    scaled = {
        "c1_over_p": sp.simplify(sp.limit(c1.subs(d, r * p) / p, p, 0)),
        "c2_over_p": sp.simplify(sp.limit(c2.subs(d, r * p) / p, p, 0)),
        "c3_over_p": sp.simplify(sp.limit(c3.subs(d, r * p) / p, p, 0)),
        "c4_over_p": sp.simplify(sp.limit(c4.subs(d, r * p) / p, p, 0)),
        "c14_over_p": sp.simplify(sp.limit(c14.subs(d, r * p) / p, p, 0)),
    }

    alpha1_expected = -8 * d * p / (d + p)
    alpha2_expected = d * (3 * d - p) / (d + p)
    return {
        "c13": str(sp.simplify(c1 + c3)),
        "c14": str(c14),
        "c123": str(c123),
        "alpha1": str(alpha1),
        "alpha2": str(alpha2),
        "Gcos_over_GN": str(cosmology_to_newton),
        "small_p_ratios": {key: str(value) for key, value in scaled.items()},
        "all_coefficients_O_p_for_fixed_r": True,
        "passed": (
            sp.simplify(c1 + c3) == 0
            and sp.simplify(alpha1 - alpha1_expected) == 0
            and sp.simplify(alpha2 - alpha2_expected) == 0
            and sp.simplify(cosmology_to_newton - (1 - p)) == 0
        ),
    }


def ownership_result() -> dict[str, Any]:
    sections = {
        "damping": damping_variation(),
        "metric_maps": metric_map_identities(),
        "coframe": coframe_redundancy_identity(),
        "rank_one": rank_one_frobenius_identity(),
        "multimode": multimode_vorticity_example(),
        "public_surface": public_surface_identities(),
    }
    return {
        "sections": sections,
        "all_symbolic_checks_pass": all(
            section["passed"] for section in sections.values()
        ),
        "primitive_decision": (
            "replace the covariant raw-gradient metric ansatz by the inverse "
            "connected-covariance map and define u as its unique timelike "
            "Landau eigenvector"
        ),
        "correspondence_decision": (
            "operator basis and O(p) decoupling are derived; numerical c_i(p,r) "
            "ratios and universal matter descent remain EFT matching data"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(ownership_result(), indent=2, sort_keys=True))
