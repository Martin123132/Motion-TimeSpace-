from derive_annular_source_gravity_20260914 import EvidenceRun
import sympy as sp


def main():
    evidence = EvidenceRun('annular-position-force-flux-identity-attempt01', __file__)
    try:
        evidence.own(evidence.root / 'DERIVATION-20260929-position-force-flux-form.md')
        coordinate, parameter = sp.symbols('coordinate parameter', real=True)
        split = sp.Rational(1, 3)
        edges = [sp.Integer(0), split, sp.Integer(1)]
        fluxes = [(1 + parameter) * (1 + 2 * coordinate + coordinate**2) + parameter * coordinate**3,
            (3 - parameter) * (1 - coordinate + 2 * coordinate**2) + parameter * sp.exp(coordinate)]
        directions = [sp.diff(value, parameter) for value in fluxes]
        local_shapes = []
        for lower, upper in zip(edges[:-1], edges[1:]):
            local = (coordinate - lower) / (upper - lower)
            local_shapes.append([(1-local)*(1-2*local), 4*local*(1-local), local*(2*local-1)])
        indices = [[0, 1, 2], [2, 3, 4]]
        for node in range(5):
            tests = [local_shapes[cell][indices[cell].index(node)] if node in indices[cell] else sp.Integer(0) for cell in range(2)]
            weak = -sum(sp.integrate(directions[cell] * sp.diff(tests[cell], coordinate),
                (coordinate, edges[cell], edges[cell + 1])) for cell in range(2))
            volume = sum(sp.integrate(sp.diff(directions[cell], coordinate) * tests[cell],
                (coordinate, edges[cell], edges[cell + 1])) for cell in range(2))
            jump = (directions[1] - directions[0]).subs(coordinate, split) * tests[0].subs(coordinate, split)
            boundary = directions[0].subs(coordinate, 0) * tests[0].subs(coordinate, 0)
            boundary -= directions[1].subs(coordinate, 1) * tests[1].subs(coordinate, 1)
            error = sp.simplify(weak - volume - jump - boundary)
            evidence.check('exact_P2_flux_derivative_node_' + str(node), error == 0, str(error))
            if node == 2:
                evidence.check('negative_control_omitted_internal_jump', sp.simplify(weak - volume - boundary) != 0,
                    str(sp.simplify(weak - volume - boundary)))
            if node in [0, 4]:
                evidence.check('negative_control_omitted_outer_term_' + str(node), sp.simplify(weak - volume - jump) != 0,
                    str(sp.simplify(weak - volume - jump)))
            evidence.report['cases'].append(dict(node=node, weak=str(sp.simplify(weak)), volume=str(sp.simplify(volume)),
                jump=str(sp.simplify(jump)), boundary=str(sp.simplify(boundary))))
        evidence.report.update(scope='Exact manufactured P2 flux integration-by-parts signs and required traces',
            actual_k0_force_recomputed=False, numerical_precision_gap_closed=False, github_action=False,
            subagents_used=False, original_workbench_write=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
