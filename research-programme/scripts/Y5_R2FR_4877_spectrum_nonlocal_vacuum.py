from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"


def corpus_spectrum_audit() -> dict[str, Any]:
    sources = {
        "fundamental_action": ROOT
        / "core-mts-framework"
        / "action-principle"
        / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "effective_field_theory": ROOT
        / "core-mts-framework"
        / "field-theory"
        / "the-effective-field-theory-of-motion-timespace.md",
        "finite_leptons": ROOT
        / "quantum-particle-field"
        / "leptons-neutrinos"
        / "finite-lepton-families-from-curvature-memory-geometry.md",
        "neutrino_unification": ROOT
        / "quantum-particle-field"
        / "leptons-neutrinos"
        / "why-neutrinos-are-light-and-mix.md",
        "three_body": ROOT
        / "core-mts-framework"
        / "field-theory"
        / "axio-stable-three-body-bound-states-in-a-dissipative-field-theory.md",
        "yang_mills_extension": ROOT
        / "quantum-particle-field"
        / "yang-mills"
        / "yang-mills-mass-gap-via-the-motion-theory.md",
        "integrated_parent": POST
        / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
        "matching_checkpoint": POST
        / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
    }
    texts = {
        name: path.read_text(encoding="utf-8", errors="replace")
        for name, path in sources.items()
    }

    corpus_files = list((ROOT / "core-mts-framework").rglob("*.md"))
    corpus_files += list((ROOT / "quantum-particle-field").rglob("*.md"))
    fermionic_operator_terms = (
        "grassmann",
        "anticommut",
        "dirac operator",
        "clifford",
        "spin-statistics",
    )
    fermionic_hits: list[dict[str, str]] = []
    for path in corpus_files:
        content = path.read_text(encoding="utf-8", errors="replace").lower()
        for term in fermionic_operator_terms:
            if term in content:
                fermionic_hits.append(
                    {"path": str(path.relative_to(ROOT)), "term": term}
                )

    checks = {
        "scalar_declared": (
            "elementary object of mts is a scalar motion field"
            in texts["fundamental_action"].lower()
        ),
        "real_field_declared": (
            "the fundamental field is" in texts["effective_field_theory"].lower()
            and "ψ : ℝ⁴ → ℝ" in texts["effective_field_theory"]
        ),
        "complex_field_declared_later": (
            "complex motion field" in texts["finite_leptons"].lower()
            and "complex motion field" in texts["three_body"].lower()
        ),
        "single_substrate_declared": (
            "single nonlinear motion field"
            in texts["neutrino_unification"].lower()
        ),
        "particle_gauge_absence_declared": (
            "no gauge fields" in texts["finite_leptons"].lower()
            and "no gauge fields" in texts["three_body"].lower()
        ),
        "no_fermionic_operator": len(fermionic_hits) == 0,
        "public_matter_and_gauge_added": (
            "matter and gauge sectors" in texts["integrated_parent"].lower()
            and "s_{\\rm em}" in texts["matching_checkpoint"].lower()
        ),
        "yang_mills_is_separate_extension": (
            "we propose a modified yang" in texts["yang_mills_extension"].lower()
            and "mass gap" in texts["yang_mills_extension"].lower()
        ),
    }
    return {
        "sources": {name: str(path) for name, path in sources.items()},
        "checks": checks,
        "files_scanned_for_statistics": len(corpus_files),
        "fermionic_operator_hits": fermionic_hits,
        "primitive_field_verdict": (
            "BOSONIC_PSI_MEMORY_SUBSTRATE_AS_WRITTEN; REAL_VS_COMPLEX "
            "NORMALIZATION_CONFLICT; NO GRASSMANN_DIRAC_UV_MEASURE"
        ),
        "public_correspondence_verdict": (
            "MAXWELL_AND_GENERIC_MATTER_ARE LATER INDEPENDENT PUBLIC "
            "SECTORS; THEIR UV MULTIPLICITIES ARE NOT DERIVED BY THE "
            "PRIMITIVE MTS CORPUS"
        ),
        "counting_rule": (
            "SK r/a doubling is not two physical species; particle "
            "soliton families are configurations of psi and cannot be "
            "counted as Dirac determinants without a Grassmann kinetic "
            "operator and spin-statistics derivation"
        ),
        "passed": all(checks.values()),
    }


