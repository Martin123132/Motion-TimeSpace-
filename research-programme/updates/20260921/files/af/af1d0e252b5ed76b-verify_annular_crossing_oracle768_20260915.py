from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from run_annular_source_fitted_crossing_20260915 import profile
from verify_annular_source_fitted_crossing_precision_20260915 import oracle_difference
from scipy.integrate import solve_ivp
import numpy as np
import time


def main():
    evidence = EvidenceRun('annular-crossing-oracle768-attempt01', __file__)
    try:
        previous_path = evidence.root/'source-intake/navier-stokes/20260914/annular-source-fitted-fine-crossing-attempt01/oracle-512.npz'
        evidence.own(previous_path)
        saved = np.load(previous_path)
        times, previous_states = saved['times'], saved['states']
        previous = TwoSidedGRCharacteristics(512, mass=0., source=.03)
        oracle = TwoSidedGRCharacteristics(768, mass=0., source=.03)
        radius, unused, unused2 = oracle.mesh(6.03, .06)
        unused, gradient = profile(radius)
        temporal = -.06*gradient
        fields = np.stack([temporal+gradient, temporal-gradient], axis=1)
        states = [oracle.pack(fields, np.array([6.03, .03*.06/np.sqrt(1-.06**2), 0.]))]
        started, calls = time.monotonic(), 0
        for index in range(1, len(times)):
            solution = solve_ivp(oracle.rhs, (times[index-1], times[index]), states[-1], t_eval=[times[index]],
                method='DOP853', rtol=2e-10, atol=2e-12, max_step=.1/768)
            evidence.check('interval'+str(index)+'_finished', solution.success, solution.message)
            states.append(solution.y[:, -1])
            calls += solution.nfev
            output = evidence.output/('accepted-'+str(index)+'.npz')
            np.savez_compressed(output, times=times[:index+1], states=np.array(states))
            evidence.own(output, 'outputs')
            evidence.report['progress'] = dict(accepted_time=float(times[index]), rhs_evaluations=calls, seconds=time.monotonic()-started)
            evidence.save()
        states = np.array(states)
        output = evidence.output/'oracle-768.npz'
        np.savez_compressed(output, times=times, states=states)
        evidence.own(output, 'outputs')
        energies = np.array([oracle.energy(state)[0] for state in states])
        drift = float(np.max(abs(energies-energies[0]))/abs(energies[0]))
        differences = [oracle_difference(previous, first, oracle, second, 12) for first, second in zip(previous_states, states)]
        forces = []
        for model, history in [(previous, previous_states), (oracle, states)]:
            force = []
            for state in history:
                fields, position, momentum, velocity = model.unpack(state)
                force.append(model.source_force(fields, position, velocity))
            forces.append(np.array(force))
        force_error = float(np.max(abs(forces[0]-forces[1])))
        evidence.check('finite_states_and_energy', np.isfinite(states).all() and drift < 2e-6, drift)
        evidence.check('force_reference_resolution_below_absolute_gate', force_error < 2e-7, force_error)
        evidence.check('field_reference_resolution_below_one_fiftieth_gate', max(differences) < 1e-4, differences)
        evidence.check('source_clock_reference_resolution', np.max(abs(states[:, -3:]-previous_states[:, -3:])) < 5e-8,
                       float(np.max(abs(states[:, -3:]-previous_states[:, -3:]))))
        evidence.report.update(scope='Additional independent flat crossing characteristic oracle; no MTS terms and no altered physical data.',
            degree=768, seconds=time.monotonic()-started, rhs_evaluations=calls, energy_relative_drift=drift,
            field_vector_resolution_differences=differences, force_reference_errors=abs(forces[0]-forces[1]).tolist(),
            final_force=float(forces[1][-1]), observed_resolution_is_not_certified_error_bound=True,
            live_quadratic_geometry_qualified=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
