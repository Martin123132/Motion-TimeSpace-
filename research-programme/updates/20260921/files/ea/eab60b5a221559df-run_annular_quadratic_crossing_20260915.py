from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from run_annular_source_fitted_crossing_20260915 import initial, evolve, diagnostics, field_comparison
import argparse
import json
import time
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-counts', type=int, nargs='+', default=[33, 65, 129, 257])
    parser.add_argument('--label', required=True)
    arguments = parser.parse_args()
    evidence = EvidenceRun(arguments.label, __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        for folder in ['annular-quadratic-source-fitted-action-attempt01', 'annular-source-fitted-crossing-precision-attempt01']:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            evidence.check(folder+'_qualified', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            evidence.own(path)
        oracle_path = intake/'annular-source-fitted-fine-crossing-attempt01/oracle-512.npz'
        evidence.own(oracle_path)
        saved = np.load(oracle_path)
        times, exact_states = saved['times'], saved['states']
        oracle = TwoSidedGRCharacteristics(512, mass=0., source=.03)
        exact_velocities = np.array([oracle.unpack(state)[3] for state in exact_states])
        fields, position, momentum, velocity = oracle.unpack(exact_states[-1])
        exact_force = oracle.source_force(fields, position, velocity)
        evidence.report.update(arguments=vars(arguments), original_crossing_data_and_gates_unchanged=True,
            spatial_degree=2, all_original_vertex_Gram_rows_retained=True, true_quadratic_source_gradient_jump_used=True,
            source_field_momentum_derivative_retained=True, original_linear_subspace_exactly_preserved=True,
            no_fitted_coefficient_added=True, energy_projection=False, live_quadratic_geometry_qualified=False,
            prespecified_accuracy_gates=dict(field=.005, source=5e-7, velocity=2e-5, clock=2e-7, force_absolute=2e-7, force_relative=.02))
        for base_count in arguments.base_counts:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                system = QuadraticSourceFittedAction(base_count, gram, background_mass=0.)
                started = time.monotonic()
                states, evaluations = [initial(system)], 0
                for index in range(1, len(times)):
                    accepted, calls = evolve(system, states[-1], times[index-1:index+1])
                    states.append(accepted[-1])
                    evaluations += calls
                    destination = evidence.output/(branch+'-'+str(base_count)+'-accepted-'+str(index)+'.npz')
                    np.savez_compressed(destination, times=times[:index+1], states=np.array(states))
                    evidence.own(destination, 'outputs')
                    evidence.report['progress'] = dict(branch=branch, base_count=base_count, scalar_dofs=system.count,
                        accepted_time=float(times[index]), seconds=time.monotonic()-started)
                    evidence.save()
                    if time.monotonic()-started > 7200:
                        raise RuntimeError('Two-hour per-case safe checkpoint reached; accepted states preserved.')
                states = np.array(states)
                destination = evidence.output/(branch+'-'+str(base_count)+'.npz')
                np.savez_compressed(destination, times=times, states=states)
                evidence.own(destination, 'outputs')
                row = diagnostics(system, times, states)
                errors = [field_comparison(system, state, oracle, exact) for state, exact in zip(states, exact_states)]
                positions = states[:, system.count]
                old_vertices = system.base_radii[(system.base_radii > positions.min()) & (system.base_radii < positions.max())]
                source_error = float(max(abs(positions-exact_states[:, -3])))
                velocity_error = float(max(abs(states[:, 2*system.count+1]-exact_velocities)))
                clock_error = float(max(abs(states[:, -1]-exact_states[:, -1])))
                force_error = float(abs(row['final_force']-exact_force))
                force_relative = float(force_error/abs(exact_force))
                row.update(branch=branch, base_count=base_count, scalar_dofs=system.count, original_base_vertices_crossed=old_vertices.tolist(),
                    field_errors=errors, maximum_field_error=max(errors), maximum_source_error=source_error,
                    maximum_velocity_error=velocity_error, maximum_clock_error=clock_error,
                    final_force_absolute_error=force_error, final_force_relative_error=force_relative,
                    strict_force_gate=bool(force_error < 2e-7 and force_relative < .02), strict_waveform_gate=bool(max(errors) < .005),
                    strict_source_clock_gate=bool(source_error < 5e-7 and velocity_error < 2e-5 and clock_error < 2e-7),
                    seconds=time.monotonic()-started, rhs_evaluations=evaluations)
                evidence.report['cases'].append(row)
                evidence.check(branch+str(base_count)+'_finite_base_vertex_crossing', np.isfinite(states).all() and len(old_vertices) > 0)
                evidence.check(branch+str(base_count)+'_positive_map', row['minimum_jacobian'] > .9)
                evidence.check(branch+str(base_count)+'_EL_and_energy', row['maximum_euler_residual'] < 2e-10 and row['energy_relative_drift'] < 2e-8, row)
                evidence.save()
                print(row, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
