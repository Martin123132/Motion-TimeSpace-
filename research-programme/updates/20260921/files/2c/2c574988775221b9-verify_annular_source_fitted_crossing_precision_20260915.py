from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_source_fitted_action_20260915 import SourceFittedAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from run_annular_source_fitted_crossing_20260915 import initial, evolve, field_comparison
import json
import numpy as np


def oracle_difference(first, first_state, second, second_state, order):
    edges = np.unique(np.concatenate([np.linspace(5.2, 6.8, 257), [first_state[-3], second_state[-3]]]))
    points, weights = np.polynomial.legendre.leggauss(order)
    radius = ((edges[:-1, None]+edges[1:, None])/2+np.diff(edges)[:, None]*points/2).ravel()
    measure = (np.diff(edges)[:, None]*weights/2).ravel()*radius**2
    first_time, first_gradient = first.sample(first_state, radius)
    second_time, second_gradient = second.sample(second_state, radius)
    squared = np.dot(measure, (first_time-second_time)**2+(first_gradient-second_gradient)**2)
    norm = np.dot(measure, second_time**2+second_gradient**2)
    return float(np.sqrt(squared/norm))


def finite_shape_force(system, instant, coordinates, rates):
    acceleration = system.acceleration(instant, coordinates, rates)
    data = system.evaluate(instant, coordinates, rates)
    radius, jacobian, displacement = system.mapping(system.reference_radius, coordinates[-1])
    jacobian_derivative = np.where(system.reference_radius < system.anchor, 1/(system.anchor-system.radii[0]), -1/(system.radii[-1]-system.anchor))
    cell, shape, radial = system.reference_cell, system.reference_shape, system.reference_radial
    local_rates = np.column_stack([rates[cell], rates[cell+1]])
    local_acceleration = np.column_stack([acceleration[cell], acceleration[cell+1]])
    gradient = data['field_radial']
    gradient_time = np.sum(radial*local_rates, axis=1)/jacobian-gradient*jacobian_derivative*rates[-1]/jacobian
    second_time = np.sum(shape*local_acceleration, axis=1)-displacement*acceleration[-1]*gradient-2*displacement*rates[-1]*gradient_time
    coefficient = data['coefficient']
    coefficient_radial = system.coefficient(instant, radius+1e-24j).imag/1e-24
    coefficient_time = system.coefficient(instant+1e-24j, radius).imag/1e-24
    temporal_coefficient = radius**4/coefficient
    temporal_coefficient_time = -radius**4*coefficient_time/coefficient**2
    smooth_euler = coefficient_radial*gradient-temporal_coefficient_time*data['field_time']-temporal_coefficient*second_time
    bulk = float(np.dot(data['weight'], displacement*gradient*smooth_euler))
    anchor_index = np.searchsorted(system.radii, system.anchor)
    edges = np.insert(system.radii, anchor_index, system.anchor)
    nodal_scalar = np.insert(coordinates[:-1], anchor_index, 0.)
    unused, segment_jacobian, unused2 = system.mapping((edges[:-1]+edges[1:])/2, coordinates[-1])
    segment_gradient = np.diff(nodal_scalar)/np.diff(edges)/segment_jacobian
    physical, unused, edge_displacement = system.mapping(edges[1:-1], coordinates[-1])
    edge_coefficient = system.coefficient(instant, physical)
    edge_speed = edge_displacement*rates[-1]
    pressure = .5*(edge_coefficient-physical**4*edge_speed**2/edge_coefficient)*(segment_gradient[:-1]**2-segment_gradient[1:]**2)
    boundary_sum = float(np.dot(edge_displacement, pressure))
    physical_source_pressure = float(pressure[anchor_index-1])
    factor, unused, unused2 = system.gram_data(system.anchor, coordinates[:-1])
    gamma = np.asarray(system.sampling.T @ factor**2)/(2*system.spacing)
    nodal_radius, nodal_jacobian, nodal_displacement = system.mapping(system.radii, coordinates[-1])
    nodal_derivative = np.where(system.radii < system.anchor, 1/(system.anchor-system.radii[0]), -1/(system.radii[-1]-system.anchor))
    nodal_coefficient = system.coefficient(instant, nodal_radius)
    nodal_radial = system.coefficient(instant, nodal_radius+1e-24j).imag/1e-24
    gram_force = float(-np.dot(gamma, nodal_radial*nodal_displacement/nodal_jacobian-nodal_coefficient*nodal_derivative/nodal_jacobian**2))
    return dict(physical_source_pressure=physical_source_pressure, interior_mesh_pressure=boundary_sum-physical_source_pressure,
                smooth_bulk_euler_projection=bulk, Gram_shape_force=gram_force, derived_finite_force=boundary_sum-bulk+gram_force)


