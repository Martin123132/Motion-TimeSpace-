from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_continuum_characteristics_20260915 import LiveContinuumCharacteristics
from run_annular_live_continuum_evolution_20260915 import proper_acceleration_test
from annular_live_continuum_comparison_tools_20260915 import oracle_difference
from scipy.integrate import solve_ivp
import numpy as np
import json
import time


def main():
    evidence = EvidenceRun('annular-live-continuum-refinement-attempt02', __file__)
    try:
        previous = evidence.output.parent/'annular-live-continuum-evolution-attempt01'
        failed = evidence.output.parent/'annular-live-continuum-refinement-attempt01/status.json'
        evidence.own(failed)
        evidence.check('unbounded_trial_step_failure_preserved', json.loads(failed.read_text())['state'] == 'failed')
        status_path = previous/'status.json'
        status = json.loads(status_path.read_text())
        evidence.own(status_path)
        evidence.check('previous_live_controls_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        started = time.perf_counter()
        system = LiveContinuumCharacteristics(384, 8, 18, radial_spacing=.025, label_order=12)
        state, initial_geometry = system.initial()
        times = np.linspace(0., .02, 5)
        states, calls = [state.copy()], 0
        max_step = 8/system.degree**2
        for lower, upper in zip(times[:-1], times[1:]):
            result = solve_ivp(system.rhs, (lower, upper), states[-1], method='DOP853', rtol=2e-10, atol=2e-12,
                               max_step=max_step, first_step=min(max_step, upper-lower), t_eval=[upper])
            if not result.success:
                raise RuntimeError(result.message)
            states.append(result.y[:, -1])
            calls += result.nfev
            raw = evidence.output/('accepted-time-'+format(upper, '.3f')+'.npz')
            np.savez_compressed(raw, time=upper, state=states[-1])
            evidence.own(raw, 'outputs')
            evidence.report['accepted_time'] = float(upper)
            evidence.report['rhs_calls'] = calls
            evidence.save()
            print(dict(accepted_time=upper, rhs_calls=calls, seconds=time.perf_counter()-started), flush=True)
        states = np.array(states)
        geometry = system.solve(states[-1])
        radial, current = geometry.check_radial(), system.current_test(states[-1])
        acceleration = proper_acceleration_test(system, states[-1])
        mass_drift = max(abs(system.solve(state).mass_nodes[-1, -1]-initial_geometry.mass_nodes[-1, -1]) for state in states)
        raw = evidence.output/'degree384.npz'
        np.savez_compressed(raw, times=times, states=states, mass=geometry.mass_nodes, radial_nodes=geometry.nodes,
                            log_lapse=geometry.log_lapse_nodes, **current)
        evidence.own(raw, 'outputs')
        row = dict(degree=384, layer_degree=8, radial_degree=18, radial_spacing=.025, label_order=12, width=.02,
                   coupling=.1, duration=.02, max_step=max_step, first_step=max_step, seconds=time.perf_counter()-started, rhs_calls=calls,
                   mass_radial_residual=radial[0], lapse_radial_residual=radial[1], current_error=current['error'],
                   proper_acceleration_error=acceleration['error'], exterior_mass_drift=float(mass_drift))
        evidence.report['cases'].append(row)
        evidence.save()
        print(row, flush=True)
        evidence.check('refined_independent_radial_constraints', max(radial) < 2e-8, row)
        evidence.check('refined_independent_mass_time_current', current['error'] < 2e-8, row)
        evidence.check('refined_unprojected_exterior_mass', mass_drift < 2e-9, row)
        evidence.check('refined_derived_proper_acceleration', acceleration['error'] < 2e-7, row)
        for degree in [96, 192]:
            old = previous/('degree'+str(degree)+'-main.npz')
            evidence.own(old)
            saved = np.load(old)
            coarse = LiveContinuumCharacteristics(degree, 4, 14, radial_spacing=.05)
            differences = oracle_difference(coarse, saved['states'], system, states)
            diagnostics = evidence.output/('degree'+str(degree)+'-comparison.npz')
            np.savez_compressed(diagnostics, times=times, differences=differences)
            evidence.own(diagnostics, 'outputs')
            comparison = dict(degree=degree, maximum_field_difference=float(np.max(differences[:, 0])),
                              source_difference=float(np.max(differences[:, 1])), velocity_difference=float(np.max(differences[:, 2])),
                              clock_difference=float(np.max(differences[:, 3])))
            evidence.report['cases'].append(comparison)
            evidence.save()
            print(comparison, flush=True)
        coarse, fine = evidence.report['cases'][-2:]
        evidence.check('independent_continuum_fields_refine', fine['maximum_field_difference'] < 2e-6
                       and fine['maximum_field_difference'] < .8*coarse['maximum_field_difference'], [coarse, fine])
        evidence.check('independent_continuum_source_and_clocks_refine', fine['source_difference'] < 1e-8
                       and fine['velocity_difference'] < 2e-7 and fine['clock_difference'] < 1e-8, fine)
        evidence.report.update(independent_common_live_geometry_continuum_evolved=True, numerical_trial_step_capped=True,
                               sampled_finite_time_continuum_accuracy_qualified=True, all_mesh_convergence_theorem=False,
                               original_equations_preparation_and_gates_unchanged=True,
                               source_and_geometry_equations_not_transplanted_from_cut_action=True,
                               same_original_repaired_live_preparation=True, finite_width_held_fixed=True,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
