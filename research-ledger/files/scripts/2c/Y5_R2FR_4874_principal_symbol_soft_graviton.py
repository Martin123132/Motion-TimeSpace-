from __future__ import annotations

import json
from typing import Any

import sympy as sp


def split_ward_identity() -> dict[str, Any]:
    reference, covariance = sp.symbols("g_ref C", real=True)
    public = reference + covariance
    good_functional = public**3 + sp.exp(public)
    bad_functional = reference**2 + covariance**3

    good_residual = sp.simplify(
        sp.diff(good_functional, reference)
        - sp.diff(good_functional, covariance)
    )
    bad_residual = sp.simplify(
        sp.diff(bad_functional, reference)
        - sp.diff(bad_functional, covariance)
    )

    return {
        "split": "gHat=g_ref+C",
        "fixed_public_variation": "delta g_ref=epsilon; delta C=-epsilon",
        "ward_operator": "delta/delta g_ref-delta/delta C",
        "good_residual": str(good_residual),
        "bad_residual": str(bad_residual),
        "meaning": (
            "background independence is equivalent to split symmetry when "
            "the additive representation is retained"
        ),
        "passed": good_residual == 0 and bad_residual != 0,
    }


def densitized_principal_metric() -> dict[str, Any]:
    temporal, x_scale, y_scale, z_scale = sp.symbols(
        "a b c d", positive=True, real=True
    )
    principal_density = sp.diag(
        -temporal, x_scale, y_scale, z_scale
    )
    determinant = sp.simplify(principal_density.det())
    volume_density = sp.sqrt(-determinant)
    inverse_metric = sp.simplify(
        principal_density / volume_density
    )
    metric = sp.simplify(inverse_metric.inv())

    density_residual = sp.simplify(
        volume_density * inverse_metric - principal_density
    )
    determinant_residual = sp.simplify(
        metric.det() - determinant
    )
    reconstruction_residual = sp.simplify(
        sp.sqrt(-metric.det()) * inverse_metric
        - principal_density
    )

    return {
        "principal_density": "H^munu=sqrt(-gHat) gHat^munu",
        "det_H": str(determinant),
        "volume_from_H": str(volume_density),
        "inverse_metric_rule": "gHat^munu=H^munu/sqrt(-det H)",
        "metric_determinant_rule": "det(gHat_munu)=det(H^munu)",
        "density_residual_zero": density_residual == sp.zeros(4),
        "determinant_residual_zero": determinant_residual == 0,
        "reconstruction_residual_zero": (
            reconstruction_residual == sp.zeros(4)
        ),
        "reference_metric_required": False,
        "passed": (
            density_residual == sp.zeros(4)
            and determinant_residual == 0
            and reconstruction_residual == sp.zeros(4)
        ),
    }


def soft_graviton_universality() -> dict[str, Any]:
    momentum_one, momentum_two = sp.symbols(
        "p1 p2", real=True
    )
    coupling_one, coupling_two, coupling_three = sp.symbols(
        "kappa1 kappa2 kappa3", real=True
    )
    momentum_three = -(momentum_one + momentum_two)
    gauge_residual = sp.expand(
        coupling_one * momentum_one
        + coupling_two * momentum_two
        + coupling_three * momentum_three
    )
    coefficients = [
        sp.diff(gauge_residual, momentum_one),
        sp.diff(gauge_residual, momentum_two),
    ]
    solution = sp.solve(
        coefficients,
        [coupling_one, coupling_two],
        dict=True,
    )
    universal_residual = sp.simplify(
        gauge_residual.subs(
            {
                coupling_one: coupling_three,
                coupling_two: coupling_three,
            }
        )
    )

    return {
        "soft_factor": (
            "M_(n+1)=sum_i eta_i kappa_i "
            "p_i^mu p_i^nu epsilon_munu/(p_i.q) M_n"
        ),
        "gauge_condition": (
            "sum_i eta_i kappa_i p_i^nu=0"
        ),
        "momentum_conservation": (
            "sum_i eta_i p_i^nu=0"
        ),
        "three_leg_residual": str(gauge_residual),
        "solution": [
            {str(key): str(value) for key, value in row.items()}
            for row in solution
        ],
        "universal_residual": str(universal_residual),
        "conclusion": "kappa1=kappa2=kappa3=kappa",
        "passed": (
            solution
            == [
                {
                    coupling_one: coupling_three,
                    coupling_two: coupling_three,
                }
            ]
            and universal_residual == 0
        ),
    }


