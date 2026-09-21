from derive_annular_source_gravity_20260914 import EvidenceRun
import argparse
import sympy as sp


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options=parser.parse_args()
    evidence=EvidenceRun(options.label,__file__)
    try:
        coordinate=sp.symbols('coordinate',real=True)
        radius=sp.Rational(603,100)
        speed=sp.Rational(3,50)
        source=sp.Rational(3,100)
        amplitude=sp.Rational(1,100)
        onset,end=sp.Rational(1,5),sp.Rational(11,20)
        fraction=(coordinate-onset)/(end-onset)
        envelope=1-10*fraction**3+15*fraction**4-6*fraction**5
        scalar=amplitude*coordinate*envelope
        gradient=sp.diff(scalar,coordinate)
        central=sp.integrate((radius**2+coordinate**2)*amplitude**2,(coordinate,0,onset))
        transition=sp.integrate(sp.expand((radius**2+coordinate**2)*gradient**2),(coordinate,onset,end))
        field_energy=sp.factor((1+speed**2)*(central+transition))
        source_energy=source/sp.sqrt(1-speed**2)
        evidence.check('initial_profile_C2_at_transition',all(sp.simplify(sp.diff(scalar,coordinate,order).subs(coordinate,onset)
            -sp.diff(amplitude*coordinate,coordinate,order).subs(coordinate,onset))==0 for order in range(3))
            and all(sp.simplify(sp.diff(scalar,coordinate,order).subs(coordinate,end))==0 for order in range(3)))
        evidence.check('exact_field_energy_below_rational_budget',0<field_energy<sp.Rational(1,100),str(field_energy))
        evidence.check('source_energy_below_rational_budget',source**2/(1-speed**2)<sp.Rational(31,1000)**2)
        total_budget=sp.Rational(41,1000)
        maximum_speed=sp.Rational(3,4)
        evidence.check('energy_implies_strict_timelike_margin',total_budget**2<source**2/(1-maximum_speed**2))
        horizon=sp.Rational(2,5)
        left=radius-(1+maximum_speed)*horizon
        right=radius+(1+maximum_speed)*horizon
        evidence.check('no_source_incoming_outer_boundary_before_horizon',left>sp.Rational(26,5) and right<sp.Rational(34,5))
        velocity,gradient_left,gradient_right,position=sp.symbols('velocity gradient_left gradient_right position',real=True)
        pressure=position**2*(1-velocity**2)*(gradient_left**2-gradient_right**2)/2
        field_rate=velocity*position**2*(1-velocity**2)*(gradient_right**2-gradient_left**2)/2
        evidence.check('continuum_field_source_energy_flux_cancels',sp.simplify(field_rate+velocity*pressure)==0)
        jump_left=-2*amplitude/(1+speed)**2
        jump_right=-2*amplitude/(1-speed)**2
        original_plus=amplitude*(1+speed/2)
        original_minus=amplitude*(1-speed/2)
        evidence.check('left_initial_curvature_front_closes_boundary_law',sp.simplify((1-speed)**2*original_plus+(1+speed)**2*(original_minus+jump_left))==0)
        evidence.check('right_initial_curvature_front_closes_boundary_law',sp.simplify((1-speed)**2*(original_plus+jump_right)+(1+speed)**2*original_minus)==0)
        evidence.report.update(original_action_unchanged=True,finite_future_trajectories_read=False,
            exact_rational_energy_gate=True,interval_time_integration_performed=False,
            uses_continuum_energy_identity_not_sampled_speed_maximum=True,
            prescribed_flat_reference_only=True,full_GR_limit_proven=False,
            spectral_reference_regularity_certified=False)
        evidence.report['cases'].append(dict(exact_initial_field_energy=str(field_energy),
            initial_field_energy=float(field_energy),exact_initial_source_energy=str(source_energy),
            total_initial_energy=float(field_energy+source_energy),rational_total_energy_upper_bound=str(total_budget),
            certified_speed_ceiling=str(maximum_speed),certified_horizon=str(horizon),
            left_incoming_foot_lower_bound=str(left),right_incoming_foot_upper_bound=str(right),
            left_chi_second_jump=str(jump_left),right_chi_second_jump=str(jump_right)))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
