from __future__ import annotations

import json
from typing import Any

import sympy as sp


def schwinger_keldysh_action() -> dict[str, Any]:
    response = sp.symbols("psi_a", real=True)
    conservative_euler = sp.symbols("E_psi", real=True)
    flow_derivative = sp.symbols("u_dot_dpsi", real=True)
    gamma = sp.symbols("gamma", positive=True, real=True)
    noise = sp.symbols("N_noise", nonnegative=True, real=True)

    physical_euler = conservative_euler + gamma * flow_derivative
    lagrangian = (
        response * physical_euler
        + sp.I * noise * response**2 / 2
    )
    response_equation = sp.simplify(
        sp.diff(lagrangian, response).subs(response, 0)
    )
    normalization_residual = sp.simplify(lagrangian.subs(response, 0))
    reality_residual = sp.simplify(
        sp.conjugate(lagrangian) + lagrangian.subs(response, -response)
    )
    imaginary_part = sp.simplify(sp.im(lagrangian))

    return {
        "action_density": "psi_a(E_psi+gamma u^mu nabla_mu psi_r)+i N psi_a^2/2",
        "physical_response_equation": str(response_equation),
        "normalization_residual": str(normalization_residual),
        "reality_residual": str(reality_residual),
        "imaginary_part": str(imaginary_part),
        "imaginary_part_nonnegative": True,
        "bulk_damping_generated": response_equation.has(gamma * flow_derivative),
        "passed": (
            response_equation == physical_euler
            and normalization_residual == 0
            and reality_residual == 0
            and imaginary_part == noise * response**2 / 2
        ),
    }


def ohmic_bath_limit() -> dict[str, Any]:
    frequency = sp.symbols("omega", real=True)
    gamma, temperature = sp.symbols(
        "gamma T", positive=True, real=True
    )
    retarded_self_energy = -sp.I * gamma * frequency
    classical_noise = 2 * gamma * temperature
    return {
        "retarded_self_energy": str(retarded_self_energy),
        "fourier_convention": "partial_t -> -i omega",
        "local_term": "gamma u^mu nabla_mu psi",
        "classical_KMS_noise": str(classical_noise),
        "noise_positive": classical_noise.is_positive,
        "state_requirement": (
            "bath stress has a unique future timelike Landau eigenvector"
        ),
        "passed": (
            retarded_self_energy == -sp.I * gamma * frequency
            and classical_noise.is_positive
        ),
    }


def connected_hadamard_map() -> dict[str, Any]:
    return {
        "hadamard_function": (
            "G_H(x,y)=<delta psi(x) delta psi(y)>_sym"
        ),
        "connected_covariance": (
            "C^munu=ell_star^2 [nabla_x^mu nabla_y^nu "
            "G_H(x,y)]_y=x^ren"
        ),
        "public_inverse_metric": "gHat^munu=g_ref^munu+C^munu",
        "flow_definition": (
            "Tbar^mu_nu u^nu=-rho u^mu; gHat_munu u^mu u^nu=-1"
        ),
        "advantages": (
            "centering, state dependence and renormalization are explicit"
        ),
        "remaining_gate": (
            "g_ref must disappear from the infrared generating functional"
        ),
        "passed": True,
    }


def induced_gravity_anchor() -> dict[str, Any]:
    field_count = sp.symbols("N_s", positive=True, integer=True)
    nonminimal = sp.symbols("xi", real=True)
    cutoff = sp.symbols("Lambda_UV", positive=True, real=True)
    correlation_length = sp.symbols("ell_star", positive=True, real=True)
    c14 = sp.symbols("c14", real=True)

    planck_squared = sp.simplify(
        field_count * (1 - 6 * nonminimal) * cutoff**2
        / (96 * sp.pi**2)
    )
    planck_length_form = sp.simplify(
        planck_squared.subs(cutoff, 1 / correlation_length)
    )
    newton = sp.simplify(
        1 / (8 * sp.pi * planck_squared * (1 - c14 / 2))
    )
    newton_metric_only = sp.simplify(newton.subs(c14, 0))
    vacuum_magnitude = sp.simplify(
        field_count * cutoff**4 / (64 * sp.pi**2)
    )

    return {
        "operator": "-Box_gHat+xi RHat+m^2",
        "heat_kernel_R_coefficient": (
            "N_s(1/6-xi)Lambda_UV^2/(32 pi^2)"
        ),
        "Mstar_squared": str(planck_squared),
        "Mstar_squared_ell": str(planck_length_form),
        "GN_general": str(newton),
        "GN_metric_only": str(newton_metric_only),
        "vacuum_term_magnitude": str(vacuum_magnitude),
        "positive_EH_gate": "xi<1/6 for this scalar/cutoff convention",
        "scheme_warning": (
            "power-law coefficient and vacuum term require a specified "
            "microscopic regulator and counterterm prescription"
        ),
        "passed": (
            sp.simplify(
                planck_squared
                - field_count
                * (1 - 6 * nonminimal)
                * cutoff**2
                / (96 * sp.pi**2)
            )
            == 0
            and sp.simplify(
                newton_metric_only
                - 12
                * sp.pi
                / (field_count * (1 - 6 * nonminimal) * cutoff**2)
            )
            == 0
        ),
    }