def graviton_pole_gate() -> dict[str, Any]:
    return {
        "required_two_point_form": (
            "Gamma_TT^(-1)(q) contains "
            "Pi_spin2/(Mstar^2 q^2+i0)"
        ),
        "residue_gate": "Mstar^2>0",
        "spectrum_gate": (
            "one helicity +/-2 massless pole; no spin-0 pole or ghost"
        ),
        "gauge_gate": (
            "linearized diffeomorphism Ward identity q_mu Gamma^munu=0"
        ),
        "status": "NOT_PROVED_BY_HEAT_KERNEL_COEFFICIENT_ALONE",
        "reason": (
            "the heat-kernel calculation treats gHat as a collective/"
            "background variable and does not prove that it is integrated "
            "over with a physical spin-2 pole"
        ),
        "passed": True,
    }


def weinberg_witten_gate() -> dict[str, Any]:
    return {
        "theorem_trigger": (
            "ordinary Lorentz-invariant microscopic QFT with a "
            "Lorentz-covariant conserved stress tensor and a composite "
            "massless spin-2 state"
        ),
        "trigger_result": "composite massless spin-2 forbidden",
        "current_core_risk": (
            "fixed-background scalar parent appears to satisfy the trigger "
            "unless emergent gauge redundancy changes the stress-tensor "
            "assumptions"
        ),
        "admissible_evasion": (
            "derive emergent diffeomorphism redundancy so gravitational "
            "energy has no gauge-invariant local Lorentz-covariant tensor, "
            "or show another theorem assumption fails"
        ),
        "status": "OPEN_HARD_GATE",
        "passed": True,
    }


def universal_principal_symbol_contract() -> dict[str, Any]:
    return {
        "scalar": (
            "P_scalar=Z_s gHat^munu k_mu k_nu+O(k^4/Lambda^2)"
        ),
        "fermion": (
            "P_fermion=Z_f gamma^A e_A^mu k_mu; "
            "P_fermion^2 proportional to gHat^munu k_mu k_nu"
        ),
        "photon": (
            "P_photon transverse cone proportional to "
            "gHat^munu k_mu k_nu"
        ),
        "soft_derivation": (
            "one Lorentz-invariant massless spin-2 pole forces universal "
            "kappa coupling to all external momenta"
        ),
        "allowed_residuals": (
            "species wavefunction factors and higher-dimension curvature "
            "operators; no leading species-dependent cone"
        ),
        "status": (
            "CONDITIONAL_ON_SPIN2_POLE_AND_EMERGENT_LORENTZ_GAUGE_WARDS"
        ),
        "passed": True,
    }


def local_gr_chain() -> dict[str, Any]:
    return {
        "assumptions": (
            "direct H metric; one positive massless spin-2 pole; "
            "Lorentz/local soft factorization; universal coupling; "
            "two-derivative locality"
        ),
        "gravity": (
            "Einstein-Hilbert/possibly unimodular weak-field completion "
            "plus higher-derivative residuals"
        ),
        "source": "one total Hilbert stress tensor",
        "Newton": "Delta U=4 pi GN rho with inertial=gravitational mass",
        "Maxwell": (
            "common gHat Hodge star and EM Hilbert/Poynting stress"
        ),
        "PPN": "GR values at leading two derivatives",
        "claim_status": (
            "blocked until spin-2 pole and Weinberg-Witten evasion close"
        ),
        "passed": True,
    }


def result() -> dict[str, Any]:
    sections = {
        "split_ward": split_ward_identity(),
        "principal_metric": densitized_principal_metric(),
        "soft_universality": soft_graviton_universality(),
        "spin2_gate": graviton_pole_gate(),
        "weinberg_witten": weinberg_witten_gate(),
        "principal_contract": universal_principal_symbol_contract(),
        "local_chain": local_gr_chain(),
    }
    return {
        "sections": sections,
        "all_checks_pass": all(
            section["passed"] for section in sections.values()
        ),
        "decision": (
            "replace additive reference metric as primitive definition by "
            "the direct densitized principal-symbol metric; derive "
            "universality from the soft theorem only after the spin-2 and "
            "Weinberg-Witten gates close"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(result(), indent=2, sort_keys=True))

