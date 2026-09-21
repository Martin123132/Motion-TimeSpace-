from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import GradedP2System
from run_annular_P2_continuum_bridge_20260918 import checked_load
from run_annular_P2_live_exponential_20260919 import diagnostics
from scipy.integrate import DOP853
from time import perf_counter
import argparse
import contextlib
import json
import numpy as np


def encode(basis, delta):
    result = delta.copy()
    for index, (modes, mass_modes) in enumerate(zip(basis['modes'], basis['mass_modes'])):
        result[0, index, :-1] = basis['frequency'][index, :-1]*(mass_modes.T @ delta[0, index, :-1])
        result[1, index, :-1] = modes.T @ delta[1, index, :-1]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-P2-live-exponential-direct-'+args.branch+'-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, branch=args.branch,
            independent_original_physical_RHS_used=True, no_modal_split_in_DOP853=True,
            same_initial_canonical_state=True, short_control_not_full_window_comparison=True,
            duration=2.5e-6, maximum_wall_seconds=3600., original_force_readout=True)
        source = 'annular-P2-live-exponential-'+args.branch+'-257-attempt01'
        basis = checked_load(evidence, source, 'frozen-canonical-basis.npz')
        target = checked_load(evidence, source, 'steps16-accepted001.npz')
        initial, duration = basis['initial'], float(target['time'])
        evidence.check('matching_first_fine_step', duration == evidence.report['duration'])
        system = GradedP2System(257, args.branch == 'MTS', 4e-5)
        evaluations = 0

        def rhs(time, state):
            nonlocal evaluations
            if perf_counter()-started > evidence.report['maximum_wall_seconds']:
                raise RuntimeError('Direct-control safe budget reached; accepted steps retained.')
            evaluations += 1
            if evaluations > 120:
                raise RuntimeError('Direct-control evaluation cap reached; accepted steps retained.')
            return system.rhs(time, state)

        endpoints = []
        for tag, tolerance in [('standard', 1e-11), ('tight', 2e-12)]:
            first_evaluation = evaluations
            solver = DOP853(rhs, 0., initial.ravel(), duration, first_step=duration,
                max_step=duration, rtol=tolerance, atol=tolerance/100)
            accepted = 0
            while solver.status == 'running':
                solver.step()
                if solver.status == 'failed':
                    raise RuntimeError('Original RHS DOP853 step failed.')
                accepted += 1
                path = evidence.output/(tag+'-accepted'+str(accepted).zfill(3)+'.npz')
                np.savez_compressed(path, time=solver.t, state=solver.y.reshape(initial.shape))
                evidence.own(path, 'outputs')
                evidence.report.update(active_tolerance=tag, accepted_time=float(solver.t),
                    accepted_steps=accepted, evaluations=evaluations, seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(dict(branch=args.branch, tag=tag, time=float(solver.t),
                    evaluations=evaluations, seconds=perf_counter()-started)), flush=True)
            evidence.check(tag+'_reached_endpoint', solver.status == 'finished' and solver.t == duration)
            endpoints.append(solver.y.reshape(initial.shape).copy())
            evidence.report['cases'].append(dict(tolerance=tag, rtol=tolerance, atol=tolerance/100,
                evaluations=evaluations-first_evaluation, accepted_steps=accepted))
        energy_scale = np.linalg.norm(encode(basis, initial)[:, :, :-1])
        control_error = float(np.linalg.norm(encode(basis, endpoints[0]-endpoints[1])[:, :, :-1])/energy_scale)
        method_error = float(np.linalg.norm(encode(basis, target['state']-endpoints[1])[:, :, :-1])/energy_scale)
        standard = diagnostics(system, endpoints[0])
        explicit = diagnostics(system, endpoints[1])
        exponential = diagnostics(system, target['state'])
        force_control_error = abs(standard['reduced_wave_force']-explicit['reduced_wave_force'])
        force_difference = abs(explicit['reduced_wave_force']-exponential['reduced_wave_force'])
        source_gap = float(np.max(abs(target['state'][0, :, -1]-endpoints[1][0, :, -1])))
        evidence.report.update(relative_energy_RK_tolerance_difference=control_error,
            relative_energy_exponential_vs_RK_difference=method_error,
            source_position_difference=source_gap, force_difference=force_difference,
            independent_standard_diagnostics=standard,
            independent_explicit_diagnostics=explicit, exponential_diagnostics=exponential,
            force_RK_tolerance_difference=force_control_error,
            short_algorithm_agreement_pass=bool(control_error < 1e-8 and method_error < 1e-6
                and force_control_error < 2e-10 and force_difference < 2e-9 and source_gap < 1e-9),
            force_RK_tolerance_uncertainty_not_separately_extracted=False,
            continuum_accuracy_claim=False, evaluations=evaluations, seconds=perf_counter()-started)
        for tag, row in [('standard', standard), ('explicit', explicit), ('exponential', exponential)]:
            evidence.check(tag+'_endpoint_domain_constraints', row['canonical_residual'] < 2e-11
                and max(row['radial_residual']) < 2e-9 and row['maximum_timelike_ratio'] < 1
                and row['minimum_material_jacobian'] > 0)
        evidence.check('RK_tolerance_change_small', control_error < 1e-8, control_error)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(branch=args.branch, state='complete',
            method_error=method_error, force_difference=force_difference,
            passes=evidence.report['short_algorithm_agreement_pass'], seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
