from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_sparse_repaired_cut_20260915 import SparseRepairedCut
from annular_radiation_benchmark_preparation_20260915 import source_initial, initial_profile
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from run_annular_repaired_GR_force_benchmark_20260915 import physical_field_error
from scipy.integrate import solve_ivp
import json
import numpy as np
import time


def main():
    evidence = EvidenceRun('annular-repaired-GR-force-benchmark-attempt02', __file__)
    try:
        previous = evidence.output.parent/'annular-repaired-GR-force-benchmark-attempt01'
        failed = json.loads((previous/'status.json').read_text())
        evidence.own(previous/'status.json')
        evidence.check('first_waveform_resolution_failure_preserved', failed['state'] == 'failed'
                       and failed['checks'][-1]['name'] == 'reference_physical_waveform_accuracy')
        oracle_directory = evidence.output.parent/'annular-two-sided-GR-oracle-attempt02'
        evidence.own(oracle_directory/'status.json')
        evidence.own(oracle_directory/'degree384.npz')
        saved = np.load(oracle_directory/'degree384.npz')
        times, oracle_states = saved['times'], saved['states']
        oracle = TwoSidedGRCharacteristics(384)
        count = 1505
        for gram in [False, True]:
            started = time.perf_counter()
            branch = 'MTS' if gram else 'reference'
            system = SparseRepairedCut(count, gram, order=8, background_mass=.7)
            initial = source_initial()
            scalar, unused, temporal = initial_profile(system.radii)
            coordinates, rates = np.append(scalar, initial['position']), np.append(temporal, initial['velocity'])
            state0 = np.concatenate([coordinates, rates, [0.]])
            source_cell = np.searchsorted(system.radii, initial['position'])-1
            def rhs(time_value, state):
                position, velocity = np.split(state[:-1], 2)
                lapse, root = system.metric(time_value, position[-1])
                clock = np.sqrt(lapse**2-velocity[-1]**2/root**2)
                return np.concatenate([velocity, system.acceleration(time_value, position, velocity), [clock]])
            def crossing(time_value, state):
                position = state[count]
                return min(position-system.radii[source_cell], system.radii[source_cell+1]-position)-1e-8
            crossing.terminal, crossing.direction = True, -1
            result = solve_ivp(rhs, (0., .02), state0, method='DOP853', rtol=2e-11, atol=2e-13,
                               max_step=.05*system.spacing, t_eval=times, events=crossing)
            raw = evidence.output/(branch+'-1505.npz')
            np.savez_compressed(raw, times=result.t, states=result.y.T, event_times=result.t_events[0])
            evidence.own(raw, 'outputs')
            evidence.check(branch+'_complete_without_crossing', result.success and len(result.t) == len(times) and len(result.t_events[0]) == 0)
            energies, errors, forces, source_errors, velocity_errors = [], [], [], [], []
            for time_value, state, oracle_state in zip(times, result.y.T, oracle_states):
                coordinates, rates = np.split(state[:-1], 2)
                data = system.evaluate(time_value, coordinates, rates)
                energies.append(rates @ data['momenta']-data['action'])
                errors.append(physical_field_error(system, coordinates, rates, oracle, oracle_state))
                acceleration = system.acceleration(time_value, coordinates, rates)
                varied = system.evaluate(time_value+1e-24j, coordinates.astype(complex)+1e-24j*rates, rates.astype(complex)+1e-24j*acceleration)
                force = system.source_covector(time_value, coordinates, rates, wave=True)-varied['field_momenta'][-1].imag/1e-24
                fields, position, unused, velocity = oracle.unpack(oracle_state)
                forces.append((force, oracle.source_force(fields, position, velocity)))
                source_errors.append(abs(coordinates[-1]-position))
                velocity_errors.append(abs(rates[-1]-velocity))
            forces = np.array(forces)
            phase = (result.y[count]-system.radii[source_cell])/system.spacing
            coarse = next(row for row in failed['cases'] if row['branch'] == branch and row['count'] == 1025 and row['label'] == 'main')
            row = dict(branch=branch, count=count, seconds=time.perf_counter()-started, rhs_calls=result.nfev,
                       maximum_physical_field_error=float(max(errors)), maximum_source_error=float(max(source_errors)),
                       maximum_velocity_error=float(max(velocity_errors)), maximum_clock_error=float(np.max(abs(result.y[-1]-oracle_states[:, -1]))),
                       maximum_relative_force_error=float(np.max(abs(forces[:, 0]-forces[:, 1]))/np.max(abs(forces[:, 1]))),
                       energy_drift=float(np.max(abs(np.array(energies)-energies[0]))), minimum_cell_margin=float(np.min(np.minimum(phase, 1-phase))),
                       final_source=float(result.y[count, -1]), final_velocity=float(result.y[2*count+1, -1]))
            evidence.report['cases'].append(row)
            diagnostics = evidence.output/(branch+'-1505-diagnostics.npz')
            np.savez_compressed(diagnostics, times=times, physical_field_errors=errors, radiation_force=forces,
                                source_errors=source_errors, velocity_errors=velocity_errors, energy=energies)
            evidence.own(diagnostics, 'outputs')
            print(row, flush=True)
            evidence.check(branch+'_original_physical_waveform_gate', row['maximum_physical_field_error'] < .005 and row['maximum_physical_field_error'] < .8*coarse['maximum_physical_field_error'], row)
            evidence.check(branch+'_original_radiation_force_gate', row['maximum_relative_force_error'] < .02, row)
            evidence.check(branch+'_original_source_motion_and_clock_gates', row['maximum_source_error'] < 5e-7 and row['maximum_velocity_error'] < 2e-5 and row['maximum_clock_error'] < 2e-7, row)
            evidence.check(branch+'_original_energy_gate_and_regular_cell_phase', row['energy_drift'] < 2e-9 and row['minimum_cell_margin'] > .15, row)
            coarse_path = previous/(branch+'-129-main.npz')
            half_path = previous/(branch+'-129-halfstep.npz')
            evidence.own(coarse_path)
            evidence.own(half_path)
            half_error = float(np.max(abs(np.load(coarse_path)['states']-np.load(half_path)['states'])))
            evidence.check(branch+'_saved_whole_trajectory_halfstep_gate', half_error < 2e-9, half_error)
        evidence.report.update(scope='Same prescribed-Schwarzschild, two-sided characteristic/source comparison with finer scalar grid only; count1505 chosen to retain the noncrossing source-cell interval at unchanged duration.',
                               underresolved_first_attempt_retained=True, equations_initial_data_and_gates_unchanged=True,
                               continuum_force_not_fitted=True, all_Gram_rows_retained=True,
                               boundary_field_momentum_rate_retained=True, no_energy_or_position_projection=True,
                               short_controlled_moving_GR_force_benchmark_completed=True,
                               live_backreaction_continuum_comparison_completed=False,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
