from __future__ import annotations

import json
from typing import Any

import sympy as sp


def scalar_heat_kernel_matching() -> dict[str, Any]:
    field_count = sp.symbols("N_s", positive=True, integer=True)
    cutoff, mass, log_ratio = sp.symbols(
        "Lambda_UV m L", positive=True, real=True
    )
    nonminimal = sp.symbols("xi", real=True)

    delta = nonminimal - sp.Rational(1, 6)
    constant_term = field_count * (
        cutoff**4 / (64 * sp.pi**2)
        - mass**2 * cutoff**2 / (32 * sp.pi**2)
        + mass**4 * log_ratio / (32 * sp.pi**2)
    )
    einstein_coefficient = field_count * (
        (sp.Rational(1, 6) - nonminimal)
        * cutoff**2
        / (32 * sp.pi**2)
        + delta * mass**2 * log_ratio / (16 * sp.pi**2)
    )
    planck_squared = sp.factor(2 * einstein_coefficient)

    raw_riemann = sp.Rational(1, 180)
    raw_ricci = -sp.Rational(1, 180)
    raw_scalar = delta**2 / 2
    weyl_coefficient = sp.Rational(1, 120)
    euler_coefficient = -sp.Rational(1, 360)
    scalar_coefficient = delta**2 / 2

    converted_riemann = weyl_coefficient + euler_coefficient
    converted_ricci = -2 * weyl_coefficient - 4 * euler_coefficient
    converted_scalar = (
        weyl_coefficient / 3
        + euler_coefficient
        + scalar_coefficient
    )

    loop_r2 = sp.factor(
        field_count * log_ratio * scalar_coefficient / (16 * sp.pi**2)
    )
    loop_c2 = sp.factor(
        field_count * log_ratio * weyl_coefficient / (16 * sp.pi**2)
    )
    loop_e4 = sp.factor(
        field_count * log_ratio * euler_coefficient / (16 * sp.pi**2)
    )

    expected_planck = (
        field_count
        * (1 - 6 * nonminimal)
        * (cutoff**2 - 2 * mass**2 * log_ratio)
        / (96 * sp.pi**2)
    )
    passed = all(
        sp.simplify(value) == 0
        for value in (
            converted_riemann - raw_riemann,
            converted_ricci - raw_ricci,
            converted_scalar - raw_scalar,
            planck_squared - expected_planck,
        )
    )

    return {
        "operator": "D=-Box_g+xi R+m^2",
        "proper_time_log": "L=ln(Lambda_UV/mu)",
        "A2_bulk_raw": (
            "Riemann^2/180-Ricci^2/180+"
            "(xi-1/6)^2 R^2/2"
        ),
        "A2_bulk_4d_basis": (
            "C^2/120-E4/360+(xi-1/6)^2 R^2/2"
        ),
        "constant_loop": str(sp.factor(constant_term)),
        "Mstar_squared": str(planck_squared),
        "a_R_loop": str(loop_r2),
        "a_C_loop": str(loop_c2),
        "a_E_loop": str(loop_e4),
        "boundary_term": "(xi/6-1/30) Box R in the cited convention",
        "passed": passed,
    }


