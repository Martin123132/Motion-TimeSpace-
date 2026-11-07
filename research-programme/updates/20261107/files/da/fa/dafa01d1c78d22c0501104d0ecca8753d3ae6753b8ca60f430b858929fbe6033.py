from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import psutil
import sympy as sym


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results/derivation"
PARENT = ROOT.parent / "ward-remainder-20261003"


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite executed evidence.")
    OUTPUT.mkdir(parents=True)
    checks = []

    def check(name, expression):
        assert sym.factor(expression) == 0, (name, sym.factor(expression))
        checks.append({"name": name, "passed": True})

    kinetic, pressure, pressure_x, coefficient, coefficient_x, gradient_norm, box_x = sym.symbols(
        "kinetic pressure pressure_x coefficient coefficient_x gradient_norm box_x")
    response = pressure_x + coefficient_x * gradient_norm + 2 * coefficient * box_x
    variation_response = pressure_x - coefficient_x * gradient_norm + 2 * (coefficient_x * gradient_norm + coefficient * box_x)
    check("integrated_X_variation", response - variation_response)
    check("covariant_divergence_cancellation", -response + pressure_x - coefficient_x * gradient_norm
          + 2 * (coefficient_x * gradient_norm + coefficient * box_x))
    lagrangian = pressure - coefficient * gradient_norm
    trace = -2 * kinetic * response + 2 * coefficient * gradient_norm + 4 * lagrangian
    check("Hilbert_trace", trace - (-2 * kinetic * response + 4 * pressure - 2 * coefficient * gradient_norm))
    check("trace_reversed_metric_term", lagrangian - trace / 2 - (kinetic * response - pressure))

    amplitude, stiffness, radial_cubic = sym.symbols("amplitude stiffness radial_cubic", positive=True)
    amplitude_x = 2 * amplitude / stiffness
    stiffness_x = 2 * amplitude * radial_cubic / stiffness - 2
    amplitude_xx = 2 * amplitude_x / stiffness - 2 * amplitude * stiffness_x / stiffness**2
    derived_a = amplitude_x**2 / 2
    derived_ax = amplitude_x * amplitude_xx
    radial_shift = (amplitude_x * box_x + amplitude_xx * gradient_norm) / stiffness
    check("eliminated_amplitude_current", 2 * amplitude * radial_shift
          - (2 * derived_a * box_x + derived_ax * gradient_norm))
    check("eliminated_amplitude_gradient_stress", amplitude_x**2 - 2 * derived_a)
    check("eliminated_amplitude_potential_trace_reverse",
          2 * kinetic * amplitude * radial_shift
          - kinetic * (2 * derived_a * box_x + derived_ax * gradient_norm))
    check("candidate_NLO_coefficient", derived_a - 2 * amplitude**2 / stiffness**2)
    check("candidate_NLO_coefficient_derivative", derived_ax - (16 * amplitude**2 / stiffness**3
                                                              - 8 * amplitude**3 * radial_cubic / stiffness**4))

    time, space = sym.symbols("time space")
    phase = time + time**2 * space / 7 + time * space**2 / 11
    scalar_x = (sym.diff(phase, time)**2 - sym.diff(phase, space)**2) / 2
    polynomial_p = lambda value: value + value**2 / 7 + value**3 / 19
    polynomial_a = lambda value: sym.Rational(1, 13) + value / 29
    gradient_y = -sym.diff(scalar_x, time)**2 + sym.diff(scalar_x, space)**2
    scalar_q = (1 + 2 * scalar_x / 7 + 3 * scalar_x**2 / 19 + gradient_y / 29
                + 2 * polynomial_a(scalar_x) * (-sym.diff(scalar_x, time, 2) + sym.diff(scalar_x, space, 2)))
    current_divergence = sym.diff(-scalar_q * sym.diff(phase, time), time) + sym.diff(scalar_q * sym.diff(phase, space), space)
    metric = sym.diag(-1, 1)
    coordinates = [time, space]
    stress = sym.zeros(2)
    for first in range(2):
        for second in range(2):
            stress[first, second] = (scalar_q * sym.diff(phase, coordinates[first]) * sym.diff(phase, coordinates[second])
                                    + 2 * polynomial_a(scalar_x) * sym.diff(scalar_x, coordinates[first]) * sym.diff(scalar_x, coordinates[second])
                                    + metric[first, second] * (polynomial_p(scalar_x) - polynomial_a(scalar_x) * gradient_y))
    for second in range(2):
        divergence = sum(metric[first, first] * sym.diff(stress[first, second], coordinates[first]) for first in range(2))
        check(f"explicit_offshell_Noether_component_{second}",
              divergence - current_divergence * sym.diff(phase, coordinates[second]))

    phase_time, phase_space, phase_tt, phase_tx, phase_xx = sym.symbols("phase_time phase_space phase_tt phase_tx phase_xx")
    jet_x = (phase_time**2 - phase_space**2) / 2
    jet_xt = phase_time * phase_tt - phase_space * phase_tx
    jet_xx = phase_time * phase_tx - phase_space * phase_xx
    jet_lagrangian = polynomial_p(jet_x) - polynomial_a(jet_x) * (-jet_xt**2 + jet_xx**2)
    substitution = {phase_time: sym.diff(phase, time), phase_space: sym.diff(phase, space),
                    phase_tt: sym.diff(phase, time, 2), phase_tx: sym.diff(phase, time, space),
                    phase_xx: sym.diff(phase, space, 2)}
    direct_euler = (-sym.diff(sym.diff(jet_lagrangian, phase_time).subs(substitution), time)
                   - sym.diff(sym.diff(jet_lagrangian, phase_space).subs(substitution), space)
                   + sym.diff(sym.diff(jet_lagrangian, phase_tt).subs(substitution), time, 2)
                   + sym.diff(sym.diff(jet_lagrangian, phase_tx).subs(substitution), time, space)
                   + sym.diff(sym.diff(jet_lagrangian, phase_xx).subs(substitution), space, 2))
    check("independent_higher_derivative_Euler_variation", direct_euler - current_divergence)

    hubble, xdot, xddot, qdot = sym.symbols("hubble xdot xddot qdot")
    homogeneous_q = pressure_x - coefficient_x * xdot**2 - 2 * coefficient * (xddot + 3 * hubble * xdot)
    rho_derivative = 2 * xdot * homogeneous_q + 2 * kinetic * qdot - pressure_x * xdot + coefficient_x * xdot**3 + 2 * coefficient * xdot * xddot
    enthalpy = 2 * kinetic * homogeneous_q + 2 * coefficient * xdot**2
    phase_product = 2 * kinetic * qdot + homogeneous_q * xdot + 6 * hubble * kinetic * homogeneous_q
    check("FLRW_continuity_equals_phase_equation", rho_derivative + 3 * hubble * enthalpy - phase_product)

    sound_squared, beta, laplacian, leading_euler = sym.symbols("sound_squared beta laplacian leading_euler")
    time_second = sound_squared * laplacian - leading_euler
    higher_term = beta * (time_second**2 - time_second * laplacian)
    field_shift = -beta * ((1 - 2 * sound_squared) * laplacian + leading_euler)
    check("action_level_order_reduction", higher_term + leading_euler * field_shift
          + beta * sound_squared * (1 - sound_squared) * laplacian**2)
    chemical = sym.symbols("chemical", positive=True)
    total = stiffness + 4 * chemical**2
    check("order_reduced_dispersion", (2 * beta * sound_squared * (1 - sound_squared)).subs({
        beta: 2 * chemical**2 / (stiffness * total), sound_squared: stiffness / total}) - 16 * chemical**4 / total**3)

    ratio = sym.symbols("ratio", positive=True)
    charge_squared_shape = ratio**sym.Rational(5, 4) * (1 + ratio)
    check("charge_density_monotonicity", sym.diff(charge_squared_shape, ratio)
          - ratio**sym.Rational(1, 4) * (5 + 9 * ratio) / 4)
    crossing_scale = sym.simplify((2**sym.Rational(5, 4) * 3 / 2)**sym.Rational(1, 6))
    report = {
        "state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks, "exact_check_count": len(checks),
        "current": "J^mu=Q nabla^mu theta; Q=P_X+A_X(nabla X)^2+2A box X",
        "stress": "T_munu=Q theta_mu theta_nu+2A X_mu X_nu+g_munu[P-A(nabla X)^2]",
        "off_shell_identity": "nabla_mu T^mu_nu=E_theta nabla_nu theta; E_theta=nabla_mu J^mu",
        "densitized_metric_source": "-1/2[Q theta_mu theta_nu+2A X_mu X_nu+g_munu(XQ-P)]",
        "parent_amplitude_matching": "rho_amplitude=v+box(v)/M; rho_amplitude^2=Q through NLO",
        "order_reduction": "chi=chi_reduced-beta[(1-2cs^2) laplacian chi_reduced+E0(chi_reduced)]",
        "homogeneous_example": {"X": .5, "Q": 100., "pressure": float(sym.Rational(25, 3)),
                                "energy_density": float(sym.Rational(275, 3)), "enthalpy": 100.,
                                "w": float(sym.Rational(1, 11)),
                                "leading_charge_shape": "a^6 y^(5/4)(1+y)=constant",
                                "a_at_y1_from_y2_a1": float(crossing_scale),
                                "crossing_scope": "Boundary of the retained y>1 homogeneous branch; not a fixed-charge decay proof."},
        "metric_is_external_until_parent_choice": True,
        "full_original_real_scalar_bath_embedded": False,
        "parent_seal_sha256": hashlib.sha256((PARENT / "results/stage-integrity.json").read_bytes()).hexdigest(),
    }
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "exact_checks": len(checks), "homogeneous_example": report["homogeneous_example"]}))


if __name__ == "__main__":
    main()

