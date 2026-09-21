from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_characteristic_field_20260917 import FullCharacteristicField
from derive_annular_characteristic_source_20260917 import force
import argparse
import numpy as np
import sympy as sp


def leading_inner(instant, coordinate):
    source_speed, forcing = .06, .02/6.03
    retardation = np.where(coordinate <= 0., instant+coordinate/(1+source_speed), instant-coordinate/(1-source_speed))
    return forcing*(instant**2-np.maximum(retardation, 0.)**2)/2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            no_nonlinear_finite_trajectory_rerun=True, scalar_reference_only=True, both_finite_actions_unmodified=True,
            exact_forced_convected_halfline_solution=True, matching_to_evolved_finite_action_proven=False,
            initial_layer_only_not_later_envelope=True, uniform_nonlinear_remainder_proven=False)
        instant, coordinate, speed, forcing, radius, slope = sp.symbols('tau y speed forcing radius slope', real=True)
        free = forcing*instant**2/2
        left = forcing*(instant**2-(instant+coordinate/(1+speed))**2)/2
        right = forcing*(instant**2-(instant-coordinate/(1-speed))**2)/2
        for name, value in [('free', free), ('left', left), ('right', right)]:
            operator = sp.diff(value, instant, 2)-2*speed*sp.diff(value, instant, coordinate)-(1-speed**2)*sp.diff(value, coordinate, 2)
            evidence.check(name+'_exact_forced_wave', sp.simplify(operator-forcing) == 0)
        evidence.check('source_boundary_zero', left.subs(coordinate, 0) == 0 and right.subs(coordinate, 0) == 0)
        for name, value, front in [('left', left, -(1+speed)*instant), ('right', right, (1-speed)*instant)]:
            evidence.check(name+'_front_value_continuous', sp.simplify((value-free).subs(coordinate, front)) == 0)
            evidence.check(name+'_front_spatial_derivative_continuous', sp.simplify(sp.diff(value-free, coordinate).subs(coordinate, front)) == 0)
            evidence.check(name+'_front_temporal_derivative_continuous', sp.simplify(sp.diff(value-free, instant).subs(coordinate, front)) == 0)
        trace_difference = sp.diff(left, coordinate).subs(coordinate, 0)-sp.diff(right, coordinate).subs(coordinate, 0)
        pressure = radius**2*(1-speed**2)*slope*trace_difference.subs(forcing, 2*slope/radius)
        evidence.check('inner_pressure_recovers_reference_force_slope', sp.simplify(pressure+4*radius*slope**2*instant) == 0)
        evidence.check('initial_inner_state_zero', not np.any(leading_inner(0., np.linspace(-8., 8., 257))))
        reference = FullCharacteristicField(tight=True, horizon=.021)
        scaled_times = [.5, 1., 2., 4., 6.4]
        coordinates = np.linspace(-8., 8., 257)
        for count in [513, 1025, 2049, 4097]:
            spacing = 1.6/(count-1)
            rows = []
            for tau in scaled_times:
                time = spacing*tau
                state = reference.source.sol(time)
                physical = state[0]+spacing*coordinates
                values = reference.sample(time, physical)
                actual = (values['phi']-.01*spacing*coordinates)/spacing**2
                predicted = leading_inner(tau, coordinates)
                discrepancy = float(max(abs(actual-predicted)))
                actual_force = float(force(time, state))
                predicted_force = -.002412*time
                rows.append(dict(tau=tau, time=time, maximum_scaled_field_remainder=discrepancy,
                    scaled_remainder_over_h=discrepancy/spacing, reference_force=actual_force,
                    leading_force=predicted_force, force_remainder=actual_force-predicted_force,
                    force_remainder_over_h_squared=(actual_force-predicted_force)/spacing**2))
            row = dict(base_count=count, h=spacing, cases=rows,
                maximum_scaled_field_remainder=max(value['maximum_scaled_field_remainder'] for value in rows),
                maximum_scaled_remainder_over_h=max(value['scaled_remainder_over_h'] for value in rows))
            evidence.report['cases'].append(row)
            evidence.check(str(count)+'_finite_reference_expansion', np.isfinite([value for point in rows for value in point.values()]).all())
            evidence.save()
            print({name: value for name, value in row.items() if name != 'cases'}, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
