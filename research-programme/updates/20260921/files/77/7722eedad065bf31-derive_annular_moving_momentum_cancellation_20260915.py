from derive_annular_source_gravity_20260914 import EvidenceRun
import sympy as sp
import json


def main():
    evidence = EvidenceRun('annular-moving-momentum-cancellation-attempt01', __file__)
    try:
        left_length, right_length, velocity, kinetic, coefficient, left_slope, right_slope = sp.symbols('L D V A C H_minus H_plus', real=True)
        fraction = sp.symbols('x', real=True)
        left_momentum = sp.integrate(kinetic*(-velocity*left_slope)*(-left_slope*fraction)*left_length, (fraction, 0, 1))
        right_momentum = sp.integrate(kinetic*(-velocity*right_slope)*right_slope*(fraction-1)*right_length, (fraction, 0, 1))
        momentum = left_momentum+right_momentum
        expected = kinetic*velocity*(left_slope**2*left_length+right_slope**2*right_length)/2
        evidence.check('leading_field_source_momentum_is_mesh_small', sp.simplify(momentum-expected) == 0)
        momentum_rate = velocity*(sp.diff(momentum, left_length)-sp.diff(momentum, right_length))
        leading_rate = kinetic*velocity**2*(left_slope**2-right_slope**2)/2
        evidence.check('mesh_small_momentum_has_finite_time_derivative', sp.simplify(momentum_rate-leading_rate) == 0)
        pressure = (coefficient-kinetic*velocity**2)*(left_slope**2-right_slope**2)/2
        evidence.check('static_looking_shape_covector_requires_momentum_cancellation', sp.simplify(pressure+leading_rate-coefficient*(left_slope**2-right_slope**2)/2) == 0)
        path = evidence.output.parent/'annular-continuum-moving-force-limit-attempt01/status.json'
        previous = json.loads(path.read_text())
        evidence.own(path)
        for branch in ['reference', 'MTS']:
            rows = [row for row in previous['cases'] if row['count'] == 1025 and row['velocity'] == .25 and row['branch'] == branch]
            error = max(abs(row['source_field_momentum_rate']-row['static_factor_error'])/row['static_factor_error'] for row in rows)
            evidence.report['cases'].append(dict(branch=branch, maximum_relative_leading_momentum_rate_error=error))
            evidence.check(branch+'_finite_rate_term_observed_at_fine_mesh', len(rows) == 3 and error < .015, error)
        evidence.report.update(field_source_momentum_O_h_but_time_derivative_not_O_h_generically=True,
                               correct_force_requires_cancellation_before_continuum_limit=True,
                               no_claim_of_pointwise_vanishing_zeta_dot=True,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
