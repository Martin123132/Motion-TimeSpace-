from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from scipy.integrate import solve_ivp
import json
import numpy as np
import time


def main():
    evidence = EvidenceRun('annular-two-sided-GR-oracle-attempt02', __file__)
    try:
        original = evidence.output.parent/'annular-two-sided-GR-oracle-attempt01'
        status = json.loads((original/'status.json').read_text())
        evidence.own(original/'status.json')
        evidence.check('first_underresolved_oracle_preserved_failed', status['state'] == 'failed'
                       and status['checks'][-1]['name'] == 'independent_continuum_fields_refine')
        for degree in [48, 96, 192]:
            evidence.own(original/('degree'+str(degree)+'.npz'))
        degree = 384
        system = TwoSidedGRCharacteristics(degree)
        times = np.linspace(0., .02, 9)
        started = time.perf_counter()
        result = solve_ivp(system.rhs, (0., .02), system.initial_state, method='DOP853',
                           rtol=2e-11, atol=2e-13, max_step=1/degree**2, t_eval=times)
        raw = evidence.output/('degree'+str(degree)+'.npz')
        np.savez_compressed(raw, times=result.t, states=result.y.T)
        evidence.own(raw, 'outputs')
        energy = np.array([system.energy(state)[0] for state in result.y.T])
        rate = max(abs(system.energy(state.astype(complex)+1e-24j*system.rhs(time_value, state))[0].imag/1e-24)
                   for time_value, state in zip(times, result.y.T))
        coarse = np.load(original/'degree192.npz')
        coarse_system = TwoSidedGRCharacteristics(192)
        radius = np.linspace(5.2, 6.8, 3201)
        field_error = max(max(np.max(abs(first-second)) for first, second in zip(coarse_system.sample(coarse_state, radius), system.sample(fine_state, radius)))
                          for coarse_state, fine_state in zip(coarse['states'], result.y.T))
        source_error = np.max(abs(coarse['states'][:, -3:]-result.y[-3:].T))
        row = dict(degree=degree, seconds=time.perf_counter()-started, rhs_calls=result.nfev,
                   energy_drift=float(np.max(abs(energy-energy[0]))), energy_derivative=float(rate),
                   comparison_degree=192, maximum_field_difference=float(field_error), source_difference=float(source_error),
                   initial_field_energy=float(system.energy(system.initial_state)[1]), final_source=result.y[-3:, -1].tolist())
        evidence.report['cases'].append(row)
        print(row, flush=True)
        evidence.check('refined_solver_finished', result.success and len(result.t) == len(times), row)
        evidence.check('original_field_refinement_gate_unchanged', field_error < .3*status['refinement'][-1]['maximum_field_difference'] and field_error < 2e-6, row)
        evidence.check('original_energy_gate_unchanged', row['energy_drift'] < 2e-10 and row['energy_derivative'] < 2e-8, row)
        evidence.report.update(scope='Prescribed Schwarzschild two-sided continuum characteristic/source oracle; scalar spatial degree refined without changing equations, source law, initial data or gates.',
                               original_underresolved_attempt_retained=True, original_gates_unchanged=True,
                               no_energy_or_position_projection=True, live_backreaction_oracle_completed=False,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
