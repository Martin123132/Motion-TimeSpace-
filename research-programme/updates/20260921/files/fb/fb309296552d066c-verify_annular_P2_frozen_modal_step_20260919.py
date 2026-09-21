from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import GradedP2System, scalar_pencil
from run_annular_P2_continuum_bridge_20260918 import checked_load
from scipy.integrate import solve_ivp
from scipy.linalg import eigh, solve_banded
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-P2-frozen-modal-step-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            no_live_nonlinear_forward_evolution=True, only_frozen_scalar_linear_evolution=True,
            geometry_and_source_position_held_fixed=True, source_velocity_set_zero_for_fixture=True,
            not_the_actual_moving_source_trajectory=True, all_frozen_scalar_modes_retained=True,
            full_live_P2_force_convergence_proven=False, solver_control_not_physics_evidence=True)
        folder = 'annular-P2-joint-refinement-257-cap4e-05-attempt01'
        status_path = evidence.output.parent/folder/'status.json'
        status = json.loads(status_path.read_text())
        evidence.own(status_path)
        evidence.check('paired_initial_force_gate_qualified', status['state'] == 'complete'
            and len(status['cases']) == 2 and all(row['initial_combined_gate_pass'] for row in status['cases']))
        for branch in ['reference', 'MTS']:
            data = checked_load(evidence, folder, branch+'-initial.npz')
            system = GradedP2System(257, branch == 'MTS', 4e-5)
            rates, geometry = system.solve(data['coordinates'], data['momenta'])
            layer = system.layer(0., geometry)
            values = data['coordinates'][len(system.labels)//2]
            mass, stiffness = scalar_pencil(layer, values)
            started = perf_counter()
            eigenvalues, modes = eigh(stiffness, mass, check_finite=False)
            factor_seconds = perf_counter()-started
            frequency = np.sqrt(eigenvalues)
            modal_position = np.cos(.37*np.arange(system.count)+.1)/(np.sqrt(system.count)*frequency)
            modal_velocity = np.sin(.29*np.arange(system.count)+.2)/np.sqrt(system.count)
            modal_initial_energy = float(np.sum(modal_velocity**2+eigenvalues*modal_position**2)/2)

            def exact(time):
                cosine, sine = np.cos(frequency*time), np.sin(frequency*time)
                position = modal_position*cosine+modal_velocity*sine/frequency
                velocity = modal_velocity*cosine-frequency*modal_position*sine
                return modes @ position, modes @ velocity

            initial_position, initial_velocity = exact(0.)
            initial_energy = float((initial_position @ stiffness @ initial_position+initial_velocity @ mass @ initial_velocity)/2)
            bands = layer.evaluate(0., values, np.zeros_like(values))['mass_bands']

            def rhs(time, state):
                return np.append(state[system.count:], -solve_banded((2, 2), bands,
                    stiffness @ state[:system.count], check_finite=False))

            duration = 5*2*np.pi/frequency[-1]
            started = perf_counter()
            solution = solve_ivp(rhs, (0., duration), np.append(initial_position, initial_velocity),
                method='DOP853', rtol=2e-11, atol=2e-13, t_eval=[duration])
            explicit_seconds = perf_counter()-started
            expected_position, expected_velocity = exact(duration)
            position_error = solution.y[:system.count, -1]-expected_position
            velocity_error = solution.y[system.count:, -1]-expected_velocity
            error = np.sqrt((position_error @ stiffness @ position_error+velocity_error @ mass @ velocity_error)/(2*initial_energy))
            rows = []
            started = perf_counter()
            for time in [0., .001, .002, .003, .004]:
                position, velocity = exact(time)
                energy = float((position @ stiffness @ position+velocity @ mass @ velocity)/2)
                rows.append(dict(time=time, relative_energy_error=abs(energy/initial_energy-1)))
            propagation_seconds = perf_counter()-started
            residual = stiffness @ modes-(mass @ modes)*eigenvalues[None, :]
            mode_residual = float(np.max(np.linalg.norm(residual, axis=0)/np.maximum(1.,
                np.linalg.norm(stiffness @ modes, axis=0)+np.linalg.norm(mass @ modes, axis=0)*eigenvalues)))
            backward_residual = float(np.max(np.linalg.norm(residual, axis=0)/
                ((np.linalg.norm(stiffness)+eigenvalues*np.linalg.norm(mass))*np.linalg.norm(modes, axis=0))))
            orthogonality = float(np.max(abs(modes.T @ mass @ modes-np.eye(system.count))))
            final_position, final_velocity = exact(.004)
            final_modal_position = modes.T @ mass @ final_position
            final_modal_velocity = modes.T @ mass @ final_velocity
            fast_initial = float((modal_velocity[-1]**2+eigenvalues[-1]*modal_position[-1]**2)/2)
            fast_final = float((final_modal_velocity[-1]**2+eigenvalues[-1]*final_modal_position[-1]**2)/2)
            row = dict(branch=branch, scalar_nodes=system.count, minimum_eigenvalue=float(eigenvalues[0]),
                maximum_frequency=float(frequency[-1]), factorization_seconds=factor_seconds,
                five_saved_time_propagation_seconds=propagation_seconds,
                physical_space_explicit_seconds=explicit_seconds, explicit_evaluations=solution.nfev,
                explicit_duration=float(duration), relative_energy_norm_difference=float(error),
                normalized_mode_residual=mode_residual, mass_orthogonality_error=orthogonality,
                normwise_backward_residual=backward_residual,
                modal_physical_initial_energy_relative_difference=abs(modal_initial_energy/initial_energy-1),
                fastest_mode_initial_energy=fast_initial, fastest_mode_final_energy=fast_final,
                fastest_mode_fraction=fast_initial/initial_energy, times=rows)
            evidence.report['cases'].append(row)
            evidence.check(branch+'_positive_complete_pencil', np.all(eigenvalues > 0) and modes.shape == (system.count, system.count))
            evidence.check(branch+'_eigen_backward_error_and_normalization', backward_residual < 2e-12 and orthogonality < 2e-10, row)
            evidence.check(branch+'_physical_space_RK_matches_exact_modal_step', solution.success and error < 2e-8, float(error))
            evidence.check(branch+'_frozen_energy_conservation', max(item['relative_energy_error'] for item in rows) < 2e-8)
            evidence.check(branch+'_fastest_mode_not_discarded', fast_initial/initial_energy > 1e-5 and abs(fast_final/fast_initial-1) < 2e-8)
            print(json.dumps(row), flush=True)
        log = evidence.output/'completion-log.txt'
        with log.open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(log, 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
