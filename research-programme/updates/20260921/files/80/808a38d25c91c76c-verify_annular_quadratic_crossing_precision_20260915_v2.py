from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from annular_source_fitted_action_20260915 import SourceFittedAction
from verify_annular_source_fitted_crossing_precision_20260915 import finite_shape_force
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from run_annular_source_fitted_crossing_20260915 import initial, evolve, field_comparison
import argparse
import json
import numpy as np


def shape_force(system, instant, coordinates, rates):
    acceleration = system.acceleration(instant, coordinates, rates)
    data = system.evaluate(instant, coordinates, rates)
    radius, jacobian, displacement = system.mapping(system.reference_radius, coordinates[-1])
    jacobian_derivative = np.where(system.reference_radius < system.anchor, 1/(system.anchor-system.radii[0]), -1/(system.radii[-1]-system.anchor))
    indices, shape, radial = system.reference_indices, system.reference_shape, system.reference_radial
    elements = np.clip(np.searchsorted(system.edges, system.reference_radius, side='right')-1, 0, len(system.edges)-2)
    lengths = np.diff(system.edges)[elements]
    second_radial = np.tile([4., -8., 4.], (len(elements), 1))/lengths[:, None]**2
    second_radial *= system.element_indices[elements] >= 0
    second_gradient = np.sum(second_radial*coordinates[:-1][indices], axis=1)/jacobian**2
    gradient = data['field_radial']
    gradient_reference_rate = np.sum(radial*rates[:-1][indices], axis=1)/jacobian-gradient*jacobian_derivative*rates[-1]/jacobian
    mesh_speed = displacement*rates[-1]
    second_time = np.sum(shape*acceleration[:-1][indices], axis=1)-displacement*acceleration[-1]*gradient-2*mesh_speed*gradient_reference_rate+mesh_speed**2*second_gradient
    coefficient = data['coefficient']
    coefficient_radial = system.coefficient(instant, radius+1e-24j).imag/1e-24
    coefficient_time = system.coefficient(instant+1e-24j, radius).imag/1e-24
    temporal_coefficient = radius**4/coefficient
    temporal_coefficient_time = -radius**4*coefficient_time/coefficient**2
    smooth_euler = coefficient_radial*gradient+coefficient*second_gradient-temporal_coefficient_time*data['field_time']-temporal_coefficient*second_time
    bulk = float(np.dot(data['weight'], displacement*gradient*smooth_euler))
    element_values = coordinates[:-1][np.maximum(system.element_indices, 0)]*(system.element_indices >= 0)
    unused, element_jacobian, unused2 = system.mapping((system.edges[:-1]+system.edges[1:])/2, coordinates[-1])
    physical_lengths = np.diff(system.edges)*element_jacobian
    left_gradient = element_values @ np.array([-3., 4., -1.])/physical_lengths
    right_gradient = element_values @ np.array([1., -4., 3.])/physical_lengths
    physical, unused, node_displacement = system.mapping(system.edges[1:-1], coordinates[-1])
    node_coefficient = system.coefficient(instant, physical)
    node_speed = node_displacement*rates[-1]
    pressure = .5*(node_coefficient-physical**4*node_speed**2/node_coefficient)*(right_gradient[:-1]**2-left_gradient[1:]**2)
    source_index = np.searchsorted(system.edges, system.anchor)-1
    source_pressure = float(pressure[source_index])
    boundary = float(node_displacement @ pressure)
    factors = system.lifted @ coordinates[:-1]
    gamma = np.asarray(system.sampling.T @ factors**2)/(2*system.gram_spacing)
    node_radius, node_jacobian, node_displacement = system.mapping(system.radii, coordinates[-1])
    node_derivative = np.where(system.radii < system.anchor, 1/(system.anchor-system.radii[0]), -1/(system.radii[-1]-system.anchor))
    coefficient_node = system.coefficient(instant, node_radius)
    coefficient_radial_node = system.coefficient(instant, node_radius+1e-24j).imag/1e-24
    gram_force = float(-gamma @ (coefficient_radial_node*node_displacement/node_jacobian-coefficient_node*node_derivative/node_jacobian**2))
    varied = system.evaluate(instant+1e-24j, coordinates+1e-24j*rates, rates+1e-24j*acceleration)
    coordinate_force = system.source_covector(instant, coordinates, rates, wave=True)
    momentum_rate = varied['field_momenta'][-1].imag/1e-24
    return dict(canonical_force=float(coordinate_force-momentum_rate), derived_force=boundary-bulk+gram_force,
        physical_source_pressure=source_pressure, interior_mesh_pressure=boundary-source_pressure,
        smooth_bulk_euler_projection=bulk, Gram_shape_force=gram_force, global_source_momentum_derivative=float(momentum_rate),
        flat_mechanical_momentum_rate=float(system.source_mass*acceleration[-1]/(1-rates[-1]**2)**1.5))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folders', nargs='+', default=['annular-quadratic-crossing-attempt01'])
    parser.add_argument('--extra-oracle-folder')
    parser.add_argument('--linear-folder')
    parser.add_argument('--label', required=True)
    arguments = parser.parse_args()
    evidence = EvidenceRun(arguments.label, __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        failed_path = intake/'annular-quadratic-crossing-precision-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        evidence.check('original_coarse_quadrature_failure_preserved', failed['state'] == 'failed' and any(not row['passed'] and row['name'] == 'reference33_comparison_quadrature_agrees' for row in failed['checks']))
        evidence.own(failed_path)
        evidence.own(evidence.root/'scripts/verify_annular_quadratic_crossing_precision_20260915.py')
        reference_folder = intake/'annular-source-fitted-fine-crossing-attempt01'
        oracle512, oracle384 = TwoSidedGRCharacteristics(512, mass=0.), TwoSidedGRCharacteristics(384, mass=0.)
        saved = np.load(reference_folder/'oracle-512.npz')
        times, exact512 = saved['times'], saved['states']
        exact384 = np.load(reference_folder/'oracle-384.npz')['states']
        for name in ['oracle-512.npz', 'oracle-384.npz']:
            evidence.own(reference_folder/name)
        oracle_forces = []
        for oracle, states in [(oracle512, exact512), (oracle384, exact384)]:
            values = []
            for state in states:
                fields, position, momentum, velocity = oracle.unpack(state)
                values.append(oracle.source_force(fields, position, velocity))
            oracle_forces.append(np.array(values))
        oracle_degrees = [512, 384]
        if arguments.extra_oracle_folder:
            folder = intake/arguments.extra_oracle_folder
            status = json.loads((folder/'status.json').read_text())
            evidence.check('additional_oracle_qualified', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            evidence.own(folder/'status.json')
            evidence.own(folder/'oracle-768.npz')
            saved_extra = np.load(folder/'oracle-768.npz')
            if not np.array_equal(saved_extra['times'], times):
                raise ValueError('Oracle times differ.')
            oracle768 = TwoSidedGRCharacteristics(768, mass=0.)
            values = []
            for state in saved_extra['states']:
                fields, position, momentum, velocity = oracle768.unpack(state)
                values.append(oracle768.source_force(fields, position, velocity))
            oracle_forces.append(np.array(values))
            oracle_degrees.append(768)
        seen = set()
        for folder in arguments.folders:
            path = intake/folder
            status = json.loads((path/'status.json').read_text())
            evidence.check(folder+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            evidence.own(path/'status.json')
            for original in status['cases']:
                base_count, branch = original['base_count'], original['branch']
                key = (base_count, branch)
                if key in seen:
                    raise ValueError('Duplicate quadratic case in precision study.')
                seen.add(key)
                system = QuadraticSourceFittedAction(base_count, branch == 'MTS', background_mass=0.)
                state_path = path/(branch+'-'+str(base_count)+'.npz')
                states = np.load(state_path)['states']
                evidence.own(state_path)
                decompositions = [shape_force(system, instant, *np.split(state[:-1], 2)) for instant, state in zip(times, states)]
                force_values = np.array([row['canonical_force'] for row in decompositions])
                residual = max(abs(row['derived_force']-row['canonical_force']) for row in decompositions)
                evidence.check(branch+str(base_count)+'_independent_quadratic_shape_force_identity', residual < 2e-11, float(residual))
                momentum_residual = max(abs(row['canonical_force']-row['flat_mechanical_momentum_rate']) for row in decompositions)
                evidence.check(branch+str(base_count)+'_physical_impulse_derivative_identity', momentum_residual < 2e-11, float(momentum_residual))
                fields16 = [field_comparison(system, state, oracle512, exact, order=16) for state, exact in zip(states, exact512)]
                fields24 = [field_comparison(system, state, oracle512, exact, order=24) for state, exact in zip(states, exact512)]
                quadrature_difference = float(max(abs(np.array(fields16)-fields24)))
                evidence.check(branch+str(base_count)+'_comparison_quadrature_agrees', quadrature_difference < 2e-8, quadrature_difference)
                final_errors = [float(abs(force_values[-1]-values[-1])) for values in oracle_forces]
                velocities = states[:, 2*system.count+1]
                physical_momenta = system.source_mass*velocities/np.sqrt(1-velocities**2)
                impulse_error = physical_momenta-exact512[:, -2]
                impulse_error -= impulse_error[0]
                row = dict(branch=branch, base_count=base_count, scalar_dofs=system.count,
                    recomputed_field_errors_order24=fields24, recomputed_maximum_field_error=max(fields24),
                    recomputed_waveform_gate=bool(max(fields24) < .005), quadrature16_24_maximum_difference=quadrature_difference,
                    original6_vs_recomputed24_maximum_difference=float(max(abs(np.array(original['field_errors'])-fields24))),
                    full_force_decompositions=decompositions, sampled_force_errors512=abs(force_values-oracle_forces[0]).tolist(),
                    sampled_force_errors384=abs(force_values-oracle_forces[1]).tolist(),
                    sampled_force_errors_checked_oracles={str(degree): abs(force_values-values).tolist() for degree, values in zip(oracle_degrees, oracle_forces)},
                    final_reference_forces=[float(values[-1]) for values in oracle_forces],
                    final_force_errors_checked_oracles=final_errors,
                    checked_oracle_degrees=oracle_degrees, final_force_gate_passes_all_checked_oracles=all(error < 2e-7 and error/abs(values[-1]) < .02 for error, values in zip(final_errors, oracle_forces)),
                    stricter_nine_time_absolute_force_gate=bool(max(abs(force_values-oracle_forces[0])) < 2e-7),
                    original_final_force_gate=original['strict_force_gate'], original_field_gate=original['strict_waveform_gate'],
                    original_source_clock_gate=original['strict_source_clock_gate'],
                    maximum_sampled_accumulated_impulse_error=float(np.max(abs(impulse_error))),
                    impulse_computed_from_mechanical_momentum_not_nine_point_force_quadrature=True)
                evidence.report['cases'].append(row)
                if base_count == 129:
                    refined, calls = evolve(system, initial(system), times, step_factor=.1)
                    state_error = float(np.max(abs(refined-states)))
                    evidence.check(branch+'_129_temporal_and_restart_control', state_error < 2e-8, state_error)
                    output = evidence.output/(branch+'-129-halfstep.npz')
                    np.savez_compressed(output, times=times, states=refined)
                    evidence.own(output, 'outputs')
                    row.update(halfstep_maximum_state_difference=state_error, halfstep_rhs_evaluations=calls)
                evidence.save()
        evidence.report['linear_cases'] = []
        if arguments.linear_folder:
            path = intake/arguments.linear_folder
            status = json.loads((path/'status.json').read_text())
            evidence.check('linear_refinement_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            evidence.own(path/'status.json')
            for original in status['cases']:
                count, branch = original['count'], original['branch']
                system = SourceFittedAction(count, branch == 'MTS', background_mass=0.)
                state_path = path/(branch+'-'+str(count)+'.npz')
                states = np.load(state_path)['states']
                evidence.own(state_path)
                decompositions, forces = [], []
                for instant, state in zip(times, states):
                    coordinates, rates = np.split(state[:-1], 2)
                    acceleration = system.acceleration(instant, coordinates, rates)
                    varied = system.evaluate(instant+1e-24j, coordinates+1e-24j*rates, rates+1e-24j*acceleration)
                    force = system.source_covector(instant, coordinates, rates, wave=True)-varied['field_momenta'][-1].imag/1e-24
                    decomposition = finite_shape_force(system, instant, coordinates, rates)
                    decomposition.update(canonical_force=float(force), flat_mechanical_momentum_rate=float(system.source_mass*acceleration[-1]/(1-rates[-1]**2)**1.5))
                    forces.append(force)
                    decompositions.append(decomposition)
                forces = np.array(forces)
                residual = max(abs(row['derived_finite_force']-row['canonical_force']) for row in decompositions)
                evidence.check(branch+str(count)+'_linear_shape_force_identity', residual < 2e-11, float(residual))
                residual = max(abs(row['flat_mechanical_momentum_rate']-row['canonical_force']) for row in decompositions)
                evidence.check(branch+str(count)+'_linear_momentum_and_final_force_identity', residual < 2e-11 and abs(forces[-1]-original['final_force']) < 2e-11, float(residual))
                difference = abs(field_comparison(system, states[-1], oracle512, exact512[-1], order=10)-original['field_errors'][-1])
                evidence.check(branch+str(count)+'_linear_comparison_quadrature_agrees', difference < 2e-8, float(difference))
                errors = [float(abs(forces[-1]-values[-1])) for values in oracle_forces]
                evidence.report['linear_cases'].append(dict(branch=branch, count=count, full_force_decompositions=decompositions,
                    checked_oracle_degrees=oracle_degrees, final_reference_forces=[float(values[-1]) for values in oracle_forces],
                    final_force_errors_checked_oracles=errors,
                    final_force_gate_passes_all_checked_oracles=all(error < 2e-7 and error/abs(values[-1]) < .02 for error, values in zip(errors, oracle_forces)),
                    sampled_force_errors_checked_oracles={str(degree): abs(forces-values).tolist() for degree, values in zip(oracle_degrees, oracle_forces)},
                    original_final_force_gate=original['strict_force_gate'], stricter_nine_time_absolute_force_gate=bool(max(abs(forces-oracle_forces[0])) < 2e-7)))
                evidence.save()
        evidence.report.update(scope='Fixed-background quadratic and optional linear crossing precision; final-force gate distinguished from a stricter sampled-trajectory force gate.',
            arguments=vars(arguments), no_fitted_coefficient_added=True, original_linear_action_embedded=True,
            all_original_vertex_Gram_rows_retained=True, source_field_momentum_derivative_retained=True,
            original_coarse_quadrature_failure_preserved=True, refined_comparison_orders=[16,24],
            live_quadratic_geometry_qualified=False, uniform_all_time_force_bound_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