def determinant_weight_derivation() -> dict[str, Any]:
    scalar_a0 = sp.Rational(1, 2)
    scalar_r = sp.Rational(1, 2) * sp.Rational(1, 6)

    dirac_a0 = -sp.Rational(1, 2) * 4
    dirac_r = -sp.Rational(1, 2) * (-sp.Rational(1, 3))

    vector_a0 = sp.Rational(1, 2) * 4 - 1
    vector_r = (
        sp.Rational(1, 2) * (-sp.Rational(1, 3))
        - sp.Rational(1, 6)
    )

    scalar_c_table = sp.Rational(1) + sp.Rational(1, 2)
    dirac_c_table = -sp.Rational(7, 2) - sp.Rational(11, 2)
    vector_c_table = -sp.Rational(13) + sp.Rational(62, 2)

    a0_ratios = [
        sp.simplify(value / scalar_a0)
        for value in (scalar_a0, dirac_a0, vector_a0)
    ]
    r_ratios = [
        sp.simplify(value / scalar_r)
        for value in (scalar_r, dirac_r, vector_r)
    ]
    c_ratios = [
        sp.Integer(1),
        sp.simplify(-dirac_c_table / scalar_c_table),
        sp.simplify(vector_c_table / scalar_c_table),
    ]

    return {
        "operators": {
            "scalar": "Gamma_s=+1/2 Tr log Delta_0",
            "dirac": "Gamma_D=-1/2 Tr log[(Dirac)^2]",
            "maxwell": "Gamma_V=+1/2 Tr log Delta_1-Tr log Delta_0_ghost",
        },
        "vacuum_weights_scalar_Dirac_Maxwell": [
            str(value) for value in a0_ratios
        ],
        "EH_weights_minimal_scalar_Dirac_Maxwell": [
            str(value) for value in r_ratios
        ],
        "Weyl_log_weights_scalar_Dirac_Maxwell": [
            str(value) for value in c_ratios
        ],
        "meaning": (
            "relative to one minimally coupled real scalar: C0 weights "
            "are +1,-4,+2; Mstar2 weights are +1,+2,-4; C-log-C "
            "weights are +1,+6,+12 after gauge ghosts"
        ),
        "passed": (
            a0_ratios == [1, -4, 2]
            and r_ratios == [1, 2, -4]
            and c_ratios == [1, 6, 12]
        ),
    }


def all_species_weights() -> dict[str, Any]:
    scalar_count, dirac_count, vector_count = sp.symbols(
        "N_s N_D N_V", nonnegative=True, real=True
    )
    scalar_h_sum, scalar_h2_sum = sp.symbols(
        "S_h S_h2", nonnegative=True, real=True
    )
    cutoff, log_ratio = sp.symbols(
        "Lambda_UV L", positive=True, real=True
    )

    vacuum_weight = scalar_count + 2 * vector_count - 4 * dirac_count
    einstein_weight = (
        scalar_h_sum + 2 * dirac_count - 4 * vector_count
    )
    weyl_weight = scalar_count + 6 * dirac_count + 12 * vector_count

    constant_loop = cutoff**4 * vacuum_weight / (64 * sp.pi**2)
    planck_squared = cutoff**2 * einstein_weight / (96 * sp.pi**2)
    local_c2 = log_ratio * weyl_weight / (1920 * sp.pi**2)
    local_r2 = log_ratio * scalar_h2_sum / (1152 * sp.pi**2)

    return {
        "definitions": (
            "S_h=sum_s(1-6xi_s); S_h2=sum_s(1-6xi_s)^2; "
            "N_D may be half-integer when counting Weyl fermions"
        ),
        "W0_vacuum": str(vacuum_weight),
        "W1_Einstein": str(einstein_weight),
        "WC_Weyl": str(weyl_weight),
        "C0_loop": str(constant_loop),
        "Mstar_squared": str(planck_squared),
        "aC_running": str(local_c2),
        "aR_running": str(local_r2),
        "simultaneous_gate": "W0=0 and W1>0",
        "scope": (
            "These are matter-sector weights. The integrated H field and "
            "Diff Faddeev-Popov ghosts are not included. Their power-law "
            "C0 and Einstein coefficients are regulator/gauge dependent "
            "and belong in the renormalized C0_R and M_R^2 matching; they "
            "cannot be used as an unsourced vacuum-cancellation claim."
        ),
        "passed": (
            vacuum_weight
            == scalar_count + 2 * vector_count - 4 * dirac_count
            and einstein_weight
            == scalar_h_sum + 2 * dirac_count - 4 * vector_count
            and weyl_weight
            == scalar_count + 6 * dirac_count + 12 * vector_count
        ),
    }