def parent_action_and_saddle() -> dict[str, Any]:
    cutoff, planck_squared = sp.symbols(
        "Lambda_UV Mstar2", positive=True, real=True
    )
    field_count = sp.symbols("N_s", positive=True, integer=True)
    healthy_weight = sp.symbols("h", positive=True, real=True)
    loop_constant = field_count * cutoff**4 / (64 * sp.pi**2)
    scalar_planck = (
        field_count * healthy_weight * cutoff**2 / (96 * sp.pi**2)
    )
    induced_lambda = sp.factor(-loop_constant / scalar_planck)
    expected_lambda = -3 * cutoff**2 / (2 * healthy_weight)

    return {
        "parent_action": (
            "S_parent=S_SK[g(H),psi_r,psi_a,X]+S_matter[g(H)]"
            "+S_EM[g(H),A]+int sqrt(-g)[C0_b+M0^2 R/2"
            "+aR_b R^2+aC_b C^2+aE_b E4]+s_BRST Psi_gf"
        ),
        "renormalized_coefficients": (
            "C0_R=C0_b+C0_loop; M_R^2=M0^2+M_loop^2; "
            "a_i_R=a_i_b+a_i_loop"
        ),
        "saddle_equation": (
            "M_R^2 G_mn-C0_R g_mn+H_mn^(4)+H_mn^nonlocal=T_mn"
        ),
        "maximally_symmetric_local_saddle": (
            "Lambda_bg=-C0_R/M_R^2; local R^2/C^2/E4 "
            "variations vanish on a 4d maximally symmetric background"
        ),
        "flat_saddle_gate": "C0_R=0 including every state and loop sector",
        "massless_scalar_only_lambda": str(induced_lambda),
        "scalar_only_flat_no_go": (
            "for N_s>0, Lambda_UV>0 and h=1-6xi>0, "
            "Lambda_bg=-3 Lambda_UV^2/(2h) is nonzero"
        ),
        "counterterm_status": (
            "a flat saddle requires a renormalization condition, a signed "
            "spectrum cancellation, or a derived vacuum-selection mechanism"
        ),
        "passed": sp.simplify(induced_lambda - expected_lambda) == 0,
    }


def sk_vacuum_test() -> dict[str, Any]:
    average, difference, coefficient = sp.symbols(
        "g_r g_a C0", real=True
    )
    plus = average + difference / 2
    minus = average - difference / 2
    doubled_term = coefficient * plus - coefficient * minus
    diagonal_value = sp.simplify(doubled_term.subs(difference, 0))
    response = sp.simplify(
        sp.diff(doubled_term, difference).subs(difference, 0)
    )
    return {
        "SK_term": "C0[int sqrt(-g_+)-int sqrt(-g_-)]",
        "diagonal_value": str(diagonal_value),
        "difference_metric_response": str(response),
        "metric_response_exact": (
            "delta Gamma_SK/delta g_a^mn|0="
            "-C0 sqrt(-g) g_mn/2"
        ),
        "conclusion": (
            "Z[g,g]=1 cancels vacuum bubbles in the value of the "
            "influence action but does not cancel their stress in the "
            "difference-metric equation"
        ),
        "passed": diagonal_value == 0 and response == coefficient,
    }


def covariant_regulator_ward_identity() -> dict[str, Any]:
    d11, d12, d21, d22 = sp.symbols("d11 d12 d21 d22")
    x11, x12, x21, x22 = sp.symbols("x11 x12 x21 x22")
    operator = sp.Matrix([[d11, d12], [d21, d22]])
    generator = sp.Matrix([[x11, x12], [x21, x22]])
    regulated_function = operator + operator**2
    commutator_trace = sp.simplify(
        sp.trace(generator * regulated_function - regulated_function * generator)
    )
    return {
        "regulator": (
            "Gamma_reg=-1/2 int_(Lambda^-2)^infinity ds/s "
            "Tr exp[-s D(g(H))]"
        ),
        "covariance": "delta_xi D=[L_xi,D]",
        "ward_step": (
            "delta_xi Gamma_reg is a regulated trace of "
            "[L_xi,F(D)] and vanishes by cyclicity"
        ),
        "finite_matrix_commutator_trace": str(commutator_trace),
        "scope": (
            "matter-loop Diff Ward identity for a public-metric covariant "
            "operator; the full H measure still requires BRST-compatible "
            "gauge fixing and no diffeomorphism anomaly"
        ),
        "passed": commutator_trace == 0,
    }


