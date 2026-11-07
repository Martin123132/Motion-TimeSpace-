from derive_annular_source_gravity_20260914 import EvidenceRun
import sympy as sp


def main():
    evidence = EvidenceRun('annular-force-moving-cut-identity-attempt01', __file__)
    try:
        evidence.own(evidence.root/'DERIVATION-20260929-force-moving-cut-terms.md')
        coordinate, parameter = sp.symbols('coordinate parameter', real=True)
        center, speed = sp.Rational(2, 5), sp.Rational(3, 7)
        cut = center+speed*parameter
        left = (1+parameter)*(1+coordinate+coordinate**2)
        families = dict(discontinuous=(left, (2-parameter)*(1+coordinate**3)),
            continuous=(left, left+(coordinate-cut)*(2+coordinate+parameter)))
        tests = [(1-coordinate)*(1-2*coordinate), 4*coordinate*(1-coordinate), coordinate*(2*coordinate-1)]
        for name, (minus, plus) in families.items():
            minus_zero, plus_zero = minus.subs(parameter, 0), plus.subs(parameter, 0)
            minus_direction, plus_direction = [sp.diff(value, parameter).subs(parameter, 0) for value in [minus, plus]]
            baseline_jump = (plus_zero-minus_zero).subs(coordinate, center)
            direction_jump = (plus_direction-minus_direction).subs(coordinate, center)
            if name == 'continuous':
                evidence.check('continuous_family_trace', sp.simplify((plus-minus).subs(coordinate, cut)) == 0)
                evidence.check('continuous_trace_derivative_transport', sp.simplify(direction_jump
                    +speed*sp.diff(plus_zero-minus_zero, coordinate).subs(coordinate, center)) == 0)
            for node, test in enumerate(tests):
                derivative = sp.diff(test, coordinate)
                force = -sp.integrate(minus*derivative, (coordinate, 0, cut))
                force -= sp.integrate(plus*derivative, (coordinate, cut, 1))
                exact = sp.diff(force, parameter).subs(parameter, 0)
                regular = -sp.integrate(minus_direction*derivative, (coordinate, 0, center))
                regular -= sp.integrate(plus_direction*derivative, (coordinate, center, 1))
                moving = baseline_jump*speed*derivative.subs(coordinate, center)
                volume = sp.integrate(sp.diff(minus_direction, coordinate)*test, (coordinate, 0, center))
                volume += sp.integrate(sp.diff(plus_direction, coordinate)*test, (coordinate, center, 1))
                jump = direction_jump*test.subs(coordinate, center)
                outer = minus_direction.subs(coordinate, 0)*test.subs(coordinate, 0)
                outer -= plus_direction.subs(coordinate, 1)*test.subs(coordinate, 1)
                evidence.check(name+':Leibniz:'+str(node), sp.simplify(exact-regular-moving) == 0)
                evidence.check(name+':full_flux_identity:'+str(node), sp.simplify(exact-volume-jump-outer-moving) == 0)
                if name == 'discontinuous':
                    evidence.check(name+':omitted_moving_cut_fails:'+str(node), sp.simplify(exact-regular) != 0)
                else:
                    evidence.check(name+':omitted_H_jump_fails:'+str(node), sp.simplify(exact-volume-outer) != 0)
                evidence.report['cases'].append(dict(family=name, node=node,
                    exact=str(sp.simplify(exact)), regular=str(sp.simplify(regular)),
                    moving_cut=str(sp.simplify(moving)), flux_jump=str(sp.simplify(jump)), valid_for_claim=False))
        evidence.report.update(scope='Exact manufactured moving-cut and regular-flux decomposition',
            actual_metric_trace_continuity_certified=False, actual_position_reaction_modified=False,
            github_action=False, subagents_used=False, original_workbench_write=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
