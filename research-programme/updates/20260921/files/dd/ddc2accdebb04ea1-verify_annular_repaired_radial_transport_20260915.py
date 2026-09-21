from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_repaired_live_geometry_20260915 import RepairedLiveSystem, DensityTable
from annular_repaired_live_current_20260915 import LiveTangent
from verify_annular_repaired_live_controls_20260915 import deformed_preparation
from run_annular_cut_curved_background_20260915 import BackgroundCutAction
from annular_cut_initial_data_20260915 import compatible_initial_state
from scipy.integrate import solve_ivp
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-repaired-radial-transport-attempt01', __file__)
    try:
        evolution = evidence.output.parent/'annular-repaired-live-evolution-attempt01'
        failure = evidence.output.parent/'annular-repaired-live-method-attempt01/status.json'
        failed = json.loads(failure.read_text())
        evidence.own(failure)
        evidence.check('material_refinement_hypothesis_failure_preserved', failed['state'] == 'failed'
                       and failed['checks'][-1]['name'] == 'reference_deformed_material_current_refines')
        evidence.own(evolution/'status.json')
        targets = np.array([5.993, 6.023, 6.03, 6.037, 6.105, 6.41])
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            current_rows = []
            for degree, step in [(10, 1e-4), (14, 1e-4), (18, 1e-4), (18, 2e-5)]:
                system = RepairedLiveSystem(17, gram, 12, degree, action_order=10, label_order=12)
                coordinates, momenta, rates, geometry = deformed_preparation(system)
                tangent = LiveTangent(system, coordinates, momenta, difference_step=step)
                comparison = tangent.compare(targets, label_order=12)
                radial_errors = tangent.geometry.off_grid_residual(tangent.rates)
                density = DensityTable(tangent.material, targets)
                density.update(tangent.rates)
                mass, log_lapse, mass_radial, unused = tangent.geometry.values(targets)
                exact_radial = density.rhs(mass, log_lapse)[0]
                transport_estimate = -density.velocity*(mass_radial-exact_radial)
                row = dict(branch=branch, radial_degree=degree, layer_degree=12, difference_step=step,
                           current_error=comparison['on_shell_error'], radial_mass_error=radial_errors[0],
                           radial_lapse_error=radial_errors[1],
                           translated_profile_error_estimate=float(np.max(abs(transport_estimate))),
                           remainder_after_translation_estimate=float(np.max(abs(comparison['radial_time_derivative']-comparison['on_shell_current']-transport_estimate))))
                current_rows.append(row)
                evidence.report['cases'].append(row)
                path = evidence.output/(branch+'-'+str(degree)+'-'+str(step)+'.npz')
                np.savez_compressed(path, **comparison, radial_mass_residual=mass_radial-exact_radial, translation_estimate=transport_estimate)
                evidence.own(path, 'outputs')
                print(row, flush=True)
                evidence.check(branch+str(degree)+str(step)+'_original_current_gate', row['current_error'] < 2e-8, row)
            evidence.check(branch+'_radial_current_refinement_identifies_error', current_rows[1]['current_error'] < .2*current_rows[0]['current_error']
                           and current_rows[1]['current_error'] < 2e-10, current_rows)
            evidence.check(branch+'_higher_radial_and_time_controls', max(row['current_error'] for row in current_rows[1:]) < 2e-10, current_rows)
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
            row = dict(branch=branch, control='independent_zero_backreaction_solver', coordinate_error=coordinate_error,
                       final_velocity_error=velocity_error)
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
        evidence.report.update(radial_and_time_current_refinement_tested=True,
                               original_wrong_error_attribution_retained_as_failed=True,
                               matter_and_gravity_equations_unchanged=True,
                               independent_prescribed_background_recovery_checked=True,
                               nonzero_interior_metric_evolution_checked=True,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
