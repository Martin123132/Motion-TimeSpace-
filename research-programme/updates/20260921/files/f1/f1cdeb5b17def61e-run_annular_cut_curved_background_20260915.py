from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_covariant_cut_action_v2_20260915 import CurvedCutAction, history_state
from scipy.integrate import solve_ivp
import numpy as np
import json


class BackgroundCutAction(CurvedCutAction):
    def __init__(self, count, gram, mass=.7):
        super().__init__(count, gram, order=8, stationary=True)
        self.background_mass = mass

    def metric(self, time, radius):
        root = np.sqrt(1-2*self.background_mass/radius)
        return root, root


def run_case(evidence, count, gram, mass=.7, step=.001, tag=''):
    system = BackgroundCutAction(count, gram, mass)
    coordinates, rates, unused = history_state(system, 0.)
    initial = np.concatenate([coordinates, rates, [0.]])
    initial_data = system.evaluate(0., coordinates, rates)
    initial_energy = rates @ initial_data['momenta']-initial_data['action']
    cell = np.searchsorted(system.radii, coordinates[-1])-1
    def rhs(time, state):
        coordinates, rates = np.split(state[:-1], 2)
        lapse, root = system.metric(time, coordinates[-1])
        clock = np.sqrt(lapse**2-rates[-1]**2/root**2)
        return np.concatenate([rates, system.acceleration(time, coordinates, rates), [clock]])
    def cell_event(time, state):
        position = state[system.count]
        return min(position-system.radii[cell], system.radii[cell+1]-position)-1e-7
    cell_event.terminal = True
    cell_event.direction = -1
    times = np.linspace(0., .05, 21)
    solution = solve_ivp(rhs, (0., .05), initial, method='DOP853', rtol=2e-11, atol=2e-13,
                         max_step=step, t_eval=times, dense_output=True, events=cell_event)
    label = ('MTS' if gram else 'reference')+'-'+str(count)+'-mass-'+str(mass)+tag
    path = evidence.output/(label+'.npz')
    np.savez_compressed(path, times=solution.t, states=solution.y, radii=system.radii,
                        event_times=solution.t_events[0], event_states=solution.y_events[0])
    evidence.own(path, 'outputs')
    evidence.check(label+'_complete_before_source_cell_crossing', solution.success and len(solution.t) == len(times)
                   and not len(solution.t_events[0]), solution.message)
    energy_error = 0.
    minimum_inertia = np.inf
    for time, state in zip(solution.t, solution.y.T):
        coordinates, rates = np.split(state[:-1], 2)
        data = system.evaluate(time, coordinates, rates)
        energy_error = max(energy_error, abs(rates @ data['momenta']-data['action']-initial_energy)/abs(initial_energy))
        minimum_inertia = min(minimum_inertia, np.linalg.eigvalsh(data['inertia']).min())
    euler_error = 0.
    for time in [.01, .025, .04]:
        derivative_step = 2e-5
        momenta = []
        for offset in [-2, -1, 1, 2]:
            coordinates, rates = np.split(solution.sol(time+offset*derivative_step)[:-1], 2)
            momenta.append(system.evaluate(time+offset*derivative_step, coordinates, rates)['momenta'])
        differentiated = (momenta[0]-8*momenta[1]+8*momenta[2]-momenta[3])/(12*derivative_step)
        coordinates, rates = np.split(solution.sol(time)[:-1], 2)
        data = system.evaluate(time, coordinates, rates)
        covector = np.append(data['scalar_covector'], system.source_covector(time, coordinates, rates))
        euler_error = max(euler_error, np.max(abs(differentiated-covector)))
    evidence.check(label+'_unprojected_energy', energy_error < 1e-8, float(energy_error))
    evidence.check(label+'_positive_full_inertia', minimum_inertia > 0, float(minimum_inertia))
    evidence.check(label+'_independent_trajectory_Euler_equations', euler_error < 2e-7, float(euler_error))
    row = dict(branch='MTS' if gram else 'reference', count=count, mass=mass, tag=tag, step=step,
               relative_energy_error=float(energy_error), minimum_inertia=float(minimum_inertia),
               independent_Euler_error=float(euler_error), final_radius=float(solution.y[system.count, -1]),
               final_velocity=float(solution.y[2*system.count+1, -1]), final_proper_clock=float(solution.y[-1, -1]),
               nfev=solution.nfev)
    evidence.report['cases'].append(row)
    evidence.save()
    print(row, flush=True)
    return solution.y


def main():
    evidence = EvidenceRun('annular-cut-curved-background-evolution-attempt01', __file__)
    try:
        coarse = {}
        for count in [17, 33, 65]:
            for gram in [False, True]:
                coarse[count, gram] = run_case(evidence, count, gram)
        for gram in [False, True]:
            finer = run_case(evidence, 17, gram, step=.0005, tag='-half-step')
            difference = float(np.max(abs(finer-coarse[17, gram])))
            evidence.check(('MTS' if gram else 'reference')+'_half_step_state', difference < 2e-8, difference)
            run_case(evidence, 17, gram, mass=0., tag='-flat')
        evidence.report.update(scope='Repaired scalar/source action evolving on prescribed Schwarzschild and flat backgrounds, not live self-gravity.',
                               source_force_derived_from_full_action=True,
                               old_trace_multiplier_absent=True,
                               field_or_energy_projection=False,
                               background_backreaction_evolved=False,
                               continuum_waveform_accuracy_qualified=False,
                               source_cell_crossing_transfer_derived=False,
                               unique_parent_boundary_selection_proven=False,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