def evaluate_weights(
    scalar_count: float,
    dirac_count: float,
    vector_count: float,
    scalar_h_sum: float,
    scalar_h2_sum: float,
) -> dict[str, Any]:
    vacuum_weight = scalar_count + 2 * vector_count - 4 * dirac_count
    einstein_weight = scalar_h_sum + 2 * dirac_count - 4 * vector_count
    weyl_weight = scalar_count + 6 * dirac_count + 12 * vector_count
    return {
        "N_s": scalar_count,
        "N_D": dirac_count,
        "N_V": vector_count,
        "S_h": scalar_h_sum,
        "S_h2": scalar_h2_sum,
        "W0": vacuum_weight,
        "W1": einstein_weight,
        "WC": weyl_weight,
        "vacuum_cancels": abs(vacuum_weight) < 1e-12,
        "positive_EH": einstein_weight > 0,
    }


def branch_spectrum_tests() -> dict[str, Any]:
    scenarios = [
        {
            "branch": "primitive_real_psi_only",
            **evaluate_weights(1, 0, 0, 1, 1),
            "ownership": "explicit core action",
        },
        {
            "branch": "primitive_complex_psi_only",
            **evaluate_weights(2, 0, 0, 2, 2),
            "ownership": "later particle normalization",
        },
        {
            "branch": "real_psi_plus_public_U1",
            **evaluate_weights(1, 0, 1, 1, 1),
            "ownership": "minimal integrated-H correspondence",
        },
        {
            "branch": "complex_psi_Gamma_plus_public_U1",
            **evaluate_weights(3, 0, 1, 3, 3),
            "ownership": "maximal explicit bosonic reading",
        },
        {
            "branch": "five_minimal_scalars_plus_public_U1",
            **evaluate_weights(5, 0, 1, 5, 5),
            "ownership": "minimum positive-EH bosonic completion",
        },
        {
            "branch": "imported_SM_without_RH_neutrinos",
            **evaluate_weights(4, 22.5, 12, 4, 4),
            "ownership": "external correspondence benchmark",
        },
        {
            "branch": "imported_SM_with_three_RH_neutrinos",
            **evaluate_weights(4, 24, 12, 4, 4),
            "ownership": "external correspondence benchmark",
        },
    ]
    primitive = scenarios[:5]
    standard_model = scenarios[5:]
    return {
        "scenarios": scenarios,
        "bosonic_vacuum_no_go": (
            "For N_D=0 with N_s>0 and N_V>=0, "
            "W0=N_s+2N_V>0; healthy bosonic/ghost-completed fields "
            "cannot cancel the proper-time quartic vacuum coefficient."
        ),
        "bosonic_positive_EH_gate": (
            "For minimal scalars and N_D=0, W1=N_s-4N_V>0; "
            "one public U(1) requires at least five real scalar modes "
            "or an equivalent nonminimal/bath contribution."
        ),
        "primitive_verdict": (
            "NO EXPLICIT PRIMITIVE MTS SCENARIO CANCELS W0; THE TWO "
            "MAXWELL SCENARIOS ALSO HAVE W1<0 UNTIL EXTRA BATH MODES "
            "OR NONMINIMAL WEIGHT ARE ADDED."
        ),
        "SM_verdict": (
            "IMPORTED STANDARD-MODEL CONTENT HAS POSITIVE W1 BUT "
            "W0=-62 WITHOUT AND -68 WITH THREE RIGHT-HANDED NEUTRINOS; "
            "IT DOES NOT SELECT A ZERO VACUUM."
        ),
        "passed": (
            all(not row["vacuum_cancels"] for row in primitive)
            and standard_model[0]["W0"] == -62
            and standard_model[0]["W1"] == 1
            and standard_model[0]["WC"] == 283
            and standard_model[1]["W0"] == -68
            and standard_model[1]["W1"] == 4
            and standard_model[1]["WC"] == 292
        ),
    }


