from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_current_20260918 import EvolvingP2System, LiveP2Tangent
import numpy as np


def main():
    evidence = EvidenceRun('annular-P2-current-tangent-resolution-attempt01', __file__)
    try:
        evidence.report.update(no_forward_evolution=True, github_action=False, subagents_used=False,
            finite_label_collocation_not_exact_Galerkin=True, full_GR_limit_proven=False,
            current_pairing_does_not_replace_full_vector_Euler_residual=True,
            full_live_P2_force_convergence_proven=False)
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            records = []
            for degree, difference_step in [(6, 2e-5), (6, 1e-5), (10, 2e-5)]:
                system = EvolvingP2System(17, gram, layer_degree=degree, radial_degree=18)
                coordinates, momenta, unused, unused2 = system.initial(deformed=True)
                tangent = LiveP2Tangent(system, coordinates, momenta, difference_step)
                nodes = [tangent.layer_data(label).noether() for label in system.labels]
                offgrid = [tangent.layer_data(label).noether() for label in [-.37, .03, .41]]
                row = dict(branch=branch, label_degree=degree, difference_step=difference_step,
                    nodal_scalar=max(item['scalar_euler'] for item in nodes), nodal_source=max(item['source_euler'] for item in nodes),
                    offgrid_scalar=max(item['scalar_euler'] for item in offgrid), offgrid_source=max(item['source_euler'] for item in offgrid),
                    nodal_Noether=max(item['residual'] for item in nodes), offgrid_Noether=max(item['residual'] for item in offgrid))
                records.append((row, tangent.acceleration))
                evidence.report['cases'].append(row)
                evidence.save()
                print(row, flush=True)
                prefix=branch+str(degree)+str(difference_step)
                evidence.check(prefix+'_nodal_full_vector_Euler', max(row['nodal_scalar'], row['nodal_source']) < 2e-8, row)
                evidence.check(prefix+'_full_Noether_separate_from_vector', max(row['nodal_Noether'], row['offgrid_Noether']) < 2e-8)
            difference = float(max(abs(records[0][1]-records[1][1]).ravel()))
            evidence.check(branch+'_tangent_time_difference_control', difference < 2e-7, difference)
            ratio = records[2][0]['offgrid_scalar']/records[0][0]['offgrid_scalar']
            evidence.report.setdefault('label_residual_ratios', {})[branch] = ratio
            evidence.check(branch+'_offgrid_scalar_residual_label_refinement', ratio < .5, ratio)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
