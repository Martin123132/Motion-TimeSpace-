from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from scipy.integrate import solve_ivp
import numpy as np
import time


def main():
    evidence = EvidenceRun('annular-two-sided-GR-oracle-attempt01', __file__)
    saved = {}
    try:
        times = np.linspace(0., .02, 9)
        for degree in [48, 96, 192]:
            started = time.perf_counter()
            system = TwoSidedGRCharacteristics(degree)
            evidence.check(str(degree)+'_independent_derivative_and_quadrature',
                           np.max(abs(system.derivative @ system.coordinate-1)) < 2e-10 and abs(np.sum(system.weights)-1) < 2e-13)
            result = solve_ivp(system.rhs, (0., .02), system.initial_state, method='DOP853',
                               rtol=2e-11, atol=2e-13, max_step=1/degree**2, t_eval=times)
            raw = evidence.output/('degree'+str(degree)+'.npz')
            np.savez_compressed(raw, times=result.t, states=result.y.T)
            evidence.own(raw, 'outputs')
            energy = np.array([system.energy(state)[0] for state in result.y.T])
            energy_rate = max(abs(system.energy(state.astype(complex)+1e-24j*system.rhs(time_value, state))[0].imag/1e-24)
                              for time_value, state in zip(times, result.y.T))
            forces = [system.source_force(*[system.unpack(state)[index] for index in [0, 1, 3]]) for state in result.y.T]
            row = dict(degree=degree, seconds=time.perf_counter()-started, rhs_calls=result.nfev,
                       energy_drift=float(np.max(abs(energy-energy[0]))), energy_derivative=float(energy_rate),
                       initial_field_energy=float(system.energy(system.initial_state)[1]),
                       minimum_radiation_force=float(min(forces)), maximum_radiation_force=float(max(forces)),
                       final_source=result.y[-3:, -1].tolist())
            evidence.report['cases'].append(row)
            print(row, flush=True)
            evidence.check(str(degree)+'_solver_finished_and_nonzero_radiation', result.success and len(result.t) == len(times) and min(forces) > 1e-4, row)
            saved[degree] = system, result
        comparisons = []
        radius = np.linspace(5.2, 6.8, 3201)
        for lower, upper in [(48, 96), (96, 192)]:
            first, lower_result = saved[lower]
            second, upper_result = saved[upper]
            errors = [max(np.max(abs(left-right)) for left, right in zip(first.sample(lower_state, radius), second.sample(upper_state, radius)))
                      for lower_state, upper_state in zip(lower_result.y.T, upper_result.y.T)]
            row = dict(lower=lower, upper=upper, maximum_field_difference=float(max(errors)),
                       source_difference=float(np.max(abs(lower_result.y[-3:]-upper_result.y[-3:]))))
            comparisons.append(row)
        evidence.report['refinement'] = comparisons
        evidence.check('independent_continuum_fields_refine', comparisons[-1]['maximum_field_difference'] < .3*comparisons[0]['maximum_field_difference']
                       and comparisons[-1]['maximum_field_difference'] < 2e-6, comparisons)
        fine = evidence.report['cases'][-1]
        evidence.check('fine_continuum_energy_without_projection', fine['energy_drift'] < 2e-10 and fine['energy_derivative'] < 2e-8, fine)
        evidence.report.update(scope='Independent two-sided continuum characteristics plus proper-time moving source on prescribed Schwarzschild mass .7; zero wave/source backreaction, not the live finite-width oracle.',
                               continuum_source_force_from_rest_frame_pressure=True,
                               incoming_characteristic_boundary_values_eliminated_analytically=True,
                               no_energy_or_position_projection=True,
                               independent_of_repaired_cut_cell_action=True,
                               live_backreaction_oracle_completed=False,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