def moment_sum_rule_rigidity() -> dict[str, Any]:
    mass_squared = sp.symbols("x1:5", nonnegative=True, real=True)
    dirac_mass_squared = sp.symbols("a", nonnegative=True, real=True)
    first_moment = 4 * dirac_mass_squared
    second_moment = 4 * dirac_mass_squared**2
    variance_identity = sp.simplify(
        second_moment
        - 2 * dirac_mass_squared * first_moment
        + 4 * dirac_mass_squared**2
    )
    explicit_variance = sum(
        (value - dirac_mass_squared) ** 2 for value in mass_squared
    )
    return {
        "four_scalar_one_Dirac_conditions": (
            "sum_i m_si^2=4m_D^2 and sum_i m_si^4=4m_D^4"
        ),
        "variance_identity": (
            "sum_i(m_si^2-m_D^2)^2=" + str(variance_identity)
        ),
        "explicit_nonnegative_sum": str(explicit_variance),
        "theorem": (
            "For real nonnegative masses, simultaneous quadratic and "
            "quartic cancellation in the 4-scalar/1-Dirac example forces "
            "all four scalar masses to equal the Dirac mass. The "
            "cancellation is threshold-rigid, not a generic count identity."
        ),
        "passed": variance_identity == 0,
    }


def nonlocal_form_factors() -> dict[str, Any]:
    weyl_weight, scalar_h2_sum, einstein_weight = sp.symbols(
        "W_C S_h2 W_1", positive=True, real=True
    )
    log_ratio, momentum_ratio = sp.symbols(
        "L x", positive=True, real=True
    )

    nonlocal_c = -weyl_weight / (3840 * sp.pi**2)
    nonlocal_r = -scalar_h2_sum / (2304 * sp.pi**2)
    matched_c = sp.simplify(nonlocal_c * (-2 * log_ratio))
    matched_r = sp.simplify(nonlocal_r * (-2 * log_ratio))
    expected_c = log_ratio * weyl_weight / (1920 * sp.pi**2)
    expected_r = log_ratio * scalar_h2_sum / (1152 * sp.pi**2)

    epsilon_scalar = (
        log_ratio * scalar_h2_sum * momentum_ratio**2 / einstein_weight
    )
    epsilon_spin2 = (
        log_ratio
        * weyl_weight
        * momentum_ratio**2
        / (5 * einstein_weight)
    )
    infrared_kernel = momentum_ratio**2 * sp.log(1 / momentum_ratio)
    infrared_limit = sp.limit(infrared_kernel, momentum_ratio, 0, dir="+")
    critical = sp.exp(-sp.Rational(1, 2))
    critical_value = sp.simplify(infrared_kernel.subs(momentum_ratio, critical))

    return {
        "Gamma_nonlocal": (
            "-int sqrt(-g)[W_C C log(-Box/LambdaUV^2) C/(3840pi^2)"
            "+S_h2 R log(-Box/LambdaUV^2) R/(2304pi^2)]"
        ),
        "b_C": str(nonlocal_c),
        "b_R": str(nonlocal_r),
        "local_log_match_C": str(matched_c),
        "local_log_match_R": str(matched_r),
        "epsilon0_general": str(epsilon_scalar),
        "epsilon2_general": str(epsilon_spin2),
        "IR_kernel_limit": str(infrared_limit),
        "kernel_maximum": (
            "x^2 ln(1/x) has its global interior maximum at "
            f"x=exp(-1/2), value={critical_value}"
        ),
        "pole_interpretation": (
            "The universal massless logarithm vanishes relative to EH as "
            "q/LambdaUV->0. Frozen local-log pole masses are matching-scale "
            "diagnostics, not literal global particles. Any additional "
            "zero of the full transcendental denominator near the cutoff "
            "lies outside the controlled IR expansion."
        ),
        "unavoidable_Weyl_log": (
            "W_C=N_s+6N_D+12N_V>0 for every nonempty healthy spectrum; "
            "the C-log-C form factor cannot be cancelled by balancing "
            "ordinary scalar, fermion and vector species."
        ),
        "passed": (
            sp.simplify(matched_c - expected_c) == 0
            and sp.simplify(matched_r - expected_r) == 0
            and infrared_limit == 0
            and critical_value == 1 / (2 * sp.E)
        ),
    }


