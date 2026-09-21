from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_current_20260918 import EvolvingP2System, LiveP2Tangent, P2Material
from scipy.integrate import solve_ivp
from time import perf_counter
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-live-P2-current-evolution-attempt01', __file__)
    try:
        qualification = evidence.root/'source-intake/navier-stokes/20260914/annular-live-P2-independent-current-attempt01/status.json'
        current_status = json.loads(qualification.read_text())
        evidence.check('independent_initial_current_qualified_first', current_status['state'] == 'complete'
            and all(row['passed'] for row in current_status['checks']))
        evidence.own(qualification)
        evidence.report.update(no_forward_evolution=False, short_forward_evolution=True,
            github_action=False, subagents_used=False, mass_or_current_projection_used=False,
            initial_and_final_current_from_explicit_horizontal_extension=True,
            unique_parent_shift_extension_proven=False, arbitrary_covariance_proven=False,
            full_live_P2_force_convergence_proven=False, time_and_label_refinement_separate=True,
            current_not_defined_from_radial_mass_derivative=True)
        duration = .004
        trajectories = {}
        for mode, layer_degree, step, wave in [('principal', 6, .001, True), ('half_step', 6, .0005, True),
                ('label_refined', 8, .001, True), ('zero_wave', 6, .001, False)]:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                key = branch+'_'+mode
                started = perf_counter()
                print('Starting '+key, flush=True)
                system = EvolvingP2System(17, gram, layer_degree=layer_degree, radial_degree=18)
                coordinates, momenta, unused, unused2 = system.initial(wave=wave)
                initial = np.stack([coordinates, momenta]).ravel()
                solution = solve_ivp(system.rhs, (0., duration), initial, method='DOP853',
                    rtol=2e-10, atol=2e-12, max_step=step, t_eval=np.linspace(0., duration, 5))
                states = solution.y.T.reshape(-1, 2, len(system.labels), system.count+1)
                diagnostics, rates_saved, mass_profiles = [], [], []
                probes = np.array([5.28, 5.57, 5.91, 6.024, 6.0313, 6.037, 6.25, 6.72])
                for time, state in zip(solution.t, states):
                    position, momentum = state
                    rates, geometry = system.solve(position, momentum)
                    material = P2Material(system, position)
                    lapse, root = geometry.metric(position[:, -1])
                    diagnostics.append(dict(time=float(time), exterior_mass=float(geometry.mass_nodes[-1, -1]),
                        source_minimum_jacobian=material.minimum_jacobian,
                        spatial_minimum_jacobian=material.minimum_spatial_jacobian,
                        timelike_ratio=float(max(abs(rates[:, -1]/(lapse*root)))),
                        momentum_residual=system.canonical_residual(position, momentum, rates, geometry)))
                    rates_saved.append(rates)
                    mass_profiles.append(geometry.values(probes)[0])
                destination = evidence.output/(key+'.npz')
                np.savez_compressed(destination, times=solution.t, states=states, rates=np.array(rates_saved),
                    probes=probes, masses=np.array(mass_profiles), labels=system.labels)
                evidence.own(destination, 'outputs')
                row = dict(branch=branch, mode=mode, duration=duration, maximum_step=step,
                    base_count=17, layer_degree=layer_degree, radial_degree=18, wave=wave,
                    solver_success=bool(solution.success), solver_message=solution.message, evaluations=int(solution.nfev),
                    mass_drift=max(abs(item['exterior_mass']-diagnostics[0]['exterior_mass']) for item in diagnostics),
                    interior_mass_change=float(max(abs(np.array(mass_profiles)[-1]-mass_profiles[0]))),
                    source_displacement=float(states[-1, 0, layer_degree//2, -1]-states[0, 0, layer_degree//2, -1]),
                    diagnostics=diagnostics)
                evidence.report['cases'].append(row)
                evidence.save()
                evidence.check(key+'_completed_full_short_interval', solution.success and len(states) == 5 and solution.t[-1] == duration, solution.message)
                evidence.check(key+'_unprojected_exterior_mass', row['mass_drift'] < 2e-9, row['mass_drift'])
                evidence.check(key+'_canonical_ordered_timelike', all(item['momentum_residual'] < 2e-10
                    and item['source_minimum_jacobian'] > 0 and item['spatial_minimum_jacobian'] > 0
                    and item['timelike_ratio'] < 1 for item in diagnostics), diagnostics)
                evidence.check(key+'_nontrivial_motion_and_geometry', row['source_displacement'] > 1e-5 and row['interior_mass_change'] > 1e-7,
                    [row['source_displacement'], row['interior_mass_change']])
                if mode == 'principal':
                    tangent = LiveP2Tangent(system, *states[-1])
                    compared = tangent.compare(probes, label_order=12)
                    row['final_current'] = compared
                    row['final_radial_residual'] = tangent.geometry.off_grid_residual(tangent.rates)
                    evidence.check(key+'_evolved_independent_current', max(item['error'] for item in compared) < 2e-8, compared)
                    evidence.check(key+'_evolved_on_shell_current', max(item['on_shell_error'] for item in compared) < 2e-8)
                    evidence.check(key+'_evolved_radial_equations', max(row['final_radial_residual']) < 2e-7, row['final_radial_residual'])
                trajectories[key] = (system, states, np.array(rates_saved), np.array(mass_profiles))
                row['seconds'] = perf_counter()-started
                evidence.save()
                print(dict(branch=branch, mode=mode, mass_drift=row['mass_drift'], interior_change=row['interior_mass_change'],
                    evaluations=solution.nfev, seconds=row['seconds']), flush=True)
        for branch in ['reference', 'MTS']:
            system, baseline, baseline_rates, baseline_mass = trajectories[branch+'_principal']
            unused, changed, changed_rates, changed_mass = trajectories[branch+'_half_step']
            difference = dict(state=float(max(abs(changed-baseline).ravel())), rates=float(max(abs(changed_rates-baseline_rates).ravel())),
                mass=float(max(abs(changed_mass-baseline_mass).ravel())))
            evidence.check(branch+'_whole_state_time_refinement', max(difference.values()) < 2e-8, difference)
            refined, changed, changed_rates, changed_mass = trajectories[branch+'_label_refined']
            interpolation = P2Material(refined, changed[-1, 0]).interpolation(system.labels)
            represented = np.einsum('ij,tkjm->tkim', interpolation, changed)
            represented_rates = np.einsum('ij,tjm->tim', interpolation, changed_rates)
            difference = dict(state=float(max(abs(represented-baseline).ravel())), rates=float(max(abs(represented_rates-baseline_rates).ravel())),
                mass=float(max(abs(changed_mass-baseline_mass).ravel())))
            evidence.check(branch+'_whole_state_label_refinement', max(difference.values()) < 2e-8, difference)
        unused, reference, reference_rates, reference_mass = trajectories['reference_zero_wave']
        unused, mts, mts_rates, mts_mass = trajectories['MTS_zero_wave']
        dust_difference = max(float(max(abs(reference-mts).ravel())), float(max(abs(reference_rates-mts_rates).ravel())),
            float(max(abs(reference_mass-mts_mass).ravel())))
        evidence.check('paired_zero_wave_trajectory_identity', dust_difference < 2e-13, dust_difference)
        evidence.report.update(short_coupled_P2_evolution_qualified=True, duration=duration,
            continuum_force_accuracy_or_long_time_stability_claim=False, full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
