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
    evidence = EvidenceRun('annular-P2-bulk513-first-step-'+args.branch+'-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False, branch=args.branch,
            full_live_P2_force_convergence_proven=False, no_modal_split_in_RK=True,
            base_count=513, source_cap=1e-5, duration=4e-5/64, maximum_wall_seconds=1800.,
            independent_first_step_only=True, independent_full_short_pilot_control=False,
            unchanged_action_source_Gram_and_preparation=True)
        folder = 'annular-P2-bulk513-evolution-'+args.branch+'-attempt01'
        basis = checked_load(evidence, folder, 'frozen-canonical-basis.npz')
        exponential = checked_load(evidence, folder, 'steps64-accepted001.npz')
        evidence.check('same_first_fine_time', float(exponential['time']) == evidence.report['duration'])
        initial = basis['initial']
        system = IndexedGradedP2System(513, args.branch == 'MTS', 1e-5)
        states = []
        calls = 0

        def rhs(time, state):
            nonlocal calls
            if perf_counter()-started > evidence.report['maximum_wall_seconds']:
                raise RuntimeError('First-step independent control wall limit reached.')
            calls += 1
            return system.rhs(time, state)

        for tag, divisor, tolerance in [('standard', 1, 1e-11), ('tight', 2, 2e-12)]:
            step = evidence.report['duration']/divisor
            solver = DOP853(rhs, 0., initial.ravel(), evidence.report['duration'],
                first_step=step, max_step=step, rtol=tolerance, atol=tolerance/100)
            accepted = 0
            while solver.status == 'running':
                solver.step()
                if solver.status == 'failed':
                    raise RuntimeError('Independent physical RHS integration failed.')
                accepted += 1
                path = evidence.output/(tag+'-accepted'+str(accepted).zfill(3)+'.npz')
                np.savez_compressed(path, time=solver.t, state=solver.y.reshape(initial.shape))
                evidence.own(path, 'outputs')
                evidence.report.update(active=tag, accepted_time=float(solver.t), calls=calls, seconds=perf_counter()-started)
                evidence.save()
            state = solver.y.reshape(initial.shape)
            endpoint = diagnostics(system, state)
            evidence.check(tag+'_endpoint_constraints_and_current', endpoint['canonical_residual'] < 2e-11
                and max(endpoint['radial_residual']) < 2e-9 and endpoint['noether']['residual'] < 2e-9
                and endpoint['noether']['source_euler'] < 2e-8 and endpoint['noether']['scalar_euler'] < 2e-8)
            evidence.check(tag+'_regular_domain', endpoint['minimum_material_jacobian'] > 0
                and endpoint['maximum_timelike_ratio'] < 1)
            evidence.report['cases'].append(dict(tag=tag, maximum_step=step, tolerance=tolerance,
                accepted_steps=accepted, endpoint=endpoint))
            states.append(state.copy())
        exp_endpoint = diagnostics(system, exponential['state'])
        evidence.check('exponential_endpoint_constraints', exp_endpoint['canonical_residual'] < 2e-11
            and max(exp_endpoint['radial_residual']) < 2e-9)
        scale = np.linalg.norm(encode(basis, initial)[:, :, :-1])
        control_state = float(np.linalg.norm(encode(basis, states[-1]-states[0])[:, :, :-1])/scale)
        method_state = float(np.linalg.norm(encode(basis, states[-1]-exponential['state'])[:, :, :-1])/scale)
        control_force = abs(evidence.report['cases'][1]['endpoint']['reduced_wave_force']
            -evidence.report['cases'][0]['endpoint']['reduced_wave_force'])
        method_force = abs(evidence.report['cases'][1]['endpoint']['reduced_wave_force']-exp_endpoint['reduced_wave_force'])
        source_gap = float(np.max(abs(states[-1][0, :, -1]-exponential['state'][0, :, -1])))
        evidence.report.update(RK_relative_state_change=control_state, method_relative_state_change=method_state,
            RK_force_change=control_force, method_force_change=method_force, source_gap=source_gap,
            independent_first_step_agreement_pass=bool(control_state < 1e-8 and method_state < 1e-6
                and control_force < 2e-10 and method_force < 2e-9 and source_gap < 1e-9),
            exponential_endpoint=exp_endpoint, seconds=perf_counter()-started, calls=calls)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', branch=args.branch, RK_force_change=control_force,
            method_force_change=method_force, passes=evidence.report['independent_first_step_agreement_pass'],
            seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
