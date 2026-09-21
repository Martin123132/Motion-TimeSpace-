import os
for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
from time import perf_counter
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_compatible_h_evolution_20260914 import CompatibleEvolution
from annular_constrained_mass_relative_energy_20260914 import quadrature
from compare_annular_regulators_to_continuum_20260914 import compare, target_refinement_noise


def physical_errors(system, state, time, fine, coarse, index):
    offsets, weights = quadrature(20)
    data = system.geometry(time, state).layer(offsets)
    radii = data['R'][:, 1:-1]
    edge_radii = (data['R'][:, :-1]+data['R'][:, 1:])/2
    if radii.min() < 5 or radii.max() > 6 or edge_radii.min() < 5 or edge_radii.max() > 6:
        raise ValueError('Do not extrapolate the continuum outside the annulus.')
    targets = []
    for archive in [fine, coarse]:
        fields = archive['states'][index].reshape(3, len(archive['radii']))
        targets.append([CubicSpline(archive['radii'], fields[2], extrapolate=False)(radii),
                        CubicSpline(archive['radii'], fields[1], extrapolate=False)(edge_radii)])
    error_momentum = data['p'][:, 1:-1]-targets[0][0]
    error_gradient = np.diff(data['chi'], axis=1)/system.spacing-targets[0][1]

    def norm(momentum, gradient):
        return float(weights @ (np.sum(system.node_weights[1:-1]*momentum**2/radii**2, axis=1)+
                                  np.sum(system.spacing*edge_radii**2*gradient**2, axis=1)))**.5

    error = norm(error_momentum, error_gradient)
    noise = norm(targets[0][0]-targets[1][0], targets[0][1]-targets[1][1])
    return dict(physical_energy_error=error**2/2, physical_energy_norm=error, physical_target_noise_norm=noise)


