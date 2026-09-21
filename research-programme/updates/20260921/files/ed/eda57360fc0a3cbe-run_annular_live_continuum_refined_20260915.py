from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_continuum_characteristics_20260915 import LiveContinuumCharacteristics
from run_annular_live_continuum_evolution_20260915 import evolve, proper_acceleration_test
from annular_live_continuum_comparison_tools_20260915 import oracle_difference
import numpy as np
import json
import time


def main():
    evidence = EvidenceRun('annular-live-continuum-refinement-attempt01', __file__)
    try:
        previous = evidence.output.parent/'annular-live-continuum-evolution-attempt01'
        previous_status = previous/'status.json'
        status = json.loads(previous_status.read_text())
        evidence.own(previous_status)
        evidence.check('previous_live_evolution_controls_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        started = time.perf_counter()
        system = LiveContinuumCharacteristics(384, 8, 18, radial_spacing=.025, label_order=12)
        trajectory, initial_geometry, calls = evolve(system)
        geometry = system.solve(trajectory.y[:, -1])
        radial = geometry.check_radial()
        current = system.current_test(trajectory.y[:, -1])
        acceleration = proper_acceleration_test(system, trajectory.y[:, -1])
        mass_drift = max(abs(system.solve(state).mass_nodes[-1, -1]-initial_geometry.mass_nodes[-1, -1]) for state in trajectory.y.T)
        raw = evidence.output/'degree384.npz'
        np.savez_compressed(raw, times=trajectory.t, states=trajectory.y.T, mass=geometry.mass_nodes, radial_nodes=geometry.nodes,
                            log_lapse=geometry.log_lapse_nodes, **current)
        evidence.own(raw, 'outputs')
        row = dict(degree=384, layer_degree=8, radial_degree=18, radial_spacing=.025, label_order=12, width=.02,
                   coupling=.1, duration=.02, seconds=time.perf_counter()-started, rhs_calls=calls,
                   mass_radial_residual=radial[0], lapse_radial_residual=radial[1], current_error=current['error'],
                   proper_acceleration_error=acceleration['error'], exterior_mass_drift=float(mass_drift))
        evidence.report['cases'].append(row)
        evidence.save()
        print(row, flush=True)
        evidence.check('refined_independent_radial_constraints', max(radial) < 2e-8, row)
        evidence.check('refined_independent_mass_time_current', current['error'] < 2e-8, row)
        evidence.check('refined_unprojected_exterior_mass', mass_drift < 2e-9, row)
        evidence.check('refined_derived_proper_acceleration', acceleration['error'] < 2e-7, row)
        for degree in [96, 192]:
            old = previous/('degree'+str(degree)+'-main.npz')
            evidence.own(old)
            saved = np.load(old)
            coarse = LiveContinuumCharacteristics(degree, 4, 14, radial_spacing=.05)
            differences = oracle_difference(coarse, saved['states'], system, trajectory.y.T)
            diagnostics = evidence.output/('degree'+str(degree)+'-comparison.npz')
            np.savez_compressed(diagnostics, times=trajectory.t, differences=differences)
            evidence.own(diagnostics, 'outputs')
            comparison = dict(degree=degree, maximum_field_difference=float(np.max(differences[:, 0])),
                              source_difference=float(np.max(differences[:, 1])), velocity_difference=float(np.max(differences[:, 2])),
                              clock_difference=float(np.max(differences[:, 3])))
            evidence.report['cases'].append(comparison)
            evidence.save()
            print(comparison, flush=True)
        coarse, fine = evidence.report['cases'][-2:]
        evidence.check('independent_continuum_fields_refine', fine['maximum_field_difference'] < 2e-6
                       and fine['maximum_field_difference'] < .8*coarse['maximum_field_difference'], [coarse, fine])
        evidence.check('independent_continuum_source_and_clocks_refine', fine['source_difference'] < 1e-8
                       and fine['velocity_difference'] < 2e-7 and fine['clock_difference'] < 1e-8, fine)
        evidence.report.update(independent_common_live_geometry_continuum_evolved=True,
                               sampled_finite_time_continuum_accuracy_qualified=True, all_mesh_convergence_theorem=False,
                               source_and_geometry_equations_not_transplanted_from_cut_action=True,
                               same_original_repaired_live_preparation=True, finite_width_held_fixed=True,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
