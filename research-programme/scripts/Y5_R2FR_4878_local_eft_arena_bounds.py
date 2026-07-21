from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
OUTPUT = POST / "source-intake" / "mts_residuals"

C = 299_792_458.0
G = 6.67430e-11
HBAR = 1.054_571_817e-34
LP2 = G * HBAR / C**3
LBAR_P2 = 8 * math.pi * LP2
LBAR_P = math.sqrt(LBAR_P2)

R10_MIN_M = 52.0e-6
R_EARTH_M = 6.371e6
R_GALILEO_M = 2.960e7
R_SUN_M = 6.957e8
CASSINI_IMPACT_M = 1.6 * R_SUN_M
AU_M = 149_597_870_700.0
MERCURY_A_M = 5.790905e10
MERCURY_E = 0.205630
MERCURY_PERIOD_DAYS = 87.9691
ARCSEC_PER_RAD = 206_264.806_247_096_36
DAYS_PER_CENTURY = 36_525.0


def source_contract() -> dict[str, Any]:
    local_sources = {
        "prior_checkpoint": (
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
        ),
        "prior_validation": (
            OUTPUT / "P8_Y5_BRR545_4877_VALIDATION.csv",
            "VAL4877_OVERALL",
        ),
        "r10_tex": (
            POST
            / "source-intake"
            / "r10_curve_acquisition"
            / "4635"
            / "source"
            / "FB_ISL_pdf.tex",
            "percent-level measurements of $G_N$",
        ),
        "r10_vector_figure": (
            POST
            / "source-intake"
            / "r10_curve_acquisition"
            / "4635"
            / "source"
            / "fig5b1.pdf",
            None,
        ),
        "r10_vector_curve": (
            OUTPUT
            / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv",
            "R10_EOTWASH2020_ABS_ALPHA_VECTOR_FROM_FIG5B1",
        ),
        "arena_sources": (
            OUTPUT / "P8_Y5_R2FR_4800_ARENA_PROJECTION_INPUT.csv",
            "ppn_gamma_cassini_required_tau",
        ),
        "local_linear_gr": (
            POST
            / "4719-Y5-R2FR-local-linearized-GR-limit-and-Poisson-equation-residual-bound.md",
            "Poisson",
        ),
        "non_eh_matrix": (
            POST
            / "4720-Y5-R2FR-EH-reduction-parent-signature-or-nonEH-operator-coefficient-matrix.md",
            "R^2",
        ),
        "maxwell_checkpoint": (
            POST
            / "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md",
            "Poynting",
        ),
    }
    rows: list[dict[str, Any]] = []
    for source_id, (path, marker) in local_sources.items():
        exists = path.exists()
        marker_found = exists
        if exists and marker is not None and path.suffix.lower() != ".pdf":
            marker_found = marker in path.read_text(
                encoding="utf-8", errors="replace"
            )
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker or "binary_path_only",
                "marker_found": marker_found,
            }
        )
    web_sources = {
        "strict_eft_r2_absence": "https://arxiv.org/abs/1911.10108",
        "quadratic_gravity_potentials": "https://arxiv.org/abs/1508.00010",
        "pure_gravity_quantum_potential": "https://arxiv.org/abs/hep-th/0211072",
        "r10_primary": "https://arxiv.org/abs/2002.11761",
        "cassini_primary": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
        "galileo_primary": "https://arxiv.org/abs/1906.06161",
        "mercury_primary": "https://www.osti.gov/biblio/22863119",
        "gw_speed_primary": "https://arxiv.org/abs/1710.05834",
    }
    return {
        "local_rows": rows,
        "web_sources": web_sources,
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


def projector_transfer() -> dict[str, Any]:
    d0, d2, epsilon = sp.symbols("d0 d2 epsilon", real=True)
    a0 = 1 + d0
    a2 = 1 + d2
    phi_exact = sp.Rational(4, 3) / a2 - sp.Rational(1, 3) / a0
    psi_exact = sp.Rational(2, 3) / a2 + sp.Rational(1, 3) / a0
    gamma_exact = sp.factor(psi_exact / phi_exact)

    def first_order(expression: sp.Expr) -> sp.Expr:
        scaled = expression.subs({d0: epsilon * d0, d2: epsilon * d2})
        return sp.expand(sp.series(scaled, epsilon, 0, 2).removeO()).subs(
            epsilon, 1
        )

    phi_linear = first_order(phi_exact)
    psi_linear = first_order(psi_exact)
    gamma_linear = first_order(gamma_exact)
    expected_phi = 1 + d0 / 3 - 4 * d2 / 3
    expected_psi = 1 - d0 / 3 - 2 * d2 / 3
    expected_gamma = 1 + 2 * (d2 - d0) / 3

    q2, m0_squared, m2_squared = sp.symbols(
        "q2 m0_squared m2_squared", positive=True
    )
    scalar_kernel = sp.apart(
        1 / (q2 * (1 + q2 / m0_squared)), q2
    )
    spin2_kernel = sp.apart(
        1 / (q2 * (1 + q2 / m2_squared)), q2
    )
    return {
        "A0": "1+d0",
        "A2": "1+d2",
        "Phi_over_Phi_Newton_exact": str(phi_exact),
        "Psi_over_Psi_Newton_exact": str(psi_exact),
        "gamma_exact": str(gamma_exact),
        "Phi_over_Phi_Newton_linear": str(phi_linear),
        "Psi_over_Psi_Newton_linear": str(psi_linear),
        "gamma_linear": str(gamma_linear),
        "massive_scalar_kernel": str(scalar_kernel),
        "massive_spin2_kernel": str(spin2_kernel),
        "resummed_Phi": (
            "-GM/r [1+(1/3)exp(-m0 r)-(4/3)exp(-m2 r)]"
        ),
        "resummed_Psi": (
            "-GM/r [1-(1/3)exp(-m0 r)-(2/3)exp(-m2 r)]"
        ),
        "passed": (
            sp.simplify(phi_linear - expected_phi) == 0
            and sp.simplify(psi_linear - expected_psi) == 0
            and sp.simplify(gamma_linear - expected_gamma) == 0
            and sp.simplify(
                scalar_kernel
                - (1 / q2 - 1 / (q2 + m0_squared))
            )
            == 0
            and sp.simplify(
                spin2_kernel
                - (1 / q2 - 1 / (q2 + m2_squared))
            )
            == 0
        ),
    }


def strict_eft_contact_branch() -> dict[str, Any]:
    a_r, a_c, q_squared = sp.symbols("a_R a_C q_squared", real=True)
    lbar_squared = sp.symbols("lbar_P_squared", positive=True)
    d0_local = 12 * a_r * lbar_squared * q_squared
    d2_local = -4 * a_c * lbar_squared * q_squared
    phi_integrand_correction = sp.simplify(
        (d0_local / 3 - 4 * d2_local / 3) / q_squared
    )
    psi_integrand_correction = sp.simplify(
        (-d0_local / 3 - 2 * d2_local / 3) / q_squared
    )

    hierarchy_factor = LBAR_P2 / R10_MIN_M**2
    control_fraction = 1.0e-2
    a_r_cap = control_fraction / (12 * hierarchy_factor)
    a_c_cap = control_fraction / (4 * hierarchy_factor)
    return {
        "branch": "STRICT_PERTURBATIVE_EFT_SELECTED",
        "d0_local": str(d0_local),
        "d2_local": str(d2_local),
        "Phi_Fourier_integrand_correction": str(phi_integrand_correction),
        "Psi_Fourier_integrand_correction": str(psi_integrand_correction),
        "support_theorem": (
            "The q^2 factors cancel the massless 1/q^2 propagator. "
            "The remaining momentum polynomial Fourier-transforms to "
            "delta^3(r) and derivatives, so it vanishes between "
            "nonoverlapping compact source supports."
        ),
        "field_redefinition_scope": (
            "R^2 and Ricci^2 operators can be moved into local matter "
            "contact operators order by order; they do not create a "
            "long-range Yukawa force in strict EFT."
        ),
        "r10_shortest_separation_m": R10_MIN_M,
        "lbar_P_m": LBAR_P,
        "hierarchy_factor_lbarP2_over_r2": hierarchy_factor,
        "control_fraction": control_fraction,
        "aR_abs_control_cap": a_r_cap,
        "aC_abs_control_cap": a_c_cap,
        "cap_kind": "EFT_DERIVATIVE_CONTROL_NOT_EMPIRICAL_BOUND",
        "r10_yukawa_curve_applies": False,
        "passed": (
            q_squared not in phi_integrand_correction.free_symbols
            and q_squared not in psi_integrand_correction.free_symbols
            and 2.42e-60 < hierarchy_factor < 2.44e-60
            and 3.42e56 < a_r_cap < 3.45e56
            and 1.02e57 < a_c_cap < 1.04e57
        ),
    }


def _read_r10_curve() -> list[dict[str, float]]:
    path = (
        OUTPUT
        / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv"
    )
    rows: list[dict[str, float]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "lambda_m": float(row["lambda_m"]),
                    "alpha_bound_abs": float(row["alpha_bound_abs"]),
                }
            )
    return sorted(rows, key=lambda row: row["lambda_m"])