def run():
    evidence = EvidenceRun('annular-source-collision-regulators-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        folder = intake/'annular-source-collision-continuum-attempt01'
        status_path = folder/'status.json'
        baseline = json.loads(status_path.read_text())
        evidence.own(status_path)
        evidence.check('active_continuum_passed', baseline['state'] == 'complete' and all(row['passed'] for row in baseline['checks']))
        archives = {}
        for count in [1025, 2049]:
            path = folder/('continuum_count'+str(count)+'.npz')
            evidence.own(path)
            archives[count] = dict(np.load(path, allow_pickle=False))
        evidence.report.update(scope='Identical continuation of original saved preparations: reference and MTS through first source collision to .45.',
                               no_parameters_refitted=True, time_beyond_analytic_uniform_interval=True,
                               complete_parent_source_action_derived=False, arbitrary_source_stability_proven=False)
        offsets, weights = quadrature(20)
        times = np.array([.06, .1, .2, .3, .35, .4, .45])
        for count in [33, 65, 129]:
            for gram, label, old_label in [(False, 'reference', 'GR_control'), (True, 'MTS', 'metric_Gram')]:
                started = perf_counter()
                system = CompatibleEvolution(count, gram, degree=8)
                path = intake/'annular-compatible-h-evolution-main-attempt01'/(old_label+'_count'+str(count)+'.npz')
                evidence.own(path)
                saved = np.load(path, allow_pickle=False)
                evidence.check(label+str(count)+'_restart_at_saved_time', abs(saved['times'][-1]-.06) < 1e-15)
                state = saved['states'][-1].copy()
                states = [state]
                for lower, upper in zip(times, times[1:]):
                    evidence.report['progress'] = dict(branch=label, count=count, segment_start=float(lower), segment_end=float(upper))
                    evidence.save()
                    solution = solve_ivp(system.rhs, (lower, upper), state, method='DOP853', rtol=2e-11,
                                         atol=2e-13, max_step=min((upper-lower)/8, system.spacing/4), t_eval=[upper])
                    if not solution.success:
                        raise RuntimeError(solution.message)
                    state = solution.y[:, -1]
                    states.append(state)
                    segment = evidence.output/(label+'_count'+str(count)+'_t'+format(upper, '.2f')+'.npz')
                    np.savez_compressed(segment, state=state, time=upper, calls=system.calls)
                    evidence.own(segment, 'outputs')
                    evidence.save()
                    print(label+' '+str(count)+' saved t='+str(upper), flush=True)
                rows, total_masses = [], []
                for time, state in zip(times, states):
                    index = int(np.argmin(abs(archives[2049]['times']-time)))
                    if abs(archives[2049]['times'][index]-time) > 1e-14:
                        raise ValueError('Continuum time does not match regulator sample.')
                    row, profiles = compare(system, time, state, archives[2049], index)
                    row.update(physical_errors(system, state, time, archives[2049], archives[1025], index))
                    noise = target_refinement_noise(count, archives[2049], archives[1025], index)
                    geometry = system.geometry(time, state)
                    data = geometry.layer(offsets)
                    total = float(geometry.metric([geometry.edges[-1]])['mu'][0])
                    total_masses.append(total)
                    reaction = -data['Gchi'][:, -1]
                    target_row = baseline['cases'][-1]['diagnostics'][index]
                    row.update(branch=label, mass=total, minimum_F=float(geometry.minimum_F),
                               holding_reaction_mean=float(weights @ reaction),
                               holding_reaction_rms=float(np.sqrt(weights @ reaction**2)),
                               target_wall_force=target_row['wall_force'],
                               target_required_surface_pressure=target_row['source_pressure'],
                               source_power=float(weights @ (reaction*data['q'][:, -1])),
                               source_q_max=float(abs(data['q'][:, -1]).max()),
                               source_reservoir_error=float(abs(data['energy']-.003).max()),
                               collocation_defect=float(geometry.collocation_defect), target_noise=noise)
                    rows.append(row)
                    evidence.report['cases'].append(row)
                    prefix = label+str(count)+'_'+str(time)
                    evidence.check(prefix+'_regular_finite', row['minimum_F'] > .5 and all(np.isfinite(row[key]) for key in
                        ['energy_error', 'physical_energy_error', 'mass_max_error', 'log_lapse_max_error', 'holding_reaction_mean']))
                    evidence.check(prefix+'_fixed_source_no_work', abs(row['source_power']) < 1e-13 and row['source_q_max'] < 1e-13 and row['source_reservoir_error'] < 1e-12)
                    evidence.check(prefix+'_collocation', row['collocation_defect'] < 1e-9, row['collocation_defect'])
                    evidence.check(prefix+'_physical_target_resolved', row['physical_target_noise_norm'] < .02*row['physical_energy_norm']+1e-13)
                    for key, value in noise.items():
                        evidence.check(prefix+'_target_resolved_'+key, value < .02*row[key]+1e-13, dict(noise=value, error=row[key]))
                    if time == .45:
                        output = evidence.output/(label+'_count'+str(count)+'_final_profiles.npz')
                        np.savez_compressed(output, **profiles)
                        evidence.own(output, 'outputs')
                drift = max(abs(value-float(saved['total_mass'][0])) for value in total_masses)
                evidence.check(label+str(count)+'_mass_conservation', drift < 1e-8, drift)
                evidence.check(label+str(count)+'_source_actually_forced', max(abs(row['holding_reaction_mean']) for row in rows) > .1)
                path = evidence.output/(label+'_count'+str(count)+'.npz')
                np.savez_compressed(path, times=times, states=np.array(states), total_mass=np.array(total_masses))
                evidence.own(path, 'outputs')
                evidence.report.setdefault('timings', []).append(dict(branch=label, count=count, seconds=perf_counter()-started, calls=system.calls, mass_drift=drift))
                evidence.save()
                print(label+' '+str(count)+' comparison finished; seconds='+str(perf_counter()-started), flush=True)
        refinement = []
        for label in ['reference', 'MTS']:
            for time in [.3, .4, .45]:
                rows = [row for row in evidence.report['cases'] if row['branch'] == label and row['time'] == time]
                for key in ['energy_error', 'physical_energy_error', 'chi_L2', 'mass_max_error', 'log_lapse_max_error']:
                    values = [row[key] for row in rows]
                    refinement.append(dict(branch=label, time=time, quantity=key, values=values,
                                           decreases=all(later < earlier for earlier, later in zip(values, values[1:]))))
        evidence.report['collision_refinement'] = refinement
        evidence.report['both_branches_refine_all_declared_collision_norms'] = all(row['decreases'] for row in refinement)
        evidence.check('comparison_recorded_all_predeclared_norms', len(refinement) == 30)
        evidence.report['progress'] = dict(state='all_segments_saved')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()
