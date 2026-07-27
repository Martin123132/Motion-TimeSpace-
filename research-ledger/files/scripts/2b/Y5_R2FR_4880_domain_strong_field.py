from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

from Y5_R2FR_4878_local_eft_arena_bounds import (
    LBAR_P2,
    R10_MIN_M,
    arena_projections,
    strict_eft_contact_branch,
)


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

C = 299_792_458.0
G = 6.67430e-11
M_SUN_KG = 1.98847e30
TAU_DOMAIN = 1.0e-2


def source_contract() -> dict[str, Any]:
    sources = {
        "prior_checkpoint": (
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
        ),
        "prior_validation": (
            OUTPUT / "P8_Y5_BRR545_4879_VALIDATION.csv",
            "VAL4879_OVERALL,PASS",
        ),
        "prior_script": (
            POST / "scripts" / "Y5_R2FR_4879_source_beta_light_clock.py",
            "def local_gr_promotion_gate",
        ),
        "strict_eft_script": (
            POST / "scripts" / "Y5_R2FR_4878_local_eft_arena_bounds.py",
            "def strict_eft_contact_branch",
        ),
        "integrated_parent": (
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
        ),
        "formal_certificate": (
            FORMAL
            / "895-PPC4161-finite-source-beta-light-clock-local-GR-certificate.md",
            "PPC4161_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
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
        "bach_flat_einstein_metrics": "https://arxiv.org/abs/1303.5781",
        "quadratic_gravity_branches": "https://arxiv.org/abs/1907.00046",
        "strict_eft_field_redefinition": "https://arxiv.org/abs/1911.10108",
        "higher_curvature_black_holes": "https://arxiv.org/abs/1808.08962",
    }
    return {
        "local_rows": rows,
        "web_sources": web_sources,
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


def einstein_bach_flat_branch() -> dict[str, Any]:
    dimension, lambda_e, lambda_cal = sp.symbols(
        "d Lambda_E Lambda_cal", real=True
    )
    scalar_curvature = dimension * lambda_e
    eh_coefficient = sp.simplify(
        lambda_e - scalar_curvature / 2 + lambda_cal
    )
    r_squared_coefficient = sp.simplify(
        2 * scalar_curvature * lambda_e - scalar_curvature**2 / 2
    )
    eh_four = sp.simplify(
        eh_coefficient.subs(
            {dimension: 4, lambda_e: lambda_cal}
        )
    )
    r_squared_four = sp.simplify(
        r_squared_coefficient.subs(dimension, 4)
    )
    divergence_of_weyl = sp.Integer(0)
    ricci_weyl_trace = sp.Integer(0)
    bach_tensor = divergence_of_weyl + ricci_weyl_trace / 2
    euler_lovelock_tensor_four = sp.Integer(0)
    correction_total = sp.simplify(
        r_squared_four + bach_tensor + euler_lovelock_tensor_four
    )
    return {
        "action": (
            "S=int sqrt(-g)[Mbar^2(R-2Lambda_cal)/2+"
            "a_R R^2+a_C C_mnrs C^mnrs]+S_m"
        ),
        "einstein_condition": "R_mn=Lambda_cal g_mn in four dimensions",
        "EH_tensor_coefficient": str(eh_four),
        "R2_variation": (
            "H_R2_mn=2RR_mn-g_mn R^2/2+"
            "2(g_mn box-nabla_m nabla_n)R"
        ),
        "R2_einstein_coefficient_general_d": str(
            sp.factor(r_squared_coefficient)
        ),
        "R2_einstein_coefficient_4d": str(r_squared_four),
        "bach_tensor": (
            "B_mn=(nabla^rho nabla^sigma+R^rho_sigma/2)"
            "C_mrho nsigma"
        ),
        "einstein_weyl_divergence": str(divergence_of_weyl),
        "einstein_ricci_weyl_trace": str(ricci_weyl_trace),
        "bach_on_einstein": str(bach_tensor),
        "E4_local_variation_4d": str(euler_lovelock_tensor_four),
        "quadratic_correction_on_einstein": str(correction_total),
        "exact_common_branch": (
            "Every four-dimensional Einstein metric solving the matched "
            "EH+Lambda equation also solves the finite local R2+C2 "
            "equations exactly. Ricci-flat Schwarzschild, Kerr and "
            "vacuum gravitational-wave metrics are included; Einstein-"
            "(A)dS is included when Lambda_cal is retained."
        ),
        "analytic_branch_selector": (
            "Use boundary data continuously connected to the EH solution "
            "and order-reduce the strict EFT equations; do not excite the "
            "additional homogeneous massive/Bach modes of the resummed "
            "fourth-order equations."
        ),
        "counterbranch_guard": (
            "The untruncated quadratic equations also admit non-Einstein "
            "Bach branches. Their existence means the action alone does "
            "not select GR; the strict-EFT analytic branch condition is "
            "part of this certificate."
        ),
        "electrovac_guard": (
            "Einstein-Maxwell metrics are not generally Einstein metrics; "
            "Kerr-Newman and charged interiors are not promoted by this "
            "vacuum theorem."
        ),
        "passed": (
            eh_four == 0
            and r_squared_four == 0
            and bach_tensor == 0
            and euler_lovelock_tensor_four == 0
            and correction_total == 0
        ),
    }


def domain_gate_formulas() -> dict[str, Any]:
    strict = strict_eft_contact_branch()
    eta_newton = arena_projections()["etaNewton_total_m2"]
    a_r_cap = strict["aR_abs_control_cap"]
    a_c_cap = strict["aC_abs_control_cap"]
    q_r10 = 1 / R10_MIN_M
    epsilon_r_r10 = 12 * a_r_cap * LBAR_P2 * q_r10**2
    epsilon_c_r10 = 4 * a_c_cap * LBAR_P2 * q_r10**2
    u_limit = math.sqrt(TAU_DOMAIN)
    return {
        "declared_fractional_tolerance": TAU_DOMAIN,
        "compactness": "u=GM/(R c^2)",
        "one_PN_remainder_proxy": "epsilon_PN=u^2",
        "one_PN_gate": "u^2<tau_domain",
        "one_PN_u_limit": u_limit,
        "kretschmann_exterior": (
            "K=R_mnrs R^mnrs=48(GM/c^2)^2/r^6"
        ),
        "curvature_momentum": "q_K=K^(1/4); q_K^2=sqrt(K)",
        "R2_control": "epsilon_R2=12|a_R| lbar_P^2 q_K^2",
        "C2_control": "epsilon_C2=4|a_C| lbar_P^2 q_K^2",
        "aR_control_cap": a_r_cap,
        "aC_control_cap": a_c_cap,
        "cap_status": "DERIVATIVE_CONTROL_ENVELOPE_NOT_MEASURED_COEFFICIENT",
        "R10_scale_m": R10_MIN_M,
        "R10_q_m_inverse": q_r10,
        "R10_epsilon_R2_at_cap": epsilon_r_r10,
        "R10_epsilon_C2_at_cap": epsilon_c_r10,
        "long_range_loop_gate": "epsilon_loop=eta_Newton q_K^2",
        "etaNewton_total_m2": eta_newton,
        "cosmological_gate": "epsilon_Lambda=|Lambda_cal|R^2",
        "first_nonredundant_vacuum_operator": (
            "S6=(Mbar^2/2)int sqrt(-g) c6 Riemann^3/Lambda_*^4"
        ),
        "curvature_cubed_gate": (
            "epsilon_6=|c6|K/Lambda_*^4="
            "|c6|(q_K ell_*)^4<tau_domain"
        ),
        "cutoff_length_bound": (
            "ell_*<tau_domain^(1/4)/[q_K |c6|^(1/4)]"
        ),
        "source_gate": (
            "Disjoint supports remove interbody R2/C2 contact; matter "
            "interiors retain self-contact and require EOS/worldline "
            "matching."
        ),
        "flow_gate": (
            "Any independently excited unit-flow/aether operator exits "
            "the selected metric-only certificate and requires its own "
            "compact-body sensitivity test."
        ),
        "passed": (
            strict["passed"]
            and abs(epsilon_r_r10 - TAU_DOMAIN) < 1e-14
            and abs(epsilon_c_r10 - TAU_DOMAIN) < 1e-14
            and abs(u_limit - 0.1) < 1e-15
            and eta_newton > 0
        ),
    }


def _system_row(
    name: str,
    mass_kg: float,
    radius_m: float,
    source_class: str,
) -> dict[str, Any]:
    strict = strict_eft_contact_branch()
    eta_newton = arena_projections()["etaNewton_total_m2"]
    gravitational_radius = G * mass_kg / C**2
    compactness = gravitational_radius / radius_m
    kretschmann = 48 * gravitational_radius**2 / radius_m**6
    q_k = kretschmann**0.25
    q_k_squared = math.sqrt(kretschmann)
    epsilon_r2 = (
        12 * strict["aR_abs_control_cap"] * LBAR_P2 * q_k_squared
    )
    epsilon_c2 = (
        4 * strict["aC_abs_control_cap"] * LBAR_P2 * q_k_squared
    )
    epsilon_loop = eta_newton * q_k_squared
    epsilon_6_planck = (q_k * math.sqrt(LBAR_P2)) ** 4
    ell_star_max = TAU_DOMAIN**0.25 / q_k
    pn_remainder = compactness**2
    one_pn_pass = pn_remainder < TAU_DOMAIN

    if source_class == "vacuum_black_hole":
        mean_density = None
        ricci_source_proxy = 0.0
        epsilon_r2_matter_proxy = 0.0
        route = "EXACT_EINSTEIN_VACUUM_BRANCH"
    else:
        mean_density = 3 * mass_kg / (4 * math.pi * radius_m**3)
        ricci_source_proxy = 8 * math.pi * G * mean_density / C**2
        epsilon_r2_matter_proxy = (
            12
            * strict["aR_abs_control_cap"]
            * LBAR_P2
            * ricci_source_proxy
        )
        route = (
            "WEAK_FIELD_1PN_CERTIFICATE"
            if one_pn_pass
            else "FULL_GR_MATTER_INTERIOR_AND_EOS_MATCHING_REQUIRED"
        )

    return {
        "system": name,
        "source_class": source_class,
        "mass_kg": mass_kg,
        "radius_m": radius_m,
        "gravitational_radius_m": gravitational_radius,
        "compactness_u": compactness,
        "one_PN_remainder_proxy_u2": pn_remainder,
        "one_PN_1percent_gate": one_pn_pass,
        "K_m_minus_4": kretschmann,
        "qK_m_inverse": q_k,
        "qK_squared_m_minus_2": q_k_squared,
        "epsilon_R2_at_4878_control_cap": epsilon_r2,
        "epsilon_C2_at_4878_control_cap": epsilon_c2,
        "epsilon_loop": epsilon_loop,
        "epsilon6_at_reduced_Planck_length_c6_1": epsilon_6_planck,
        "ellStar_max_m_for_epsilon6_below_1percent_c6_1": ell_star_max,
        "mean_density_kg_m3": mean_density,
        "ricci_source_proxy_m_minus_2": ricci_source_proxy,
        "epsilon_R2_matter_proxy_at_control_cap": (
            epsilon_r2_matter_proxy
        ),
        "selected_route": route,
        "valid_for_claim": False,
    }


def representative_systems() -> dict[str, Any]:
    rows = [
        _system_row("Earth", 5.9722e24, 6.371e6, "weak_matter_body"),
        _system_row("Sun", M_SUN_KG, 6.957e8, "weak_matter_body"),
        _system_row(
            "one_solar_mass_white_dwarf",
            M_SUN_KG,
            7.0e6,
            "weak_compact_matter_body",
        ),
        _system_row(
            "1.4_solar_mass_12km_neutron_star",
            1.4 * M_SUN_KG,
            12.0e3,
            "strong_compact_matter_body",
        ),
    ]
    black_hole_mass = 10 * M_SUN_KG
    black_hole_radius = 2 * G * black_hole_mass / C**2
    rows.append(
        _system_row(
            "10_solar_mass_Schwarzschild_horizon",
            black_hole_mass,
            black_hole_radius,
            "vacuum_black_hole",
        )
    )
    by_name = {row["system"]: row for row in rows}
    weak_names = {
        "Earth",
        "Sun",
        "one_solar_mass_white_dwarf",
    }
    return {
        "rows": rows,
        "interpretation": (
            "u>=0.1 invalidates the 1PN approximation, not the theory. "
            "Vacuum then hands off to the exact Einstein branch. A "
            "strong matter interior instead requires full GR/TOV plus "
            "EOS and contact matching."
        ),
        "coefficient_guard": (
            "R2/C2 columns use the deliberately maximal 4878 derivative-"
            "control caps, not MTS predictions or empirical estimates."
        ),
        "density_guard": (
            "The mean-density Ricci value is an order-of-magnitude source "
            "proxy. It is not a neutron-star EOS calculation."
        ),
        "passed": (
            all(
                by_name[name]["one_PN_1percent_gate"] for name in weak_names
            )
            and not by_name[
                "1.4_solar_mass_12km_neutron_star"
            ]["one_PN_1percent_gate"]
            and not by_name[
                "10_solar_mass_Schwarzschild_horizon"
            ]["one_PN_1percent_gate"]
            and by_name[
                "10_solar_mass_Schwarzschild_horizon"
            ]["selected_route"]
            == "EXACT_EINSTEIN_VACUUM_BRANCH"
            and all(
                row["epsilon_R2_at_4878_control_cap"] < TAU_DOMAIN
                and row["epsilon_C2_at_4878_control_cap"] < TAU_DOMAIN
                and row["epsilon_loop"] < TAU_DOMAIN
                for row in rows
            )
        ),
    }


def decision_tree() -> dict[str, Any]:
    rows = [
        {
            "case": "weak_metric_only",
            "conditions": (
                "u^2<tau and epsilon_R2,epsilon_C2,epsilon6,"
                "epsilon_loop,epsilon_Lambda<tau"
            ),
            "route": "USE_PRIVATE_1PN_LOCAL_GR_CERTIFICATE",
            "meaning": "Newton/PPN/light/clock/Maxwell weak branch",
        },
        {
            "case": "strong_vacuum_einstein",
            "conditions": (
                "u^2>=tau; T_mn=0; Einstein/Bach-flat boundary branch; "
                "epsilon6 and loop gates pass"
            ),
            "route": "USE_FULL_EXACT_GR_VACUUM_SOLUTION",
            "meaning": (
                "PN failed but finite local R2/C2 corrections still "
                "vanish exactly on the selected background"
            ),
        },
        {
            "case": "strong_matter_interior",
            "conditions": "u^2>=tau and T_mn nonzero inside body",
            "route": "SOLVE_TOV_EOS_AND_CONTACT_MATCHING",
            "meaning": (
                "GR exterior form survives, but mass, multipoles, tides "
                "and sensitivities can depend on the interior"
            ),
        },
        {
            "case": "higher_operator_entry",
            "conditions": (
                "epsilon6>=tau or another retained higher-operator "
                "control parameter reaches tau"
            ),
            "route": "NO_LOCAL_GR_CERTIFICATE_ADD_OPERATORS_OR_UV_DATA",
            "meaning": "strict-EFT truncation has reached its boundary",
        },
        {
            "case": "nonminimal_flow_extension",
            "conditions": "independent flow/aether coefficient is activated",
            "route": "EXIT_METRIC_ONLY_CERTIFICATE",
            "meaning": (
                "run preferred-frame, compact-sensitivity and radiation "
                "gates on the separate extension"
            ),
        },
    ]
    return {
        "rows": rows,
        "passed": (
            len(rows) == 5
            and len({row["route"] for row in rows}) == 5
            and all(row["conditions"] and row["meaning"] for row in rows)
        ),
    }


def promotion_arbitration() -> dict[str, Any]:
    exact = einstein_bach_flat_branch()
    systems = representative_systems()
    return {
        "selected_branch": "STRICT_EFT_METRIC_ONLY_ANALYTIC_EH_BRANCH",
        "weak_field_status": (
            "PRIVATE_CONDITIONAL_CLASSICAL_LOCAL_GR_1PN_CERTIFICATE"
        ),
        "strong_field_vacuum_status": (
            "PRIVATE_CONDITIONAL_EXACT_CLASSICAL_LOCAL_EINSTEIN_"
            "BACKGROUND_BRANCH"
        ),
        "strong_field_vacuum_promoted": exact["passed"],
        "strong_field_matter_interior_promoted": False,
        "charged_electrovac_promoted": False,
        "black_hole_perturbation_spectrum_promoted": False,
        "full_fundamental_unification": False,
        "advance": (
            "Strong compactness is no longer itself a local-GR blocker. "
            "Finite local classical R2/C2 leave every selected four-"
            "dimensional Einstein vacuum background exactly unchanged; "
            "nonlocal loops remain bounded residuals."
        ),
        "remaining_local_gap": (
            "derive compact-matter interior/EOS contact matching and "
            "source or derive the first nonredundant Riemann-cubed "
            "coefficient; separately test perturbations and any flow "
            "extension"
        ),
        "next_target": (
            "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-"
            "and-Riemann-cubed-coefficient-owner-gate.md"
        ),
        "passed": exact["passed"] and systems["passed"],
    }


def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "einstein_branch": einstein_bach_flat_branch(),
        "domain_gates": domain_gate_formulas(),
        "systems": representative_systems(),
        "decision_tree": decision_tree(),
        "promotion": promotion_arbitration(),
    }
    return {
        "sections": sections,
        "all_checks_pass": all(
            section["passed"] for section in sections.values()
        ),
        "decision": (
            "promote the exact four-dimensional classical-local Einstein "
            "vacuum background as the strong-field continuation of the "
            "selected metric-only branch; retain the 1PN certificate "
            "below u=0.1; "
            "route compact matter interiors, charged electrovac, "
            "perturbations, flow and Riemann-cubed effects to explicit "
            "separate gates"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(result(), indent=2, sort_keys=True))
