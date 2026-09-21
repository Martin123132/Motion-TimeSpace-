from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_sparse_repaired_cut_20260915 import SparseRepairedCut
from annular_radiation_benchmark_preparation_20260915 import source_initial, initial_profile
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from scipy.integrate import solve_ivp
import json
import numpy as np
import time


def physical_field_error(system, coordinates, rates, oracle, oracle_state):
    endpoints = np.unique(np.concatenate([system.radii, [coordinates[-1], oracle_state[-3]]]))
    lengths = np.diff(endpoints)
    radius = (endpoints[:-1, None]+lengths[:, None]*system.fractions).ravel()
    weight = (lengths[:, None]*system.weights).ravel()
    cells, shape, radial, motion = system.features(radius, coordinates[-1])
    values = np.column_stack([coordinates[cells], coordinates[cells+1]])
    velocities = np.column_stack([rates[cells], rates[cells+1]])
    temporal = np.sum(shape*velocities, axis=1)+np.sum(motion*values, axis=1)*rates[-1]
    gradient = np.sum(radial*values, axis=1)
    target_temporal, target_gradient = oracle.sample(oracle_state, radius)
    coefficient = system.coefficient(0., radius)
    error_squared = weight @ (radius**4/coefficient*(temporal-target_temporal)**2+coefficient*(gradient-target_gradient)**2)
    return np.sqrt(error_squared/(2*oracle.energy(oracle.initial_state)[1]))


def main():
    evidence = EvidenceRun('annular-repaired-GR-force-benchmark-attempt01', __file__)
    try:
        oracle_directory = evidence.output.parent/'annular-two-sided-GR-oracle-attempt02'
        status_path = oracle_directory/'status.json'
        status = json.loads(status_path.read_text())
        evidence.own(status_path)
        evidence.check('independent_oracle_qualified', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        oracle_file = oracle_directory/'degree384.npz'
        evidence.own(oracle_file)
        saved = np.load(oracle_file)
        times, oracle_states = saved['times'], saved['states']
        oracle = TwoSidedGRCharacteristics(384)
        initial = source_initial()
        final_states = {}
        cases = [(count, .05, 'main') for count in [65, 129, 257, 513, 1025]]+[(129, .025, 'halfstep')]
        for count, step_factor, label in cases:
            for gram in [False, True]:
                started = time.perf_counter()
                system = SparseRepairedCut(count, gram, order=8, background_mass=.7)
                scalar, unused, temporal = initial_profile(system.radii)
                coordinates = np.append(scalar, initial['position'])
                rates = np.append(temporal, initial['velocity'])
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
                                   max_step=step_factor*system.spacing, t_eval=times, events=crossing)
                key = ('MTS' if gram else 'reference')+'-'+str(count)+'-'+label
                raw = evidence.output/(key+'.npz')
                np.savez_compressed(raw, times=result.t, states=result.y.T, event_times=result.t_events[0])
                evidence.own(raw, 'outputs')
                evidence.check(key+'_complete_without_cell_crossing', result.success and len(result.t) == len(times) and len(result.t_events[0]) == 0)
                energies, errors, forces, source_errors, velocity_errors = [], [], [], [], []
                for time_value, state, oracle_state in zip(times, result.y.T, oracle_states):
                    coordinates, rates = np.split(state[:-1], 2)
                    data = system.evaluate(time_value, coordinates, rates)
                    energies.append(rates @ data['momenta']-data['action'])
                    errors.append(physical_field_error(system, coordinates, rates, oracle, oracle_state))
                    acceleration = system.acceleration(time_value, coordinates, rates)
                    varied = system.evaluate(time_value+1e-24j, coordinates.astype(complex)+1e-24j*rates,
                                              rates.astype(complex)+1e-24j*acceleration)
                    momentum_rate = varied['field_momenta'][-1].imag/1e-24
                    force = system.source_covector(time_value, coordinates, rates, wave=True)-momentum_rate
                    fields, position, unused, velocity = oracle.unpack(oracle_state)
                    target_force = oracle.source_force(fields, position, velocity)
                    forces.append((force, target_force))
                    source_errors.append(abs(coordinates[-1]-position))
                    velocity_errors.append(abs(rates[-1]-velocity))
                forces = np.array(forces)
                row = dict(key=key, branch='MTS' if gram else 'reference', count=count, label=label,
                           seconds=time.perf_counter()-started, rhs_calls=result.nfev,
                           maximum_physical_field_error=float(max(errors)), maximum_source_error=float(max(source_errors)),
                           maximum_velocity_error=float(max(velocity_errors)),
                           maximum_clock_error=float(np.max(abs(result.y[-1]-oracle_states[:, -1]))),
                           maximum_relative_force_error=float(np.max(abs(forces[:, 0]-forces[:, 1]))/np.max(abs(forces[:, 1]))),
                           energy_drift=float(np.max(abs(np.array(energies)-energies[0]))),
                           final_source=float(result.y[count, -1]), final_velocity=float(result.y[2*count+1, -1]))
                evidence.report['cases'].append(row)
                diagnostics = evidence.output/(key+'-diagnostics.npz')
                np.savez_compressed(diagnostics, times=times, physical_field_errors=errors, radiation_force=forces,
                                    source_errors=source_errors, velocity_errors=velocity_errors, energy=energies)
                evidence.own(diagnostics, 'outputs')
                print(row, flush=True)
                evidence.check(key+'_unprojected_energy', row['energy_drift'] < 2e-9, row)
                final_states[key] = result.y[:, -1]
        for branch in ['reference', 'MTS']:
            rows = [row for row in evidence.report['cases'] if row['branch'] == branch and row['label'] == 'main']
            fine = rows[-1]
            evidence.check(branch+'_physical_waveform_accuracy', fine['maximum_physical_field_error'] < .005
                           and fine['maximum_physical_field_error'] < .8*rows[-2]['maximum_physical_field_error'], rows)
            evidence.check(branch+'_independent_radiation_force_accuracy', fine['maximum_relative_force_error'] < .02, fine)
            evidence.check(branch+'_source_motion_and_clock_accuracy', fine['maximum_source_error'] < 5e-7
                           and fine['maximum_velocity_error'] < 2e-5 and fine['maximum_clock_error'] < 2e-7, fine)
            half_error = float(np.max(abs(final_states[branch+'-129-main']-final_states[branch+'-129-halfstep'])))
            evidence.check(branch+'_whole_state_halfstep', half_error < 2e-9, half_error)
        evidence.report.update(scope='Repaired reference and all-factor MTS against an independent continuum two-sided characteristic moving-source solver on the SAME prescribed Schwarzschild metric; not a live-backreaction continuum comparison.',
                               continuum_force_not_fitted=True, all_Gram_rows_retained=True,
                               boundary_field_momentum_rate_retained=True,
                               physical_sampling_splits_both_source_positions=True,
                               no_energy_or_position_projection=True,
                               short_controlled_moving_GR_force_benchmark_completed=True,
                               live_backreaction_continuum_comparison_completed=False,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
