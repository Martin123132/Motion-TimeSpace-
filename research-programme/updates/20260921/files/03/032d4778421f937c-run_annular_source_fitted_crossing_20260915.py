from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_source_fitted_action_20260915 import SourceFittedAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from scipy.integrate import solve_ivp
import argparse
import json
import time
import numpy as np


def profile(radius):
    offset = np.asarray(radius)-6.03
    distance = abs(offset)
    envelope, envelope_gradient = np.ones_like(offset), np.zeros_like(offset)
    transition = (distance > .2) & (distance < .55)
    fraction = (distance[transition]-.2)/.35
    envelope[transition] = 1-10*fraction**3+15*fraction**4-6*fraction**5
    envelope_gradient[transition] = (-30*fraction**2+60*fraction**3-30*fraction**4)*np.sign(offset[transition])/.35
    envelope[distance >= .55] = 0.
    return .01*offset*envelope, .01*(envelope+offset*envelope_gradient)


def initial(system, zero=False):
    scalar, gradient = profile(system.radii)
    if zero:
        scalar, gradient = scalar*0., gradient*0.
    unused, unused2, displacement = system.mapping(system.radii, 6.03)
    rates = (displacement-1)*.06*gradient
    return np.concatenate([scalar, [6.03], rates, [.06, 0.]])


def evolve(system, initial_state, times, step_factor=.2):
    def flow(instant, state):
        coordinates, rates = np.split(state[:-1], 2)
        return np.append(system.rhs(instant, state[:-1]), system.evaluate(instant, coordinates, rates)['clock'])
    solution = solve_ivp(flow, (times[0], times[-1]), initial_state, t_eval=times,
                         method='DOP853', rtol=2e-10, atol=2e-12, max_step=step_factor*system.spacing)
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution.y.T, solution.nfev


def field_comparison(system, state, oracle, oracle_state, order=6):
    coordinates, rates = np.split(state[:-1], 2)
    mapped, unused, unused2 = system.mapping(np.append(system.radii, system.anchor), coordinates[-1])
    edges = np.unique(np.append(mapped, oracle_state[-3]))
    points, weights = np.polynomial.legendre.leggauss(order)
    physical = ((edges[:-1, None]+edges[1:, None])/2+np.diff(edges)[:, None]*points/2).ravel()
    measure = (np.diff(edges)[:, None]*weights/2).ravel()
    left = physical < coordinates[-1]
    reference = np.where(left, system.radii[0]+(physical-system.radii[0])*(system.anchor-system.radii[0])/(coordinates[-1]-system.radii[0]),
                         system.radii[-1]-(system.radii[-1]-physical)*(system.radii[-1]-system.anchor)/(system.radii[-1]-coordinates[-1]))
    unused, unused2, temporal, gradient = system.sample(reference, coordinates, rates)
    exact_temporal, exact_gradient = oracle.sample(oracle_state, physical)
    numerator = np.dot(measure*physical**2, (temporal-exact_temporal)**2+(gradient-exact_gradient)**2)
    denominator = np.dot(measure*physical**2, exact_temporal**2+exact_gradient**2)
    return float(np.sqrt(numerator/denominator))


