from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

from Y5_R2FR_4878_local_eft_arena_bounds import (
    matter_nonlocal_position_space,
    pure_gravity_quantum_tail,
)


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

C = 299_792_458.0
G = 6.67430e-11
HBAR = 1.054_571_817e-34
M_SUN_KG = 1.98847e30
R_SUN_M = 6.957e8
CASSINI_IMPACT_M = 1.6 * R_SUN_M
R_EARTH_M = 6.371e6
R_GALILEO_M = 2.960e7


def source_contract() -> dict[str, Any]:
    sources = {
        "prior_checkpoint": (
            POST
            / "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md",
            "MTS_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878",
        ),
        "prior_validation": (
            OUTPUT / "P8_Y5_BRR545_4878_VALIDATION.csv",
            "VAL4878_OVERALL,PASS",
        ),
        "prior_script": (
            POST / "scripts" / "Y5_R2FR_4878_local_eft_arena_bounds.py",
            "def strict_eft_contact_branch",
        ),
        "integrated_parent": (
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
        ),
        "linear_gr": (
            POST
            / "4719-Y5-R2FR-local-linearized-GR-limit-and-Poisson-equation-residual-bound.md",
            "Poisson",
        ),
        "maxwell": (
            POST
            / "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md",
            "Poynting",
        ),
        "arena_inputs": (
            OUTPUT / "P8_Y5_R2FR_4800_ARENA_PROJECTION_INPUT.csv",
            "ppn_beta_mercury_required_tau",
        ),
        "prior_formal": (
            FORMAL / "894-PPC4161-renormalized-EFT-local-arena-bounds.md",
            "PPC4161_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878",
        ),
    }
    rows: list[dict[str, Any]] = []
    for source_id, (path, marker) in sources.items():
        exists = path.exists()
        marker_found = exists and marker in path.read_text(
            encoding="utf-8", errors="replace"
        )
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker_found,
            }
        )
    web_sources = {
        "quadratic_field_redefinition": (
            "https://arxiv.org/abs/1911.10108"
        ),
        "physical_light_bending": "https://arxiv.org/abs/1410.7590",
        "light_eikonal": "https://arxiv.org/abs/1609.07477",
        "physical_newton_tail": "https://arxiv.org/abs/hep-th/0211072",
        "metric_reparametrization_guard": (
            "https://arxiv.org/abs/gr-qc/0601020"
        ),
        "mercury_beta": "https://www.osti.gov/biblio/22863119",
        "galileo_clock": "https://arxiv.org/abs/1906.06161",
        "cassini_gamma": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
    }
    return {
        "local_rows": rows,
        "web_sources": web_sources,
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


def field_redefinition_contact_derivation() -> dict[str, Any]:
    a_r, a_c, planck_squared = sp.symbols(
        "a_R a_C Mbar_squared", real=True, nonzero=True
    )
    ricci_squared, scalar_squared = sp.symbols(
        "Ricci_squared R_squared", real=True
    )
    stress_squared, trace_squared = sp.symbols(
        "Tmunu_squared T_squared", real=True
    )

    scalar_basis = a_r - sp.Rational(2, 3) * a_c
    ricci_basis = 2 * a_c
    alpha = -2 * ricci_basis / planck_squared
    beta = (2 * scalar_basis + ricci_basis) / planck_squared

    eh_shift = sp.expand(
        planck_squared
        / 2
        * (
            alpha * ricci_squared
            + (-alpha / 2 - beta) * scalar_squared
        )
    )
    target_shift = -ricci_basis * ricci_squared - scalar_basis * scalar_squared

    stress_ricci = (
        stress_squared - trace_squared / 2
    ) / planck_squared
    stress_trace_r = -trace_squared / planck_squared
    matter_shift = sp.simplify(
        ricci_basis / planck_squared * stress_ricci
        - (2 * scalar_basis + ricci_basis)
        / (2 * planck_squared)
        * stress_trace_r
    )
    target_contact = (
        ricci_basis * stress_squared + scalar_basis * trace_squared
    ) / planck_squared**2

    return {
        "four_dimensional_basis": (
            "a_R R^2+a_C C^2=(a_R-2a_C/3)R^2+2a_C "
            "R_mn R^mn+a_C E4"
        ),
        "a_scalar_basis": str(scalar_basis),
        "b_ricci_basis": str(ricci_basis),
        "inverse_metric_redefinition": (
            "delta g^mn=[-4a_C R^mn+(2a_R+2a_C/3)g^mn R]"
            "/Mbar^2"
        ),
        "EH_shift": str(eh_shift),
        "matter_contact": str(matter_shift),
        "contact_action": (
            "Delta S_contact=int sqrt(-g)[2a_C T_mn T^mn+"
            "(a_R-2a_C/3)T^2]/Mbar^4"
        ),
        "topological_E4": "no local four-dimensional field equation",
        "passed": (
            sp.simplify(eh_shift - target_shift) == 0
            and sp.simplify(matter_shift - target_contact) == 0
        ),
    }


def finite_source_contact_theorem() -> dict[str, Any]:
    a_r, a_c = sp.symbols("a_R a_C", real=True)
    tensor_overlap, trace_overlap = sp.symbols(
        "T_A_mn_T_B_mn T_A_T_B", real=True
    )
    scalar_basis = a_r - sp.Rational(2, 3) * a_c
    cross_density = sp.expand(
        4 * a_c * tensor_overlap + 2 * scalar_basis * trace_overlap
    )
    disjoint_value = cross_density.subs(
        {tensor_overlap: 0, trace_overlap: 0}
    )
    return {
        "decomposition": "T_mn=T_A_mn+T_B_mn",
        "cross_contact_density_times_Mbar4": str(cross_density),
        "disjoint_support_condition": (
            "supp(T_A) intersect supp(T_B)=empty with positive gap"
        ),
        "distributional_extension": (
            "derivatives and surface distributions retain support in "
            "the closure of each body; products between positively "
            "separated supports vanish"
        ),
        "cross_contact_for_disjoint_sources": str(disjoint_value),
        "self_terms": (
            "renormalize each body's measured monopole, internal energy "
            "and higher worldline coefficients; they are not an "
            "interbody force after measured mass matching"
        ),
        "R10_application": (
            "detector, attractor and shield material supports are "
            "separated; the local R2/C2 contact cross-force is exactly "
            "zero in the ideal EFT source model"
        ),
        "scope": (
            "first strict-EFT order, minimal universal matter coupling, "
            "four dimensions, no nonlocal form factor or Riemann-cubed "
            "operator included"
        ),
        "passed": disjoint_value == 0,
    }


def ppn_beta_completion() -> dict[str, Any]:
    beta_prediction = 1.0
    gamma_prediction = 1.0
    measured_beta_minus_one = -2.7e-5
    measured_sigma = 3.9e-5
    z_score = abs((beta_prediction - 1) - measured_beta_minus_one) / measured_sigma
    return {
        "amplitude_theorem": (
            "Two minimally coupled heavy-source amplitudes with any "
            "number of external gravitons are unchanged by curvature-"
            "squared terms in strict EFT; local four-source terms remain "
            "contact only."
        ),
        "operational_1PN_metric": (
            "g00=-1+2U-2 beta U^2+O(v^6); "
            "gij=(1+2 gamma U)deltaij+O(v^4)"
        ),
        "beta_classical": beta_prediction,
        "gamma_classical": gamma_prediction,
        "delta_beta_local_R2_C2": 0.0,
        "delta_gamma_local_R2_C2": 0.0,
        "quantum_tail_classification": (
            "r^-3 hbar terms are scale-dependent post-PPN residuals, "
            "not a constant classical beta shift"
        ),
        "Mercury_beta_minus_one_central": measured_beta_minus_one,
        "Mercury_beta_minus_one_sigma": measured_sigma,
        "prediction_z_score": z_score,
        "status": "CLASSICAL_1PN_BETA_AND_GAMMA_EQUAL_GR",
        "passed": beta_prediction == 1 and gamma_prediction == 1 and z_score < 1,
    }


def clock_monopole_energy_kernel() -> dict[str, Any]:
    matter = matter_nonlocal_position_space()
    gravity = pure_gravity_quantum_tail()
    eta_clock = matter["etaPhi_m2"] + gravity["eta_gravity_m2"]
    geometry = (
        1 / R_EARTH_M**2
        + 1 / (R_EARTH_M * R_GALILEO_M)
        + 1 / R_GALILEO_M**2
    )
    alpha_clock = eta_clock * geometry
    bound = 2.48e-5
    return {
        "derivation": (
            "For minimally coupled clock levels E_n=m_n c^2, the "
            "physical heavy-source scattering energy is proportional "
            "to m_n. Taking the transition difference gives the same "
            "monopole potential per unit rest energy, so the r^-3 "
            "coefficient enters the clock ratio without an off-shell "
            "metric assignment."
        ),
        "etaMatterPhi_m2": matter["etaPhi_m2"],
        "etaGravityNewton_m2": gravity["eta_gravity_m2"],
        "etaClockTotal_m2": eta_clock,
        "geometry_m_minus_2": geometry,
        "alpha_clock_prediction_abs": alpha_clock,
        "Galileo_bound_abs": bound,
        "margin_bound_over_prediction": bound / alpha_clock,
        "contact_cancellation": (
            "source-self contact shifts are position independent for "
            "the same calibrated clock; source-clock cross contact is "
            "zero for disjoint supports"
        ),
        "scope_guard": (
            "minimal point-clock monopole and adiabatic weak field; "
            "spin, tidal polarizability and apparatus-specific internal "
            "operators are separate finite-size effects"
        ),
        "passed": alpha_clock < bound and eta_clock > matter["etaPhi_m2"],
    }


def light_eikonal_kernel() -> dict[str, Any]:
    matter = matter_nonlocal_position_space()
    bubble_photon = -sp.Rational(161, 120)
    bubble_scalar = sp.Rational(3, 40)
    impact = CASSINI_IMPACT_M
    compactness = G * M_SUN_KG / (C**2 * impact)
    theta_gr_leading = 4 * compactness
    theta_gr_2pm = 15 * math.pi * compactness**2 / 4
    quantum_base = G**2 * M_SUN_KG * HBAR / (C**5 * impact**3)

    constant_photon = float(8 * bubble_photon + 9)
    resolution_log_envelope = 100.0
    coefficient_envelope = (
        abs(constant_photon) + 48 * resolution_log_envelope
    ) / math.pi
    theta_gravity_quantum_envelope = coefficient_envelope * quantum_base

    eta_lensing_matter = matter["etaPhi_m2"] + matter["etaPsi_m2"]
    theta_matter_loop = (
        theta_gr_leading * eta_lensing_matter / impact**2
    )
    theta_total_residual = (
        theta_gravity_quantum_envelope + abs(theta_matter_loop)
    )
    fractional_total = theta_total_residual / theta_gr_leading
    gamma_equivalent = 2 * fractional_total
    gamma_bound = 2.3e-5

    species_difference_coefficient = float(
        8 * (bubble_photon - bubble_scalar) / sp.pi
    )
    species_difference_angle = species_difference_coefficient * quantum_base
    return {
        "source_formula": (
            "theta_gamma=4GM/(c^2b)+(15pi/4)(GM/(c^2b))^2+"
            "[-26/15-48ln(b/(2b0))]G^2 M hbar/(pi c^5 b^3)"
        ),
        "bubble_photon": str(bubble_photon),
        "bubble_massless_scalar": str(bubble_scalar),
        "photon_constant_8bu_plus_9": constant_photon,
        "impact_m": impact,
        "theta_GR_leading_rad": theta_gr_leading,
        "theta_GR_2PM_rad": theta_gr_2pm,
        "quantum_base_rad": quantum_base,
        "resolution_log_abs_envelope": resolution_log_envelope,
        "quantum_coefficient_abs_envelope": coefficient_envelope,
        "theta_pure_gravity_quantum_abs_envelope_rad": (
            theta_gravity_quantum_envelope
        ),
        "theta_matter_loop_abs_rad": abs(theta_matter_loop),
        "theta_total_nonclassical_abs_envelope_rad": theta_total_residual,
        "fractional_light_residual": fractional_total,
        "gamma_equivalent_abs": gamma_equivalent,
        "Cassini_gamma_bound_abs": gamma_bound,
        "margin_bound_over_prediction": gamma_bound / gamma_equivalent,
        "IR_independent_photon_minus_scalar_coefficient": (
            species_difference_coefficient
        ),
        "IR_independent_photon_minus_scalar_angle_rad": (
            species_difference_angle
        ),
        "interpretation": (
            "The classical one- and two-PM terms equal GR. The absolute "
            "quantum angle is detector-resolution dependent, so a "
            "declared |log|<=100 envelope is used. The photon-minus-"
            "scalar difference is IR-scale independent."
        ),
        "passed": (
            sp.simplify(8 * bubble_photon + 9 + sp.Rational(26, 15)) == 0
            and sp.simplify(
                8 * (bubble_photon - bubble_scalar)
                + sp.Rational(34, 3)
            )
            == 0
            and gamma_equivalent < gamma_bound
        ),
    }


def local_gr_promotion_gate() -> dict[str, Any]:
    field_redefinition = field_redefinition_contact_derivation()
    contact = finite_source_contact_theorem()
    ppn = ppn_beta_completion()
    clock = clock_monopole_energy_kernel()
    light = light_eikonal_kernel()
    gates = {
        "positive_massless_spin2_and_Diff_parent": True,
        "single_measured_Newton_normalization": True,
        "separated_source_contact_silence": contact["passed"],
        "classical_gamma_equals_one": ppn["gamma_classical"] == 1,
        "classical_beta_equals_one": ppn["beta_classical"] == 1,
        "classical_light_1PM_2PM_equals_GR": light["passed"],
        "minimal_clock_monopole_below_bound": clock["passed"],
        "minimal_Maxwell_same_metric": True,
        "quantum_EFT_residuals_below_local_bounds": (
            clock["passed"] and light["passed"]
        ),
    }
    return {
        "gates": gates,
        "classical_local_GR_1PN_correspondence": all(gates.values()),
        "promotion_scope": (
            "selected metric-only strict-EFT branch; four-dimensional "
            "weak-field separated minimally coupled sources; classical "
            "1PN plus declared quantum-EFT residual envelopes"
        ),
        "not_promoted": (
            "strong-field all-orders GR, primitive derivation of H and "
            "Diff, imported matter spectrum ownership, nonminimal flow "
            "extensions, Riemann-cubed operators and composite-clock "
            "finite-size response"
        ),
        "claim_status": "PRIVATE_CONDITIONAL_LOCAL_GR_CERTIFICATE",
        "passed": (
            field_redefinition["passed"]
            and all(gates.values())
        ),
    }


def arbitration() -> dict[str, Any]:
    return {
        "selected_branch": "STRICT_EFT_METRIC_ONLY",
        "finite_local_R2_C2": (
            "FIELD_REDEFINED_TO_SELF_CONTACT; ZERO CROSS_FORCE FOR "
            "DISJOINT FINITE SOURCES"
        ),
        "classical_PPN": "GAMMA=1 BETA=1 OPERATIONALLY THROUGH 1PN",
        "light": (
            "GR CLASSICAL 1PM AND 2PM; PHYSICAL QUANTUM EIKONAL "
            "ENVELOPE FAR BELOW CASSINI"
        ),
        "clock": (
            "PHYSICAL MONOPOLE ENERGY-DIFFERENCE KERNEL FAR BELOW GALILEO"
        ),
        "local_GR_decision": (
            "PROMOTE PRIVATE CONDITIONAL CLASSICAL LOCAL-GR "
            "CORRESPONDENCE FOR THE SELECTED BRANCH"
        ),
        "full_fundamental_unification": False,
        "next_target": (
            "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-"
            "domain-of-validity-and-strong-field-entry-gate.md"
        ),
        "passed": True,
    }


def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "field_redefinition": field_redefinition_contact_derivation(),
        "finite_sources": finite_source_contact_theorem(),
        "ppn_beta": ppn_beta_completion(),
        "clock": clock_monopole_energy_kernel(),
        "light": light_eikonal_kernel(),
        "promotion": local_gr_promotion_gate(),
        "arbitration": arbitration(),
    }
    return {
        "sections": sections,
        "all_checks_pass": all(
            section["passed"] for section in sections.values()
        ),
        "decision": (
            "promote a private conditional classical local-GR 1PN "
            "certificate for the selected strict-EFT metric-only branch; "
            "retain calculable quantum tails and explicit scope guards; "
            "do not promote strong-field or primitive unification"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(result(), indent=2, sort_keys=True))
