from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import GradedSourceAction, nested_embedding
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
import contextlib
import json
import numpy as np
import sympy as symbolic


def main():
    evidence = EvidenceRun('annular-P2-graded-source-algebra-attempt02', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_forward_evolution=True,
            nested_space_not_new_physical_force=True, full_live_P2_force_convergence_proven=False,
            uniform_halfline_mass_law_not_a_graded_live_convergence_theorem=True)
        coordinate = symbolic.symbols('coordinate', real=True)
        basis = symbolic.Matrix([(1-coordinate)*(1-2*coordinate), 4*coordinate*(1-coordinate), coordinate*(2*coordinate-1)])
        mass = symbolic.integrate(basis*basis.T, (coordinate, 0, 1))
        endpoints = mass.extract([0, 2], [0, 2])-mass.extract([0, 2], [1])*mass.extract([1], [0, 2])/mass[1, 1]
        evidence.check('P2_endpoint_mass_after_midpoint_elimination', endpoints == symbolic.Matrix([[3, -1], [-1, 3]])/24)
        tail = symbolic.Rational(1, 8)+symbolic.sqrt(2)/12
        evidence.check('positive_halfline_tail_fixed_point', symbolic.simplify(tail-(symbolic.Rational(1, 4)-1/(576*tail))) == 0)
        boundary = symbolic.Rational(1, 8)-1/(576*tail)
        evidence.check('exact_halfline_boundary_mass', symbolic.simplify(boundary-1/(6*symbolic.sqrt(2))) == 0)
        for cells in [8, 16, 32]:
            reduced = np.zeros((cells+1, cells+1))
            for element in range(cells):
                reduced[element:element+2, element:element+2] += np.array([[3., -1.], [-1., 3.]])/24
            numerical = reduced[0, 0]-reduced[0, 1:] @ np.linalg.solve(reduced[1:, 1:], reduced[1:, 0])
            evidence.check('finite_halfline_'+str(cells), abs(numerical-1/(6*np.sqrt(2))) < 2e-12, float(numerical))
        for count in [65, 129, 257]:
            for gram in [False, True]:
                coarse = LocallyRefinedSourceAction(count, gram, order=32, background_mass=.7, source_splits=8)
                fine = GradedSourceAction(count, gram)
                embedding = nested_embedding(coarse, fine)
                values = np.append(.001*np.sin(coarse.radii*3.7)+.0002*np.cos(coarse.radii*8.2), coarse.anchor+.003)
                rates = np.append(.0003*np.cos(coarse.radii*2.1), .04)
                fine_values = np.append(embedding @ values[:-1], values[-1])
                fine_rates = np.append(embedding @ rates[:-1], rates[-1])
                old, new = coarse.evaluate(0., values, rates), fine.evaluate(0., fine_values, fine_rates)
                row = dict(branch='MTS' if gram else 'reference', base_count=count, scalar_nodes=fine.count,
                    source_bisections=fine.source_bisections,
                    action_error=float(abs(old['action']-new['action'])),
                    kinetic_error=float(abs(old['kinetic']-new['kinetic'])),
                    potential_error=float(abs(old['potential']-new['potential'])),
                    momentum_pullback_error=float(max(abs(embedding.T @ new['momenta'][:-1]-old['momenta'][:-1]))),
                    scalar_covector_pullback_error=float(max(abs(embedding.T @ new['scalar_covector']-old['scalar_covector']))),
                    source_covector_error=float(abs(coarse.source_covector(0., values, rates)-fine.source_covector(0., fine_values, fine_rates))),
                    lifted_operator_error=float(np.max(abs((fine.lifted @ embedding-coarse.lifted).toarray()), initial=0.)))
                evidence.report['cases'].append(row)
                key = row['branch']+str(count)
                evidence.check(key+'_embedded_action', max(row['action_error'], row['kinetic_error'], row['potential_error']) < 2e-12, row)
                evidence.check(key+'_embedded_momentum', row['momentum_pullback_error'] < 2e-12)
                evidence.check(key+'_embedded_covectors', max(row['scalar_covector_pullback_error'], row['source_covector_error']) < 2e-9)
                evidence.check(key+'_Gram_operator_retained', row['lifted_operator_error'] < 2e-9)
                source = int(np.searchsorted(fine.edges, fine.anchor))
                evidence.check(key+'_positive_graded_cells', min(np.diff(fine.edges)) > 0
                    and max(np.diff(fine.edges)[source-1:source+1]) <= fine.source_cap)
        with (evidence.output/'completion-log.txt').open('w') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion-log.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), cases=evidence.report['cases'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