def diagnostics(system, times, states):
    energies, residuals, forces, momenta, minimum_jacobian = [], [], [], [], 1.
    for instant, state in zip(times, states):
        coordinates, rates = np.split(state[:-1], 2)
        data = system.evaluate(instant, coordinates, rates)
        acceleration = system.acceleration(instant, coordinates, rates)
        shifted = system.evaluate(instant+1e-24j, coordinates+1e-24j*rates, rates+1e-24j*acceleration)
        covector = np.append(data['scalar_covector'], system.source_covector(instant, coordinates, rates))
        residuals.append(float(np.max(abs(shifted['momenta'].imag/1e-24-covector))))
        forces.append(float(system.source_covector(instant, coordinates, rates, wave=True)-shifted['field_momenta'][-1].imag/1e-24))
        energies.append(float(system.energy(instant, coordinates, rates)))
        momenta.append(float(data['field_momenta'][-1]))
        minimum_jacobian = min(minimum_jacobian, float(min(data['jacobian'])))
    positions = states[:, system.count]
    velocities = states[:, 2*system.count+1]
    old_nodes_crossed = system.radii[(system.radii > positions.min()) & (system.radii < positions.max())]
    return dict(energy_relative_drift=float(max(abs(np.array(energies)-energies[0]))/abs(energies[0])),
        maximum_euler_residual=max(residuals), minimum_jacobian=minimum_jacobian,
        old_grid_nodes_crossed=old_nodes_crossed.tolist(), minimum_velocity=float(min(velocities)),
        final_position=float(positions[-1]), final_velocity=float(velocities[-1]), final_clock=float(states[-1, -1]),
        final_force=forces[-1], maximum_absolute_source_field_momentum=float(max(abs(np.array(momenta)))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--counts', type=int, nargs='+', default=[33, 65, 129])
    parser.add_argument('--oracle-degrees', type=int, nargs='+', default=[192, 256])
    arguments = parser.parse_args()
    evidence = EvidenceRun(arguments.label, __file__)
    times = np.linspace(0., .4, 9)
    evidence.report.update(arguments=vars(arguments), preparation='Additional flat-background crossing control: original compact-quintic shape and amplitude .01; velocity .06, T=.4; not replacement live data.',
        fixed_background_mass=0., time_samples=times.tolist(), all_Gram_rows_retained=True, source_field_momentum_derivative_retained=True,
        energy_projection=False, live_source_fitted_geometry_qualified=False, uniform_phase_convergence_proven=False)
    try:
        preflight = evidence.root/'source-intake/navier-stokes/20260914/annular-source-fitted-action-qualification-attempt01/status.json'
        qualification = json.loads(preflight.read_text())
        evidence.check('variational_action_qualified_before_crossing', qualification['state'] == 'complete' and all(row['passed'] for row in qualification['checks']))
        evidence.own(preflight)
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            system = SourceFittedAction(33, gram, background_mass=0.)
            states, evaluations = evolve(system, initial(system, zero=True), times)
            error = max(np.max(abs(states[:, system.count]-(6.03+.06*times))),
                        np.max(abs(states[:, -1]-times*np.sqrt(1-.06**2))), np.max(abs(states[:, 2*system.count+1]-.06)))
            evidence.check(branch+'_zero_wave_analytic_crossing', error < 2e-12, float(error))
        oracle_results = []
        for degree in arguments.oracle_degrees:
            started = time.monotonic()
            oracle = TwoSidedGRCharacteristics(degree, mass=0., source=.03)
            radius, unused, unused2 = oracle.mesh(6.03, .06)
            unused, gradient = profile(radius)
            temporal = -.06*gradient
            fields = np.stack([temporal+gradient, temporal-gradient], axis=1)
            seed = oracle.pack(fields, np.array([6.03, .03*.06/np.sqrt(1-.06**2), 0.]))
            solution = solve_ivp(oracle.rhs, (0., .4), seed, t_eval=times, method='DOP853',
                                 rtol=2e-10, atol=2e-12, max_step=.1/degree)
            evidence.check('oracle'+str(degree)+'_evolution_finished', solution.success, solution.message)
            states = solution.y.T
            energies = np.array([oracle.energy(state)[0] for state in states])
            drift = float(max(abs(energies-energies[0]))/abs(energies[0]))
            evidence.check('oracle'+str(degree)+'_finite_conserved_control', np.isfinite(states).all() and drift < 2e-6, drift)
            destination = evidence.output/('oracle-'+str(degree)+'.npz')
            np.savez_compressed(destination, times=times, states=states)
            evidence.own(destination, 'outputs')
            evidence.report['cases'].append(dict(kind='oracle', degree=degree, energy_relative_drift=drift,
                rhs_evaluations=solution.nfev, seconds=time.monotonic()-started))
            oracle_results.append((oracle, states))
            evidence.save()
            print(evidence.report['cases'][-1], flush=True)
        oracle, exact_states = oracle_results[-1]
        oracle_force = []
        for state in exact_states:
            fields, position, momentum, velocity = oracle.unpack(state)
            oracle_force.append(oracle.source_force(fields, position, velocity))
        if len(oracle_results) > 1:
            previous, previous_states = oracle_results[-2]
            force_previous = []
            for state in previous_states:
                fields, position, momentum, velocity = previous.unpack(state)
                force_previous.append(previous.source_force(fields, position, velocity))
            evidence.report['oracle_resolution'] = dict(source_clock_max=float(np.max(abs(previous_states[:, -3:]-exact_states[:, -3:]))),
                force_absolute_max=float(max(abs(np.array(force_previous)-oracle_force))), final_force=float(oracle_force[-1]),
                force_resolution_pass=bool(max(abs(np.array(force_previous)-oracle_force)) < 2e-7))
        for count in arguments.counts:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                started = time.monotonic()
                system = SourceFittedAction(count, gram, background_mass=0.)
                states, evaluations = evolve(system, initial(system), times)
                destination = evidence.output/(branch+'-'+str(count)+'.npz')
                np.savez_compressed(destination, times=times, states=states)
                evidence.own(destination, 'outputs')
                row = diagnostics(system, times, states)
                field_errors = [field_comparison(system, state, oracle, exact) for state, exact in zip(states, exact_states)]
                source_error = float(max(abs(states[:, count]-exact_states[:, -3])))
                exact_velocity = np.array([oracle.unpack(state)[3] for state in exact_states])
                velocity_error = float(max(abs(states[:, 2*count+1]-exact_velocity)))
                clock_error = float(max(abs(states[:, -1]-exact_states[:, -1])))
                force_error = float(abs(row['final_force']-oracle_force[-1]))
                force_relative = float(force_error/abs(oracle_force[-1]))
                row.update(kind='source_fitted', branch=branch, count=count, rhs_evaluations=evaluations,
                    maximum_field_error=max(field_errors), field_errors=field_errors, maximum_source_error=source_error,
                    maximum_velocity_error=velocity_error, maximum_clock_error=clock_error,
                    final_force_absolute_error=force_error, final_force_relative_error=force_relative,
                    strict_force_gate=bool(force_error < 2e-7 and force_relative < .02),
                    strict_waveform_gate=bool(max(field_errors) < .005),
                    strict_source_clock_gate=bool(source_error < 5e-7 and velocity_error < 2e-5 and clock_error < 2e-7),
                    seconds=time.monotonic()-started)
                evidence.report['cases'].append(row)
                evidence.check(branch+str(count)+'_genuine_old_grid_crossing', len(row['old_grid_nodes_crossed']) > 0, row['old_grid_nodes_crossed'])
                evidence.check(branch+str(count)+'_positive_map_and_finite_state', row['minimum_jacobian'] > .9 and np.isfinite(states).all())
                evidence.check(branch+str(count)+'_EL_and_energy', row['maximum_euler_residual'] < 2e-11 and row['energy_relative_drift'] < 2e-8, row)
                evidence.check(branch+str(count)+'_moving_field_momentum_not_zero', row['maximum_absolute_source_field_momentum'] > 1e-8)
                evidence.save()
                print(row, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
