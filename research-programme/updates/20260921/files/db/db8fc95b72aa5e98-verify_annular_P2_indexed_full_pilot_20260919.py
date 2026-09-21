from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from run_annular_P2_continuum_bridge_20260918 import checked_load
from verify_annular_P2_live_exponential_direct_20260919 import encode
from run_annular_P2_live_exponential_20260919 import diagnostics
from scipy.integrate import DOP853
from time import perf_counter
import argparse
import contextlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-P2-indexed-full-pilot-control-'+args.branch+'-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, branch=args.branch, duration=4e-5,
            original_action_and_preparation_retained=True, no_modal_split_in_RK=True,
            indexed_kernel_not_identical_floating_point_implementation=True,
            original_indexed_RHS_agreement_prerequisite=True,
            independent_control_covers_whole_new_short_pilot=True,
            previous_point004_window_not_retested=True, maximum_wall_seconds=2700.)
        prerequisite = evidence.output.parent/'annular-P2-indexed-live-geometry-attempt01/status.json'
        qualified = json.loads(prerequisite.read_text())
        evidence.own(prerequisite)
        evidence.check('indexed_kernel_qualified_before_evolution', qualified['state'] == 'complete'
            and all(row['passed'] for row in qualified['checks']))
        source = 'annular-P2-live-exponential-'+args.branch+'-257-attempt01'
        basis = checked_load(evidence, source, 'frozen-canonical-basis.npz')
        target = checked_load(evidence, source, 'trajectory-steps16.npz')
        source_status_path = evidence.output.parent/source/'status.json'
        source_status = json.loads(source_status_path.read_text())
        evidence.own(source_status_path)
        initial, times = basis['initial'], target['times']
        evidence.check('same_initial_state_and_short_horizon', np.array_equal(initial, target['states'][0])
            and times[0] == 0. and times[-1] == evidence.report['duration'])
        system = IndexedGradedP2System(257, args.branch == 'MTS', 4e-5)
        calls = 0

        def rhs(time, state):
            nonlocal calls
            if perf_counter()-started > evidence.report['maximum_wall_seconds'] or calls >= 800:
                raise RuntimeError('Safe indexed-control budget reached; accepted states retained.')
            calls += 1
            return system.rhs(time, state)

        trajectories, controls = [], []
        for tag, maximum_step, tolerance in [('standard', 5e-6, 1e-11), ('tight', 2.5e-6, 2e-12)]:
            solver = DOP853(rhs, 0., initial.ravel(), float(times[-1]), first_step=maximum_step,
                max_step=maximum_step, rtol=tolerance, atol=tolerance/100)
            saved = np.empty_like(target['states'])
            saved[0] = initial
            filled, accepted, first_calls = 1, 0, calls
            while solver.status == 'running':
                solver.step()
                if solver.status == 'failed':
                    raise RuntimeError('Indexed original-equation DOP853 failed.')
                accepted += 1
                interpolant = solver.dense_output()
                while filled < len(times) and times[filled] <= solver.t:
                    saved[filled] = interpolant(float(times[filled])).reshape(initial.shape)
                    filled += 1
                path = evidence.output/(tag+'-accepted'+str(accepted).zfill(3)+'.npz')
                np.savez_compressed(path, time=solver.t, state=solver.y.reshape(initial.shape))
                evidence.own(path, 'outputs')
                evidence.report.update(active=tag, accepted_time=float(solver.t), accepted_steps=accepted,
                    filled_samples=filled, calls=calls, seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(dict(branch=args.branch, phase=tag, time=float(solver.t),
                    calls=calls, seconds=perf_counter()-started)), flush=True)
            evidence.check(tag+'_all_requested_times_saved', solver.status == 'finished' and filled == len(times)
                and np.all(np.isfinite(saved)))
            path = evidence.output/(tag+'-trajectory.npz')
            np.savez_compressed(path, times=times, states=saved)
            evidence.own(path, 'outputs')
            diagnostic = diagnostics(system, saved[-1])
            evidence.check(tag+'_canonical_radial_and_regular_endpoint', diagnostic['canonical_residual'] < 2e-11
                and max(diagnostic['radial_residual']) < 2e-9 and diagnostic['maximum_timelike_ratio'] < 1
                and diagnostic['minimum_material_jacobian'] > 0)
            evidence.check(tag+'_current_Euler_endpoint', diagnostic['noether']['residual'] < 2e-9
                and diagnostic['noether']['source_euler'] < 2e-8 and diagnostic['noether']['scalar_euler'] < 2e-8)
            controls.append(diagnostic)
            trajectories.append(saved)
            evidence.report['cases'].append(dict(tag=tag, maximum_step=maximum_step, rtol=tolerance,
                accepted_steps=accepted, RHS_calls_after_initialization=calls-first_calls, endpoint=diagnostic))
            evidence.save()
        scale = np.linalg.norm(encode(basis, initial)[:, :, :-1])
        differences = []
        for index, time in enumerate(times):
            rk_difference = np.linalg.norm(encode(basis, trajectories[0][index]-trajectories[1][index])[:, :, :-1])/scale
            method_difference = np.linalg.norm(encode(basis, target['states'][index]-trajectories[1][index])[:, :, :-1])/scale
            source_gap = np.max(abs(target['states'][index, 0, :, -1]-trajectories[1][index, 0, :, -1]))
            differences.append(dict(time=float(time), RK_relative_difference=float(rk_difference),
                exponential_RK_relative_difference=float(method_difference), source_gap=float(source_gap)))
        force_rk_error = abs(controls[0]['reduced_wave_force']-controls[1]['reduced_wave_force'])
        force_method_error = abs(source_status['cases'][-1]['reduced_wave_force']-controls[1]['reduced_wave_force'])
        state_gate = max(row['RK_relative_difference'] for row in differences) < 1e-8
        method_gate = max(row['exponential_RK_relative_difference'] for row in differences) < 1e-6
        source_gate = max(row['source_gap'] for row in differences) < 1e-9
        evidence.report.update(saved_time_differences=differences,
            endpoint_force_RK_refinement_difference=force_rk_error,
            endpoint_force_exponential_RK_difference=force_method_error,
            independent_short_pilot_agreement_pass=bool(state_gate and method_gate and source_gate
                and force_rk_error < 2e-10 and force_method_error < 2e-9),
            endpoint_force_only_not_all_time_force_bound=True,
            spatial_force_convergence_claim=False, seconds=perf_counter()-started, total_RHS_calls=calls)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(branch=args.branch, state='complete',
            force_RK_difference=force_rk_error, force_method_difference=force_method_error,
            passes=evidence.report['independent_short_pilot_agreement_pass'], seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
