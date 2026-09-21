from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_source_fitted_action_20260915 import SourceFittedAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from run_annular_source_fitted_crossing_20260915 import initial, evolve, diagnostics, field_comparison
import argparse
import json
import time
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--counts', type=int, nargs='+', default=[2049])
    parser.add_argument('--label', required=True)
    arguments = parser.parse_args()
    evidence = EvidenceRun(arguments.label, __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        oracle_path = intake/'annular-source-fitted-fine-crossing-attempt01/oracle-512.npz'
        qualification_path = intake/'annular-source-fitted-crossing-precision-attempt01/status.json'
        qualification = json.loads(qualification_path.read_text())
        evidence.check('saved_independent_oracle_qualified', qualification['state'] == 'complete' and qualification['independent_oracle_qualified_for_this_control'])
        evidence.own(oracle_path)
        evidence.own(qualification_path)
        saved = np.load(oracle_path)
        times, exact_states = saved['times'], saved['states']
        oracle = TwoSidedGRCharacteristics(512, mass=0., source=.03)
        exact_velocities = np.array([oracle.unpack(state)[3] for state in exact_states])
        fields, position, momentum, velocity = oracle.unpack(exact_states[-1])
        exact_force = oracle.source_force(fields, position, velocity)
        evidence.report.update(arguments=vars(arguments), original_crossing_data_and_gates_unchanged=True,
            all_Gram_rows_retained=True, source_field_momentum_derivative_retained=True,
            energy_projection=False, live_source_fitted_geometry_qualified=False,
            prespecified_accuracy_gates=dict(field=.005, source=5e-7, velocity=2e-5, clock=2e-7, force_absolute=2e-7, force_relative=.02),
            adaptive_timestep_restarted_at_saved_intervals=True)
        for count in arguments.counts:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                system = SourceFittedAction(count, gram, background_mass=0.)
                states, evaluations = [initial(system)], 0
                started = time.monotonic()
                for index in range(1, len(times)):
                    accepted, calls = evolve(system, states[-1], times[index-1:index+1])
                    states.append(accepted[-1])
                    evaluations += calls
                    destination = evidence.output/(branch+'-'+str(count)+'-accepted-'+str(index)+'.npz')
                    np.savez_compressed(destination, times=times[:index+1], states=np.array(states))
                    evidence.own(destination, 'outputs')
                    evidence.report['progress'] = dict(branch=branch, count=count, accepted_time=float(times[index]), rhs_evaluations=evaluations, seconds=time.monotonic()-started)
                    evidence.save()
                    print(evidence.report['progress'], flush=True)
                    if time.monotonic()-started > 7200:
                        raise RuntimeError('Two-hour per-case safe checkpoint reached; accepted states preserved.')
                states = np.array(states)
                destination = evidence.output/(branch+'-'+str(count)+'.npz')
                np.savez_compressed(destination, times=times, states=states)
                evidence.own(destination, 'outputs')
                row = diagnostics(system, times, states)
                errors = [field_comparison(system, state, oracle, exact) for state, exact in zip(states, exact_states)]
                source_error = float(max(abs(states[:, count]-exact_states[:, -3])))
                velocity_error = float(max(abs(states[:, 2*count+1]-exact_velocities)))
                clock_error = float(max(abs(states[:, -1]-exact_states[:, -1])))
                force_error = float(abs(row['final_force']-exact_force))
                force_relative = float(force_error/abs(exact_force))
                row.update(branch=branch, count=count, field_errors=errors, maximum_field_error=max(errors),
                    maximum_source_error=source_error, maximum_velocity_error=velocity_error, maximum_clock_error=clock_error,
                    final_force_absolute_error=force_error, final_force_relative_error=force_relative,
                    strict_force_gate=bool(force_error < 2e-7 and force_relative < .02),
                    strict_waveform_gate=bool(max(errors) < .005),
                    strict_source_clock_gate=bool(source_error < 5e-7 and velocity_error < 2e-5 and clock_error < 2e-7),
                    seconds=time.monotonic()-started, rhs_evaluations=evaluations)
                evidence.report['cases'].append(row)
                evidence.check(branch+str(count)+'_finite_crossing', np.isfinite(states).all() and len(row['old_grid_nodes_crossed']) > 0)
                evidence.check(branch+str(count)+'_positive_map', row['minimum_jacobian'] > .9)
                evidence.check(branch+str(count)+'_EL_and_energy', row['maximum_euler_residual'] < 2e-11 and row['energy_relative_drift'] < 2e-8, row)
                evidence.save()
                print(row, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
