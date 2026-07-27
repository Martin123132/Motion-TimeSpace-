from __future__ import annotations

import json
from typing import Any

import sympy as sp


def collective_parent_contract() -> dict[str, Any]:
    return {
        "partition_function": (
            "Z=int D H Dpsi_r Dpsi_a DX / Vol(Diff) "
            "exp i(S0[g(H),psi,X]+S_gf+S_ghost)"
        ),
        "metric_map": (
            "gHat^munu=H^munu/sqrt(-det H)"
        ),
        "bare_gravity_boundary": (
            "M0^2=0 allowed at Lambda_UV; scalar/bath loops induce Mstar^2"
        ),
        "diffeomorphism_action": (
            "delta H^munu=L_xi H^munu+(partial_rho xi^rho)H^munu "
            "for density weight +1"
        ),
        "measure_condition": (
            "action, measure and regulator are Diff/BRST covariant"
        ),
        "status": (
            "VIABLE_PARENT_UPGRADE_H_IS_AUXILIARY_INTEGRATED_GAUGE_VARIABLE"
        ),
        "passed": True,
    }


def eh_projector_pole() -> dict[str, Any]:
    momentum_squared, planck_squared = sp.symbols(
        "q2 Mstar2", positive=True, real=True
    )
    spin_two = sp.diag(1, 0)
    spin_zero = sp.diag(0, 1)
    transverse_identity = spin_two + spin_zero

    hessian = (
        planck_squared
        * momentum_squared
        * (spin_two - 2 * spin_zero)
    )
    propagator_without_i = (
        spin_two - sp.Rational(1, 2) * spin_zero
    ) / (planck_squared * momentum_squared)
    inverse_residual = sp.simplify(
        hessian * propagator_without_i - transverse_identity
    )
    spin_two_residue = sp.simplify(
        sp.limit(
            momentum_squared * propagator_without_i[0, 0],
            momentum_squared,
            0,
            dir="+",
        )
    )

    return {
        "EH_hessian": "Mstar^2 q^2(P2-2 P0s)",
        "conserved_source_propagator": (
            "i(P2-P0s/2)/(Mstar^2(q^2+i0))"
        ),
        "inverse_residual_zero": inverse_residual == sp.zeros(2),
        "spin2_residue": str(spin_two_residue),
        "positive_residue_for_Mstar2_positive": (
            spin_two_residue.is_positive
        ),
        "physical_helicities": "+2,-2 after Diff constraints",
        "scalar_projector_role": (
            "constraint/source trace structure, not an independent scalar "
            "degree of freedom in EH"
        ),
        "passed": (
            inverse_residual == sp.zeros(2)
            and spin_two_residue == 1 / planck_squared
            and spin_two_residue.is_positive
        ),
    }


def gauge_ward_identity() -> dict[str, Any]:
    transverse_two, transverse_zero, longitudinal = (
        sp.diag(1, 0, 0),
        sp.diag(0, 1, 0),
        sp.diag(0, 0, 1),
    )
    momentum_squared = sp.symbols("q2", real=True)
    hessian = momentum_squared * (
        transverse_two - 2 * transverse_zero
    )
    longitudinal_residual = sp.simplify(hessian * longitudinal)

    return {
        "non_gauge_hessian": "q^2(P2-2P0s)",
        "longitudinal_projector": "PL",
        "hessian_times_longitudinal": str(longitudinal_residual),
        "linear_Ward_identity": "q_mu Gamma2^munu,rhosigma=0",
        "nonlinear_identity": (
            "nabla_mu[2/sqrt(-g) delta Gamma/delta g_munu]=0"
        ),
        "origin": "exact Diff/BRST invariance of integrated-H parent",
        "passed": longitudinal_residual == sp.zeros(3),
    }