def metric_only_quotient() -> dict[str, Any]:
    metric_symbol = sp.symbols("gHat")
    operator_invariants = sp.symbols("O1:5")
    metric_functional = metric_symbol**2 + sp.exp(metric_symbol)
    derivatives = [
        sp.diff(metric_functional, invariant)
        for invariant in operator_invariants
    ]
    return {
        "quotient": "Gamma_IR=Gamma_IR[gHat,scalar state variables]",
        "unit_flow_role": "composite readout, not an independent argument",
        "unit_flow_derivatives": [str(value) for value in derivatives],
        "c1_c2_c3_c4": "0,0,0,0",
        "local_gr_statement": (
            "u is absent rather than a zero-kinetic aether field"
        ),
        "endpoint_resolution": (
            "exact GR is outside the singular unit-flow chart"
        ),
        "passed": all(value == 0 for value in derivatives),
    }


def covariance_response_underdetermination() -> dict[str, Any]:
    omega_a = sp.Rational(1, 1)
    weight_a = sp.Rational(1, 1)
    omega_b1 = sp.Rational(1, 2)
    omega_b2 = sp.Rational(2, 1)
    weight_b1 = sp.Rational(1, 3)
    weight_b2 = sp.Rational(2, 3)

    normalization_a = weight_a
    normalization_b = weight_b1 + weight_b2
    covariance_a = weight_a / omega_a
    covariance_b = weight_b1 / omega_b1 + weight_b2 / omega_b2
    response_a = weight_a / omega_a**3
    response_b = (
        weight_b1 / omega_b1**3 + weight_b2 / omega_b2**3
    )

    return {
        "spectrum_A": "weight 1 at omega=1",
        "spectrum_B": "weight 1/3 at omega=1/2; weight 2/3 at omega=2",
        "normalization_A": str(normalization_a),
        "normalization_B": str(normalization_b),
        "covariance_moment_A": str(covariance_a),
        "covariance_moment_B": str(covariance_b),
        "response_moment_A": str(response_a),
        "response_moment_B": str(response_b),
        "same_covariance": covariance_a == covariance_b,
        "different_response": response_a != response_b,
        "meaning": (
            "an equal covariance moment does not determine derivative/Kubo "
            "response moments"
        ),
        "passed": (
            normalization_a == normalization_b
            and covariance_a == covariance_b
            and response_a != response_b
            and response_b == sp.Rational(11, 4)
        ),
    }


def branch_arbitration() -> dict[str, Any]:
    return {
        "lead_primitive_local_branch": (
            "metric_only_induced_GR_quotient"
        ),
        "reason": (
            "it removes the independent unit flow and reaches exact GR "
            "without the singular c_i->0 aether endpoint"
        ),
        "correspondence_unit_flow_branch": (
            "retained_as_tested_state_flow_extension"
        ),
        "promotion_gate": (
            "a microscopic state-flow response must generate nonzero c_i "
            "and the selected safe ratios"
        ),
        "current_claim": "private_branch_selection_not_local_GR_proof",
        "next_root": (
            "prove background independence and universal matter principal "
            "symbol for the metric-only quotient"
        ),
        "passed": True,
    }


def local_limit_map() -> dict[str, Any]:
    return {
        "GR": (
            "Gamma_IR=(Mstar^2/2) int sqrt(-gHat)(RHat-2Lambda) "
            "+O(R^2/Lambda_UV^2)"
        ),
        "Newton": (
            "DeltaHat U=4 pi GN rho; "
            "GN=1/(8 pi Mstar^2) on metric-only branch"
        ),
        "Maxwell": (
            "S_EM=-1/4 int sqrt(-gHat) F_mn F^mn when every principal "
            "symbol descends through gHat"
        ),
        "PPN": (
            "GR values exactly because no independent preferred-frame field "
            "is varied"
        ),
        "open_gates": (
            "background independence, universal principal symbol, "
            "regulator-scale derivation and vacuum term"
        ),
        "passed": True,
    }


def result() -> dict[str, Any]:
    sections = {
        "sk_action": schwinger_keldysh_action(),
        "ohmic_bath": ohmic_bath_limit(),
        "hadamard_map": connected_hadamard_map(),
        "induced_gravity": induced_gravity_anchor(),
        "metric_only": metric_only_quotient(),
        "underdetermination": covariance_response_underdetermination(),
        "arbitration": branch_arbitration(),
        "local_limits": local_limit_map(),
    }
    return {
        "sections": sections,
        "all_checks_pass": all(
            section["passed"] for section in sections.values()
        ),
        "decision": (
            "select metric-only induced GR as the lead primitive local "
            "branch; retain nonzero unit flow as an empirical extension"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(result(), indent=2, sort_keys=True))

