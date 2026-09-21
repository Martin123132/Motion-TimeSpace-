from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_local_spectral_step_20260916 import spectral_step
from run_annular_source_fitted_crossing_20260915 import initial
import json


def main():
    evidence = EvidenceRun('annular-local-stiffness-attempt01',__file__)
    try:
        for count,splits in [(257,8),(513,4)]:
            for gram in [False,True]:
                system = LocallyRefinedSourceAction(count,gram,background_mass=0.,source_splits=splits)
                row = spectral_step(system,initial(system))
                row.update(count=count,source_splits=splits,branch='MTS' if gram else 'reference')
                evidence.check(str(count)+row['branch']+'_resolved_positive_field_spectrum',row['largest_field_eigenvalue'] > 0 and row['eigen_residual'] < 2e-8,row)
                evidence.report['cases'].append(row)
                print(json.dumps(row),flush=True)
        evidence.report.update(scope='Frozen action-metric stiffness measurement for numerical time-step selection; no physical coupling or force adjustment.',
            live_quadratic_geometry_qualified=False,full_nonlinear_stability_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
