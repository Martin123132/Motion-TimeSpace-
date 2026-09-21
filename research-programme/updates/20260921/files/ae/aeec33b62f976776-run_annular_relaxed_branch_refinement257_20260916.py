from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_relaxed_trace_action_20260916 import RelaxedTraceSourceAction, relaxed_shape_force, relaxed_spectral_step
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from run_annular_source_fitted_crossing_20260915 import initial, diagnostics, field_comparison
from scipy.integrate import solve_ivp
import json
import time
import numpy as np


def integrate_interval(system, state, start, end, step, tight=False):
    def flow(instant, value):
        coordinates, rates = np.split(value[:-1], 2)
        return np.append(system.rhs(instant, value[:-1]), system.evaluate(instant, coordinates, rates)['clock'])
    cap = step*(.5 if tight else 1.)
    result = solve_ivp(flow, (start, end), state, t_eval=[start, end], method='DOP853',
                       rtol=2e-12 if tight else 2e-10, atol=2e-14 if tight else 2e-12,
                       max_step=cap, first_step=cap/2)
    if not result.success:
        raise RuntimeError(result.message)
    return result.y[:, -1], result.nfev


def main():
    evidence = EvidenceRun('annular-relaxed-branch-refinement257-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        preflight_path = intake/'annular-relaxed-branch-qualification-attempt01/status.json'
        preflight = json.loads(preflight_path.read_text())
        evidence.own(preflight_path)
        evidence.check('variational_candidate_qualified', preflight['state']=='complete' and len(preflight['checks'])==120 and all(row['passed'] for row in preflight['checks']))
        old_folder = intake/'annular-quadratic-crossing-attempt01'
        old_status = json.loads((old_folder/'status.json').read_text())
        evidence.own(old_folder/'status.json')
        evidence.check('unrelaxed_baselines_preserved', old_status['state']=='complete')
        oracles, exact_states, exact_forces = {}, {}, {}
        times = np.linspace(0., .4, 9)
        for degree in [384, 512, 768]:
            folder = intake/('annular-crossing-oracle768-attempt01' if degree==768 else 'annular-source-fitted-fine-crossing-attempt01')
            path = folder/('oracle-'+str(degree)+'.npz')
            evidence.own(path)
            saved = np.load(path)
            evidence.check('oracle'+str(degree)+'_same_times', np.array_equal(saved['times'], times))
            model = TwoSidedGRCharacteristics(degree, mass=0.)
            states = saved['states']
            forces = []
            for state in states:
                fields, position, momentum, velocity = model.unpack(state)
                forces.append(model.source_force(fields, position, velocity))
            oracles[degree], exact_states[degree], exact_forces[degree] = model, states, np.array(forces)
        evidence.report.update(original_profile_and_final_time_unchanged=True, auxiliary_trace_not_physical_jump=True,
            original_sampling_rows_retained=True, kinetic_source_current_retained=True, energy_projection=False,
            no_fitted_parameter=True, candidate_not_original_action=True, source_splits=1,
            time_samples=times.tolist(), prespecified_gates=dict(field=.005, source=5e-7, velocity=2e-5, clock=2e-7, force_absolute=2e-7, force_relative=.02),
            dynamic_convergence_from_unrelaxed_action_proven=False, live_geometry_qualified=False)
        for count in [257]:
            for gram in [False, True]:
                branch = 'relaxed_MTS' if gram else 'reference'
                prefix = branch+str(count)
                system = RelaxedTraceSourceAction(count, gram, background_mass=0.)
                started = time.monotonic()
                states = [initial(system)]
                evaluations = 0
                spectra = []
                for index in range(1, len(times)):
                    step = relaxed_spectral_step(system, states[-1])
                    if step['eigen_residual'] >= 2e-8:
                        raise RuntimeError('Unresolved relaxed-action spectrum.')
                    spectra.append(step)
                    state, calls = integrate_interval(system, states[-1], times[index-1], times[index], step['maximum_step'])
                    states.append(state)
                    evaluations += calls
                    destination = evidence.output/(branch+'-'+str(count)+'-accepted-'+str(index)+'.npz')
                    np.savez_compressed(destination, times=times[:index+1], states=np.array(states))
                    evidence.own(destination, 'outputs')
                    evidence.report['progress'] = dict(branch=branch, count=count, accepted_time=float(times[index]), seconds=time.monotonic()-started)
                    evidence.save()
                    print(evidence.report['progress'], flush=True)
                    if time.monotonic()-started > 3600:
                        raise RuntimeError('One-hour per-case safe checkpoint; accepted intervals preserved.')
                states = np.array(states)
                destination = evidence.output/(branch+'-'+str(count)+'.npz')
                np.savez_compressed(destination, times=times, states=states)
                evidence.own(destination, 'outputs')
                row = diagnostics(system, times, states)
                decompositions = [relaxed_shape_force(system, instant, *np.split(state[:-1], 2)) for instant, state in zip(times, states)]
                forces = np.array([item['canonical_force'] for item in decompositions])
                fields16 = [field_comparison(system, state, oracles[512], exact, order=16) for state, exact in zip(states, exact_states[512])]
                fields24 = [field_comparison(system, state, oracles[512], exact, order=24) for state, exact in zip(states, exact_states[512])]
                evidence.check(prefix+'_finite_positive_map', np.isfinite(states).all() and row['minimum_jacobian']>.9)
                evidence.check(prefix+'_EL_and_energy', row['maximum_euler_residual']<2e-10 and row['energy_relative_drift']<2e-8, row)
                evidence.check(prefix+'_independent_relaxed_force_identity', max(abs(item['canonical_force']-item['derived_force']) for item in decompositions)<2e-10
                               and max(abs(item['canonical_force']-item['flat_mechanical_momentum_rate']) for item in decompositions)<2e-10)
                quadrature_error = float(max(abs(np.array(fields16)-fields24)))
                evidence.check(prefix+'_field_quadrature16_24', quadrature_error<2e-8, quadrature_error)
                positions = states[:, system.count]
                crossed = system.base_radii[(system.base_radii>min(positions)) & (system.base_radii<max(positions))]
                evidence.check(prefix+'_original_base_vertex_crossed', len(crossed)>0)
                exact_velocity = np.array([oracles[512].unpack(state)[3] for state in exact_states[512]])
                source_error = float(max(abs(positions-exact_states[512][:, -3])))
                velocity_error = float(max(abs(states[:, 2*system.count+1]-exact_velocity)))
                clock_error = float(max(abs(states[:, -1]-exact_states[512][:, -1])))
                force_errors = {str(degree):abs(forces-values).tolist() for degree, values in exact_forces.items()}
                final_flags = {str(degree):bool(abs(forces[-1]-values[-1])<2e-7 and abs(forces[-1]-values[-1])/abs(values[-1])<.02) for degree, values in exact_forces.items()}
                sampled_flags = {str(degree):bool(max(abs(forces-values))<2e-7) for degree, values in exact_forces.items()}
                old_branch = 'MTS' if gram else 'reference'
                old_path = old_folder/(old_branch+'-'+str(count)+'.npz')
                evidence.own(old_path)
                old_states = np.load(old_path)['states']
                old_row = next(item for item in old_status['cases'] if item['base_count']==count and item['branch']==old_branch)
                difference = float(np.max(abs(states-old_states)))
                if not gram:
                    evidence.check(prefix+'_old_reference_reproduced', difference<2e-8, difference)
                row.update(branch=branch, base_count=count, scalar_dofs=system.count, source_splits=1,
                    full_force_decompositions=decompositions, forces=forces.tolist(), field_errors=fields24, maximum_field_error=max(fields24),
                    maximum_source_error=source_error, maximum_velocity_error=velocity_error, maximum_clock_error=clock_error,
                    reference_final_forces={str(degree):float(values[-1]) for degree, values in exact_forces.items()},
                    force_errors=force_errors, final_force_flags_by_reference=final_flags, sampled_force_flags_by_reference=sampled_flags,
                    final_force_absolute_error=force_errors['512'][-1], final_force_relative_error=force_errors['512'][-1]/abs(exact_forces[512][-1]),
                    final_force_passes_all_references=all(final_flags.values()), sampled_force_passes_all_references=all(sampled_flags.values()),
                    strict_waveform_gate=bool(max(fields24)<.005), strict_source_clock_gate=bool(source_error<5e-7 and velocity_error<2e-5 and clock_error<2e-7),
                    original_base_vertices_crossed=crossed.tolist(), old_unrelaxed_final_force_error=old_row['final_force_absolute_error'],
                    state_difference_from_old_same_mesh=difference, old_unrelaxed_field_error=old_row['maximum_field_error'],
                    spectral_step_history=spectra, quadrature16_24_difference=quadrature_error,
                    seconds=time.monotonic()-started, rhs_evaluations=evaluations)
                evidence.report['cases'].append(row)
                evidence.save()
                print(json.dumps({key:row[key] for key in ['branch','base_count','maximum_field_error','final_force_absolute_error','final_force_passes_all_references','sampled_force_passes_all_references','seconds']}), flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