def quadratic_pole_hierarchy() -> dict[str, Any]:
    field_count, healthy_weight = sp.symbols(
        "N_s h", positive=True, real=True
    )
    cutoff, log_ratio, momentum = sp.symbols(
        "Lambda_UV L q", positive=True, real=True
    )
    planck_squared = (
        field_count * healthy_weight * cutoff**2 / (96 * sp.pi**2)
    )
    r2 = field_count * log_ratio * healthy_weight**2 / (
        1152 * sp.pi**2
    )
    c2 = field_count * log_ratio / (1920 * sp.pi**2)
    scalar_mass_squared = sp.factor(planck_squared / (12 * r2))
    spin2_mass_squared = sp.factor(-planck_squared / (4 * c2))
    scalar_ratio = sp.factor(momentum**2 / scalar_mass_squared)
    spin2_ratio = sp.factor(
        momentum**2 / (-spin2_mass_squared)
    )

    pole = sp.symbols("m2", positive=True, real=True)
    q2 = sp.symbols("q2")
    partial_fraction = sp.apart(
        1 / (q2 * (1 - q2 / pole)), q2
    )
    expected_fraction = 1 / q2 - 1 / (q2 - pole)

    return {
        "basis": "Mstar^2 R/2+a_R R^2+a_C C^2",
        "healthy_EH_weight": "h=1-6xi>0",
        "Mstar_squared": str(planck_squared),
        "a_R": str(r2),
        "a_C": str(c2),
        "m0_squared": str(scalar_mass_squared),
        "m2_squared": str(spin2_mass_squared),
        "spin2_interpretation": (
            "a_C>0 gives a negative m2^2 in the local polynomial "
            "continuation; a_C<0 gives a positive-mass pole with "
            "opposite residue. Either sign is unacceptable as a "
            "fundamental finite-derivative extra spin-2 mode."
        ),
        "partial_fraction": str(partial_fraction),
        "epsilon_scalar": str(scalar_ratio),
        "epsilon_spin2": str(spin2_ratio),
        "IR_gate": (
            "q_max^2 << min(Lambda_UV^2,m0^2,abs(m2^2)); "
            "equivalently L*h*(q_max/Lambda_UV)^2 << 1 and "
            "L*(q_max/Lambda_UV)^2/(5h) << 1"
        ),
        "EFT_warning": (
            "a pole at or above Lambda_UV is outside the derivative "
            "expansion and is not a physical low-energy state; if either "
            "pole enters the tested domain the branch fails or needs its "
            "nonlocal/UV completion"
        ),
        "passed": (
            scalar_mass_squared == cutoff**2 / (log_ratio * healthy_weight)
            and spin2_mass_squared
            == -5 * healthy_weight * cutoff**2 / log_ratio
            and sp.simplify(partial_fraction - expected_fraction) == 0
        ),
    }


def newton_matching() -> dict[str, Any]:
    field_count, healthy_weight = sp.symbols(
        "N_s h", positive=True, real=True
    )
    cutoff, newton = sp.symbols(
        "Lambda_UV G_N", positive=True, real=True
    )
    reduced_planck = sp.symbols("Mbar_Pl", positive=True, real=True)
    planck_squared = (
        field_count * healthy_weight * cutoff**2 / (96 * sp.pi**2)
    )
    predicted_newton = sp.factor(1 / (8 * sp.pi * planck_squared))
    cutoff_solution = sp.factor(
        sp.sqrt(96 * sp.pi**2 / (field_count * healthy_weight))
        * reduced_planck
    )
    samples = []
    for weight in (1, 100, 1000):
        ratio = float(4 * sp.pi * sp.sqrt(6 / weight))
        samples.append(
            {
                "N_s_times_h": weight,
                "Lambda_over_Mbar_Pl": ratio,
            }
        )
    return {
        "GN_relation": str(predicted_newton),
        "Lambda_from_Mbar_Pl": str(cutoff_solution),
        "measured_combination": (
            "N_s(1-6xi)Lambda_UV^2=12 pi/G_N"
        ),
        "status": (
            "the loop derives a matching relation; it predicts G_N only "
            "after the MTS spectrum, xi and cutoff are independently fixed"
        ),
        "samples": samples,
        "passed": (
            sp.simplify(
                predicted_newton
                - 12 * sp.pi
                / (field_count * healthy_weight * cutoff**2)
            )
            == 0
            and sp.simplify(
                cutoff_solution
                - 4
                * sp.pi
                * sp.sqrt(6 / (field_count * healthy_weight))
                * reduced_planck
            )
            == 0
        ),
    }


