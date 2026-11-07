from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from construct_annular_septic_response_20261003 import pin
import sympy as sp


def main():
    pin(2)
    evidence = EvidenceRun('annular-zero-load-third-jet-law-attempt01', __file__)
    try:
        time = sp.Symbol('t', real=True)
        beta, speed = sp.symbols('beta speed_square', positive=True)
        A_second, C_second, mean, mean_second, jump_second, coefficient_second = sp.symbols('A_second C_second mean mean_second jump_second coefficient_second')
        force = A_second * time**2 / 2
        shape = C_second * time**2 / 2
        gradient_mean = mean + mean_second * time**2 / 2
        gradient_jump = jump_second * time**2 / 2
        moving_coefficient = beta + coefficient_second * time**2 / 2
        jump_equation = sp.diff(moving_coefficient * gradient_jump - force, time, 2).subs(time, 0)
        point_equation = sp.diff(force * gradient_mean + shape, time, 2).subs(time, 0)
        evidence.check('zero_initial_load_jump_equation', sp.simplify(jump_equation - (beta * jump_second - A_second)) == 0)
        evidence.check('zero_initial_load_point_compatibility', sp.simplify(point_equation - (A_second * mean + C_second)) == 0)
        evidence.check('mean_second_is_not_divided_by_zero', sp.diff(point_equation, mean_second) == 0)
        third_jump = A_second / (beta * speed)
        evidence.check('bulk_third_jet_jump_solves_transmission', sp.simplify(jump_equation.subs(jump_second, speed * third_jump)) == 0)
        report = verify_report(evidence, 'source-intake/navier-stokes/20260914/annular-septic-source-corrected-time-response-attempt01/status.json')
        evidence.check('measured_maximum_outside_old_active_region', not report['witnesses']['jump']['witness_in_original_active_region'])
        evidence.report.update(derived_law='[ell] = A_ddot/(beta*c^2)', required_compatibility='C_ddot + g*A_ddot = 0',
            assumptions=['A0=C0=0', 'initial gradient jump zero', 'initial curvature jump zero', 'time symmetry', 'positive beta and c^2', 'common local metric coefficients'],
            no_division_by_A=True, inherited_mean_third_may_be_retained_if_compatible=True,
            measured_jump_second=report['witnesses']['jump'],
            measured_inactive_point_second=report['witnesses']['point']['inactive_maximum'],
            exact_zero_load_assumptions_not_inferred_from_numeric_mask=True,
            repaired_profile_constructed=False, github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
