from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_relaxed_trace_action_20260916 import RelaxedTraceSourceAction, relaxed_shape_force, relaxed_spectral_step
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from run_annular_source_fitted_crossing_20260915 import initial
from scipy.linalg import solve_banded
import numpy as np


def main():
    evidence = EvidenceRun('annular-relaxed-branch-qualification-attempt01', __file__)
    try:
        for count in [33, 65, 129]:
            for background in [0., .7]:
                for gram in [False, True]:
                    branch = 'relaxed_MTS' if gram else 'reference'
                    prefix = str(count)+branch+'mass'+str(background)
                    system = RelaxedTraceSourceAction(count, gram, background_mass=background)
                    original = LocallyRefinedSourceAction(count, gram, background_mass=background, source_splits=1)
                    reference = LocallyRefinedSourceAction(count, False, background_mass=background, source_splits=1)
                    state = initial(system)
                    coordinates, rates = np.split(state[:-1], 2)
                    coordinates[:-1] += .0003*np.sin(11*(system.radii-system.anchor))
                    rates[:-1] += .0005*np.cos(7*(system.radii-system.anchor))
                    coordinates[-1] = 6.061
                    data = system.evaluate(0., coordinates, rates)
                    old = original.evaluate(0., coordinates, rates)
                    bulk = reference.evaluate(0., coordinates, rates)
                    trace = system.trace_data(0., coordinates)
                    expected_action = bulk['action']-trace['residual'] @ (trace['weights']*trace['residual'])/2
                    evidence.check(prefix+'_positive_stationary_auxiliary_action', abs(data['action']-expected_action) < 2e-13
                                   and abs(data['auxiliary_stationarity'])<2e-12 and data['relaxed_Gram_energy']>=0)
                    evidence.check(prefix+'_all_rows_and_full_kinetic_momenta_retained', system.original.shape==original.original.shape
                                   and np.max(abs(data['momenta']-old['momenta']))<2e-14
                                   and np.max(abs(data['cross']-old['cross']))<2e-14 and data['source_inertia']==old['source_inertia'])
                    field_error, momentum_error = 0., 0.
                    for phase in [.13, .71, 1.37]:
                        direction = np.sin(np.arange(system.count+1)*phase)
                        field_direction = direction.copy()
                        field_direction[-1] = 0.
                        perturbed = system.evaluate(0., coordinates+1e-24j*field_direction, rates)
                        field_error = max(field_error, abs(float(perturbed['action'].imag/1e-24-data['scalar_covector'] @ direction[:-1])))
                        perturbed = system.evaluate(0., coordinates, rates+1e-24j*direction)
                        momentum_error = max(momentum_error, abs(float(perturbed['action'].imag/1e-24-data['momenta'] @ direction)))
                    evidence.check(prefix+'_field_variational_derivative', field_error < 2e-10, field_error)
                    evidence.check(prefix+'_velocity_variational_derivative', momentum_error < 2e-11, momentum_error)
                    perturbed_coordinates = coordinates.astype(complex)
                    perturbed_coordinates[-1] += 1e-24j
                    weight_b = system.trace_data(0., perturbed_coordinates)['weights'].imag/1e-24
                    envelope = -trace['residual'] @ (weight_b*trace['residual'])/2
                    source_difference = system.source_covector(0., coordinates, rates)-reference.source_covector(0., coordinates, rates)
                    evidence.check(prefix+'_source_envelope_covector', abs(source_difference-envelope) < 2e-11, float(abs(source_difference-envelope)))
                    original_coefficient = system.coefficient
                    probe = lambda radius: .3+np.sin(2.7*np.asarray(radius))
                    expected_dual = np.dot(data['weight']*data['density_dual'], data['coefficient']*probe(data['radius']))
                    node_radius = system.mapping(system.radii, coordinates[-1])[0]
                    expected_dual += np.dot(data['nodal_dual'], data['nodal']*probe(node_radius))
                    try:
                        system.coefficient = lambda instant, radius: original_coefficient(instant, radius)*(1+1e-24j*probe(radius))
                        dual_value = system.evaluate(0., coordinates, rates)['action'].imag/1e-24
                    finally:
                        system.coefficient = original_coefficient
                    evidence.check(prefix+'_bulk_and_nodal_coefficient_duals', abs(dual_value-expected_dual) < 2e-12, float(abs(dual_value-expected_dual)))
                    solved_cross = solve_banded((2, 2), data['mass_bands'], data['cross'])
                    evidence.check(prefix+'_positive_coupled_inertia', data['source_inertia']-data['cross'] @ solved_cross > 0)
                    acceleration = system.acceleration(0., coordinates, rates)
                    varied = system.evaluate(1e-24j, coordinates+1e-24j*rates, rates+1e-24j*acceleration)
                    covector = np.append(data['scalar_covector'], system.source_covector(0., coordinates, rates))
                    euler_error = float(np.max(abs(varied['momenta'].imag/1e-24-covector)))
                    energy_rate = float(system.energy(1e-24j, coordinates+1e-24j*rates, rates+1e-24j*acceleration).imag/1e-24)
                    evidence.check(prefix+'_Euler_and_autonomous_energy_identity', euler_error < 2e-10 and abs(energy_rate)<2e-10,
                                   dict(euler_error=euler_error, energy_rate=energy_rate))
                    if not gram:
                        evidence.check(prefix+'_reference_exactly_unchanged', abs(data['action']-old['action'])<2e-14
                                       and np.max(abs(data['scalar_covector']-old['scalar_covector']))<2e-12
                                       and np.max(abs(acceleration-original.acceleration(0., coordinates, rates)))<2e-10)
                    if background==0.:
                        shape = relaxed_shape_force(system, 0., coordinates, rates)
                        evidence.check(prefix+'_independent_shape_and_mechanical_force', abs(shape['canonical_force']-shape['derived_force'])<2e-10
                                       and abs(shape['canonical_force']-shape['flat_mechanical_momentum_rate'])<2e-10, shape)
                        zero = initial(system, zero=True)
                        zero_coordinates, zero_rates = np.split(zero[:-1], 2)
                        evidence.check(prefix+'_zero_field_free_motion', np.max(abs(system.acceleration(0., zero_coordinates, zero_rates)))<2e-13)
                        spectrum = relaxed_spectral_step(system, state)
                        evidence.check(prefix+'_relaxed_stiffness_solver_guard', spectrum['largest_field_eigenvalue']>0 and spectrum['eigen_residual']<2e-8, spectrum)
                    evidence.report['cases'].append(dict(count=count, branch=branch, background_mass=background,
                        auxiliary_trace=float(data['auxiliary_trace']), actual_derivative_jump=float(data['physical_reference_jump']),
                        original_action=float(old['action']), candidate_action=float(data['action']), field_derivative_error=field_error,
                        momentum_derivative_error=momentum_error, no_physical_trace_constraint_imposed=True))
                    evidence.save()
        evidence.report.update(scope='Separate static-relaxation variational candidate; derivative and instantaneous equations qualified, no evolved-force pass yet.',
            source_field_momentum_retained=True, original_sampling_rows_retained=True, no_new_fitted_parameter=True,
            derivative_trace_overwritten=False, legacy_gradient_Gram_helpers_rejected=True,
            dynamic_convergence_from_original_action_proven=False, live_geometry_qualified=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
