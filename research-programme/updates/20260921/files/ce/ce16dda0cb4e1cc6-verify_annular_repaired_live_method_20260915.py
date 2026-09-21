from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_repaired_live_geometry_20260915 import RepairedLiveSystem
from annular_repaired_live_current_20260915 import LiveTangent
from verify_annular_repaired_live_controls_20260915 import deformed_preparation
from run_annular_cut_curved_background_20260915 import BackgroundCutAction
from annular_cut_initial_data_20260915 import compatible_initial_state
from scipy.integrate import solve_ivp
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-repaired-live-method-attempt01', __file__)
    try:
        evolution = evidence.output.parent/'annular-repaired-live-evolution-attempt01'
        status = json.loads((evolution/'status.json').read_text())
        evidence.check('sealed_input_evolutions_completed', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        evidence.own(evolution/'status.json')
        targets = [5.993, 6.023, 6.03, 6.037, 6.105, 6.41]
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            current_rows = []
            for degree, step in [(8, 1e-4), (12, 1e-4), (12, 2e-5)]:
                system = RepairedLiveSystem(17, gram, degree, 10, action_order=10, label_order=12)
                coordinates, momenta, rates, geometry = deformed_preparation(system)
                tangent = LiveTangent(system, coordinates, momenta, difference_step=step)
                comparison = tangent.compare(targets, label_order=12)
                row = dict(branch=branch, layer_degree=degree, difference_step=step,
                           error=comparison['on_shell_error'], off_shell_error=comparison['error'],
                           Euler_current_correction=comparison['current_euler_correction'],
                           off_grid_canonical_residual=system.canonical_residual(coordinates, momenta, rates, geometry, True))
                current_rows.append(row)
                evidence.report['cases'].append(row)
                raw = evidence.output/(branch+'-'+str(degree)+'-'+str(step)+'.npz')
                np.savez_compressed(raw, **comparison)
                evidence.own(raw, 'outputs')
                print(row, flush=True)
                evidence.check(branch+str(degree)+str(step)+'_unchanged_temporal_gate', row['error'] < 2e-8, row)
            evidence.check(branch+'_deformed_material_current_refines', current_rows[1]['error'] < current_rows[0]['error']*.2
                           and current_rows[1]['error'] < 2e-10, current_rows)
            evidence.check(branch+'_fine_material_time_difference_stable', max(row['error'] for row in current_rows[1:]) < 2e-10, current_rows)
            raw_path = evolution/(branch+'-17-no_backreaction.npz')
            evidence.own(raw_path)
            saved = np.load(raw_path)
            background = BackgroundCutAction(17, gram)
            initial_coordinates, initial_rates, unused = compatible_initial_state(background, 0.)
            solution = solve_ivp(background.rhs, (0., .02), np.concatenate([initial_coordinates, initial_rates]),
                                 method='DOP853', rtol=2e-11, atol=2e-13, max_step=.001, t_eval=saved['time'])
            canonical = saved['state'][:324].reshape(2, 9, 18, -1)
            coordinate_error = float(np.max(abs(solution.y[:18]-canonical[0, 4])))
            velocity_error = float(np.max(abs(solution.y[18:, -1]-saved['rates'][4])))
            row = dict(branch=branch, control='Independent velocity-form prescribed-background solver versus new canonical solver at zero backreaction.',
                       coordinate_error=coordinate_error, final_velocity_error=velocity_error)
            evidence.report['cases'].append(row)
            evidence.check(branch+'_independent_prescribed_background_recovered', solution.success and max(coordinate_error, velocity_error) < 2e-9, row)
            live_path = evolution/(branch+'-17-main.npz')
            evidence.own(live_path)
            saved_live = np.load(live_path)
            system = RepairedLiveSystem(17, gram, 8, 10)
            coordinates, momenta = saved_live['state'][:324, -1].reshape(2, 9, 18)
            unused, geometry = system.solve(coordinates, momenta)
            unused, unused2, unused3, initial_geometry = system.initial()
            probe = np.array([6.023, 6.03, 6.037])
            change = float(np.max(abs(geometry.values(probe)[0]-initial_geometry.values(probe)[0])))
            evidence.check(branch+'_interior_metric_actually_changes', change > 1e-5, change)
        evidence.report.update(time_and_material_current_refinement_checked=True,
                               independent_prescribed_background_recovery_checked=True,
                               nonzero_interior_metric_evolution_checked=True,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