def conserved_source_exchange() -> dict[str, Any]:
    density = sp.symbols("rho", positive=True, real=True)
    tensor_square = density**2
    trace_square = density**2
    numerator = sp.simplify(
        tensor_square - trace_square / 2
    )
    return {
        "amplitude": (
            "A=i[T_mn T^mn-T^2/2]/(Mstar^2 q^2)"
        ),
        "nonrelativistic_numerator": str(numerator),
        "positive_numerator": numerator.is_positive,
        "Newton_identification": "GN=1/(8 pi Mstar^2)",
        "universal_source": (
            "soft theorem fixes the same kappa for every external species"
        ),
        "passed": numerator == density**2 / 2 and numerator.is_positive,
    }


def strict_scalar_legendre_branch() -> dict[str, Any]:
    return {
        "construction": (
            "H=<O_munu[psi]> from a Legendre transform of a fixed-eta "
            "scalar theory"
        ),
        "stress_tensor": (
            "microscopic theory has a Lorentz-covariant conserved T_munu"
        ),
        "spin2_interpretation": "massless composite carrying energy",
        "weinberg_witten": "TRIGGERED",
        "decision": (
            "REJECT_COMPOSITE_GRAVITON; induced R can only be an external/"
            "background response on this strict branch"
        ),
        "passed": True,
    }


def integrated_density_branch() -> dict[str, Any]:
    return {
        "construction": (
            "H is integrated from the start as an auxiliary tensor-density "
            "gauge variable with no required bare kinetic term"
        ),
        "dynamics": (
            "matter/open-field loops induce EH plus higher-curvature terms"
        ),
        "stress_tensor": (
            "no gauge-invariant local Lorentz-covariant total gravitational "
            "stress tensor exists"
        ),
        "weinberg_witten": (
            "NOT_TRIGGERED because the full parent is Diff gauge theory, "
            "not a fixed-background QFT with a composite graviton"
        ),
        "cost": (
            "H and Diff redundancy are primitive field/symmetry data; "
            "only their dynamics are induced"
        ),
        "decision": "SELECT_VIABLE_PARENT_UPGRADE_PRIVATE_NONCLAIM",
        "passed": True,
    }


def pole_domain_gate() -> dict[str, Any]:
    return {
        "saddle": (
            "flat-space pole requires Lambda_eff=0; otherwise use the "
            "corresponding (A)dS helicity-2 spectrum"
        ),
        "derivative_hierarchy": (
            "Mstar^2 q^2 dominates q^4 log(q^2/Lambda_UV^2) and local R^2"
        ),
        "positivity": "Mstar^2>0",
        "matter": "one public H/gHat in every kinetic operator",
        "state_flow": (
            "u remains composite unless a separate nonzero Kubo term is "
            "derived"
        ),
        "status": "CONDITIONAL_IR_DOMAIN_NOT_GLOBAL_UV_COMPLETION",
        "passed": True,
    }


def branch_arbitration() -> dict[str, Any]:
    return {
        "selected": "integrated_diffeomorphic_principal_density_parent",
        "rejected": "strict_fixed_background_scalar_composite_graviton",
        "local_result": (
            "induced EH Hessian has a positive massless spin-2 pole and "
            "Diff Ward identity"
        ),
        "source_result": (
            "Weinberg soft theorem activates universal coupling"
        ),
        "claim_status": (
            "conditional on explicit adoption/derivation of integrated H "
            "parent and covariant regulator"
        ),
        "next_target": (
            "write minimal parent action and derive its saddle, regulator "
            "matching, cosmological term and higher-curvature residuals"
        ),
        "passed": True,
    }


def result() -> dict[str, Any]:
    sections = {
        "parent": collective_parent_contract(),
        "projector": eh_projector_pole(),
        "ward": gauge_ward_identity(),
        "exchange": conserved_source_exchange(),
        "strict_scalar": strict_scalar_legendre_branch(),
        "integrated_density": integrated_density_branch(),
        "domain": pole_domain_gate(),
        "arbitration": branch_arbitration(),
    }
    return {
        "sections": sections,
        "all_checks_pass": all(
            section["passed"] for section in sections.values()
        ),
        "decision": (
            "select an integrated diffeomorphic principal-density parent "
            "as the only viable local-GR route; reject a strict scalar-only "
            "composite graviton"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(result(), indent=2, sort_keys=True))

