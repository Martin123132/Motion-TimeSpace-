from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from run_annular_source_fitted_crossing_20260915 import profile, initial
import numpy as np
import sympy as sp


def third_derivative(radius):
    offset = np.asarray(radius)-6.03
    selected = (abs(offset) > .2) & (abs(offset) < .55)
    fraction = (abs(offset[selected])-.2)/.35
    second_envelope = (-60*fraction+180*fraction**2-120*fraction**3)/.35**2
    third_envelope = (-60+360*fraction-360*fraction**2)*np.sign(offset[selected])/.35**3
    result = np.zeros_like(offset)
    result[selected] = .01*(3*second_envelope+offset[selected]*third_envelope)
    return result


def quadrature(edges, order=16):
    points, weights = np.polynomial.legendre.leggauss(order)
    radius = ((edges[1:, None]+edges[:-1, None])/2+np.diff(edges)[:, None]*points/2).ravel()
    measure = (np.diff(edges)[:, None]*weights/2).ravel()
    return radius, measure


def main():
    evidence = EvidenceRun('annular-quadratic-initial-error-law-attempt01', __file__)
    try:
        coordinate = sp.symbols('xi')
        cubic_error = coordinate*(coordinate-sp.Rational(1, 2))*(coordinate-1)/6
        constant = sp.integrate(sp.diff(cubic_error, coordinate)**2, (coordinate, 0, 1))
        evidence.check('quadratic_derivative_error_kernel_exact', constant == sp.Rational(1, 720), str(constant))
        radius, measure = quadrature(np.array([5.2, 5.48, 5.83, 6.03, 6.23, 6.58, 6.8]), 48)
        unused, gradient = profile(radius)
        mesh_factor = np.where(radius < 6.03, (radius-5.2)/.83, (6.8-radius)/.77)
        numerator = np.dot(measure*radius**2*(1+.06**2*mesh_factor**2), third_derivative(radius)**2)
        denominator = np.dot(measure*radius**2*(1+.06**2), gradient**2)
        coefficient = float(np.sqrt(numerator/(720*denominator)))
        for count in [33, 65, 129, 257, 513]:
            system = QuadraticSourceFittedAction(count, False, background_mass=0.)
            coordinates, rates = np.split(initial(system)[:-1], 2)
            edges = np.unique(np.concatenate([system.edges, [5.48, 5.83, 6.23, 6.58]]))
            radius, measure = quadrature(edges)
            unused, unused2, temporal, numerical_gradient = system.sample(radius, coordinates, rates)
            unused, exact_gradient = profile(radius)
            error = float(np.sqrt(np.dot(measure*radius**2, (temporal+.06*exact_gradient)**2+(numerical_gradient-exact_gradient)**2)/denominator))
            predicted = coefficient*system.gram_spacing**2
            evidence.report['cases'].append(dict(base_count=count, scalar_dofs=system.count, exact_initial_field_error=error,
                leading_prediction=predicted, coefficient_ratio=error/predicted))
        evidence.check('derived_initial_coefficient_matches_refinement', abs(evidence.report['cases'][-1]['coefficient_ratio']-1) < .01,
                       evidence.report['cases'][-1])
        order = np.log2(evidence.report['cases'][-2]['exact_initial_field_error']/evidence.report['cases'][-1]['exact_initial_field_error'])
        evidence.check('second_order_initial_energy_norm', 1.9 < order < 2.1, float(order))
        evidence.report.update(scope='Initial interpolation error for the original flat crossing profile, not an evolving force-error theorem.',
            leading_coefficient=coefficient, law='E_initial=h_base^2*K+o(h_base^2); K^2=integral R^2(1+k^2 V0^2)(f_third)^2/[720 integral R^2(1+V0^2)(f_prime)^2]',
            estimated_base_nodes_for_half_percent=float(1+1.6*np.sqrt(coefficient/.005)),
            coefficient_derived_from_profile_not_fitted=True, initial_error_does_not_certify_evolving_accuracy=True,
            all_original_vertex_Gram_rows_retained=True, live_quadratic_geometry_qualified=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
