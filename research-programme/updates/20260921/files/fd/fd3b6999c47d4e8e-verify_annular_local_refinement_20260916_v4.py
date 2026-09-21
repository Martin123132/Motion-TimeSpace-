from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from derive_annular_boundary_inertia_20260916 import boundary_inertia
from run_annular_source_fitted_crossing_20260915 import initial
from scipy.sparse import coo_matrix
import numpy as np
import json
import sympy as sp
from fractions import Fraction


def main():
    evidence = EvidenceRun('annular-local-refinement-qualification-attempt04',__file__)
    try:
        evidence.own(evidence.root/'source-intake/navier-stokes/20260914/annular-local-refinement-qualification-attempt01/status.json')
        evidence.own(evidence.root/'scripts/verify_annular_local_refinement_20260916.py')
        evidence.own(evidence.root/'scripts/verify_annular_local_refinement_20260916_v2.py')
        evidence.own(evidence.root/'source-intake/navier-stokes/20260914/annular-local-refinement-qualification-attempt02/status.json')
        evidence.own(evidence.root/'scripts/verify_annular_local_refinement_20260916_v3.py')
        evidence.own(evidence.root/'source-intake/navier-stokes/20260914/annular-local-refinement-qualification-attempt03/status.json')
        local,left,right = sp.symbols('eta left right',real=True)
        basis = lambda value: sp.Matrix([(1-value)*(1-2*value),4*value*(1-value),value*(2*value-1)])
        interpolation = sp.Matrix.hstack(basis(left),basis((left+right)/2),basis(right))*basis(local)
        exact = basis(left+(right-left)*local)
        evidence.check('symbolic_quadratic_subdivision_and_derivative_embedding',all(sp.expand(value)==0 for value in interpolation-exact)
            and all(sp.expand(value)==0 for value in sp.diff(interpolation-exact,local)))
        for count,splits in [(33,4),(65,8),(129,2),(257,8),(513,4)]:
            for gram in [False,True]:
                branch = 'MTS' if gram else 'reference'
                old = QuadraticSourceFittedAction(count,gram,background_mass=0.)
                system = LocallyRefinedSourceAction(count,gram,background_mass=0.,source_splits=splits)
                ideal_nodes = [Fraction(float(value)) for value in system.radii]
                for element,free_index in enumerate(system.element_indices[:,1]):
                    ideal_nodes[free_index] = (Fraction(float(system.edges[element]))+Fraction(float(system.edges[element+1])))/2
                embedding_rows,embedding_columns,embedding_values = [],[],[]
                for free_index,node in enumerate(ideal_nodes):
                    element = min(max(np.searchsorted(old.edges,float(node),side='right')-1,0),len(old.edges)-2)
                    left_edge,right_edge = Fraction(float(old.edges[element])),Fraction(float(old.edges[element+1]))
                    fraction = (node-left_edge)/(right_edge-left_edge)
                    values = [(1-fraction)*(1-2*fraction),4*fraction*(1-fraction),fraction*(2*fraction-1)]
                    for column,value in zip(old.element_indices[element],values):
                        if column >= 0:
                            embedding_rows.append(free_index)
                            embedding_columns.append(column)
                            embedding_values.append(float(value))
                embedding = coo_matrix((embedding_values,(embedding_rows,embedding_columns)),shape=(system.count,old.count)).tocsr()
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
                jump_absolute = float(np.max(abs(system.jump @ embedding-old.jump)))
                jump_relative = jump_absolute/float(np.max(abs(old.jump)))
                evidence.check(str(count)+branch+'_all_original_Gram_rows_and_true_jump',system.original.shape[0] == old.original.shape[0]
                    and jump_relative < 2e-12 and jump_absolute < 2e-9,dict(absolute_derivative_coefficient_error=jump_absolute,relative_derivative_coefficient_error=jump_relative))
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
