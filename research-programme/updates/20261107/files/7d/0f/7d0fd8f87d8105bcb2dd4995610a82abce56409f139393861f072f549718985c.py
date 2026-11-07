from __future__ import annotations

import sympy as algebra
from transport_common import *
import camb.symbolic as symbolic


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[];rsd_rows=[];precision_rows=[]
    def check(name,passed,value=None,limit=None):
        checks.append(dict(name=name,passed=bool(passed),value=value,limit=limit))
    epsilon,delta,phi,psi=algebra.symbols('eps delta Phi Psi',real=True)
    densitized=(1+epsilon*delta)*(1-2*epsilon*phi)**algebra.Rational(3,2)
    check('metric_volume_linear_density',algebra.simplify(algebra.diff(densitized,epsilon).subs(epsilon,0)-(delta-3*phi))==0)
    determinant=(1+2*epsilon*psi)*(1-2*epsilon*phi)**3
    check('lapse_cancels_at_first_order',algebra.simplify(algebra.diff(algebra.sqrt(determinant)*(1+epsilon*delta)/algebra.sqrt(1+2*epsilon*psi),epsilon).subs(epsilon,0)-(delta-3*phi))==0)
    newtonian=symbolic.cdm_gauge(symbolic.make_frame_invariant(symbolic.Delta_c,'Newtonian'))
    expected=symbolic.Delta_c-3*symbolic.H*symbolic.sigma/symbolic.k
    check('native_symbolic_density_gauge',algebra.simplify(newtonian-expected)==0,str(newtonian),str(expected))
    newtonian_b=symbolic.cdm_gauge(symbolic.make_frame_invariant(symbolic.Delta_b,'Newtonian')).subs(symbolic.p_b,0)
    check('native_symbolic_dust_baryon_gauge',algebra.simplify(newtonian_b-symbolic.Delta_b+3*symbolic.H*symbolic.sigma/symbolic.k)==0)
    wave,hubble,shear,eta,expansion,baryon_fraction,baryon_velocity=algebra.symbols('k H sigma eta z fb vb',real=True)
    coordinate=(delta-3*hubble*shear/wave)-3*(eta-hubble*shear/wave)
    check('metric_and_lapse_shift_cancel',algebra.simplify(coordinate-delta+3*eta)==0)
    eta_prime=wave*(shear-expansion)/3
    density_prime=-wave*(expansion+baryon_fraction*baryon_velocity)
    check('native_flat_continuity_exact',algebra.simplify(density_prime-3*eta_prime+wave*(shear+baryon_fraction*baryon_velocity))==0)
    tangent,flow_parameter=algebra.symbols('tangent g',real=True)
    decay=algebra.exp(-flow_parameter)
    mapped=2*algebra.atan(decay*tangent)
    jacobian=decay*(1+tangent**2)/(1+decay**2*tangent**2)
    check('flow_exact_jacobian',algebra.simplify(algebra.diff(mapped,tangent)*(1+tangent**2)/2-jacobian)==0)
    check('flow_exact_velocity',algebra.simplify(algebra.diff(mapped,flow_parameter)+2*decay*tangent/(1+decay**2*tangent**2))==0)
    bias_initial,density_initial,density_final=algebra.symbols('bi Di Df',nonzero=True)
    bias_final=1+(bias_initial-1)*density_initial/density_final
    check('conserved_tracer_bias',algebra.simplify((bias_final-1)*density_final-(bias_initial-1)*density_initial)==0)
    integral,initial_amplitude=algebra.symbols('I Di',real=True)
    second_order=initial_amplitude*integral+integral**2/2
    check('transport_second_harmonic_coefficient',algebra.diff(second_order,integral)==initial_amplitude+integral)
    continuity=json.loads((ROOT/'results/continuity/status.json').read_text())
    precision=json.loads((ROOT/'results/rhs-precision/status.json').read_text())
    flows=json.loads((ROOT/'results/conserved-flow/status.json').read_text())
    for branch in continuity['branches']:
        label=branch['branch']
        check(label+'_399_qualified_modes',branch['qualified_modes']==399)
        check(label+'_eight_redshifts',len(branch['rows'])==399*8)
        check(label+'_primary_continuity',branch['primary_max_residual']<1e-4,branch['primary_max_residual'],1e-4)
        check(label+'_all_continuity',branch['all_max_residual']<2e-3,branch['all_max_residual'],2e-3)
        check(label+'_conserved_density_identity',branch['conserved_identity_max_error']<1e-9,branch['conserved_identity_max_error'],1e-9)
        check(label+'_constant_matter_weights',branch['baryon_fraction_range']<1e-12)
        metric_error=max(abs(row['sync_only_residual']-row['missing_metric_rate']-row['fractional_residual']) for row in branch['rows'])
        check(label+'_missing_metric_defect_accounted',metric_error<1e-8,metric_error,1e-8)
        native=next(row for row in precision['branches'] if row['branch']==label)
        check(label+'_float32_export_identified',native['exact_float32_density_storage'])
        check(label+'_native_rhs_check',native['all_max_rhs_residual']<1e-5,native['all_max_rhs_residual'],1e-5)
        unexplained=max(max(0,abs(row['time_fd_residual'])-row['float32_rate_error_bound']-abs(row['rhs_residual'])) for row in native['rows'])
        precision_rows.append(dict(branch=label,max_fd_beyond_quantization_and_rhs=unexplained))
        check(label+'_fd_precision_envelope',unexplained<2e-5,unexplained,2e-5)
    for row in flows['rows']:
        prefix=f"{row['branch']}_{row['initial_bias']}_{row['amplitude_magnitude']}"
        check(prefix+'_positive_initial_and_final',min(row['min_initial_density'],row['min_jacobian'],row['min_final_density'])>0)
        check(prefix+'_mass_all_grids',max(row['mass_errors'])<1e-10,max(row['mass_errors']),1e-10)
        check(prefix+'_pointwise_transport',row['pointwise_mass_error']<1e-12)
        check(prefix+'_path_and_jacobian',max(row['path_equation_error'],row['jacobian_error'])<2e-8)
        check(prefix+'_no_nonlinear_promotion',not row['self_consistent_nonlinear_gravity'] and row['nonlinear_Euler_convective_source_normalized_max']>0)
        packet=np.load(ROOT/'results/continuity'/(row['branch']+'.npz'))
        mode=int(np.argmin(abs(packet['modes']-.03)));final=int(np.argmin(abs(packet['scales']-1/1.38)))
        phase=(np.arange(8192)+.5)*2*math.pi/8192
        mapped,jacobian=flow_map(phase,row['integrated_flow_amplitude'])
        amplitude=row['primordial_mode_amplitude']
        weights=1+amplitude*row['initial_coordinate_transfer']*np.cos(phase)
        velocity=packet['velocity'][mode,final]
        redshift_phase=mapped-amplitude*velocity*np.sin(mapped)
        redshift_jacobian=jacobian*(1-amplitude*velocity*np.cos(mapped))
        coefficients=[np.mean(weights*np.exp(-1j*order*redshift_phase)) for order in [0,1,2]]
        expected=amplitude*(row['final_coordinate_linear_transfer']+velocity)/2
        rsd_rows.append(dict(branch=row['branch'],initial_bias=row['initial_bias'],amplitude_magnitude=row['amplitude_magnitude'],
            redshift_min_jacobian=float(min(redshift_jacobian)),coordinate_count_linear_prediction=float(expected),
            fundamental_real=float(coefficients[1].real),second_harmonic_real=float(coefficients[2].real),
            relative_linear_error=float(abs(coefficients[1]/expected-1))))
        check(prefix+'_redshift_map_positive',min(redshift_jacobian)>0)
        check(prefix+'_redshift_total_count',abs(coefficients[0]-1)<1e-12)
    for label in ['heavy','cold','lcdm']:
        for bias in [1.,2.]:
            small=next(row for row in flows['rows'] if row['branch']==label and row['initial_bias']==bias and row['amplitude_magnitude']==.01)
            next_small=next(row for row in flows['rows'] if row['branch']==label and row['initial_bias']==bias and row['amplitude_magnitude']==.05)
            check(f'{label}_{bias}_coordinate_linear_recovery',small['fundamental_linear_absolute_error']/abs(small['linear_prediction'])<1e-5)
            check(f'{label}_{bias}_cubic_fundamental_error',100<next_small['fundamental_linear_absolute_error']/small['fundamental_linear_absolute_error']<150)
            harmonic_coefficient=small['primordial_mode_amplitude']**2*(small['initial_coordinate_transfer']*small['native_integrated_velocity']/2+small['native_integrated_velocity']**2/4)
            check(f'{label}_{bias}_derived_second_harmonic',abs(small['harmonics_real'][2]/harmonic_coefficient-1)<1e-5)
            small_rsd=next(row for row in rsd_rows if row['branch']==label and row['initial_bias']==bias and row['amplitude_magnitude']==.01)
            next_rsd=next(row for row in rsd_rows if row['branch']==label and row['initial_bias']==bias and row['amplitude_magnitude']==.05)
            check(f'{label}_{bias}_count_Kaiser_limit',small_rsd['relative_linear_error']<1e-5,small_rsd['relative_linear_error'],1e-5)
            check(f'{label}_{bias}_count_Kaiser_quadratic_error',20<next_rsd['relative_linear_error']/small_rsd['relative_linear_error']<30)
    check('no_new_fit',not continuity['actual_survey_refit'] and flows['new_parameters_fitted']==0)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        coordinate_count_redshift_probe=rsd_rows,precision_envelopes=precision_rows,
        scope='Native continuity, conserved coordinate current and prescribed-velocity positive flow. Not a complete observed relativistic number-count or nonlinear gravity solver.'),
        __file__,[ROOT/'results/continuity/status.json',ROOT/'results/rhs-precision/status.json',ROOT/'results/conserved-flow/status.json'])
    failed=[row for row in checks if not row['passed']]
    print(json.dumps(dict(count=len(checks),failed=failed,precision=precision_rows),indent=2))
    assert not failed


if __name__=='__main__':
    main()
