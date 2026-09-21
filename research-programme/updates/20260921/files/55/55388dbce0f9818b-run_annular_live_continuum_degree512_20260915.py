from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from annular_live_jump_aware_comparison_20260915 import jump_aware_difference
from run_annular_live_continuum_evolution_20260915 import proper_acceleration_test
from scipy.integrate import solve_ivp
import numpy as np
import json
import time


def main():
    evidence = EvidenceRun('annular-live-continuum-degree512-attempt01', __file__)
    try:
        for folder in ['annular-live-continuum-refinement-attempt02', 'annular-live-oracle-jump-aware-refinement-attempt01']:
            path = evidence.output.parent/folder/'status.json'
            evidence.own(path)
            evidence.check(folder+'_failed_accuracy_test_preserved', json.loads(path.read_text())['state'] == 'failed')
        equivalent = evidence.output.parent/'annular-live-barycentric-equivalence-attempt01/status.json'
        evidence.own(equivalent)
        evidence.check('barycentric_same_interpolant_qualified', json.loads(equivalent.read_text())['state'] == 'complete')
        system = BarycentricLiveContinuum(512, 8, 18, radial_spacing=.025, label_order=12)
        started = time.perf_counter()
        initial, initial_geometry = system.initial()
        times, states, calls = np.linspace(0., .02, 5), [initial], 0
        max_step = 8/system.degree**2
        for lower, upper in zip(times[:-1], times[1:]):
            if time.perf_counter()-started > 7200:
                raise RuntimeError('Safe computation budget reached; keep accepted segments for continuation.')
            result = solve_ivp(system.rhs, (lower, upper), states[-1], method='DOP853', rtol=2e-10, atol=2e-12,
                               max_step=max_step, first_step=min(max_step, upper-lower), t_eval=[upper])
            if not result.success:
                raise RuntimeError(result.message)
            states.append(result.y[:, -1])
            calls += result.nfev
            raw = evidence.output/('accepted-time-'+format(upper, '.3f')+'.npz')
            np.savez_compressed(raw, time=upper, state=states[-1])
            evidence.own(raw, 'outputs')
            evidence.report.update(accepted_time=float(upper), rhs_calls=calls)
            evidence.save()
            print(dict(accepted_time=upper, rhs_calls=calls, seconds=time.perf_counter()-started), flush=True)
        states = np.array(states)
        geometry = system.solve(states[-1])
        radial, current = geometry.check_radial(), system.current_test(states[-1])
        acceleration = proper_acceleration_test(system, states[-1])
        mass_drift = max(abs(system.solve(state).mass_nodes[-1, -1]-initial_geometry.mass_nodes[-1, -1]) for state in states)
        raw = evidence.output/'degree512.npz'
        np.savez_compressed(raw, times=times, states=states, mass=geometry.mass_nodes, radial_nodes=geometry.nodes,
                            log_lapse=geometry.log_lapse_nodes, **current)
        evidence.own(raw, 'outputs')
        row = dict(degree=512, layer_degree=8, radial_degree=18, radial_spacing=.025, label_order=12, width=.02,
                   coupling=.1, duration=.02, max_step=max_step, seconds=time.perf_counter()-started, rhs_calls=calls,
                   mass_radial_residual=radial[0], lapse_radial_residual=radial[1], current_error=current['error'],
                   proper_acceleration_error=acceleration['error'], exterior_mass_drift=float(mass_drift))
        evidence.report['cases'].append(row)
        evidence.save()
        print(row, flush=True)
        evidence.check('refined_independent_radial_constraints', max(radial) < 2e-8, row)
        evidence.check('refined_independent_temporal_current', current['error'] < 2e-8, row)
        evidence.check('unprojected_exterior_mass', mass_drift < 2e-9, row)
        evidence.check('derived_proper_clock_acceleration', acceleration['error'] < 2e-7, row)
        summaries = []
        for degree in [192, 384]:
            if degree == 192:
                path = evidence.output.parent/'annular-live-continuum-evolution-attempt01/degree192-main.npz'
                coarse = BarycentricLiveContinuum(192, 4, 14, radial_spacing=.05)
            else:
                path = evidence.output.parent/'annular-live-continuum-refinement-attempt02/degree384.npz'
                coarse = BarycentricLiveContinuum(384, 8, 18, radial_spacing=.025, label_order=12)
            evidence.own(path)
            saved = np.load(path)
            differences = jump_aware_difference(coarse, saved['states'], system, states)
            diagnostic = evidence.output/('degree'+str(degree)+'-comparison.json')
            diagnostic.write_text(json.dumps(dict(times=times.tolist(), differences=differences), indent=2, allow_nan=False)+'\n', encoding='utf-8')
            evidence.own(diagnostic, 'outputs')
            summary = dict(degree=degree, **{name:max(item[name] for item in differences) for name in differences[0]})
            summaries.append(summary)
            evidence.report['cases'].append(summary)
            evidence.save()
            print(summary, flush=True)
        coarse, fine = summaries
        evidence.check('aligned_fields_meet_original_absolute_tolerance', fine['aligned_field_error'] < 2e-6
                       and fine['aligned_field_error'] < .8*coarse['aligned_field_error'], summaries)
        evidence.check('physical_L2_keeps_gap_and_refines', fine['physical_relative_L2_error'] < .001
                       and fine['physical_absolute_L2_error'] < 2e-6
                       and fine['physical_relative_L2_error'] < .8*coarse['physical_relative_L2_error'], summaries)
        evidence.check('source_gap_is_explicit_and_small', fine['maximum_source_gap'] < 1e-8, fine)
        evidence.report.update(independent_common_live_geometry_continuum_evolved=True,
                               sampled_finite_time_continuum_accuracy_qualified=True,
                               global_sup_across_displaced_jumps_not_claimed=True,
                               corrected_norm_does_not_mask_gap=True, one_sided_absolute_tolerance_unchanged=True,
                               source_equations_width_preparation_not_changed=True,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