def _log_crossing(
    rows: list[dict[str, float]], target_alpha: float
) -> float:
    crossings: list[float] = []
    for left, right in zip(rows, rows[1:]):
        y_left = left["alpha_bound_abs"]
        y_right = right["alpha_bound_abs"]
        if (y_left - target_alpha) * (y_right - target_alpha) <= 0:
            if y_left == y_right:
                continue
            fraction = (
                math.log(target_alpha) - math.log(y_left)
            ) / (math.log(y_right) - math.log(y_left))
            crossing = math.exp(
                math.log(left["lambda_m"])
                + fraction
                * (
                    math.log(right["lambda_m"])
                    - math.log(left["lambda_m"])
                )
            )
            crossings.append(crossing)
    if len(crossings) != 1:
        raise ValueError(
            f"expected one R10 crossing for alpha={target_alpha}, "
            f"found {len(crossings)}"
        )
    return crossings[0]


def resummed_quadratic_diagnostic() -> dict[str, Any]:
    rows = _read_r10_curve()
    lambda_scalar = _log_crossing(rows, 1 / 3)
    lambda_gravity = _log_crossing(rows, 1.0)
    lambda_spin2 = _log_crossing(rows, 4 / 3)

    a_r_bound = (lambda_scalar / LBAR_P) ** 2 / 12
    a_c_abs_bound = (lambda_spin2 / LBAR_P) ** 2 / 4
    scalar_d0_at_r10 = 12 * a_r_bound * LBAR_P2 / R10_MIN_M**2
    spin2_d2_at_r10 = 4 * a_c_abs_bound * LBAR_P2 / R10_MIN_M**2
    return {
        "branch": "RESUMMED_QUADRATIC_GRAVITY_DIAGNOSTIC_ONLY",
        "curve_rows": len(rows),
        "curve_provenance": str(
            OUTPUT
            / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv"
        ),
        "alpha_1_crossing_m": lambda_gravity,
        "published_alpha_1_limit_m": 38.6e-6,
        "alpha_1_crossing_fractional_error": abs(
            lambda_gravity / 38.6e-6 - 1
        ),
        "scalar_alpha": 1 / 3,
        "lambda0_limit_m": lambda_scalar,
        "aR_internal_abs_limit": a_r_bound,
        "spin2_alpha_abs": 4 / 3,
        "lambda2_abs_envelope_m": lambda_spin2,
        "aC_internal_abs_limit": a_c_abs_bound,
        "scalar_d0_at_r10_limit": scalar_d0_at_r10,
        "spin2_abs_d2_at_r10_limit": spin2_d2_at_r10,
        "mass_relations": (
            "lambda0=sqrt(12 aR)*lbarP for aR>0; "
            "lambda2=2 sqrt(abs(aC))*lbarP for aC<0"
        ),
        "spin2_health": (
            "aC<0 gives a real massive spin-2 pole with negative residue; "
            "aC>0 gives a tachyonic/oscillatory pole. Neither is admitted "
            "as a healthy fundamental completion."
        ),
        "claim_guard": (
            "The absolute-alpha vector extraction reproduces the "
            "published alpha=1 crossing but is not the official "
            "sign-specific supplemental table. These limits remain "
            "internal nonclaim diagnostics."
        ),
        "valid_for_claim": False,
        "passed": (
            len(rows) == 176
            and abs(lambda_gravity / 38.6e-6 - 1) < 0.01
            and 53.6e-6 < lambda_scalar < 53.8e-6
            and 35.4e-6 < lambda_spin2 < 35.7e-6
            and scalar_d0_at_r10 > 1
            and spin2_d2_at_r10 > 0.4
        ),
    }