def main():
    evidence = EvidenceRun('annular-source-fitted-crossing-precision-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        coarse_path, fine_path = intake/'annular-source-fitted-crossing-attempt01', intake/'annular-source-fitted-fine-crossing-attempt01'
        statuses = []
        for path in [coarse_path, fine_path]:
            status = json.loads((path/'status.json').read_text())
            evidence.check(path.name+'_complete_with_accuracy_flags_preserved', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            evidence.own(path/'status.json')
            statuses.append(status)
        evidence.check('original_oracle_force_underresolution_not_hidden', not statuses[0]['oracle_resolution']['force_resolution_pass'])
        saved = np.load(fine_path/'oracle-512.npz')
        times, states512 = saved['times'], saved['states']
        states384 = np.load(fine_path/'oracle-384.npz')['states']
        evidence.own(fine_path/'oracle-512.npz')
        evidence.own(fine_path/'oracle-384.npz')
        oracle512, oracle384 = TwoSidedGRCharacteristics(512, mass=0.), TwoSidedGRCharacteristics(384, mass=0.)
        differences = [oracle_difference(oracle384, first, oracle512, second, 8) for first, second in zip(states384, states512)]
        alternate = [oracle_difference(oracle384, first, oracle512, second, 12) for first, second in zip(states384, states512)]
        evidence.check('oracle_vector_resolution_below_one_fiftieth_field_gate', max(differences) < 1e-4, differences)
        evidence.check('oracle_resolution_quadrature_agrees', max(abs(np.array(differences)-alternate)) < 2e-8, float(max(abs(np.array(differences)-alternate))))
        evidence.check('oracle_source_and_force_resolution', statuses[1]['oracle_resolution']['force_resolution_pass']
                       and statuses[1]['oracle_resolution']['source_clock_max'] < 5e-8, statuses[1]['oracle_resolution'])
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            system = SourceFittedAction(129, gram, background_mass=0.)
            saved_path = coarse_path/(branch+'-129.npz')
            original = np.load(saved_path)['states']
            evidence.own(saved_path)
            refined, evaluations = evolve(system, initial(system), times, step_factor=.1)
            difference = float(max(abs((refined-original).ravel())))
            evidence.check(branch+'_129_halfstep_state_agreement', difference < 2e-8, difference)
            destination = evidence.output/(branch+'-129-halfstep.npz')
            np.savez_compressed(destination, times=times, states=refined)
            evidence.own(destination, 'outputs')
            evidence.report['cases'].append(dict(kind='halfstep', branch=branch, maximum_state_difference=difference, rhs_evaluations=evaluations))
        for folder, status in zip([coarse_path, fine_path], statuses):
            for row in status['cases']:
                if row['kind'] != 'source_fitted':
                    continue
                system = SourceFittedAction(row['count'], row['branch'] == 'MTS', background_mass=0.)
                path = folder/(row['branch']+'-'+str(row['count'])+'.npz')
                states = np.load(path)['states']
                evidence.own(path)
                final_coordinates, final_rates = np.split(states[-1, :-1], 2)
                source_cell = np.searchsorted(system.radii, system.anchor)-1
                position, velocity = final_coordinates[-1], final_rates[-1]
                left_jacobian = (position-system.radii[0])/(system.anchor-system.radii[0])
                right_jacobian = (system.radii[-1]-position)/(system.radii[-1]-system.anchor)
                left_gradient = -final_coordinates[source_cell]/((system.anchor-system.radii[source_cell])*left_jacobian)
                right_gradient = final_coordinates[source_cell+1]/((system.radii[source_cell+1]-system.anchor)*right_jacobian)
                boundary_pressure = position**2*(1-velocity**2)*(left_gradient**2-right_gradient**2)/2
                coordinate_force = system.source_covector(times[-1], final_coordinates, final_rates, wave=True)
                recomputed = [field_comparison(system, state, oracle512, exact) for state, exact in zip(states, states512)]
                exact_force = statuses[1]['oracle_resolution']['final_force']
                force_error = abs(row['final_force']-exact_force)
                decomposition = finite_shape_force(system, times[-1], final_coordinates, final_rates)
                evidence.check(row['branch']+str(row['count'])+'_independent_finite_shape_force_identity',
                    abs(decomposition['derived_finite_force']-row['final_force']) < 2e-11, decomposition)
                qualified = dict(kind='qualified_comparison', count=row['count'], branch=row['branch'],
                    maximum_field_error=max(recomputed), final_force_absolute_error=float(force_error),
                    final_force_relative_error=float(force_error/abs(exact_force)),
                    strict_force_gate=bool(force_error < 2e-7 and force_error/abs(exact_force) < .02),
                    strict_waveform_gate=bool(max(recomputed) < .005),
                    physical_trace_pressure=float(boundary_pressure), full_canonical_force=row['final_force'],
                    finite_pressure_vs_canonical_gap=float(abs(boundary_pressure-row['final_force'])),
                    coordinate_force_without_momentum_derivative=float(coordinate_force),
                    source_field_momentum_derivative=float(coordinate_force-row['final_force']), shape_force_decomposition=decomposition)
                evidence.report['cases'].append(qualified)
                if row['count'] == 1025:
                    alternate = field_comparison(system, states[-1], oracle512, states512[-1], order=10)
                    evidence.check(row['branch']+'_finest_field_quadrature_agrees', abs(alternate-recomputed[-1]) < 2e-8, float(abs(alternate-recomputed[-1])))
                    evidence.check(row['branch']+'_omitted_global_momentum_is_not_accuracy_equivalent', abs(coordinate_force-row['final_force']) > 2e-7,
                                   float(abs(coordinate_force-row['final_force'])))
                evidence.save()
        evidence.report.update(scope='Independent fixed-background crossing oracle resolution, temporal controls and revised comparisons; not a live-gravity crossing test.',
            oracle_degree384_512_field_vector_differences=differences, independent_oracle_qualified_for_this_control=True,
            old_underresolved_oracle_preserved=True, finite_canonical_force_not_replaced_by_trace_pressure=True,
            all_Gram_rows_retained=True, source_field_momentum_derivative_retained=True,
            live_source_fitted_geometry_qualified=False, original_live_benchmark_replaced=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
