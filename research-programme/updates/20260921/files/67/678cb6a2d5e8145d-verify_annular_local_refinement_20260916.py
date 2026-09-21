from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from derive_annular_boundary_inertia_20260916 import boundary_inertia
from run_annular_source_fitted_crossing_20260915 import initial
from scipy.sparse import coo_matrix
import numpy as np
import json


def main():
    evidence = EvidenceRun('annular-local-refinement-qualification-attempt01',__file__)
    try:
        for count,splits in [(33,4),(65,8),(129,2),(257,8),(513,4)]:
            for gram in [False,True]:
                branch = 'MTS' if gram else 'reference'
                old = QuadraticSourceFittedAction(count,gram,background_mass=0.)
                system = LocallyRefinedSourceAction(count,gram,background_mass=0.,source_splits=splits)
                indices,shape,unused = old.features_quadratic(system.radii)
                embedding = coo_matrix((shape.ravel(),(np.repeat(np.arange(system.count),3),indices.ravel())),shape=(system.count,old.count)).tocsr()
                original = initial(old)
                original_coordinates,original_rates = np.split(original[:-1],2)
                original_coordinates[:-1] += .0003*np.sin(13*(old.radii-old.anchor))
                original_rates[:-1] += .0007*np.sin(11*(old.radii-old.anchor))
                for position in [6.03,6.09]:
                    original_coordinates[-1] = position
                    coordinates = np.append(embedding @ original_coordinates[:-1],position)
                    rates = np.append(embedding @ original_rates[:-1],original_rates[-1])
                    before = old.evaluate(0.,original_coordinates,original_rates)
                    after = system.evaluate(0.,coordinates,rates)
                    prefix = str(count)+branch+str(position)
                    evidence.check(prefix+'_old_quadratic_action_exactly_embedded',abs(before['action']-after['action']) < 2e-13)
                    evidence.check(prefix+'_full_canonical_momentum_embedded',np.max(abs(embedding.T @ after['momenta'][:-1]-before['momenta'][:-1])) < 2e-12
                        and abs(after['momenta'][-1]-before['momenta'][-1]) < 2e-12)
                    evidence.check(prefix+'_source_and_field_covectors_embedded',np.max(abs(embedding.T @ after['scalar_covector']-before['scalar_covector'])) < 2e-10
                        and abs(system.source_covector(0.,coordinates,rates)-old.source_covector(0.,original_coordinates,original_rates)) < 2e-11)
                row = boundary_inertia(system,initial(system))
                row.update(count=count,branch=branch,source_splits=splits,scalar_dofs=system.count,old_scalar_dofs=old.count)
                evidence.check(str(count)+branch+'_all_original_Gram_rows_and_true_jump',system.original.shape[0] == old.original.shape[0]
                    and np.max(abs(system.jump @ embedding-old.jump)) < 2e-9)
                evidence.report['cases'].append(row)
                evidence.save()
        path = evidence.root/'source-intake/navier-stokes/20260914/annular-boundary-capacity-attempt01/status.json'
        evidence.own(path)
        capacity = json.loads(path.read_text())
        evidence.check('refinement_counts_selected_by_derived_capacity',capacity['state']=='complete'
            and [(row['count'],row['source_splits']) for row in capacity['local_refinement_decisions']] == [(257,8),(513,4)])
        evidence.report.update(scope='Nested local quadratic refinement, full old action and Gram/source momentum retained; initial source controls, not an evolved-force pass.',
            all_original_vertex_Gram_rows_retained=True,no_force_correction=True,
            live_quadratic_geometry_qualified=False,uniform_all_time_force_bound_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