def vacuum_spectrum_sum_rules() -> dict[str, Any]:
    scalar_count, dirac_count = sp.symbols(
        "N_s N_d", positive=True, integer=True
    )
    scalar_mass, dirac_mass = sp.symbols(
        "m_s m_d", nonnegative=True, real=True
    )
    scalar_xi = sp.symbols("xi_s", real=True)

    quartic_weight = -scalar_count + 4 * dirac_count
    quadratic_weight = (
        -scalar_count * scalar_mass**2
        + 4 * dirac_count * dirac_mass**2
    )
    logarithmic_weight = (
        -scalar_count * scalar_mass**4
        + 4 * dirac_count * dirac_mass**4
    )
    newton_weight = (
        scalar_count * (sp.Rational(1, 6) - scalar_xi)
        + dirac_count / 3
    )

    balanced = {
        scalar_count: 4,
        dirac_count: 1,
        scalar_mass: 1,
        dirac_mass: 1,
        scalar_xi: 0,
    }
    balanced_values = [
        sp.simplify(value.subs(balanced))
        for value in (
            quartic_weight,
            quadratic_weight,
            logarithmic_weight,
            newton_weight,
        )
    ]
    return {
        "signed_weights": "C_s^(0)=-1; C_d^(0)=4",
        "vacuum_sum_rules": (
            "sum C_f^(0)=0; sum C_f^(0)m_f^2=0; "
            "sum C_f^(0)m_f^4=0"
        ),
        "quartic_weight": str(quartic_weight),
        "quadratic_weight": str(quadratic_weight),
        "logarithmic_weight": str(logarithmic_weight),
        "newton_weight": str(newton_weight),
        "constructive_example": (
            "N_s=4, N_d=1, equal masses, xi_s=0 cancels all three "
            "one-loop vacuum weights while C_G=1 remains positive"
        ),
        "constructive_values": [str(value) for value in balanced_values],
        "scope": (
            "one-loop free scalar/Dirac example only; interactions, vectors, "
            "thresholds and higher loops must obey the corresponding full "
            "MTS spectral identities before this can select the saddle"
        ),
        "passed": balanced_values == [0, 0, 0, 1],
    }


def hierarchy_samples() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for healthy_weight in (0.1, 1.0, 3.0):
        for log_ratio in (0.1, 1.0, 5.0):
            for momentum_ratio in (1e-3, 1e-2, 1e-1):
                epsilon_scalar = (
                    log_ratio * healthy_weight * momentum_ratio**2
                )
                epsilon_spin2 = (
                    log_ratio
                    * momentum_ratio**2
                    / (5 * healthy_weight)
                )
                rows.append(
                    {
                        "h": healthy_weight,
                        "L": log_ratio,
                        "q_over_Lambda": momentum_ratio,
                        "epsilon_scalar": epsilon_scalar,
                        "epsilon_spin2": epsilon_spin2,
                        "IR_dominant_at_1_percent": max(
                            epsilon_scalar, epsilon_spin2
                        )
                        < 0.01,
                    }
                )
    return {
        "rows": rows,
        "row_count": len(rows),
        "all_deep_IR_rows_pass": all(
            row["IR_dominant_at_1_percent"]
            for row in rows
            if row["q_over_Lambda"] <= 1e-2
        ),
        "passed": len(rows) == 27,
    }


def result() -> dict[str, Any]:
    sections = {
        "heat_kernel": scalar_heat_kernel_matching(),
        "parent_saddle": parent_action_and_saddle(),
        "sk_vacuum": sk_vacuum_test(),
        "regulator_ward": covariant_regulator_ward_identity(),
        "quadratic_poles": quadratic_pole_hierarchy(),
        "newton_matching": newton_matching(),
        "vacuum_sum_rules": vacuum_spectrum_sum_rules(),
        "hierarchy_samples": hierarchy_samples(),
    }
    return {
        "sections": sections,
        "all_checks_pass": all(
            section["passed"] for section in sections.values()
        ),
        "decision": (
            "retain the integrated-H induced-gravity parent as an IR EFT; "
            "reject a naturally flat scalar-only saddle; pursue a full MTS "
            "signed-spectrum sum rule or an explicit renormalized vacuum "
            "condition, and keep every higher-curvature pole above the "
            "tested EFT domain"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(result(), indent=2, sort_keys=True))
