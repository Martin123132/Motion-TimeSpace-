from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_sparse_repaired_cut_20260915 import SparseRepairedCut
from annular_covariant_cut_action_v2_20260915 import CurvedCutAction, history_state
import numpy as np


def main():
    evidence = EvidenceRun('annular-sparse-repaired-cut-equivalence-attempt01', __file__)
    try:
        for count in [17, 33, 65]:
            for gram in [False, True]:
                dense = CurvedCutAction(count, gram)
                sparse = SparseRepairedCut(count, gram)
                coordinates, rates, unused = history_state(dense, .1)
                first, second = dense.evaluate(.1, coordinates, rates), sparse.evaluate(.1, coordinates, rates)
                errors = {key:float(np.max(abs(first[key]-second[key]))) for key in ['action', 'wave_action', 'momenta', 'scalar_covector', 'nodal_dual']}
                bands = second['mass_bands']
                mass = np.diag(bands[1])+np.diag(bands[0, 1:], 1)+np.diag(bands[2, :-1], -1)
                errors['velocity_hessian'] = float(np.max(abs(first['inertia'][:-1, :-1]-mass)))
                errors['cross_inertia'] = float(np.max(abs(first['inertia'][:-1, -1]-second['cross'])))
                errors['source_inertia'] = float(abs(first['inertia'][-1, -1]-second['source_inertia']))
                errors['acceleration'] = float(np.max(abs(dense.acceleration(.1, coordinates, rates)-sparse.acceleration(.1, coordinates, rates))))
                row = dict(count=count, branch='MTS' if gram else 'reference', errors=errors)
                evidence.report['cases'].append(row)
                evidence.check(str(count)+row['branch']+'_full_action_and_arrow_Hessian', max(value for key, value in errors.items() if key != 'acceleration') < 2e-10, row)
                evidence.check(str(count)+row['branch']+'_independent_dense_acceleration', errors['acceleration'] < 2e-8, row)
                evidence.check(str(count)+row['branch']+'_all_factors_unchanged', np.max(abs(dense.original-sparse.original.toarray()), initial=0.) < 2e-14
                               and np.max(abs(dense.sampling-sparse.sampling.toarray()), initial=0.) < 2e-14)
        evidence.report.update(sparse_repaired_action_equivalent_to_original=True, all_Gram_rows_retained=True,
                               equations_or_forces_changed=False, full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
