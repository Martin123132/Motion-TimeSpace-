from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from run_annular_P2_continuum_bridge_20260918 import checked_load
from verify_annular_P2_live_exponential_direct_20260919 import encode
from run_annular_P2_live_exponential_20260919 import diagnostics
from scipy.integrate import DOP853
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-P2-indexed-full-pilot-control-MTS-attempt02', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False, branch='MTS',
            full_live_P2_force_convergence_proven=False, duration=4e-5, maximum_wall_seconds=2700.,
            no_modal_split_in_RK=True, previous_point004_window_not_retested=True,
            additional_endpoint_RK_refinement=True, maximum_step=1.25e-6, rtol=4e-13, atol=4e-15)
        previous_folder = 'annular-P2-indexed-full-pilot-control-MTS-attempt01'
        previous_path = evidence.output.parent/previous_folder/'status.json'
        previous = json.loads(previous_path.read_text())
        evidence.own(previous_path)
        evidence.check('previous_completed_control_failure_retained', previous['state'] == 'complete'
            and not previous['independent_short_pilot_agreement_pass'])
        old = checked_load(evidence, previous_folder, 'tight-trajectory.npz')
        basis = checked_load(evidence, 'annular-P2-live-exponential-MTS-257-attempt01', 'frozen-canonical-basis.npz')
        exponential = checked_load(evidence, 'annular-P2-live-exponential-MTS-257-attempt01', 'trajectory-steps16.npz')
        initial = old['states'][0]
        system = IndexedGradedP2System(257, True, 4e-5)
        calls = 0

        def rhs(time, state):
            nonlocal calls
            if perf_counter()-started > evidence.report['maximum_wall_seconds']:
                raise RuntimeError('Extra RK refinement safe budget reached; accepted states saved.')
            calls += 1
            return system.rhs(time, state)

        solver = DOP853(rhs, 0., initial.ravel(), evidence.report['duration'],
            first_step=evidence.report['maximum_step'], max_step=evidence.report['maximum_step'],
            rtol=evidence.report['rtol'], atol=evidence.report['atol'])
        states, times = [initial], [0.]
        while solver.status == 'running':
            solver.step()
            if solver.status == 'failed':
                raise RuntimeError('Further RK refinement failed.')
            states.append(solver.y.reshape(initial.shape).copy())
            times.append(float(solver.t))
            path = evidence.output/('accepted'+str(len(times)-1).zfill(3)+'.npz')
            np.savez_compressed(path, time=solver.t, state=states[-1])
            evidence.own(path, 'outputs')
            evidence.report.update(accepted_time=float(solver.t), calls=calls, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(dict(time=float(solver.t), calls=calls, seconds=perf_counter()-started)), flush=True)
        evidence.check('whole_short_horizon_reached', solver.t == evidence.report['duration']
            and solver.status == 'finished' and np.all(np.isfinite(states[-1])))
        path = evidence.output/'tight-trajectory.npz'
        np.savez_compressed(path, times=np.array(times), states=np.array(states))
        evidence.own(path, 'outputs')
        diagnostic = diagnostics(system, states[-1])
        previous_force = previous['cases'][-1]['endpoint']['reduced_wave_force']
        exponential_force = previous_force+0.
        pilot_path = evidence.output.parent/'annular-P2-live-exponential-MTS-257-attempt01/status.json'
        pilot = json.loads(pilot_path.read_text())
        evidence.own(pilot_path)
        exponential_force = pilot['cases'][-1]['reduced_wave_force']
        control_change = abs(diagnostic['reduced_wave_force']-previous_force)
        method_change = abs(diagnostic['reduced_wave_force']-exponential_force)
        scale = np.linalg.norm(encode(basis, initial)[:, :, :-1])
        state_change = float(np.linalg.norm(encode(basis, states[-1]-old['states'][-1])[:, :, :-1])/scale)
        method_state = float(np.linalg.norm(encode(basis, states[-1]-exponential['states'][-1])[:, :, :-1])/scale)
        evidence.check('endpoint_canonical_radial_and_current', diagnostic['canonical_residual'] < 2e-11
            and max(diagnostic['radial_residual']) < 2e-9 and diagnostic['noether']['residual'] < 2e-9)
        evidence.check('endpoint_Euler_and_regular_domain', diagnostic['noether']['source_euler'] < 2e-8
            and diagnostic['noether']['scalar_euler'] < 2e-8 and diagnostic['minimum_material_jacobian'] > 0
            and diagnostic['maximum_timelike_ratio'] < 1)
        prior_fields = previous['saved_time_differences']
        prior_state_pass = max(row['exponential_RK_relative_difference'] for row in prior_fields) < 1e-6
        prior_source_pass = max(row['source_gap'] for row in prior_fields) < 1e-9
        evidence.report.update(cases=[previous['cases'][-1], dict(tag='further_refined',
                maximum_step=evidence.report['maximum_step'], endpoint=diagnostic)],
            endpoint_force_RK_refinement_difference=control_change,
            endpoint_force_exponential_RK_difference=method_change,
            endpoint_relative_state_refinement=state_change, endpoint_relative_method_difference=method_state,
            inherited_seventeen_time_state_controls=prior_fields,
            refined_force_test_only_at_endpoint=True,
            independent_short_pilot_agreement_pass=bool(control_change < 2e-10 and method_change < 2e-9
                and state_change < 1e-8 and method_state < 1e-6 and prior_state_pass and prior_source_pass),
            previous_failed_coarse_control_preserved=True, seconds=perf_counter()-started, calls=calls)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', RK_force_change=control_change,
            method_force_change=method_change, passes=evidence.report['independent_short_pilot_agreement_pass'],
            seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
