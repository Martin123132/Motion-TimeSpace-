from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

from Y5_R2FR_4878_local_eft_arena_bounds import (
    LBAR_P2,
    strict_eft_contact_branch,
)
from Y5_R2FR_4880_domain_strong_field import representative_systems


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
A6_SOURCE = POST / "source-intake" / "heat_kernel_a6" / "4881"

C = 299_792_458.0
G = 6.67430e-11
A6_ARCHIVE_SHA256 = (
    "96CE09B011973ECA10A9F3EC5A37150479006A63B9984984F3EA2ED3CC1AC6A2"
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def source_contract() -> dict[str, Any]:
    sources = {
        "prior_checkpoint": (
            POST
            / "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md",
            "MTS_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880",
        ),
        "prior_validation": (
            OUTPUT / "P8_Y5_BRR545_4880_VALIDATION.csv",
            "VAL4880_OVERALL,PASS",
        ),
        "finite_source_contact": (
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
        ),
        "integrated_heat_kernel_parent": (
            POST
            / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876",
        ),
        "spectrum_and_nonlocal_branch": (
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
        ),
        "a6_tex": (
            A6_SOURCE / "ch4.tex",
            "a_{6}(f,D)",
        ),
        "a6_provenance": (
            A6_SOURCE / "PROVENANCE.md",
            "VASSILEVICH_A6_SOURCE_PROVENANCE_4881",
        ),
        "prior_formal": (
            FORMAL
            / "896-PPC4161-exact-Einstein-vacuum-branch-and-strong-field-domain.md",
            "PPC4161_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880",
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
    archive = A6_SOURCE / "hep-th-0306138.tar"
    archive_hash = _sha256(archive) if archive.exists() else ""
    web_sources = {
        "perfect_fluid_action": "https://arxiv.org/abs/gr-qc/9304026",
        "heat_kernel_a6": "https://arxiv.org/abs/hep-th/0306138",
        "curvature_squared_field_redefinition": (
            "https://arxiv.org/abs/1911.10108"
        ),
    }
    return {
        "local_rows": rows,
        "archive_path": str(archive),
        "archive_exists": archive.exists(),
        "archive_sha256": archive_hash,
        "archive_hash_matches": archive_hash == A6_ARCHIVE_SHA256,
        "web_sources": web_sources,
        "passed": (
            all(
                row["source_exists"] and row["marker_found"]
                for row in rows
            )
            and archive.exists()
            and archive_hash == A6_ARCHIVE_SHA256
        ),
    }


def perfect_fluid_contact_image() -> dict[str, Any]:
    energy, pressure, a_r, a_c, sound_squared = sp.symbols(
        "rho p a_R a_C c_s_squared", real=True
    )
    w = sp.symbols("w", real=True)
    scalar_basis = a_r - sp.Rational(2, 3) * a_c
    stress_squared = energy**2 + 3 * pressure**2
    trace = -energy + 3 * pressure
    contact_original = sp.expand(
        2 * a_c * stress_squared + scalar_basis * trace**2
    )
    contact_reduced = sp.expand(
        a_r * (energy - 3 * pressure) ** 2
        + 4 * a_c * energy * (energy / 3 + pressure)
    )
    derivative_energy = sp.diff(contact_reduced, energy)
    derivative_pressure = sp.diff(contact_reduced, pressure)
    pressure_function = sp.expand(
        (energy + pressure)
        * (
            derivative_energy
            + sound_squared * derivative_pressure
        )
        - contact_reduced
    )
    contact_w = sp.factor(
        contact_reduced.subs(pressure, w * energy) / energy**2
    )
    pressure_w = sp.factor(
        pressure_function.subs(pressure, w * energy) / energy**2
    )
    pressure_constant_w = sp.factor(
        pressure_w.subs(sound_squared, w)
    )
    expected_constant_w = sp.factor((1 + 2 * w) * contact_w)
    coefficient_r = sp.factor(sp.diff(pressure_w, a_r))
    coefficient_c = sp.factor(sp.diff(pressure_w, a_c))
    return {
        "signature": "(-,+,+,+)",
        "perfect_fluid_stress": (
            "T_mn=(rho+p)u_m u_n+p g_mn; u_m u^m=-1"
        ),
        "stress_squared": str(stress_squared),
        "trace": str(trace),
        "contact_original": str(contact_original),
        "contact_reduced": str(contact_reduced),
        "contact_boxed": (
            "F=a_R(rho-3p)^2+4a_C rho(rho/3+p)"
        ),
        "barotropic_action": (
            "S_fluid=-int sqrt(-g)rho(n)+"
            "int sqrt(-g)F[rho(n),p(n)]/Mbar^4"
        ),
        "thermodynamics": (
            "p=n d rho/dn-rho; d rho/dn=(rho+p)/n; "
            "c_s^2=dp/d rho"
        ),
        "effective_energy": "rho_eff=rho-F/Mbar^4",
        "effective_pressure": (
            "p_eff=p-D/Mbar^4; "
            "D=(rho+p)(F_rho+c_s^2 F_p)-F"
        ),
        "D_expanded": str(pressure_function),
        "constant_w_F_over_rho2": str(contact_w),
        "constant_w_D_over_rho2": str(pressure_constant_w),
        "constant_w_identity": "D=(1+2w)F when p=w rho",
        "D_aR_coefficient": str(coefficient_r),
        "D_aC_coefficient": str(coefficient_c),
        "radiation_trace_selector": str(
            contact_w.subs(w, sp.Rational(1, 3))
        ),
        "dust_selector": str(contact_w.subs(w, 0)),
        "off_shell_guard": (
            "Use a conserved-current fluid action rho(n), not the "
            "on-shell shorthand L_m=p; this fixes the metric variation "
            "before imposing the perfect-fluid equations."
        ),
        "passed": (
            sp.simplify(contact_original - contact_reduced) == 0
            and sp.simplify(
                pressure_constant_w - expected_constant_w
            )
            == 0
            and sp.simplify(
                contact_w
                - (
                    a_r * (1 - 3 * w) ** 2
                    + 4 * a_c * (w + sp.Rational(1, 3))
                )
            )
            == 0
        ),
    }


def corrected_tov_map() -> dict[str, Any]:
    number, energy, energy_n, contact, contact_n, planck4 = sp.symbols(
        "n rho rho_n F F_n Mbar4", real=True, nonzero=True
    )
    pressure = number * energy_n - energy
    energy_effective = energy - contact / planck4
    pressure_effective = sp.expand(
        number * (energy_n - contact_n / planck4)
        - energy_effective
    )
    expected_pressure = sp.expand(
        pressure - (number * contact_n - contact) / planck4
    )
    return {
        "fluid_variable": (
            "conserved number density n with a parent EOS rho(n)"
        ),
        "effective_EOS": (
            "rho_eff(n)=rho(n)-F(n)/Mbar^4; "
            "p_eff(n)=n d rho_eff/dn-rho_eff"
        ),
        "effective_pressure_expanded": str(pressure_effective),
        "TOV_units": "G=c=1 in the displayed radial equations",
        "mass_equation": "dm/dr=4 pi r^2 rho_eff",
        "pressure_equation": (
            "dp_eff/dr=-(rho_eff+p_eff)"
            "(m+4 pi r^3 p_eff)/[r(r-2m)]"
        ),
        "number_density_equation": (
            "dn/dr=(dp_eff/dn)^(-1) dp_eff/dr"
        ),
        "effective_sound_speed": (
            "c_s,eff^2=[p_n-n F_nn/Mbar^4]/"
            "[rho_n-F_n/Mbar^4]"
        ),
        "center_conditions": "m(0)=0; n(0)=n_c; regular metric",
        "surface_condition": (
            "p_eff(R)=0 with continuous rho(n) or an explicit surface "
            "action for a self-bound density jump"
        ),
        "metric_redefinition": (
            "The interior public metric is recovered with the inverse "
            "checkpoint-4879 local field redefinition. In vacuum "
            "R_mn=R=0, so the redefinition vanishes and the exterior is "
            "the same Schwarzschild metric with matched ADM data."
        ),
        "EOS_redundancy_theorem": (
            "At first strict-EFT order the R2/C2 compact-fluid self-"
            "contact introduces no new gravitational differential "
            "operator; it is a local renormalization of the barotropic "
            "EOS plus the local interior metric map."
        ),
        "observable_guard": (
            "A free phenomenological EOS absorbs this correction. A "
            "gravity test requires independent microphysical EOS input; "
            "mass-radius, tides and sensitivities are not parameter-free "
            "until that matching is supplied."
        ),
        "passed": sp.simplify(
            pressure_effective - expected_pressure
        )
        == 0,
    }


def compact_contact_envelopes() -> dict[str, Any]:
    strict = strict_eft_contact_branch()
    a_r_cap = strict["aR_abs_control_cap"]
    a_c_cap = strict["aC_abs_control_cap"]
    cap_ratio = a_c_cap / a_r_cap
    energy_coefficient_max = 20 * a_r_cap
    pressure_coefficient_max = 60 * a_r_cap
    rows: list[dict[str, Any]] = []
    for system in representative_systems()["rows"]:
        density = system["mean_density_kg_m3"]
        if density is None:
            continue
        source_curvature = 8 * math.pi * G * density / C**2
        x_density = LBAR_P2 * source_curvature
        energy_fraction = energy_coefficient_max * x_density
        pressure_over_energy = pressure_coefficient_max * x_density
        rows.append(
            {
                "system": system["system"],
                "mean_density_kg_m3": density,
                "source_curvature_m_minus_2": source_curvature,
                "x_density": x_density,
                "uniform_mean_density_abs_delta_rho_over_rho_benchmark": (
                    energy_fraction
                ),
                "uniform_mean_density_abs_delta_p_over_rho_benchmark": (
                    pressure_over_energy
                ),
                "uniform_mean_density_direct_deltaM_over_M_benchmark": (
                    energy_fraction
                ),
                "response_status": (
                    "UNIFORM_MEAN_DENSITY_BENCHMARK; PROFILE_MAXIMUM_AND_"
                    "FULL_STABLE_BRANCH_JACOBIAN_NOT_APPLIED"
                ),
            }
        )
    by_name = {row["system"]: row for row in rows}
    neutron = by_name["1.4_solar_mass_12km_neutron_star"]
    return {
        "causal_box": "0<=w=p/rho<=1 and 0<=c_s^2<=1",
        "exact_cap_ratio_aC_over_aR": cap_ratio,
        "energy_coefficient_proof": (
            "With |a_C|_cap=3|a_R|_cap, "
            "|F|/rho^2<=|a_R|[(1-3w)^2+12(w+1/3)]"
            "<=20|a_R| at w=1."
        ),
        "pressure_coefficient_proof": (
            "D_R=(3w-1)(6c_s^2 w+6c_s^2-5w-1), "
            "so |D_R|<=12; D_C<=16. Hence "
            "|D|/rho^2<=12|a_R|+16|a_C|=60|a_R|, "
            "with equality at w=c_s^2=1."
        ),
        "energy_coefficient_max": energy_coefficient_max,
        "pressure_coefficient_max": pressure_coefficient_max,
        "rows": rows,
        "neutron_star_mean_density_energy_fraction_benchmark": neutron[
            "uniform_mean_density_abs_delta_rho_over_rho_benchmark"
        ],
        "neutron_star_mean_density_pressure_over_energy_benchmark": neutron[
            "uniform_mean_density_abs_delta_p_over_rho_benchmark"
        ],
        "profile_mass_bound": (
            "|delta M_direct|/M<=20|a_R|_cap lbar_P^2 "
            "(8pi G/c^2)[int rho_mass^2 dV/int rho_mass dV]"
        ),
        "mass_guard": (
            "A mean density does not upper-bound int rho^2/int rho. The "
            "table is a uniform-density benchmark; a real bound needs a "
            "profile or rho_max. Profile, radius and tidal shifts also "
            "contain the TOV response Jacobian and can be enhanced near "
            "a maximum-mass turning point."
        ),
        "passed": (
            strict["passed"]
            and abs(cap_ratio - 3) < 1e-12
            and len(rows) == 4
            and 3.2e-19
            < neutron[
                "uniform_mean_density_abs_delta_rho_over_rho_benchmark"
            ]
            < 3.3e-19
            and 9.6e-19
            < neutron[
                "uniform_mean_density_abs_delta_p_over_rho_benchmark"
            ]
            < 9.8e-19
        ),
    }


def scalar_heat_kernel_a6_owner() -> dict[str, Any]:
    factorial_seven = math.factorial(7)
    coefficient_gradient = sp.Rational(9, factorial_seven)
    coefficient_box = sp.Rational(12, factorial_seven)
    coefficient_i1 = -sp.Rational(44, 9 * factorial_seven)
    coefficient_i2 = -sp.Rational(80, 9 * factorial_seven)
    coefficient_norm = sp.simplify(
        abs(coefficient_gradient)
        + abs(coefficient_box)
        + abs(coefficient_i1)
        + abs(coefficient_i2)
    )
    expected_norm = sp.Rational(313, 45360)
    h_min = 0.1
    q_over_gap_max = 0.1
    q_over_cutoff_max = 0.1
    delta_eh_max = 0.01
    epsilon_envelope = (
        6
        * float(coefficient_norm)
        / h_min
        * q_over_gap_max**2
        * q_over_cutoff_max**2
        / (1 - delta_eh_max)
    )
    return {
        "operator": "D=-box+xi R+m^2",
        "Ricci_flat_conditions": (
            "R=0; R_mn=0; E=-xi R=0; bundle curvature Omega_mn=0"
        ),
        "A6_Ricci_flat_raw": (
            "A6_RF=1/7![9 (nabla Riem)^2+12 Riem box Riem"
            "-(44/9)I1-(80/9)I2]"
        ),
        "I1": "R_ij kn R_ij lp R_kn lp",
        "I2": "R_ij kn R_il kp R_jl np",
        "coefficient_gradient": str(coefficient_gradient),
        "coefficient_box": str(coefficient_box),
        "coefficient_I1": str(coefficient_i1),
        "coefficient_I2": str(coefficient_i2),
        "absolute_operator_norm": str(coefficient_norm),
        "proper_time_integral_massive": (
            "int_(LambdaUV^-2)^infinity ds exp(-m^2 s)="
            "exp(-m^2/LambdaUV^2)/m^2"
        ),
        "scalar_loop_action_magnitude": (
            "Gamma6=N_s exp(-m^2/LambdaUV^2)/"
            "[32 pi^2 m^2] int sqrt(g) A6_RF"
        ),
        "Newton_matched_normalized_coefficient": (
            "2 zeta6/Mbar^2=6 exp(-m^2/LambdaUV^2)/"
            "[h m^2 LambdaUV^2(1-delta_EH)], h=1-6xi; "
            "delta_EH=2L(m/LambdaUV)^2"
        ),
        "scalar_a6_control": (
            "epsilon6_scalar<=6 C_A6 exp(-m^2/LambdaUV^2)/"
            "[h(1-delta_EH)] "
            "(qK/m)^2(qK/LambdaUV)^2"
        ),
        "h_min": h_min,
        "q_over_gap_max": q_over_gap_max,
        "q_over_cutoff_max": q_over_cutoff_max,
        "delta_EH_max": delta_eh_max,
        "epsilon6_scalar_envelope": epsilon_envelope,
        "massless_limit": (
            "m->0 makes the local proper-time coefficient infrared "
            "divergent; the massless primitive scalar belongs to the "
            "nonlocal form-factor branch, not a finite local c6."
        ),
        "parent_owner_equation": (
            "b6_j,total=b6_j,bare+sum_i sigma_i n_i "
            "A6_j(spin_i,xi_i) exp(-m_i^2/LambdaUV^2)/"
            "[32 pi^2 m_i^2]"
        ),
        "owned_now": (
            "scalar massive-loop A6 tensor and spectral-moment form"
        ),
        "not_owned": (
            "bare dimension-six matching, actual massive MTS spectrum, "
            "fermion/vector/graviton A6 weights and the massless "
            "nonlocal strong-field kernel"
        ),
        "total_c6_parent_derived": False,
        "passed": (
            coefficient_norm == expected_norm
            and 4.18e-5 < epsilon_envelope < 4.19e-5
        ),
    }


def parent_dimension_six_ownership() -> dict[str, Any]:
    parent_path = (
        POST
        / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md"
    )
    parent_text = parent_path.read_text(encoding="utf-8", errors="replace")
    bare_dimension_six_markers = [
        "Riemann^3",
        "Riemann cubed",
        "curvature-cubed",
        "a_6",
        "a_{6}",
    ]
    bare_dimension_six_declared = any(
        marker in parent_text for marker in bare_dimension_six_markers
    )
    rows = [
        {
            "owner_component": "4876_bare_parent",
            "status": "NO_DIMENSION_SIX_BARE_MATCHING_DECLARED",
            "consequence": (
                "the total finite b6_j cannot be predicted by the "
                "counterterm-complete four-derivative parent"
            ),
        },
        {
            "owner_component": "massive_scalar_determinant",
            "status": "A6_LOOP_KERNEL_DERIVED_CONDITIONALLY",
            "consequence": (
                "each gapped scalar supplies the exact spectral moment "
                "exp(-m^2/LambdaUV^2)/m^2 times the A6 tensor"
            ),
        },
        {
            "owner_component": "massless_primitive_scalar",
            "status": "NONLOCAL_BRANCH_NOT_FINITE_LOCAL_C6",
            "consequence": (
                "the m->0 local moment is infrared divergent and must "
                "remain in curvature form factors"
            ),
        },
        {
            "owner_component": "complete_signed_spectrum",
            "status": "SPIN_AND_MASS_SPECTRAL_MOMENT_NOT_MTS_OWNED",
            "consequence": (
                "scalar, fermion, vector, ghost, graviton and bath A6 "
                "weights cannot yet be summed"
            ),
        },
    ]
    return {
        "parent_path": str(parent_path),
        "four_derivative_parent_present": (
            "a_{R,b}" in parent_text
            and "a_{C,b}" in parent_text
            and "a_{E,b}" in parent_text
        ),
        "bare_dimension_six_declared": bare_dimension_six_declared,
        "rows": rows,
        "decision": (
            "The scalar-loop part of the dimension-six owner is now "
            "derived. The total c6 is a bare-plus-spectral matching "
            "coefficient and remains unowned; it is not set to zero."
        ),
        "passed": (
            "a_{R,b}" in parent_text
            and "a_{C,b}" in parent_text
            and "a_{E,b}" in parent_text
            and not bare_dimension_six_declared
            and len(rows) == 4
        ),
    }


def scalar_a6_strong_field_benchmarks() -> dict[str, Any]:
    owner = scalar_heat_kernel_a6_owner()
    rows: list[dict[str, Any]] = []
    selected = {
        "1.4_solar_mass_12km_neutron_star",
        "10_solar_mass_Schwarzschild_horizon",
    }
    for system in representative_systems()["rows"]:
        if system["system"] not in selected:
            continue
        q_k = system["qK_m_inverse"]
        max_compton_length = owner["q_over_gap_max"] / q_k
        max_cutoff_length = owner["q_over_cutoff_max"] / q_k
        rows.append(
            {
                "system": system["system"],
                "qK_m_inverse": q_k,
                "max_massive_gap_Compton_length_m_for_q_over_m_0p1": (
                    max_compton_length
                ),
                "max_UV_cutoff_length_m_for_q_over_Lambda_0p1": (
                    max_cutoff_length
                ),
                "scalar_a6_epsilon_envelope_h_ge_0p1": owner[
                    "epsilon6_scalar_envelope"
                ],
                "local_branch_condition": (
                    "massive gap and UV hierarchy both pass; no bare b6"
                ),
                "valid_for_claim": False,
            }
        )
    by_name = {row["system"]: row for row in rows}
    return {
        "rows": rows,
        "interpretation": (
            "If both the massive scalar gap and UV cutoff are at least "
            "ten times qK, h>=0.1 and the finite-mass Einstein-anchor "
            "shift delta_EH<=0.01, the complete raw Ricci-flat A6 "
            "operator-norm envelope is below 4.19e-5. This is a derived "
            "conditional scalar-loop bound, not a total MTS c6 value."
        ),
        "passed": (
            len(rows) == 2
            and 1000
            < by_name[
                "1.4_solar_mass_12km_neutron_star"
            ]["max_massive_gap_Compton_length_m_for_q_over_m_0p1"]
            < 1200
            and 1500
            < by_name[
                "10_solar_mass_Schwarzschild_horizon"
            ]["max_massive_gap_Compton_length_m_for_q_over_m_0p1"]
            < 1700
        ),
    }


def arbitration() -> dict[str, Any]:
    fluid = perfect_fluid_contact_image()
    tov = corrected_tov_map()
    contact = compact_contact_envelopes()
    a6 = scalar_heat_kernel_a6_owner()
    ownership = parent_dimension_six_ownership()
    return {
        "selected_branch": "STRICT_EFT_METRIC_ONLY_ANALYTIC_EH_BRANCH",
        "compact_fluid_advance": (
            "EXACT_CONTACT_TO_EFFECTIVE_EOS_AND_STANDARD_TOV_MAP_DERIVED"
        ),
        "compact_fluid_background_status": (
            "PRIVATE_CONDITIONAL_EOS_REDEFINITION_CORRESPONDENCE"
        ),
        "neutron_star_uniform_mean_density_contact_energy_benchmark": contact[
            "neutron_star_mean_density_energy_fraction_benchmark"
        ],
        "parameter_free_mass_radius_tidal_prediction": False,
        "scalar_a6_advance": (
            "MASSIVE_SCALAR_A6_KERNEL_AND_NEWTON_MATCHED_HIERARCHY_BOUND_"
            "DERIVED"
        ),
        "total_c6_parent_derived": a6["total_c6_parent_derived"],
        "full_strong_matter_GR_promoted": False,
        "full_fundamental_unification": False,
        "remaining_gap": (
            "apply the TOV response Jacobian to an independently fixed "
            "EOS away from turning points; derive the full signed "
            "dimension-six spectrum and bare matching; retain massless "
            "modes as nonlocal form factors"
        ),
        "next_target": (
            "4882-Y5-R2FR-compact-star-EOS-response-Jacobian-mass-radius-"
            "and-tidal-sensitivity-or-strong-matter-promotion-gate.md"
        ),
        "passed": (
            fluid["passed"]
            and tov["passed"]
            and contact["passed"]
            and a6["passed"]
            and ownership["passed"]
        ),
    }


def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "perfect_fluid": perfect_fluid_contact_image(),
        "tov_map": corrected_tov_map(),
        "contact_envelopes": compact_contact_envelopes(),
        "scalar_a6": scalar_heat_kernel_a6_owner(),
        "dimension_six_ownership": parent_dimension_six_ownership(),
        "a6_benchmarks": scalar_a6_strong_field_benchmarks(),
        "arbitration": arbitration(),
    }
    return {
        "sections": sections,
        "all_checks_pass": all(
            section["passed"] for section in sections.values()
        ),
        "decision": (
            "derive compact R2/C2 self-contact as a barotropic EOS "
            "renormalization with a standard TOV solve; place its uniform-"
            "mean-density neutron-star benchmark below 1e-18 at the "
            "inherited control caps and derive the profile-dependent "
            "mass bound; derive the exact massive-scalar Ricci-flat A6 "
            "kernel and a 4.2e-5 hierarchy envelope; withhold total c6 "
            "and parameter-free compact-star promotion until spectrum, "
            "bare matching and EOS response are supplied"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(result(), indent=2, sort_keys=True))
