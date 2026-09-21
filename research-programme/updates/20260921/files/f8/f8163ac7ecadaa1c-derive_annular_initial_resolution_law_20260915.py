from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_sparse_live_repaired_20260915 import SparseRepairedLiveSystem
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from annular_repaired_live_geometry_20260915 import material_weight
from annular_cut_initial_data_20260915 import compatible_initial_state
from run_annular_sparse_live_refinement_20260915 import compare
from compare_annular_repaired_live_continuum_v3_20260915 import compare_state
import numpy as np
import sympy as sp


def profile(offset):
    distance = abs(offset)
    fraction = np.clip((distance-.2)/.35, 0., 1.)
    envelope = 1-10*fraction**3+15*fraction**4-6*fraction**5
    first = (-30*fraction**2+60*fraction**3-30*fraction**4)*np.sign(offset)/.35
    second = (-60*fraction+180*fraction**2-120*fraction**3)/.35**2
    return .01*offset*envelope, .01*(envelope+offset*first), .01*(2*first+offset*second)


def integrated(geometry, count=None, order=16):
    points, weights = np.polynomial.legendre.leggauss(order)
    label_points, label_weights = np.polynomial.legendre.leggauss(10)
    total_norm, curvature, spatial_error, temporal_error = 0., 0., 0., 0.
    system = SparseRepairedLiveSystem(count or 17, False, 8, 10)
    base_coordinates, base_rates, unused = compatible_initial_state(system.layer(0., geometry), 0.)
    for label, label_weight in zip(label_points/2, label_weights*material_weight(label_points/2)/2):
        layer = system.layer(label, geometry)
        source = 6.03+.02*label
        coordinates = base_coordinates.copy()
        coordinates[-1] = source
        endpoints = np.concatenate([layer.radii[[0, -1]], source+np.array([-.55, -.2, 0., .2, .55]), geometry.edges])
        if count is not None:
            endpoints = np.concatenate([endpoints, layer.radii])
        endpoints = np.unique(endpoints[(endpoints >= layer.radii[0]) & (endpoints <= layer.radii[-1])])
        lengths = np.diff(endpoints)
        radius = (endpoints[:-1, None]+lengths[:, None]*(points+1)/2).ravel()
        quadrature = (lengths[:, None]*weights/2).ravel()
        lapse, root = geometry.metric(radius)
        kinetic, stiffness = radius**2/(lapse*root), radius**2*lapse*root
        unused, exact_gradient, second_derivative = profile(radius-source)
        exact_temporal = -.03*exact_gradient
        total_norm += label_weight*np.dot(quadrature, kinetic*exact_temporal**2+stiffness*exact_gradient**2)
        curvature += label_weight*np.dot(quadrature, stiffness*second_derivative**2)
        if count is not None:
            cell, shape, radial, motion = layer.features(radius, source)
            scalar = np.column_stack([coordinates[cell], coordinates[cell+1]])
            rate = np.column_stack([base_rates[cell], base_rates[cell+1]])
            gradient = np.sum(radial*scalar, axis=1)
            temporal = np.sum(shape*rate, axis=1)+.03*np.sum(motion*scalar, axis=1)
            spatial_error += label_weight*np.dot(quadrature, stiffness*(gradient-exact_gradient)**2)
            temporal_error += label_weight*np.dot(quadrature, kinetic*(temporal-exact_temporal)**2)
    return dict(norm=float(total_norm), curvature=float(curvature), coefficient=float(np.sqrt(curvature/(12*total_norm))),
                relative_error=float(np.sqrt((spatial_error+temporal_error)/total_norm)),
                spatial_squared_error=float(spatial_error), temporal_squared_error=float(temporal_error))


