from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_current_20260918 import EvolvingP2System, LiveP2Tangent
import numpy as np


def main():
    evidence = EvidenceRun('annular-live-P2-independent-current-attempt01', __file__)
    try:
        evidence.report.update(no_forward_evolution=True, github_action=False, subagents_used=False,
            explicit_horizontal_extension_not_unique_parent_proof=True,
            moving_edges_atoms_and_label_Jacobians_retained=True,
            current_not_defined_from_radial_mass_derivative=True,
            tangent_metric_in_current_is_an_implicit_equation_test=True,
            independent_temporal_current_tested=True, full_live_P2_force_convergence_proven=False)
        for deformed in [False, True]:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                system = EvolvingP2System(17, gram, layer_degree=6, radial_degree=18)
                coordinates, momenta, unused, unused2 = system.initial(deformed=deformed)
                tangent = LiveP2Tangent(system, coordinates, momenta)
                source = float(np.mean(coordinates[[0, -1], -1]))
                targets = np.array([5.28, 5.57, 5.91, source-.016, source-.006, source+.0013, source+.006, source+.016, 6.25, 6.72])
                compared = tangent.compare(targets, label_order=12)
                noether = [tangent.layer_data(label).noether() for label in [-.37, .03, .41]]
                row = dict(branch=branch, deformed=deformed, layer_degree=6, radial_degree=18,
                    difference_step=tangent.step, current_comparisons=compared, noether=noether,
                    maximum_error=max(item['error'] for item in compared),
                    maximum_on_shell_error=max(item['on_shell_error'] for item in compared),
                    maximum_frozen_mesh_error=max(item['frozen_mesh_error'] for item in compared),
                    radial_residual=tangent.geometry.off_grid_residual(tangent.rates))
                evidence.report['cases'].append(row)
                evidence.save()
                print(dict(branch=branch, deformed=deformed, error=row['maximum_error'],
                    on_shell=row['maximum_on_shell_error'], frozen=row['maximum_frozen_mesh_error'],
                    noether=max(item['residual'] for item in noether)), flush=True)
                prefix=branch+str(deformed)
                evidence.check(prefix+'_actual_current_vs_recomputed_mass', row['maximum_error'] < 2e-8, row['maximum_error'])
                evidence.check(prefix+'_on_shell_current_separate_collocation_control', row['maximum_on_shell_error'] < 2e-8, row['maximum_on_shell_error'])
                evidence.check(prefix+'_full_moving_Noether_identity', max(item['residual'] for item in noether) < 2e-8, noether)
                evidence.check(prefix+'_offgrid_radial_equations', max(row['radial_residual']) < 2e-7, row['radial_residual'])
                evidence.check(prefix+'_old_frozen_mesh_current_detected', row['maximum_frozen_mesh_error'] > 20*max(row['maximum_error'], 1e-12), row['maximum_frozen_mesh_error'])
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
