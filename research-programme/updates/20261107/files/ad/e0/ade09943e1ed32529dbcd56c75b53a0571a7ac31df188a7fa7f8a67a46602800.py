from __future__ import annotations

import sympy as algebra
from streaming_common import *


def log_gaussian_interval(lower,upper):
    if lower>=0:
        first=float(special.log_ndtr(-lower));second=float(special.log_ndtr(-upper))
        return first+math.log(-math.expm1(second-first))
    if upper<=0:
        first=float(special.log_ndtr(upper));second=float(special.log_ndtr(lower))
        return first+math.log(-math.expm1(second-first))
    return math.log(float(special.ndtr(upper)-special.ndtr(lower)))


def quadrature(covariance,order=18):
    nodes,weights=np.polynomial.hermite_e.hermegauss(order)
    coordinates=np.array(np.meshgrid(nodes,nodes,nodes,indexing='ij')).reshape(3,-1)
    factors=np.array(np.meshgrid(weights,weights,weights,indexing='ij')).prod(axis=0).ravel()/(2*math.pi)**1.5
    return linalg.cholesky(covariance,lower=True)@coordinates,factors


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[];identities=[];tail_bounds=[];plane_waves=[];non_gaussian=[]
    def check(name,passed,value=None,limit=None):
        checks.append(dict(name=name,passed=bool(passed),value=value,limit=limit))
    correlation,cross,variance,density_variance,moment_parameter,first_source,second_source=algebra.symbols('xi C S variance_density lam j1 j2',real=True)
    joint=algebra.exp((density_variance*(first_source**2+second_source**2)+2*correlation*first_source*second_source+
        2*cross*moment_parameter*(first_source+second_source)+variance*moment_parameter**2)/2)
    weighted=(joint+algebra.diff(joint,first_source)+algebra.diff(joint,second_source)+algebra.diff(joint,first_source,second_source)).subs({first_source:0,second_source:0})
    exact=(1+correlation+2*cross*moment_parameter+cross**2*moment_parameter**2)*algebra.exp(variance*moment_parameter**2/2)
    difference=algebra.simplify(weighted-exact)
    check('joint_Gaussian_derivative_identity',difference==0,str(difference),'0')
    normal=1+correlation;log_generating=algebra.log(exact/normal)
    expected=[2*cross/normal,variance+2*cross**2/normal-4*cross**2/normal**2,
        4*cross**3*(1-3*correlation)/normal**3,-12*cross**4*(1-6*correlation+correlation**2)/normal**4]
    for order,prediction in enumerate(expected,1):
        derived=algebra.simplify(algebra.diff(log_generating,moment_parameter,order).subs(moment_parameter,0))
        error=algebra.simplify(derived-prediction)
        check(f'cumulant{order}_exact',error==0,str(error),'0')
        identities.append(dict(order=order,expression=str(derived)))
    ratio,coordinate=algebra.symbols('alpha z',real=True)
    polynomial=1+2*ratio*coordinate/normal+ratio**2*(coordinate**2-1)/normal
    completed=(ratio**2*(coordinate+1/ratio)**2+correlation-ratio**2)/normal
    check('exact_positivity_square',algebra.simplify(polynomial-completed)==0)
    amplitude=algebra.symbols('epsilon',real=True)
    first_order=algebra.diff(exact.subs({correlation:amplitude*correlation,cross:amplitude*cross,variance:amplitude*variance}),amplitude).subs(amplitude,0)
    check('linear_pair_generator',algebra.simplify(first_order-correlation-2*moment_parameter*cross-variance*moment_parameter**2/2)==0)
    report=json.loads((ROOT/'results/pair-streaming/status.json').read_text())
    old=json.loads((PARENT/'results/derived-moments/status.json').read_text())
    for branch in report['branches']:
        label=branch['branch'];central=branch['central']
        limits={'xi_cb':2e-6,'cross_Mpc_over_h':2e-5,'pair_variance_Mpc_over_h_squared':2e-4}
        for key,limit in limits.items():
            value=branch['primary_numerical_differences']['refined'][key]
            check(label+'_refinement_'+key,value<limit,value,limit)
        parent=next(row['central'] for row in old['branches'] if row['branch']==label)
        check(label+'_parent_onepoint',abs(central['variance_displacement']-parent['one_point_variance_Mpc_over_h_squared'])<1e-7)
        common=[]
        for prior in parent['pairwise']:
            matching=[row for row in central['rows'] if row['separation_Mpc_over_h']==prior['separation_Mpc_over_h'] and row['LOS_cosine']==prior['LOS_cosine']]
            if matching:
                common.append(abs(matching[0]['pair_variance_Mpc_over_h_squared']-prior['pairwise_variance_Mpc_over_h_squared']))
        check(label+'_parent_pairwise',max(common)<1e-7,max(common),1e-7)
        check(label+'_positive_covariance',min(row['covariance_min_eigenvalue'] for row in branch['weighted'])>=-1e-10)
        check(label+'_no_refit',branch['new_parameters_fitted']==0 and not branch['nonlinear_parent_distribution_derived'])
        check(label+'_coincident_limit',all(row['mean']==0 and row['central_variance']==0 for row in branch['weighted'] if row['separation_Mpc_over_h']==0))
        check(label+'_transverse_Gaussian_limit',all(row['mean']==0 and row['third_cumulant']==0 and row['central_variance']==row['unweighted_pair_variance'] for row in branch['weighted'] if row['LOS_cosine']==0))
        for row in branch['weighted']:
            positive=row['positivity']
            if not positive['nonnegative']:
                lower,upper=positive['negative_interval_in_sigma']
                log_bound=math.log(-positive['minimum_polynomial'])+log_gaussian_interval(lower,upper)
                mass=positive['negative_mass']
                check(f"{label}_{row['sample']}_{row['separation_Mpc_over_h']}_{row['LOS_cosine']}_signed_tail_retained",
                    mass>=0 and (mass==0 or math.log(mass)<=log_bound+1e-7))
                tail_bounds.append(dict(branch=label,sample=row['sample'],separation=row['separation_Mpc_over_h'],cosine=row['LOS_cosine'],
                    log10_negative_mass_upper=log_bound/math.log(10),computed_negative_mass=mass,
                    interval_in_sigma=[lower,upper],strictly_nonnegative=False))
        for separation in [10.,50.,100.]:
            row=next(row for row in branch['weighted'] if row['sample']=='SGC' and row['LOS_cosine']==1 and row['separation_Mpc_over_h']==separation)
            density_var=row['bias']**2*central['variance_density']
            xi=row['xi_tracer'];mixed=row['cross_Mpc_over_h'];pair=row['unweighted_pair_variance']
            covariance=np.array([[density_var,xi,mixed],[xi,density_var,mixed],[mixed,mixed,pair]])
            values,weights=quadrature(covariance)
            pair_weights=(1+values[0])*(1+values[1])
            normalization=float(weights@pair_weights)
            mean=float(weights@(pair_weights*values[2]))/normalization
            second=float(weights@(pair_weights*(values[2]-mean)**2))/normalization
            third=float(weights@(pair_weights*(values[2]-mean)**3))/normalization
            fourth=float(weights@(pair_weights*(values[2]-mean)**4))/normalization-3*second**2
            for name,actual in [('pair_weight',normalization),('mean',mean),('central_variance',second),('third_cumulant',third),('fourth_cumulant',fourth)]:
                error=abs(actual-row[name])/max(1,abs(row[name]))
                check(f'{label}_{separation}_independent_joint_{name}',error<1e-9,error,1e-9)
            for frequency in [.03,.1]:
                measured=weights@(pair_weights*np.exp(1j*frequency*values[2]))/normalization
                analytic=generating(1j*frequency,xi,mixed,pair)
                error=float(abs(measured-analytic))
                check(f'{label}_{separation}_joint_characteristic_{frequency}',error<1e-10,error,1e-10)
    counter=positivity(-.2,-.4,1.)
    check('valid_covariance_counterexample',min(linalg.eigvalsh([[1,-.2,-.4],[-.2,1,-.4],[-.4,-.4,1]]))>0)
    check('signed_density_failure_detected',not counter['nonnegative'] and counter['negative_mass']>1e-3,counter['negative_mass'],1e-3)
    phi=np.arange(4096)*2*math.pi/4096
    for cosine in [0.,.3,.8,1.]:
        errors=[]
        for amplitude in [.01,.005,.0025]:
            density=1+1.87*.65*amplitude*np.cos(phi)
            shifted=phi-.37*amplitude*cosine**2*np.sin(phi)
            coefficient=np.mean(density*np.exp(-1j*shifted))
            prediction=amplitude*(1.87*.65+.37*cosine**2)/2
            error=float(abs(coefficient/prediction-1))
            errors.append(error)
            plane_waves.append(dict(cosine=cosine,amplitude=amplitude,relative_error=error))
        check(f'number_conservation_Kaiser_{cosine}',errors[-1]<1e-6,errors[-1],1e-6)
        if cosine>0:
            check(f'Kaiser_error_quadratic_{cosine}',errors[1]<.26*errors[0] and errors[2]<.26*errors[1])
    values,weights=quadrature(np.array([[1,.2,-.25],[.2,1,-.25],[-.25,-.25,1.]]))
    first=values[0]+.15*(values[0]**2-1)
    second=values[1]+.15*(values[1]**2-1)
    displacement=values[2]+.08*(values[2]**2-1)
    xi=float(weights@(first*second));mixed_first=float(weights@(first*displacement));mixed_second=float(weights@(second*displacement))
    pair=float(weights@(displacement**2));normal=1+xi
    triple=float(weights@(first*second*displacement))
    mixed21=float(weights@(first*displacement**2));mixed22=float(weights@(second*displacement**2))
    connected4=float(weights@(first*second*displacement**2))-xi*pair-2*mixed_first*mixed_second
    direct_mean=float(weights@((1+first)*(1+second)*displacement))/normal
    direct_raw=float(weights@((1+first)*(1+second)*displacement**2))/normal
    reconstructed_mean=(mixed_first+mixed_second+triple)/normal
    reconstructed_raw=pair+(2*mixed_first*mixed_second+mixed21+mixed22+connected4)/normal
    check('general_mixed_cumulant_mean',abs(direct_mean-reconstructed_mean)<1e-12)
    check('general_mixed_cumulant_second',abs(direct_raw-reconstructed_raw)<1e-12)
    gaussian_raw=pair+2*mixed_first*mixed_second/normal
    check('nonGaussian_correction_not_silent_zero',abs(direct_raw-gaussian_raw)>1e-3,abs(direct_raw-gaussian_raw),1e-3)
    non_gaussian.append(dict(triple=triple,mixed21=mixed21,mixed22=mixed22,connected4=connected4,
        direct_mean=direct_mean,direct_raw_second=direct_raw,gaussian_raw_second=gaussian_raw,
        synthetic_only=True))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        exact_cumulant_identities=identities,negative_tail_bounds=tail_bounds,physical_counterexample=counter,
        number_conservation_plane_waves=plane_waves,general_nonGaussian_example=non_gaussian,
        scope='Algebra/numerics of the stated construction; not a proof that a Gaussian linear tracer weight is a physical nonlinear density.'),
        __file__,[ROOT/'results/pair-streaming/status.json',PARENT/'results/derived-moments/status.json'])
    failed=[row for row in checks if not row['passed']]
    print(json.dumps(dict(count=len(checks),failed=failed,counterexample=counter),indent=2))
    assert not failed


if __name__=='__main__':
    main()