def matter_nonlocal_position_space() -> dict[str, Any]:
    scalar_h2_sum = 4.0
    weyl_weight = 283.0
    kappa0 = scalar_h2_sum * LBAR_P2 / (96 * math.pi**2)
    kappa2 = weyl_weight * LBAR_P2 / (480 * math.pi**2)
    eta_phi = (kappa0 + 4 * kappa2) / 3
    eta_psi = (kappa0 + 2 * kappa2) / 3
    eta_slip = 2 * (kappa0 + kappa2) / 3
    return {
        "benchmark": (
            "Imported Standard Model without right-handed neutrinos: "
            "S_h2=4 and W_C=283; correspondence benchmark, not a "
            "primitive MTS spectrum derivation."
        ),
        "fourier_identity_r_positive": (
            "integral d^3q/(2pi)^3 exp(i q.r) log(q^2/mu^2) "
            "= -1/(2pi r^3)"
        ),
        "kappa0_m2": kappa0,
        "kappa2_m2": kappa2,
        "etaPhi_m2": eta_phi,
        "etaPsi_m2": eta_psi,
        "etaSlip_m2": eta_slip,
        "potential_envelope": "abs(delta Phi/Phi_N)<=etaPhi/r^2",
        "acceleration_envelope": "abs(delta a/a_N)<=3 etaPhi/r^2",
        "slip_envelope": "abs(gamma-1)<=etaSlip/r^2",
        "no_cancellation": True,
        "passed": (
            2.76e-71 < kappa0 < 2.79e-71
            and 3.91e-70 < kappa2 < 3.94e-70
            and 5.31e-70 < eta_phi < 5.34e-70
            and 2.69e-70 < eta_psi < 2.72e-70
            and 2.78e-70 < eta_slip < 2.82e-70
        ),
    }


