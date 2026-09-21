from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_canonical_20260918 import LiveP2System as OriginalSystem
from annular_live_P2_canonical_v2_20260918 import LiveP2System as CorrectedSystem
import numpy as np


def main():
    evidence = EvidenceRun('annular-live-P2-edge-diagnosis-attempt01', __file__)
    try:
        for gram in [False, True]:
            original = OriginalSystem(17, gram, layer_degree=8)
            corrected = CorrectedSystem(17, gram, layer_degree=8)
            coordinates, momenta, rates, old = original.initial()
            new_coordinates, new_momenta, new_rates, new = corrected.initial()
            old_residual, new_residual = old.off_grid_residual(rates), new.off_grid_residual(new_rates)
            probes = np.linspace(new.edges[0], new.edges[-1], 1001)
            old_values, new_values = old.values(probes), new.values(probes)
            metric_difference = max(float(max(abs(old_values[index]-new_values[index]))) for index in [0, 1])
            row = dict(branch='MTS' if gram else 'reference', old_minimum_interval=float(min(old.lengths)),
                new_minimum_interval=float(min(new.lengths)), edge_tolerance=new.edge_tolerance,
                merged_edge_clusters=new.edge_merges, old_radial_residual=old_residual, new_radial_residual=new_residual,
                metric_profile_change=metric_difference, momentum_change=float(max(abs(momenta-new_momenta).ravel())))
            evidence.report['cases'].append(row)
            evidence.check(row['branch']+'_only_machine_width_coincidences_merged', row['old_minimum_interval'] < 1e-12
                and row['new_minimum_interval'] > 1e-6 and max(item['spread'] for item in new.edge_merges) <= new.edge_tolerance, row)
            evidence.check(row['branch']+'_same_fields_and_velocities', np.array_equal(coordinates, new_coordinates)
                and np.array_equal(rates, new_rates))
            evidence.check(row['branch']+'_radial_residual_failure_removed_without_gate_change', max(old_residual) > .01 and max(new_residual) < 2e-7)
            evidence.check(row['branch']+'_physical_solution_unchanged_to_control_precision', metric_difference < 2e-11
                and row['momentum_change'] < 2e-11)
            print(row, flush=True)
        evidence.report.update(original_failed_attempt_preserved='annular-live-P2-canonical-attempt01',
            equations_and_data_unchanged=True, acceptance_threshold_unchanged=True,
            radial_partition_roundoff_fix_only=True, no_forward_evolution=True,
            github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
