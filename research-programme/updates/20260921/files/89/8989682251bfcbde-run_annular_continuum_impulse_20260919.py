from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from run_annular_P2_continuum_bridge_20260918 import checked_load
from run_annular_P2_saved_impulse_20260919 import own_core
from scipy.integrate import DOP853
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    own_core(1)
    evidence = EvidenceRun('annular-continuum-source-impulse-attempt01', __file__)
    try:
        started = perf_counter()
        duration = 4e-5
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, original_force_requirement_unchanged=True,
            unchanged_characteristic_equations_and_preparation=True,
            augmented_observables_do_not_feed_back=True, duration=duration, maximum_wall_seconds=6000.,
            impulse_weights=[0, 1, 2], real_time_step_halving=True,
            oracle_differences_not_rigorous_error_enclosures=True)
        prior_path = evidence.output.parent/'annular-P2-live-exponential-short-continuum-attempt01/status.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        for degree in [384, 512]:
            oracle = BarycentricLiveContinuum(degree, 8, 18, radial_spacing=.025, label_order=12)
            old = checked_load(evidence, 'annular-P2-continuum-bridge-continuum-'+str(degree)+'-attempt01', 'trajectory.npz')
            initial = old['states'][0]
            previous_force = next(row['wave_force'] for row in prior['cases'] if row['kind'] == 'continuum' and row['degree'] == degree)
            for divisions in [8, 16]:
                initial_augmented = np.concatenate([initial, np.zeros(27)])
                tolerance = np.concatenate([np.full(len(initial), 2e-14), np.full(27, 2e-20)])
                calls = 0

                def rhs(time, augmented):
                    nonlocal calls
                    if perf_counter()-started > evidence.report['maximum_wall_seconds']:
                        raise RuntimeError('Continuum impulse wall budget reached; accepted states retained.')
                    calls += 1
                    flow, unused, forces = oracle.rhs_with_geometry(augmented[:-27])
                    weights = (time/duration)**np.arange(3)
                    impulses = weights[:, None]*forces['radiation'][None, :]
                    return np.concatenate([flow, impulses.ravel()])

                solver = DOP853(rhs, 0., initial_augmented, duration, first_step=duration/divisions,
                    max_step=duration/divisions, rtol=2e-12, atol=tolerance)
                targets = np.linspace(0., duration, 17)
                recorded_times, impulses, sampled_states = [0.], [np.zeros((3, 9))], [initial.copy()]
                target_index, accepted = 1, 0
                while solver.status == 'running':
                    solver.step()
                    if solver.status == 'failed':
                        raise RuntimeError('Augmented continuum solve failed.')
                    accepted += 1
                    dense = solver.dense_output()
                    while target_index < len(targets) and targets[target_index] <= solver.t:
                        sampled = dense(targets[target_index])
                        recorded_times.append(float(targets[target_index]))
                        impulses.append(sampled[-27:].reshape(3, 9))
                        sampled_states.append(sampled[:-27].copy())
                        target_index += 1
                    path = evidence.output/('degree'+str(degree)+'-max'+str(divisions)+'-accepted'+str(accepted).zfill(3)+'.npz')
                    np.savez_compressed(path, time=solver.t, state=solver.y[:-27], impulses=solver.y[-27:].reshape(3, 9))
                    evidence.own(path, 'outputs')
                    evidence.report.update(active_degree=degree, active_divisions=divisions, accepted_time=float(solver.t),
                        evaluations=calls, seconds=perf_counter()-started)
                    evidence.save()
                    if accepted % 4 == 0:
                        print(json.dumps(dict(degree=degree, divisions=divisions, accepted=accepted,
                            time=float(solver.t), seconds=perf_counter()-started)), flush=True)
                unused, geometry, forces = oracle.rhs_with_geometry(solver.y[:-27])
                force = float(forces['radiation'][4])
                evidence.check(str(degree)+'_'+str(divisions)+'_complete_finite', solver.t == duration
                    and target_index == len(targets) and np.all(np.isfinite(solver.y)))
                evidence.check(str(degree)+'_'+str(divisions)+'_same_endpoint_force', abs(force-previous_force) < 2e-10)
                path = evidence.output/('degree'+str(degree)+'-max'+str(divisions)+'-impulses.npz')
                np.savez_compressed(path, times=recorded_times, impulses=impulses, final_state=solver.y[:-27])
                evidence.own(path, 'outputs')
                observables = []
                for time, sampled_state in zip(recorded_times, sampled_states):
                    unused, sampled_geometry, sampled_forces = oracle.rhs_with_geometry(sampled_state)
                    source = sampled_geometry.material.source[4]
                    lapse, root = sampled_geometry.metric(source[0])
                    observables.append(dict(time=time, source_position=float(source[0]), material_momentum=float(source[1]),
                        source_velocity=float(sampled_forces['velocity'][4]), clock=float(sampled_forces['clock'][4]),
                        raw_material=float(sampled_forces['gravity'][4]), wave_force=float(sampled_forces['radiation'][4]),
                        lapse=float(lapse), radial_metric_root=float(root)))
                rows = []
                for fraction in [.25, .5, .75, 1.]:
                    index = int(round(16*fraction))
                    for power in [0, 1, 2]:
                        rows.append(dict(fraction=fraction, power=power, impulse=float(impulses[index][power, 4]), valid_for_claim=False))
                row = dict(degree=degree, maximum_step=duration/divisions, divisions=divisions, accepted_steps=accepted,
                    evaluations=calls, endpoint_force=force, old_endpoint_force=previous_force,
                    moments=rows, observables=observables, source_path=str(path.relative_to(evidence.root)), valid_for_claim=False)
                evidence.report['cases'].append(row)
                evidence.save()
                print(json.dumps(dict(degree=degree, divisions=divisions, accepted_steps=accepted,
                    impulse=rows[-3]['impulse'], endpoint_force=force, seconds=perf_counter()-started)), flush=True)
        for degree in [384, 512]:
            selected = [row for row in evidence.report['cases'] if row['degree'] == degree]
            evidence.check(str(degree)+'_maximum_step_really_halved', selected[0]['maximum_step'] == 2*selected[1]['maximum_step']
                and selected[1]['accepted_steps'] >= selected[0]['accepted_steps'])
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