def pure_gravity_quantum_tail() -> dict[str, Any]:
    coefficient = 41 / (10 * math.pi)
    eta_gravity = coefficient * LP2
    potential_r10 = eta_gravity / R10_MIN_M**2
    acceleration_r10 = 3 * potential_r10
    return {
        "source": "https://arxiv.org/abs/hep-th/0211072",
        "coefficient_41_over_10pi": coefficient,
        "ordinary_Planck_length_squared_m2": LP2,
        "eta_gravity_m2": eta_gravity,
        "potential": (
            "V=-G m1 m2/r [1+3G(m1+m2)/(r c^2) "
            "+(41/(10pi)) G hbar/(r^2 c^3)]"
        ),
        "classical_post_Newtonian_term": "GR_BASELINE_NOT_MTS_RESIDUAL",
        "quantum_potential_fraction_at_52um": potential_r10,
        "quantum_acceleration_fraction_at_52um": acceleration_r10,
        "scope_guard": (
            "This closes the gauge-invariant long-range Newton/scattering "
            "channel from pure graviton and ghost loops. It is not by "
            "itself an off-shell split into d0 and d2, nor a clock or "
            "light-bending kernel."
        ),
        "passed": (
            1.30 < coefficient < 1.31
            and 3.40e-70 < eta_gravity < 3.42e-70
            and acceleration_r10 < 4e-61
        ),
    }


