from __future__ import annotations

from fractions import Fraction
from velocity_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[];injections=[];numerics=[];draws=[];profiles=[]
    def check(name,passed,value=None,limit=None):
        checks.append(dict(name=name,passed=bool(passed),value=value,limit=limit))
    fits=json.loads((ROOT/'results/velocity-fits/status.json').read_text())
    parent=json.loads((PARENT/'results/diagnostic-fits/status.json').read_text())
    moment_report=json.loads((ROOT/'results/derived-moments/status.json').read_text())
    legendre={0:{0:Fraction(1)},2:{2:Fraction(3,2),0:Fraction(-1,2)},
        4:{4:Fraction(35,8),2:Fraction(-30,8),0:Fraction(3,8)},
        6:{6:Fraction(231,16),4:Fraction(-315,16),2:Fraction(105,16),0:Fraction(-5,16)}}
    expected={0:[Fraction(1,3),Fraction(1,5),Fraction(1,7)],
        2:[Fraction(2,3),Fraction(4,7),Fraction(10,21)],
        4:[Fraction(0),Fraction(8,35),Fraction(24,77)],
        6:[Fraction(0),Fraction(0),Fraction(16,231)]}
    for ell,polynomial in legendre.items():
        for index,power in enumerate([2,4,6]):
            actual=sum((2*ell+1)*coefficient/Fraction(exponent+power+1) for exponent,coefficient in polynomial.items())
            check(f'exact_leading_ell{ell}_power{power}',actual==expected[ell][index],str(actual),str(expected[ell][index]))
    random=np.random.default_rng(5807)
    variance=12.3;sample_count=200000
    for family in FAMILIES:
        if family=='gaussian':
            displacements=random.normal(0,math.sqrt(variance),(2,sample_count))
        else:
            displacements=random.laplace(0,math.sqrt(variance/2),(2,sample_count))
        pair=displacements[0]-displacements[1]
        for wave in [.01,.05,.1,.2]:
            phases=np.cos(wave*pair)
            measured=float(np.mean(phases));standard_error=float(np.std(phases,ddof=1)/math.sqrt(sample_count))
            expected_damping=math.exp(-variance*wave**2) if family=='gaussian' else (1+variance*wave**2/2)**-2
            significance=abs(measured-expected_damping)/standard_error
            check(f'{family}_independent_pair_draw_{wave}',significance<5,significance,5)
            draws.append(dict(family=family,wave=wave,measured=measured,expected=expected_damping,standard_error=standard_error))
        check(f'{family}_pair_variance_factor_two',abs(float(np.var(pair))/(2*variance)-1)<.02,float(np.var(pair)/(2*variance)),1.)
        tiny=1e-6
        damping=math.exp(-tiny) if family=='gaussian' else (1+tiny/2)**-2
        check(f'{family}_leading_coefficient',abs((1-damping)/tiny-1)<1e-6,(1-damping)/tiny,1.)
        grid=np.linspace(0,100,1001)
        positive=np.exp(-grid) if family=='gaussian' else (1+grid/2)**-2
        check(f'{family}_positive_bounded_response',np.all(positive>0) and np.all(positive<=1))
    for row in fits['rows']:
        fit=row['fit']
        prefix=f"{row['branch']}_{row['family']}_{row['cap']}_{row['kmax']}_{len(row['ells'])}"
        check(prefix+'_converged',fit['converged'] and any(value['success'] for value in fit['starts']))
        check(prefix+'_bounds',.5<=fit['bias']<=4 and 0<=fit['variance']<=64 and -10000<=fit['noise']<=10000)
        check(prefix+'_edges_explicit',fit['upper_variance_boundary']==(fit['variance']>64-1e-5) and
            fit['lower_variance_boundary']==(fit['variance']<1e-5) and
            fit['other_boundary']==(min(fit['bias']-.5,4-fit['bias'])<1e-5 or min(fit['noise']+10000,10000-fit['noise'])<.1))
        check(prefix+'_nested_improvement',row['improvement_over_no_smearing']>=-1e-6,row['improvement_over_no_smearing'],-1e-6)
        check(prefix+'_direct_table_distance',row['direct_interpolation_distance']<.01,row['direct_interpolation_distance'],.01)
        check(prefix+'_independent_direct_score',abs(row['direct_chi2_raw']-fit['chi2_raw'])<1e-6,
            abs(row['direct_chi2_raw']-fit['chi2_raw']),1e-6)
        check(prefix+'_Hartlap_data_dimension',fit['hartlap_factor']==(previous.NMOCK-fit['bins']-2)/(previous.NMOCK-1))
        check(prefix+'_coefficient_not_promoted',not row['coefficient_parent_derived'] and not row['formal_model_preference'])
    for label in ['heavy','cold','lcdm']:
        angular=AngularResponse(label)
        variants={'angular32':AngularResponse(label,nmu=32),'pchip':AngularResponse(label,method='pchip')}
        for family in FAMILIES:
            for cap in ['NGC','SGC']:
                prefix=f'{label}_{family}_{cap}'
                survey=np.load(PARENT/'results/prepared'/(cap+'.npz'))
                packet=np.load(ROOT/'results/response-tables'/(label+'-'+family+'-'+cap+'.npz'))
                indices=previous.select()
                covariance=survey['covariance'][np.ix_(indices,indices)]
                primary=next(row for row in fits['rows'] if row['branch']==label and row['family']==family and row['cap']==cap and row['kmax']==.1 and row['ells']==[0,2])
                fit=primary['fit']
                table=packet['basis'][:,:,indices]
                baseline=next(row for row in parent['rows'] if row['branch']==label and row['cap']==cap and row['kmax']==.1 and row['ells']==[0,2])['fit']
                recovered_zero=previous.fit_nuisance(table[0],survey['data'][indices],covariance)
                check(prefix+'_zero_limit_score',abs(recovered_zero['chi2_raw']-baseline['chi2_raw'])<1e-8,
                    abs(recovered_zero['chi2_raw']-baseline['chi2_raw']),1e-8)
                check(prefix+'_undamped_white_contact',np.array_equal(packet['basis'][:,3,:],np.broadcast_to(packet['basis'][0,3,:],packet['basis'][:,3,:].shape)))
                central=model(convolved(angular.poles(fit['variance'],family),survey['operator']),fit['bias'],fit['noise'])[indices]
                for name,variant in variants.items():
                    prediction=model(convolved(variant.poles(fit['variance'],family),survey['operator']),fit['bias'],fit['noise'])[indices]
                    distance=previous.covariance_norm(prediction-central,covariance)
                    check(prefix+'_'+name,distance<.01,distance,.01)
                    numerics.append(dict(branch=label,family=family,cap=cap,variant=name,distance=distance))
                for injected_variance in [.375,12.345,38.765]:
                    truth=[1.973,injected_variance,321.]
                    synthetic=model(convolved(angular.poles(truth[1],family),survey['operator']),truth[0],truth[2])[indices]
                    recovered=fit_response(packet['grid'],table,synthetic,covariance)
                    errors=[abs(recovered['bias']/truth[0]-1),abs(recovered['variance']/truth[1]-1),abs(recovered['noise']-truth[2])]
                    check(prefix+f'_offgrid_injection_{truth[1]}',errors[0]<1e-4 and errors[1]<1e-4 and errors[2]<.05,errors,[1e-4,1e-4,.05])
                    check(prefix+f'_offgrid_prediction_{truth[1]}',recovered['chi2_raw']<1e-10,recovered['chi2_raw'],1e-10)
                    injections.append(dict(branch=label,family=family,cap=cap,truth=truth,errors=errors,recovered=recovered))
                scanned=[]
                for grid_index in range(0,len(packet['grid']),8):
                    fixed=previous.fit_nuisance(table[grid_index],survey['data'][indices],covariance)
                    scanned.append(dict(variance=float(packet['grid'][grid_index]),chi2_raw=fixed['chi2_raw']))
                profile_minimum=min(row['chi2_raw'] for row in scanned)
                check(prefix+'_independent_fixed_variance_profile',fit['chi2_raw']<=profile_minimum+1e-7,fit['chi2_raw']-profile_minimum,1e-7)
                profiles.append(dict(branch=label,family=family,cap=cap,rows=scanned))
                spline=interpolate.CubicSpline(packet['grid'],table,axis=0)
                center=np.array([fit['bias'],fit['variance'],fit['noise']])
                basis=spline(center[1]);derivative=spline.derivative()(center[1])
                analytic=np.column_stack([2*center[0]*basis[0]+basis[1],model(derivative,center[0],center[2]),basis[3]])
                numerical=[]
                for parameter_index,step in enumerate([1e-5,1e-3,1e-1]):
                    upper=center.copy();lower=center.copy()
                    upper[parameter_index]+=step;lower[parameter_index]-=step
                    numerical.append((model(spline(upper[1]),upper[0],upper[2])-model(spline(lower[1]),lower[0],lower[2]))/(2*step))
                errors=np.max(abs(analytic-np.array(numerical).T),axis=0)/np.max(abs(analytic),axis=0)
                check(prefix+'_independent_jacobian',max(errors)<1e-6,errors.tolist(),1e-6)
    for branch in moment_report['branches']:
        prefix=branch['branch'];variance=branch['central']['one_point_variance_Mpc_over_h_squared']
        check(prefix+'_coherent_variance_positive',variance>0,variance,0)
        for row in branch['central']['pairwise']:
            pair=row['pairwise_variance_Mpc_over_h_squared']
            check(prefix+f"_pair_positive_bound_{row['separation_Mpc_over_h']}_{row['LOS_cosine']}",0<=pair<=4*variance,pair,4*variance)
            if row['separation_Mpc_over_h']==0:
                check(prefix+f"_coincident_pair_zero_{row['LOS_cosine']}",pair==0)
        for name,error in branch['mode_variance_normalized_changes'].items():
            check(prefix+'_moment_'+name,error<1e-4,error,1e-4)
        check(prefix+'_coherent_not_residual',branch['parent_linear_prediction'] and not branch['equal_to_fitted_residual_variance'])
    for row in moment_report['angular_Bessel_identity']:
        check(f"Bessel_{row['argument']}_{row['LOS_cosine']}",row['error']<1e-12,row['error'],1e-12)
    check('all_cases_same_six_tracer_parameters',all(row['tracer_parameters']==6 for row in fits['summaries']))
    check('same_case_same_data_count',all(len({row['data_count'] for row in fits['summaries'] if row['kmax']==kmax and row['ells']==ells})==1
        for kmax,ells in [(.1,[0,2]),(.08,[0,2]),(.12,[0,2]),(.1,[0,2,4])]))
    check('no_overlap_added',not fits['overlap_scores_added'])
    check('coherent_and_tracer_physics_separated',moment_report['not_density_weighted_pair_distribution'] and moment_report['not_residual_galaxy_velocity_calibration'])
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        independent_residual_draws=draws,offgrid_direct_injections=injections,numerical_crosschecks=numerics,
        independent_fixed_variance_profiles=profiles,real_mock_catalogs_used=False,
        scope='Exact angular coefficients and controlled numerical/stochastic validation, not nonlinear tracer or omitted-window calibration.'),
        __file__,[ROOT/'results/velocity-fits/status.json',ROOT/'results/response-tables/status.json',
            ROOT/'results/derived-moments/status.json',PARENT/'results/diagnostic-fits/status.json'])
    failed=[row for row in checks if not row['passed']]
    print(json.dumps(dict(count=len(checks),failed=failed),indent=2))
    assert not failed


if __name__=='__main__':
    main()
