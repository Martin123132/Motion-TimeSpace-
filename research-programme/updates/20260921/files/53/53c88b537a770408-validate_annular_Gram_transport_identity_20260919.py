from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_live_Gram_defect_transport_20260919 import transport_budget
import contextlib
import json
import numpy as np
import sympy as sp


def main():
    evidence = EvidenceRun('annular-Gram-transport-identity-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False,
            independent_exact_solution_not_a_parent_evolution=True,
            nonzero_path_quadrature_defect_despite_zero_ODE_error=True,
            moving_covector_identity_not_full_nonlinear_adjoint=True)
        instant, epsilon = sp.symbols('t epsilon', real=True)
        coarse = 1+instant
        fine = coarse+epsilon*instant**3
        fine_metric, coarse_metric = 1+instant, sp.Integer(1)
        coarse_momentum = sp.diff(coarse, instant)/coarse_metric
        fine_momentum = sp.diff(fine, instant)/fine_metric
        momentum_rate = fine_metric*(fine_momentum-coarse_momentum)
        configuration_rate = (fine_metric-coarse_metric)*coarse_momentum
        error = fine-coarse
        gradient = fine_metric*(fine+coarse)/2
        geometry = (fine_metric-coarse_metric)*coarse**2/2
        direct = (fine_metric*fine**2-coarse_metric*coarse**2)/2
        evidence.check('nonlinear_quadratic_secant_with_metric', sp.expand(direct-gradient*error-geometry) == 0)
        evidence.check('exact_solution_has_zero_velocity_defect', sp.simplify(sp.diff(error, instant)-momentum_rate-configuration_rate) == 0)
        evidence.check('continuous_force_defect_transport', sp.simplify(sp.diff(direct, instant)
            -gradient*momentum_rate-gradient*configuration_rate-sp.diff(gradient, instant)*error-sp.diff(geometry, instant)) == 0)
        terms = [gradient*momentum_rate, gradient*configuration_rate, sp.diff(gradient, instant)*error, sp.diff(geometry, instant)]
        integrals = [sp.integrate(term.subs(epsilon, sp.Rational(1, 7)), (instant, 0, sp.Rational(1, 3))) for term in terms]
        endpoint = direct.subs({instant:sp.Rational(1, 3), epsilon:sp.Rational(1, 7)})
        evidence.check('exact_integrated_transport', sp.simplify(sum(integrals)-endpoint) == 0)
        evidence.check('dropping_moving_covector_is_detected', integrals[2] != 0)
        evidence.check('dropping_geometry_feedback_is_detected', integrals[1]+integrals[3] != 0)
        before, after, grad_before, grad_after = sp.symbols('e0 e1 g0 g1', real=True)
        evidence.check('discrete_product_rule_exact', sp.expand(grad_after*after-grad_before*before
            -(grad_after+grad_before)*(after-before)/2-(grad_after-grad_before)*(after+before)/2) == 0)
        for intervals in [8, 16, 32]:
            times = np.linspace(0., 1/3, intervals+1)
            error_values = times**3/7
            gradients = (1+times)*(2*(1+times)+error_values)/2
            momentum = 3*times**2/7-times
            configuration = times
            geometry_values = times*(1+times)**2/2
            row = transport_budget(times, error_values[:, None], gradients[:, None],
                momentum[:, None], configuration[:, None], geometry_values, 1)
            row['known_exact_endpoint'] = float(endpoint)
            row['known_ODE_error'] = 0.
            evidence.check(str(intervals)+'_independent_analytic_endpoint', abs(row['endpoint_difference']-float(endpoint)) < 2e-15
                and row['reconstruction_error'] < 2e-15)
            evidence.check(str(intervals)+'_nonzero_quadrature_defect_not_ODE_error', abs(row['signed_terms']['reconstructed_path_quadrature']) > 1e-7)
            evidence.report['cases'].append(row)
        coarse_row, medium_row, fine_row = evidence.report['cases']
        values = [abs(row['signed_terms']['reconstructed_path_quadrature']) for row in [coarse_row, medium_row, fine_row]]
        evidence.check('exact_path_quadrature_refines_second_order', 3.8 < values[0]/values[1] < 4.2 and 3.8 < values[1]/values[2] < 4.2)
        evidence.report.update(exact_integrals=[str(value) for value in integrals], exact_endpoint=str(endpoint))
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), cases=evidence.report['cases'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