def arena_projections() -> dict[str, Any]:
    matter = matter_nonlocal_position_space()
    gravity = pure_gravity_quantum_tail()
    eta_phi = matter["etaPhi_m2"]
    eta_psi = matter["etaPsi_m2"]
    eta_slip = matter["etaSlip_m2"]
    eta_newton_total = eta_phi + gravity["eta_gravity_m2"]

    r10_potential = eta_newton_total / R10_MIN_M**2
    r10_acceleration = 3 * r10_potential
    r10_context_bound = 1.0e-2
    r10_eta_bound = r10_context_bound * R10_MIN_M**2 / 3

    cassini_slip = eta_slip / CASSINI_IMPACT_M**2
    cassini_lensing_ratio = (eta_phi + eta_psi) / CASSINI_IMPACT_M**2
    cassini_gamma_equivalent = 2 * cassini_lensing_ratio
    cassini_gamma_bound = 2.3e-5
    cassini_eta_lensing_bound = (
        cassini_gamma_bound * CASSINI_IMPACT_M**2 / 2
    )

    clock_geometry = (
        1 / R_EARTH_M**2
        + 1 / (R_EARTH_M * R_GALILEO_M)
        + 1 / R_GALILEO_M**2
    )
    clock_alpha = eta_phi * clock_geometry
    clock_bound = 2.48e-5
    clock_eta_phi_bound = clock_bound / clock_geometry

    mercury_precession_rad_orbit = (
        6
        * math.pi
        * eta_newton_total
        / (MERCURY_A_M**2 * (1 - MERCURY_E**2) ** 2)
    )
    mercury_orbits_century = DAYS_PER_CENTURY / MERCURY_PERIOD_DAYS
    mercury_precession_arcsec_century = (
        mercury_precession_rad_orbit
        * ARCSEC_PER_RAD
        * mercury_orbits_century
    )
    mercury_bound_arcsec_century = 0.0015
    mercury_arcsec_century_per_eta = (
        6
        * math.pi
        / (MERCURY_A_M**2 * (1 - MERCURY_E**2) ** 2)
        * ARCSEC_PER_RAD
        * mercury_orbits_century
    )
    mercury_eta_bound = (
        mercury_bound_arcsec_century / mercury_arcsec_century_per_eta
    )

    rows = [
        {
            "arena": "R10_52um",
            "observable": "fractional_central_acceleration",
            "prediction_abs": r10_acceleration,
            "bound_abs": r10_context_bound,
            "units": "dimensionless",
            "margin_bound_over_prediction": (
                r10_context_bound / r10_acceleration
            ),
            "projection_status": (
                "POINT_SEPARATION_ENVELOPE; EXACT_TORSION_GEOMETRY_NOT_RUN"
            ),
            "coefficient_combination": "etaNewton_total_m2",
            "coefficient_prediction_m2": eta_newton_total,
            "coefficient_bound_m2": r10_eta_bound,
        },
        {
            "arena": "Cassini_solar_impact",
            "observable": "matter_loop_gamma_equivalent_from_deflection",
            "prediction_abs": cassini_gamma_equivalent,
            "bound_abs": cassini_gamma_bound,
            "units": "dimensionless",
            "margin_bound_over_prediction": (
                cassini_gamma_bound / cassini_gamma_equivalent
            ),
            "projection_status": (
                "MATTER_FORM_FACTOR_PROJECTION; PURE_GRAVITY_LIGHT_KERNEL_OPEN"
            ),
            "coefficient_combination": "etaPhi_m2+etaPsi_m2",
            "coefficient_prediction_m2": eta_phi + eta_psi,
            "coefficient_bound_m2": cassini_eta_lensing_bound,
        },
        {
            "arena": "Galileo_redshift",
            "observable": "fractional_redshift_deviation_alpha",
            "prediction_abs": clock_alpha,
            "bound_abs": clock_bound,
            "units": "dimensionless",
            "margin_bound_over_prediction": clock_bound / clock_alpha,
            "projection_status": (
                "MATTER_METRIC_PHI_PROJECTION; PURE_GRAVITY_CLOCK_KERNEL_OPEN"
            ),
            "coefficient_combination": "etaPhi_m2",
            "coefficient_prediction_m2": eta_phi,
            "coefficient_bound_m2": clock_eta_phi_bound,
        },
        {
            "arena": "Mercury_MESSENGER",
            "observable": "extra_perihelion_precession",
            "prediction_abs": mercury_precession_arcsec_century,
            "bound_abs": mercury_bound_arcsec_century,
            "units": "arcsec_per_century",
            "margin_bound_over_prediction": (
                mercury_bound_arcsec_century
                / mercury_precession_arcsec_century
            ),
            "projection_status": "CENTRAL_POTENTIAL_NONLOCAL_TAIL",
            "coefficient_combination": "etaNewton_total_m2",
            "coefficient_prediction_m2": eta_newton_total,
            "coefficient_bound_m2": mercury_eta_bound,
        },
    ]
    return {
        "etaNewton_total_m2": eta_newton_total,
        "r10_potential_fraction": r10_potential,
        "r10_acceleration_fraction": r10_acceleration,
        "cassini_impact_m": CASSINI_IMPACT_M,
        "cassini_matter_pointwise_slip": cassini_slip,
        "cassini_matter_lensing_fraction": cassini_lensing_ratio,
        "cassini_matter_gamma_equivalent": cassini_gamma_equivalent,
        "clock_alpha": clock_alpha,
        "clock_geometry_m_minus_2": clock_geometry,
        "mercury_precession_rad_per_orbit": mercury_precession_rad_orbit,
        "mercury_precession_arcsec_per_century": (
            mercury_precession_arcsec_century
        ),
        "rows": rows,
        "all_numeric_envelopes_below_bounds": all(
            row["prediction_abs"] < row["bound_abs"] for row in rows
        ),
        "full_local_gr_claim": False,
        "claim_guard": (
            "The R10 r^-3 tail still needs the published apparatus "
            "geometry for a likelihood-level comparison. The pure "
            "gravity 41/(10pi) Newton coefficient does not determine "
            "clock or light propagation without the gauge-invariant "
            "quantum metric/observable kernel."
        ),
        "passed": (
            r10_acceleration < 1e-60
            and cassini_gamma_equivalent < 1e-86
            and clock_alpha < 2e-83
            and mercury_precession_arcsec_century < 5e-82
            and all(row["prediction_abs"] < row["bound_abs"] for row in rows)
        ),
    }


