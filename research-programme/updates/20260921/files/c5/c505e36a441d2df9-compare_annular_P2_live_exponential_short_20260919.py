from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from annular_P2_graded_source_20260919 import GradedP2System
from run_annular_P2_continuum_bridge_20260918 import checked_load
from compare_annular_P2_continuum_bridge_20260918 import physical_comparison
from annular_live_jump_aware_comparison_20260915 import jump_aware_difference
from scipy.integrate import solve_ivp
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-P2-live-exponential-short-continuum-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, duration=4e-5,
            full_window_not_retested=True, finite_spatial_refinement_not_supplied=True,
            original_force_gates_not_replaced=True, same_analytic_preparation=True,
            sampled_continuum_peak_scale=5.401196245463084e-6,
            force_absolute_gate=2e-7, force_peak_relative_gate=.005,
            oracle_force_difference_budget=2e-9, waveform_relative_gate=.005,
            source_position_gate=5e-7, source_velocity_gate=2e-5, clock_rate_gate=2e-7)
        targets = {}
        for degree in [384, 512]:
            oracle = BarycentricLiveContinuum(degree, 8, 18, radial_spacing=.025, label_order=12)
            saved = checked_load(evidence, 'annular-P2-continuum-bridge-continuum-'+str(degree)+'-attempt01', 'trajectory.npz')
            evidence.check('oracle_'+str(degree)+'_initial_time_zero', saved['times'][0] == 0.)
            maximum_step = 8/degree**2
            solution = solve_ivp(oracle.rhs, (0., evidence.report['duration']), saved['states'][0],
                method='DOP853', rtol=2e-12, atol=2e-14, max_step=maximum_step,
                first_step=min(maximum_step, evidence.report['duration']), t_eval=[evidence.report['duration']])
            evidence.check('oracle_'+str(degree)+'_finished', solution.success and np.all(np.isfinite(solution.y)))
            state = solution.y[:, -1]
            unused, geometry, forces = oracle.rhs_with_geometry(state)
            target = dict(system=oracle, geometry=geometry, state=state, force=float(forces['radiation'][4]))
            targets[degree] = target
            path = evidence.output/('continuum'+str(degree)+'.npz')
            np.savez_compressed(path, time=evidence.report['duration'], state=state)
            evidence.own(path, 'outputs')
            evidence.report['cases'].append(dict(kind='continuum', degree=degree, evaluations=solution.nfev,
                wave_force=target['force'], seconds=perf_counter()-started))
            evidence.save()
        oracle_error = abs(targets[384]['force']-targets[512]['force'])
        evidence.check('independent_oracle_force_refinement', oracle_error < evidence.report['oracle_force_difference_budget'], oracle_error)
        oracle_fields = jump_aware_difference(targets[384]['system'], np.array([targets[384]['state']]),
            targets[512]['system'], np.array([targets[512]['state']]))
        evidence.report['oracle_field_refinement'] = oracle_fields
        evidence.check('independent_oracle_waveform_refinement', max(row['physical_relative_L2_error']
            for row in oracle_fields) < .001 and max(row['aligned_field_error'] for row in oracle_fields) < 2e-6
            and max(row['maximum_source_gap'] for row in oracle_fields) < 1e-8, oracle_fields)
        fine = targets[512]
        rows = []
        for branch in ['reference', 'MTS']:
            folder = 'annular-P2-live-exponential-'+branch+'-257-attempt01'
            status_path = evidence.output.parent/folder/'status.json'
            status = json.loads(status_path.read_text())
            evidence.own(status_path)
            saved = checked_load(evidence, folder, 'trajectory-steps16.npz')
            evidence.check(branch+'_matching_time_and_scope', saved['times'][-1] == evidence.report['duration']
                and status['state'] == 'complete' and not status['full_live_P2_force_convergence_proven'])
            coordinates, momenta = saved['states'][-1]
            system = GradedP2System(257, branch == 'MTS', 4e-5)
            rates, geometry = system.solve(coordinates, momenta)
            comparison = physical_comparison(system, coordinates, rates, geometry, fine['system'], fine['geometry'])
            force = status['cases'][-1]['reduced_wave_force']
            error = abs(force-fine['force'])
            threshold = min(evidence.report['force_absolute_gate'],
                evidence.report['force_peak_relative_gate']*evidence.report['sampled_continuum_peak_scale'])
            material_pass = (comparison['source_error'] <= evidence.report['source_position_gate']
                and comparison['velocity_error'] <= evidence.report['source_velocity_gate']
                and comparison['clock_rate_error'] <= evidence.report['clock_rate_gate'])
            row = dict(branch=branch, time=evidence.report['duration'], force=force,
                continuum_force=fine['force'], force_error=error, force_threshold=threshold,
                instantaneous_force_relative_error=error/max(abs(fine['force']), 1e-300),
                force_peak_relative_error=error/evidence.report['sampled_continuum_peak_scale'],
                short_endpoint_force_gate_pass=bool(error <= threshold),
                short_endpoint_waveform_gate_pass=bool(comparison['field_error'] <= evidence.report['waveform_relative_gate']),
                short_endpoint_source_and_clock_gate_pass=bool(material_pass),
                short_endpoint_combined_gate_pass=bool(error <= threshold
                    and comparison['field_error'] <= evidence.report['waveform_relative_gate']
                    and status['empirical_final_time_budget_pass'] and material_pass),
                empirical_time_budget_pass=status['empirical_final_time_budget_pass'],
                full_interval_gate_pass=False, spatial_force_convergence_claim=False, **comparison)
            rows.append(row)
            evidence.report['cases'].append(dict(kind='finite', **row))
            evidence.save()
        evidence.report.update(results=rows, oracle_force_difference=oracle_error, seconds=perf_counter()-started,
            valid_for_physics_claim=False, full_GR_limit_proven=False)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', results=rows, oracle_difference=oracle_error,
            seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
