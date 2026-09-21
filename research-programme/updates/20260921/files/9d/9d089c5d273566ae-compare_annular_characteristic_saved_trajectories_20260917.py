from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_characteristic_field_20260917 import FullCharacteristicField
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from datetime import datetime, timezone
import argparse
import hashlib
import json
import numpy as np


def field_error(system, state, reference, instant, order):
    coordinates, rates = np.split(state[:-1], 2)
    mapped_edges = system.mapping(system.edges, coordinates[-1])[0]
    edges = np.unique(np.concatenate([mapped_edges, reference.breakpoints(instant)]))
    nodes, weights = np.polynomial.legendre.leggauss(order)
    radius = ((edges[:-1, None]+edges[1:, None])/2+np.diff(edges)[:, None]*nodes/2).ravel()
    measure = (np.diff(edges)[:, None]*weights/2).ravel()
    left = radius < coordinates[-1]
    pulled = np.where(left, 5.2+(radius-5.2)*(6.03-5.2)/(coordinates[-1]-5.2),
        6.8-(6.8-radius)*(6.8-6.03)/(6.8-coordinates[-1]))
    unused, unused2, temporal, gradient = system.sample(pulled, coordinates, rates)
    exact = reference.sample(instant, radius)
    numerator = np.dot(measure*radius**2, (temporal-exact['phi_t'])**2+(gradient-exact['phi_r'])**2)
    denominator = np.dot(measure*radius**2, exact['phi_t']**2+exact['phi_r']**2)
    return float(np.sqrt(numerator/denominator))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, original_trajectories_reused_not_rerun=True,
            finite_future_trajectories_read=False, force_fit=False, force_correction=False,
            all_branches_treated_identically=True, full_characteristic_reference_not_full_GR=True,
            original_physical_gates_unchanged=True, implementation_checks_not_physical_passes=True,
            quadrature_field_control_gate=1e-6, reference_tighter_control_inherited_not_interval_certificate=True)
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        folder = intake/'annular-full-characteristic-field-attempt01'
        path = folder/'status.json'
        evidence.own(path)
        status = json.loads(path.read_text())
        evidence.check('reference_qualified_before_comparison', status['state'] == 'complete'
            and all(row['passed'] for row in status['checks']) and not status['finite_future_trajectories_read'])
        for table in ['inputs', 'outputs']:
            for name, digest in status[table].items():
                path = evidence.root/name
                if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                    raise RuntimeError('Changed reference input: '+name)
                evidence.own(path)
        with np.load(folder/'full-characteristic-reference.npz', allow_pickle=False) as saved:
            times, source, exact_force = saved['times'].copy(), saved['source_states'].copy(), saved['forces'].copy()
        reference = FullCharacteristicField(tight=True)
        evidence.check('frozen_source_reproduced', np.max(abs(reference.source.sol(times).T-source)) < 3e-12)
        evidence.report['qualified_reference_verified_at'] = datetime.now(timezone.utc).isoformat()
        evidence.report['finite_future_trajectories_read'] = True
        evidence.report['finite_read_started_at'] = datetime.now(timezone.utc).isoformat()
        evidence.save()
        old_folder = intake/'annular-dense-GR-references-attempt01'
        path = old_folder/'status.json'
        evidence.own(path)
        old_status = json.loads(path.read_text())
        evidence.check('old_spectral_reference_complete', old_status['state'] == 'complete')
        path = old_folder/'oracle-768.npz'
        evidence.own(path)
        evidence.check('old_reference_hash', hashlib.sha256(path.read_bytes()).hexdigest() == old_status['outputs'][str(path.relative_to(evidence.root))])
        with np.load(path, allow_pickle=False) as saved:
            evidence.check('same_old_reference_times', np.array_equal(times, saved['times']))
            old_force = saved['forces'].copy()
        for count, label in [(513, 'annular-joint-rectangle-attempt01'), (1025, 'annular-joint-finer1025-attempt01')]:
            folder = intake/label
            path = folder/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(str(count)+'_saved_run_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            for branch in ['reference', 'MTS']:
                prefix = branch+str(count)
                path = folder/(branch+str(count)+'-8-trajectory.npz')
                evidence.own(path)
                evidence.check(prefix+'_saved_trajectory_hash', hashlib.sha256(path.read_bytes()).hexdigest() == status['outputs'][str(path.relative_to(evidence.root))])
                with np.load(path, allow_pickle=False) as saved:
                    evidence.check(prefix+'_same_times', np.array_equal(saved['times'], times))
                    states, forces = saved['states'].copy(), saved['forces'].copy()
                system = LocallyRefinedSourceAction(count, branch == 'MTS', background_mass=0., source_splits=8)
                evidence.check(prefix+'_shape', states.shape == (81, 2*system.count+3))
                field6, field10 = [], []
                for index, (instant, state) in enumerate(zip(times, states)):
                    field6.append(field_error(system, state, reference, instant, 6))
                    field10.append(field_error(system, state, reference, instant, 10))
                    if index % 20 == 0:
                        evidence.report['progress'] = dict(branch=branch, count=count, accepted_sample=index, time=float(instant))
                        evidence.save()
                        print(evidence.report['progress'], flush=True)
                quadrature_control = float(np.max(abs(np.asarray(field6)-field10)))
                evidence.check(prefix+'_field_quadrature_control', quadrature_control < 1e-6, quadrature_control)
                replay_errors = []
                for index in [0, 42, 80]:
                    coordinates, rates = np.split(states[index, :-1], 2)
                    acceleration = system.acceleration(times[index], coordinates, rates)[-1]
                    replay_errors.append(abs(system.source_mass*acceleration/(1-rates[-1]**2)**1.5-forces[index]))
                evidence.check(prefix+'_original_force_replay', max(replay_errors) < 2e-11, float(max(replay_errors)))
                source_error = states[:, system.count]-source[:, 0]
                velocity_error = states[:, -2]-source[:, 1]
                clock_error = states[:, -1]-source[:, 2]
                force_error = forces-exact_force
                old_force_error = forces-old_force
                final_relative = float(abs(force_error[-1]/exact_force[-1]))
                row = dict(branch=branch, base_count=count, source_splits=8,
                    maximum_relative_field_error=float(max(field10)), field_quadrature_control=quadrature_control,
                    maximum_source_error=float(max(abs(source_error))), maximum_velocity_error=float(max(abs(velocity_error))),
                    maximum_clock_error=float(max(abs(clock_error))), maximum_force_error=float(max(abs(force_error))),
                    old_reference_maximum_force_error=float(max(abs(old_force_error))),
                    terminal_force_error=float(force_error[-1]), terminal_relative_force_error=final_relative,
                    field_gate_pass=bool(max(field10) < .005),
                    source_clock_gate_pass=bool(max(abs(source_error)) < 5e-7 and max(abs(velocity_error)) < 2e-5 and max(abs(clock_error)) < 2e-7),
                    peak_absolute_force_gate_pass=bool(max(abs(force_error)) < 2e-7),
                    terminal_combined_force_gate_pass=bool(abs(force_error[-1]) < 2e-7 and final_relative < .02),
                    full_GR_limit_proven=False)
                destination = evidence.output/(prefix+'-comparison.npz')
                np.savez_compressed(destination, times=times, field_error=field10, field_error_order6=field6,
                    source_error=source_error, velocity_error=velocity_error, clock_error=clock_error,
                    force_error=force_error, old_force_error=old_force_error, original_forces=forces,
                    characteristic_forces=exact_force)
                evidence.own(destination, 'outputs')
                evidence.report['cases'].append(row)
                evidence.save()
                print(row, flush=True)
        evidence.report['refinement'] = []
        for branch in ['reference', 'MTS']:
            coarse, fine = [next(row for row in evidence.report['cases'] if row['branch'] == branch and row['base_count'] == count) for count in [513, 1025]]
            evidence.report['refinement'].append(dict(branch=branch,
                field_ratio=fine['maximum_relative_field_error']/coarse['maximum_relative_field_error'],
                force_peak_ratio=fine['maximum_force_error']/coarse['maximum_force_error'],
                two_grid_comparison_not_uniform_convergence_proof=True))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
