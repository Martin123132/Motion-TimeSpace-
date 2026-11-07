from turnover_common import *
from scipy.optimize import brentq


def main():
    modest()
    folder=ROOT/'results/turnover-scales'
    folder.mkdir(parents=True,exist_ok=False)
    checks,inputs,models=[],[ROOT/'TURNOVER-LAW.md'],{}
    for model in ['heavy','cold']:
        path=ROOT/'invariant-half-time2-prediction/runs'/f'{model}-main1280/prediction.npz'
        inputs.append(path)
        with np.load(path) as archive:
            frequency=archive['frequency'].copy()
            times=archive['coefficient_knots'].copy()
            bank=archive['coefficient_bank'].copy()
            offsets=archive['offsets'].copy()
        background=thermal_wave.thermal.ThermalBackground(model)
        inputs.extend([background.parent.source,background.native_constants])
        count=len(offsets)
        margin=int(max(-offsets[0],offsets[-1]))
        br=bank[:,count+3+margin:count+3+margin+len(frequency)]
        theta=np.array([background.at(float(coordinate))['thermal_parameter'] for coordinate in times])
        eigenvalue=bank[:,count]
        kappa=bank[:,count+1]
        clock_rate=bank[:,count+2]
        roots,dc_fractions,balance_errors=[],[],[]
        log_frequency=np.log(frequency)
        for epoch in range(len(times)):
            rate=kappa[epoch]/frequency**2+br[epoch]
            logarithm=interpolate.PchipInterpolator(log_frequency,np.log(rate))
            log_root=brentq(lambda position:float(logarithm(position))-math.log(theta[epoch]),
                           log_frequency[0],log_frequency[-1],xtol=1e-13)
            root=math.exp(log_root)
            roots.append(root)
            dc_fractions.append(kappa[epoch]/root**2/theta[epoch])
            balance_errors.append(abs(math.exp(float(logarithm(log_root)))/theta[epoch]-1))
        roots,dc_fractions=np.array(roots),np.array(dc_fractions)
        dc_scale=np.sqrt(kappa/theta)
        grid=dc_scale[:,None]*np.array([.1,.2,.5,1.,2.,5.,10.])[None,:]
        homogeneous=np.exp(-dc_scale[:,None]/grid)
        derivative=dc_scale[:,None]*homogeneous/grid**2
        second=(-2*dc_scale[:,None]/grid**3+dc_scale[:,None]**2/grid**4)*homogeneous
        left=theta[:,None]*(grid**2*second+2*grid*derivative)
        right=kappa[:,None]*homogeneous/grid**2
        identity=float(np.max(abs(left-right)/np.maximum(abs(left)+abs(right),1e-300)))
        checks.extend([
            dict(name='Positive sourced rates:'+model,passed=bool(np.all(br>0) and np.all(kappa>0) and np.all(clock_rate>0))),
            dict(name='Frozen DC exponential solves derived diffusion ODE:'+model,value=identity,limit=1e-12,passed=identity<=1e-12),
            dict(name='Implicit balance root residual:'+model,value=max(balance_errors),limit=1e-10,passed=max(balance_errors)<=1e-10),
            dict(name='BR raises balance scale above DC-only:'+model,passed=bool(np.all(roots>=dc_scale))),
            dict(name='Emission fractions physical:'+model,passed=bool(np.all((dc_fractions>0)&(dc_fractions<1))))])
        models[model]=dict(
            initial_final_balance_scale=roots[[0,-1]].tolist(),
            minimum_maximum_balance_scale=[float(roots.min()),float(roots.max())],
            initial_final_dc_scale=dc_scale[[0,-1]].tolist(),
            initial_final_dc_fraction=dc_fractions[[0,-1]].tolist(),
            initial_final_relaxation_in_expansion_units=(1/(clock_rate*theta))[[0,-1]].tolist(),
            diffusion_lambda1_fractional_difference=float(np.max(abs(eigenvalue/(2*theta)-1))),
            root_is_explanatory_not_prediction_input=True)
        np.savez_compressed(folder/(model+'.npz'),coordinate=times,theta=theta,
            balance_scale=roots,dc_scale=dc_scale,dc_fraction=dc_fractions,
            clock_rate=clock_rate,lambda1=eigenvalue,
            relaxation_expansion_time=1/(clock_rate*theta))
    finish(folder,dict(checks=checks,models=models,fitted_cutoff=False,
        same_rates_for_baseline_and_correction=True,new_history=False,
        source_urls=['https://arxiv.org/html/1109.6552v1','https://doi.org/10.1111/j.1365-2966.2011.19786.x']),
        __file__,inputs)
    print(json.dumps(dict(models=models,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