def main():
    evidence = EvidenceRun('annular-initial-resolution-law-attempt01', __file__)
    try:
        coordinate, spacing, slope = sp.symbols('xi h a', real=True)
        leading = sp.integrate((slope*coordinate)**2, (coordinate, -spacing/2, spacing/2))
        evidence.check('cell_average_derivative_variance_coefficient', sp.simplify(leading-slope**2*spacing**3/12) == 0)
        position = sp.symbols('x', positive=True)
        fraction = (position-sp.Rational(1, 5))/sp.Rational(7, 20)
        envelope = 1-10*fraction**3+15*fraction**4-6*fraction**5
        expected = sp.Rational(1, 100)*(2*sp.diff(envelope, position)+position*sp.diff(envelope, position, 2))
        evidence.check('preparation_second_derivative', sp.simplify(sp.diff(position*envelope/100, position, 2)-expected) == 0)
        path = evidence.output.parent/'annular-live-continuum-degree512-attempt01/degree512.npz'
        evidence.own(path)
        saved = np.load(path)
        oracle = BarycentricLiveContinuum(512, 8, 18, radial_spacing=.025, label_order=12)
        geometry = oracle.solve(saved['states'][0])
        baseline, control = integrated(geometry), integrated(geometry, order=24)
        evidence.check('leading_coefficient_independent_quadrature', abs(baseline['coefficient']-control['coefficient']) < 1e-10, [baseline, control])
        baseline['asymptotic_half_percent_maximum_spacing'] = .005/baseline['coefficient']
        baseline['asymptotic_half_percent_minimum_count'] = int(np.ceil(1+1.6*baseline['coefficient']/.005))
        evidence.report['analytic_leading_law'] = baseline
        for count in [33, 65, 129, 253, 513, 1025, 2049]:
            row = integrated(geometry, count)
            spacing = 1.6/(count-1)
            row.update(count=count, spacing=spacing, asymptotic_prediction=spacing*baseline['coefficient'])
            row['coefficient_relative_difference'] = abs(row['relative_error']/spacing/baseline['coefficient']-1)
            row['strict_initial_half_percent_gate'] = row['relative_error'] < .005
            evidence.report['cases'].append(row)
            evidence.save()
            print(row, flush=True)
        evidence.check('initial_error_over_h_reaches_derived_coefficient', evidence.report['cases'][-1]['coefficient_relative_difference'] < 2e-5, evidence.report['cases'][-1])
        evidence.check('temporal_interpolation_is_subleading', evidence.report['cases'][-1]['temporal_squared_error'] < 1e-4*evidence.report['cases'][-1]['spatial_squared_error'])
        evidence.check('low_grid_failure_and_1025_initial_pass_are_explicit', not evidence.report['cases'][3]['strict_initial_half_percent_gate'] and evidence.report['cases'][5]['strict_initial_half_percent_gate'])
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            system = SparseRepairedLiveSystem(65, gram, 8, 10)
            path = evidence.output.parent/'annular-repaired-live-evolution-attempt01'/f'{branch}-65-main.npz'
            evidence.own(path)
            state = np.load(path)['state'][:, -1]
            coordinates, momenta = state[:2*9*66].reshape(2, 9, 66)
            rates, actual_geometry = system.solve(coordinates, momenta)
            target_geometry = oracle.solve(saved['states'][-1])
            sparse = compare(system, coordinates, rates, state[2*9*66:], actual_geometry, oracle, target_geometry)
            dense = compare_state(system, coordinates, momenta, state[2*9*66:], oracle, saved['states'][-1])
            error = max(abs(sparse[name]-dense[name]) for name in dense)
            evidence.check(branch+'_same_physical_norm_as_previous_dense_comparator', error < 1e-12, error)
        evidence.report.update(initial_H1_error_leading_coefficient_derived=True,
            initial_profile_not_changed=True, initial_target_analytic_profile_not_spectral_interpolation=True,
            same_continuum_metric_norm_used_for_both_branches=True,
            initial_accuracy_does_not_prove_evolving_accuracy=True,
            asymptotic_count_not_a_rigorous_sufficient_resolution_bound=True,
            full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