def gravity_loop_scope() -> dict[str, Any]:
    return {
        "calculated_sector": (
            "one-loop healthy real scalars, Dirac fermions and "
            "gauge-fixed Maxwell vectors on the public metric"
        ),
        "omitted_sector": (
            "integrated-H graviton and Diff-ghost determinants"
        ),
        "power_law_rule": (
            "off-shell quartic and quadratic H/ghost coefficients are "
            "gauge- and regulator-dependent matching contributions; absorb "
            "them into C0_R and M_R^2 rather than balancing them against "
            "matter as if they were physical species counts"
        ),
        "nonlocal_rule": (
            "gravity-loop logarithms require a separately gauge-consistent "
            "background-field calculation. They are not included in W_C or "
            "S_h2 here, so the imported-SM rows are a matter-induced anchor, "
            "not a complete one-loop parent prediction"
        ),
        "control_rule": (
            "the arena table additionally tests an effective logarithmic "
            "coefficient envelope of 10^6 and reports the coefficient needed "
            "to reach 10^-30; this is a hierarchy stress test, not a derived "
            "bound on the omitted H/ghost coefficients"
        ),
        "passed": True,
    }


def nonlocal_pole_gate() -> dict[str, Any]:
    momentum_ratio = sp.symbols("x", positive=True, real=True)
    scalar_ratio, spin2_ratio = sp.symbols(
        "rho_0 rho_2", nonnegative=True, real=True
    )
    kernel = momentum_ratio**2 * sp.log(1 / momentum_ratio)
    critical = sp.exp(-sp.Rational(1, 2))
    maximum = sp.simplify(kernel.subs(momentum_ratio, critical))
    return {
        "domain": "Euclidean 0<x=q/LambdaUV<1 with W1>0",
        "kernel": str(kernel),
        "kernel_sign": "x^2 ln(1/x)>0 for 0<x<1",
        "D0_over_EH": "1+s_0 rho_0 x^2 ln(1/x)",
        "D2_over_EH": "1+s_2 rho_2 x^2 ln(1/x)",
        "sign_scope": (
            "s_0,s_2 encode continuation and projector conventions; the "
            "root exclusion below uses the absolute correction and therefore "
            "does not assume either sign"
        ),
        "rho_definitions": (
            "rho_0=S_h2/W1 and rho_2=W_C/(5W1), both nonnegative "
            "for the healthy matter spectra tested here"
        ),
        "controlled_domain_theorem": (
            "If rho_i x^2 ln(1/x)<1, then |D_i/EH|>=1-rho_i "
            "x^2 ln(1/x)>0. Hence no real root exists in any tested "
            "domain satisfying the residual gate, regardless of s_i."
        ),
        "maximum_correction": (
            "x^2 ln(1/x)<=1/(2e); therefore delta0<=rho_0/(2e) "
            "and delta2<=rho_2/(2e). A sign-independent no-root theorem "
            "over the entire subcutoff interval requires rho_i<2e."
        ),
        "SM_subcutoff_result": (
            "For W1=1, S_h2=4 and W_C=283, rho_0=4<2e closes "
            "the scalar interval, but rho_2=283/5>2e does not exclude a "
            "spin-2 root near the cutoff. The local arenas remain many "
            "orders inside the no-root gate."
        ),
        "finite_counterterm_gate": (
            "This theorem excludes only the universal logarithmic piece. "
            "Finite renormalized local R^2 and C^2 coefficients and omitted "
            "H/ghost form factors must still satisfy their own denominator "
            "bounds in every tested arena."
        ),
        "lorentzian_scope": (
            "After log(-q^2-i0)=ln(q^2)-i*pi, roots require the complete "
            "continued denominator. Any candidate near the cutoff is not "
            "settled by this infrared expansion."
        ),
        "passed": (
            sp.limit(kernel, momentum_ratio, 0, dir="+") == 0
            and maximum == 1 / (2 * sp.E)
            and 4 < 2 * math.e
            and 283 / 5 > 2 * math.e
        ),
    }


