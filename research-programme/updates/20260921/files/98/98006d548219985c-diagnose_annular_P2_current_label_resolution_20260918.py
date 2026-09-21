from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_current_20260918 import EvolvingP2System, LiveP2Tangent
from annular_repaired_live_geometry_20260915 import material_weight
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-P2-current-label-diagnosis-attempt01', __file__)
    try:
        failed_path = evidence.root/'source-intake/navier-stokes/20260914/annular-P2-current-tangent-resolution-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        evidence.own(failed_path)
        evidence.check('original_resolution_expectation_failure_retained', failed['state'] == 'failed'
            and failed['checks'][-1]['name'] == 'reference_offgrid_scalar_residual_label_refinement')
        evidence.report.update(no_forward_evolution=True, github_action=False, subagents_used=False,
            equations_and_current_gates_unchanged=True, original_6_to_10_gate_not_relabeled_passed=True,
            wider_6_to_18_refinement_test_not_a_convergence_rate_proof=True,
            full_vector_offlabel_accuracy_not_implied_by_current_accuracy=True,
            full_live_P2_force_convergence_proven=False)
        points, weights = np.polynomial.legendre.leggauss(24)
        labels, weights = points/2, weights/2*material_weight(points/2)
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            records = []
            for degree in [6, 10, 18]:
                system = EvolvingP2System(17, gram, layer_degree=degree, radial_degree=18)
                coordinates, momenta, unused, unused2 = system.initial(deformed=True)
                tangent = LiveP2Tangent(system, coordinates, momenta)
                nodes = [tangent.layer_data(label).noether() for label in system.labels]
                offgrid = [tangent.layer_data(label).noether() for label in [-.37, .03, .41]]
                fields = [tangent.layer_data(label) for label in labels]
                absolute_work = np.array([np.sum(abs(item.euler*item.rates[:-1])) for item in fields])
                work_bound = float(weights @ absolute_work)
                comparisons = []
                for target in [5.91, 6.04, 6.25]:
                    correction = []
                    for item in fields:
                        oriented = (item.nodes > target).astype(float)-float(item.coordinates[-1] > target)
                        correction.append(-np.dot(item.euler*item.rates[:-1], oriented))
                    lapse, root = tangent.geometry.metric(target)
                    comparisons.append(dict(radius=target, correction=float(abs(system.coupling*root/lapse*(weights @ correction))),
                        bound=float(system.coupling*root/lapse*work_bound)))
                row = dict(branch=branch, label_degree=degree,
                    nodal_scalar=max(item['scalar_euler'] for item in nodes), nodal_source=max(item['source_euler'] for item in nodes),
                    offgrid_scalar=max(item['scalar_euler'] for item in offgrid), offgrid_source=max(item['source_euler'] for item in offgrid),
                    noether=max(item['residual'] for item in nodes+offgrid), weighted_Euler_work_bound=work_bound,
                    weighted_current_bounds=comparisons)
                records.append(row)
                evidence.report['cases'].append(row)
                evidence.save()
                print(row, flush=True)
                prefix = branch+str(degree)
                evidence.check(prefix+'_nodal_full_vector_Euler', max(row['nodal_scalar'], row['nodal_source']) < 2e-8)
                evidence.check(prefix+'_Noether_identity', row['noether'] < 2e-8)
                evidence.check(prefix+'_derived_weighted_current_bound', all(item['correction'] <= item['bound']+1e-25 for item in comparisons))
            ratio10 = records[1]['offgrid_scalar']/records[0]['offgrid_scalar']
            ratio18 = records[2]['offgrid_scalar']/records[0]['offgrid_scalar']
            evidence.report.setdefault('resolution_results', {})[branch] = dict(ratio_6_to_10=ratio10,
                original_6_to_10_gate_pass=ratio10 < .5, ratio_6_to_18=ratio18,
                finest_offgrid_scalar=records[-1]['offgrid_scalar'])
            evidence.check(branch+'_explicit_wider_6_to_18_control', ratio18 < .5, ratio18)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
