from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_characteristic_field_20260917 import FullCharacteristicField
from pathlib import Path
import argparse
import json
import sympy as sp
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            analytic_bounds_not_sampled_maxima=True, exact_rational_majorants=True,
            formal_proof_assistant_used=False, constants_deliberately_nonsharp=True,
            actual_flat_reference_piecewise_curvature_bound_derived=True,
            actual_finite_MTS_trajectory_regularity_proven=False, base_Galerkin_residual_bound_proven=False,
            nonlinear_neighborhood_bootstrap_proven=False, force_trace_convergence_proven=False)
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        for label in ['annular-characteristic-energy-gate-attempt01', 'annular-full-characteristic-field-attempt01']:
            path = intake/label/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(label+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        fraction = sp.symbols('fraction', real=True)
        envelope = 1-10*fraction**3+15*fraction**4-6*fraction**5
        evidence.check('quintic_envelope_derivative_factored', sp.expand(sp.diff(envelope, fraction)+30*fraction**2*(1-fraction)**2) == 0)
        evidence.check('quintic_endpoint_values', envelope.subs(fraction, 0) == 1 and envelope.subs(fraction, 1) == 0)
        evidence.check('quintic_second_derivative_factored', sp.expand(sp.diff(envelope, fraction, 2)+60*fraction*(1-fraction)*(1-2*fraction)) == 0)
        evidence.check('quintic_third_derivative_bound_form', sp.expand(sp.diff(envelope, fraction, 3)+60-360*fraction*(1-fraction)) == 0)
        rational = sp.Rational
        amplitude, width, support = rational(1, 100), rational(7, 20), rational(11, 20)
        profile_bounds = [amplitude*support,
            amplitude*(1+support*rational(15, 8)/width),
            amplitude*(2*rational(15, 8)/width+support*15/width**2),
            amplitude*(3*15/width**2+support*60/width**3)]
        inner, outer, horizon, speed = rational(26, 5), rational(34, 5), rational(2, 5), rational(3, 4)
        source_mass, initial_speed, anchor = rational(3, 100), rational(3, 50), rational(603, 100)
        lower, upper, gap = anchor-speed*horizon, anchor+speed*horizon, 1-speed
        scalar0, scalar1, scalar2, scalar3 = profile_bounds
        incoming = [(1+initial_speed)*outer*scalar0/2+initial_speed*(outer-inner)*scalar0/2,
            (scalar0+(1+initial_speed)*outer*scalar1)/2,
            ((2+initial_speed)*scalar1+(1+initial_speed)*outer*scalar2)/2,
            ((3+2*initial_speed)*scalar2+(1+initial_speed)*outer*scalar3)/2]
        curvature_trace = 2*incoming[1]/(lower*gap)
        acceleration = upper**2*curvature_trace**2/source_mass
        trace_rate = 2*incoming[2]*(1+speed)/(lower*gap)+curvature_trace*(speed/lower+acceleration/gap)
        prefactor = upper**2/(2*source_mass)
        prefactor_rate = upper*speed/source_mass+5*upper**2*speed*acceleration/(2*source_mass)
        jerk = 2*prefactor_rate*curvature_trace**2+4*prefactor*curvature_trace*trace_rate
        ratio = (1+speed)/gap
        ratio_first = 2*acceleration/gap**3
        ratio_second = 2*jerk/gap**4+6*acceleration**2/gap**5
        reflected = [incoming[0], incoming[1]*ratio,
            incoming[2]*ratio**2+incoming[1]*ratio_first,
            incoming[3]*ratio**3+3*incoming[2]*ratio*ratio_first+incoming[1]*ratio_second]
        outer_bounds = [(incoming[0]+horizon*(incoming[1]+incoming[0]/inner))/(1-horizon/inner)]
        for index in range(1, 4):
            outer_bounds.append(incoming[index]+(incoming[index-1]+outer_bounds[index-1])/inner)
        wave_bounds = [max(values) for values in zip(incoming, reflected, outer_bounds)]
        second_bound = 2*wave_bounds[2]/inner+4*wave_bounds[1]/inner**2+4*wave_bounds[0]/inner**3
        third_bound = 2*wave_bounds[3]/inner+6*wave_bounds[2]/inner**2+12*wave_bounds[1]/inner**3+12*wave_bounds[0]/inner**4
        jacobian_min = min((lower-inner)/(anchor-inner), (outer-upper)/(outer-anchor))
        jacobian_max = max((upper-inner)/(anchor-inner), (outer-lower)/(outer-anchor))
        mapped_second, mapped_third = jacobian_max**2*second_bound, jacobian_max**3*third_bound
        evidence.check('strict_timelike_and_geometry_bounds', gap > 0 and jacobian_min > 0 and lower > inner and upper < outer)
        evidence.check('outer_exponential_rational_majorant_domain', horizon/inner == rational(1, 13))
        evidence.check('source_fronts_no_outer_collision', anchor-horizon > inner and anchor+horizon < outer)
        velocity, material_acceleration, material_jerk = sp.symbols('velocity material_acceleration material_jerk', real=True)
        for sign in [-1, 1]:
            denominator = 1+sign*velocity
            mapping_ratio = (1-sign*velocity)/denominator
            derivative = sp.diff(mapping_ratio, velocity)*material_acceleration/denominator
            second_derivative = (sp.diff(derivative, velocity)*material_acceleration+sp.diff(derivative, material_acceleration)*material_jerk)/denominator
            evidence.check(str(sign)+'_inverse_reflection_first_derivative', sp.simplify(derivative+2*sign*material_acceleration/denominator**3) == 0)
            evidence.check(str(sign)+'_inverse_reflection_second_derivative', sp.simplify(second_derivative+2*sign*material_jerk/denominator**4-6*material_acceleration**2/denominator**5) == 0)
        constants = dict(profile_P0=scalar0, profile_P1=scalar1, profile_P2=scalar2, profile_P3=scalar3,
            source_radius_min=lower, source_radius_max=upper, maximum_speed=speed, timelike_gap=gap,
            source_gradient_bound=curvature_trace, source_acceleration_bound=acceleration, source_jerk_bound=jerk,
            physical_phi_rr_bound=second_bound, physical_phi_rrr_piecewise_bound=third_bound,
            map_J_min=jacobian_min, map_J_max=jacobian_max,
            pulled_phi_second_bound=mapped_second, pulled_phi_third_piecewise_bound=mapped_third)
        constants.update({family+str(index): value for family, values in [('incoming_C', incoming),
            ('source_reflection_C', reflected), ('outer_reflection_C', outer_bounds), ('all_wave_C', wave_bounds)]
            for index, value in enumerate(values)})
        evidence.check('all_majorants_exact_positive_finite_rationals', all(value.is_Rational and value > 0 for value in constants.values()))
        reference = FullCharacteristicField(tight=True)
        sampled_second, sampled_acceleration = 0., 0.
        from derive_annular_characteristic_source_20260917 import rhs
        for instant in np.linspace(0., .4, 41):
            sampled = reference.sample(instant, np.linspace(5.2, 6.8, 1025))
            sampled_second = max(sampled_second, float(max(abs(sampled['phi_rr']))))
            sampled_acceleration = max(sampled_acceleration, abs(float(rhs(instant, reference.source.sol(instant))[1])))
        evidence.check('sampled_reference_below_analytic_bounds_not_source_of_bounds', sampled_second < float(second_bound)
            and sampled_acceleration < float(acceleration))
        evidence.report['cases'].append(dict(maximum_sampled_phi_rr=sampled_second,
            analytic_phi_rr_bound=float(second_bound), maximum_sampled_source_acceleration=sampled_acceleration,
            analytic_source_acceleration_bound=float(acceleration), analytic_phi_rrr_bound=float(third_bound),
            actual_initial_curvature_front_count=2, front_count_excludes_source_interface=True,
            extra_canonical_Gram_residual_rate='O(h**(1/2)) on this reference family; not total evolution error'))
        destination = evidence.output/'analytic-regularity-majorants.json'
        destination.write_text(json.dumps({name: dict(exact=str(value), approximate=float(value)) for name, value in constants.items()},
            indent=2, allow_nan=False)+'\n', encoding='utf-8')
        evidence.own(destination, 'outputs')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