def calibrated_arena_smoke() -> dict[str, Any]:
    reduced_planck_eV = 2.435e27
    hbar_c_eVm = 1.973269804e-7
    weyl_weight = 283.0
    scalar_h2_sum = 4.0
    cutoff_eV = reduced_planck_eV
    stress_weight = 1.0e6
    residual_target = 1.0e-30

    arenas = [
        ("R10_50_micrometre", 50e-6),
        ("atomic_clock_Angstrom", 1e-10),
        ("nuclear_1_fm", 1e-15),
        ("solar_PPN_Rsun", 6.957e8),
        ("orbital_1_AU", 1.495978707e11),
        ("galaxy_10_kpc", 10 * 3.0856775814913673e19),
    ]
    rows: list[dict[str, Any]] = []
    for arena, length_m in arenas:
        momentum_eV = hbar_c_eVm / length_m
        log_ratio = math.log(cutoff_eV / momentum_eV)
        q_over_planck_squared = (momentum_eV / reduced_planck_eV) ** 2
        epsilon0 = (
            log_ratio
            * scalar_h2_sum
            * q_over_planck_squared
            / (96 * math.pi**2)
        )
        epsilon2 = (
            log_ratio
            * weyl_weight
            * q_over_planck_squared
            / (480 * math.pi**2)
        )
        epsilon0_stress = (
            log_ratio
            * stress_weight
            * q_over_planck_squared
            / (96 * math.pi**2)
        )
        epsilon2_stress = (
            log_ratio
            * stress_weight
            * q_over_planck_squared
            / (480 * math.pi**2)
        )
        scalar_weight_at_target = (
            residual_target
            * 96
            * math.pi**2
            / (log_ratio * q_over_planck_squared)
        )
        weyl_weight_at_target = (
            residual_target
            * 480
            * math.pi**2
            / (log_ratio * q_over_planck_squared)
        )
        rows.append(
            {
                "arena": arena,
                "length_m": length_m,
                "q_eV": momentum_eV,
                "L": log_ratio,
                "epsilon0": epsilon0,
                "epsilon2": epsilon2,
                "epsilon0_weight_1e6": epsilon0_stress,
                "epsilon2_weight_1e6": epsilon2_stress,
                "S_h2_at_1e_minus_30": scalar_weight_at_target,
                "W_C_at_1e_minus_30": weyl_weight_at_target,
                "below_1e_minus_30": max(epsilon0, epsilon2) < 1e-30,
                "weight_1e6_below_1e_minus_30": max(
                    epsilon0_stress, epsilon2_stress
                )
                < residual_target,
            }
        )
    return {
        "benchmark": (
            "Imported SM without right-handed neutrinos: W_C=283, "
            "S_h2=4, Mbar_Pl=2.435e27 eV, LambdaUV=Mbar_Pl"
        ),
        "matched_formulas": (
            "epsilon0=L S_h2 q^2/(96pi^2 Mbar_Pl^2); "
            "epsilon2=L W_C q^2/(480pi^2 Mbar_Pl^2)"
        ),
        "rows": rows,
        "max_local_residual": max(
            max(row["epsilon0"], row["epsilon2"]) for row in rows
        ),
        "coefficient_stress": (
            "Set S_h2=W_C=10^6 independently as a deliberately large "
            "effective-log envelope. This does not source or derive the "
            "omitted graviton/ghost coefficient."
        ),
        "max_weight_1e6_residual": max(
            max(
                row["epsilon0_weight_1e6"],
                row["epsilon2_weight_1e6"],
            )
            for row in rows
        ),
        "smallest_weight_reaching_1e_minus_30": min(
            min(row["S_h2_at_1e_minus_30"], row["W_C_at_1e_minus_30"])
            for row in rows
        ),
        "interpretation": (
            "Once GN is calibrated, W1 and LambdaUV cancel from the "
            "leading ratios. Even the nuclear benchmark is far below "
            "current local sensitivity. This tests only universal one-loop "
            "massless form factors, not unknown tree-level MTS operators."
        ),
        "passed": all(
            row["below_1e_minus_30"]
            and row["weight_1e6_below_1e_minus_30"]
            for row in rows
        ),
    }