def maxwell_projection() -> dict[str, Any]:
    maxwell_path = (
        POST
        / "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md"
    )
    text = maxwell_path.read_text(encoding="utf-8", errors="replace")
    return {
        "action": (
            "S_EM=-lambda_A/4 integral sqrt(-g) F_mn F^mn "
            "+ integral sqrt(-g) A_m J^m"
        ),
        "field_equation": "nabla_mu(lambda_A F^{mu nu})=J^nu",
        "direct_aR_aC_variation_of_Maxwell_equation": 0,
        "classical_trace_in_four_dimensions": 0,
        "scalar_R2_source_from_free_EM": 0,
        "spin2_source": "traceless_Hilbert_T_EM_nonzero",
        "photon_cone": (
            "the same public metric null cone when RF^2, R_mn F^m_a "
            "F^{na}, and u_mu u_nu F^{mu a}F^nu_a are absent"
        ),
        "Poynting_role": "T_EM_0i stress transport; never a second source",
        "separate_extension_guard": (
            "Checkpoint 4854 flow-constitutive coefficients remain a "
            "separate extension and are not generated by aR or aC."
        ),
        "passed": (
            "Maxwell equations" in text
            and "two photon polarizations" in text
            and "Poynting" in text
            and "double count" in text
        ),
    }


def arbitration() -> dict[str, Any]:
    return {
        "selected_local_branch": "STRICT_RENORMALIZED_EFT",
        "finite_local_R2_C2": (
            "CONTACT_ONLY_BETWEEN_NONOVERLAPPING_SOURCES_AT_FIRST_EFT_ORDER"
        ),
        "r10_yukawa_use": (
            "RESUMMED_DIAGNOSTIC_ONLY; NOT A STRICT_EFT COEFFICIENT BOUND"
        ),
        "nonlocal_matter": "DERIVED_R_MINUS_3_TAIL_AND_ARENA_ENVELOPES",
        "pure_gravity_newton": (
            "PHYSICAL_41_OVER_10PI_LONG_RANGE_TAIL_INSERTED"
        ),
        "maxwell": (
            "EXACT_CLASSICAL_MINIMAL_PROJECTION_CLOSED_AT_THIS_ORDER"
        ),
        "local_gr_promotion": False,
        "promotion_blockers": (
            "source-size contact matching and nonlinear beta remain; "
            "the pure-gravity gauge-invariant clock/light kernels must "
            "replace off-shell H/ghost placeholders"
        ),
        "next_target": (
            "4879-Y5-R2FR-source-size-contact-matching-and-second-order-"
            "beta-completion-plus-gauge-invariant-light-kernel-or-strict-"
            "EFT-local-GR-promotion-gate.md"
        ),
        "passed": True,
    }


def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "projectors": projector_transfer(),
        "strict_eft": strict_eft_contact_branch(),
        "resummed_diagnostic": resummed_quadratic_diagnostic(),
        "matter_nonlocal": matter_nonlocal_position_space(),
        "pure_gravity": pure_gravity_quantum_tail(),
        "arenas": arena_projections(),
        "maxwell": maxwell_projection(),
        "arbitration": arbitration(),
    }
    return {
        "sections": sections,
        "all_checks_pass": all(
            section["passed"] for section in sections.values()
        ),
        "decision": (
            "select strict renormalized EFT; demote local R2/C2 Yukawa "
            "interpretation to a resummed diagnostic; retain calculated "
            "matter and pure-gravity long-range tails; close minimal "
            "Maxwell at this order; advance source-size, beta and "
            "gauge-invariant light/clock completion"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(result(), indent=2, sort_keys=True))