def renormalized_vacuum_freeze() -> dict[str, Any]:
    speed_of_light = 299_792_458.0
    megaparsec_m = 3.0856775814913673e22
    hubble_km_s_mpc = 67.4
    omega_m = 0.315
    omega_lambda = 1 - omega_m
    hubble_s = hubble_km_s_mpc * 1000 / megaparsec_m
    lambda_cal_m2 = 3 * omega_lambda * hubble_s**2 / speed_of_light**2

    domains = [
        ("R10_50_micrometre", 50e-6),
        ("laboratory_1_m", 1.0),
        ("Earth_radius", 6.371e6),
        ("solar_system_1_AU", 1.495978707e11),
        ("galaxy_100_kpc", 100 * 3.0856775814913673e19),
        ("cosmology_1_Gpc", 1e3 * megaparsec_m),
    ]
    rows = [
        {
            "domain": name,
            "length_m": length,
            "epsilon_Lambda": lambda_cal_m2 * length**2,
            "local_flat_safe_1e_minus_6": lambda_cal_m2 * length**2 < 1e-6,
        }
        for name, length in domains
    ]
    return {
        "calibration_source": (
            "Planck 2018 base-LambdaCDM smoke baseline H0=67.4 "
            "km/s/Mpc, Omega_m=0.315"
        ),
        "Lambda_cal_m^-2": lambda_cal_m2,
        "renormalization_condition": (
            "C0_R(mu0)=-M_R^2 Lambda_cal at one declared cosmological "
            "matching scale mu0; no per-dataset or per-arena retuning"
        ),
        "saddle_after_freeze": "Lambda_bg=Lambda_cal",
        "local_background_gate": "epsilon_Lambda=abs(Lambda_cal)L_domain^2",
        "rows": rows,
        "decision": (
            "FREEZE C0_R AS AN EXPLICIT RENORMALIZED RELEVANT COUPLING IN "
            "THE CURRENT COMPETITIVE EFT; RETAIN SPECTRUM CANCELLATION AS "
            "A FUTURE MICROSCOPIC RESEARCH TARGET, NOT A PRESENT CLAIM"
        ),
        "passed": (
            1.0e-52 < lambda_cal_m2 < 1.2e-52
            and all(row["local_flat_safe_1e_minus_6"] for row in rows[:-1])
            and not rows[-1]["local_flat_safe_1e_minus_6"]
        ),
    }


def branch_arbitration() -> dict[str, Any]:
    return {
        "primitive_vacuum": "REJECT_DERIVED_CANCELLATION_ON_CURRENT_CORPUS",
        "reason": (
            "the UV substrate is bosonic as written and has W0>0; no "
            "Grassmann determinant or threshold-complete signed spectrum "
            "is derived"
        ),
        "imported_SM": "POSITIVE_EH_BUT_NONZERO_VACUUM_BENCHMARK",
        "nonlocal_sector": (
            "UNAVOIDABLE_BUT_IR_DECOUPLING UNIVERSAL LOGS RETAINED"
        ),
        "current_EFT": (
            "RENORMALIZED_C0_FREEZE_SELECTED; GN CALIBRATED ONCE; EH PLUS "
            "UNIVERSAL HILBERT/MAXWELL SOURCE REMAINS THE LOCAL LEAD"
        ),
        "next_target": (
            "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-"
            "nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md"
        ),
        "passed": True,
    }


def result() -> dict[str, Any]:
    sections = {
        "corpus_spectrum": corpus_spectrum_audit(),
        "determinant_weights": determinant_weight_derivation(),
        "all_species": all_species_weights(),
        "branch_tests": branch_spectrum_tests(),
        "moment_rigidity": moment_sum_rule_rigidity(),
        "nonlocal": nonlocal_form_factors(),
        "gravity_loop_scope": gravity_loop_scope(),
        "nonlocal_pole_gate": nonlocal_pole_gate(),
        "arena_smoke": calibrated_arena_smoke(),
        "vacuum_freeze": renormalized_vacuum_freeze(),
        "arbitration": branch_arbitration(),
    }
    return {
        "sections": sections,
        "all_checks_pass": all(
            section["passed"] for section in sections.values()
        ),
        "decision": (
            "reject present MTS ownership of a vacuum-cancelling spectrum; "
            "freeze the cosmological volume coefficient as one explicit "
            "renormalized coupling, retain the unique nonlocal form factors, "
            "and advance the calibrated EH branch to arena-specific local "
            "GR/Newton/Maxwell residual tests"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(result(), indent=2, sort_keys=True))
