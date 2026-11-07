from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import numpy as np
from scipy import integrate,optimize

from cosmology_common import ROOT,inherited,modest_process,read_json,digest,save,candidate_profile,charged_shape,evaluate


def main():
    modest_process()
    preflight=read_json(ROOT/'results/preflight/status.json')
    comparison=read_json(ROOT/'results/comparison/status.json')
    reduction=read_json(ROOT/'results/adiabatic-check/status.json')
    checks=[]

    def check(name,condition,value=None):
        checks.append(dict(name=name,passed=bool(condition),value=value))
        assert condition,(name,value)

    check('preflight all passes',all(row['passed'] for row in preflight['checks']))
    data=inherited.load_likelihood_data()
    dense=replace(data,z_grid=np.linspace(0,data.z_grid[-1],8*(len(data.z_grid)-1)+1))
    by_model={row['model']:row for row in comparison['fits']}
    for row in comparison['fits']:
        name=row['model']
        check(name+' complete finite score',np.isfinite(row['chi2_total']) and row['n']==1637)
        check(name+' convergence explicitly represented',row['optimizer_converged'] or row['status']=='bounded_search_not_converged')
        check(name+' AIC arithmetic',abs(row['AIC']-row['chi2_total']-2*row['k'])<1e-9)
        check(name+' BIC arithmetic',abs(row['BIC']-row['chi2_total']-row['k']*np.log(row['n']))<1e-9)
        check(name+' edge flag consistent',row['prior_edge_flag']==any(edge['fractional_distance']<.01 for edge in row['edges']))
    for row in comparison['numerical_checks']:
        check(row['model']+' independent likelihood agreement',abs(row['inverse_vs_cholesky'])<1e-7)
        check(row['model']+' resolution shift bounded for interpretation',abs(row['dense_minus_matched'])<.2,row['dense_minus_matched'])
    dense_lcdm=evaluate('LCDM',by_model['LCDM']['parameters'],dense)['chi2_total']
    profile_checks=[]
    for row in comparison['fraction_profiles']:
        prediction=evaluate('Condensate_Lambda_free',row['parameters'],dense)
        delta=prediction['chi2_total']-dense_lcdm
        discrepancy=delta-row['delta_chi2_LCDM']
        check(row['model']+' relative score stable on denser integration',abs(discrepancy)<.1,discrepancy)
        profile_checks.append(dict(fraction=row['parameters']['f_condensate'],delta_chi2_matched=row['delta_chi2_LCDM'],delta_chi2_dense=delta,shift=discrepancy))
    zero=by_model['Condensate_Lambda_free']
    check('best charged fraction on zero boundary',zero['parameters']['f_condensate']<1e-6)
    check('zero-boundary candidate not falsely identifiable',zero['identifiable'] is False)
    check('zero-boundary score is LCDM',abs(zero['chi2_total']-by_model['LCDM']['chi2_total'])<1e-6)
    check('parent data comparison preserved',by_model['ParentScalar_Lambda_zero']['chi2_total']<by_model['LCDM']['chi2_total'])
    for log_zero in [-np.log10(3)+1e-4,0.,1.,3.]:
        state0=10**log_zero
        span=np.log1p(data.z_grid[-1])
        solution=integrate.solve_ivp(lambda location,state:24*state*(1+state)/(5+9*state),(0,span),[state0],rtol=1e-11,atol=1e-12,dense_output=True)
        exact=charged_shape(data.z_grid,log_zero)
        error=float(np.max(abs(solution.sol(np.log1p(data.z_grid))[0]/exact['y']-1)))
        check('charge root versus independent ODE '+str(log_zero),solution.success and error<1e-8,error)
        for fraction in [0.,.1,1.]:
            shape=candidate_profile('Condensate_Lambda_zero',dict(f_condensate=fraction,log10_y0=log_zero),data.z_grid)
            check('no-Lambda positive deceleration '+str((log_zero,fraction)),np.min(shape['q'])>0)
    grid=[]
    for fraction in np.linspace(0,1,21):
        for log_zero in np.linspace(-np.log10(3)+1e-4,3,17):
            parameters=dict(f_condensate=float(fraction),log10_y0=float(log_zero))
            score=evaluate('Condensate_Lambda_zero',parameters,data)['chi2_total']
            grid.append(dict(parameters=parameters,chi2=score))
    grid_best=min(grid,key=lambda row:row['chi2'])
    check('broad no-Lambda control does not reveal hidden good fit',grid_best['chi2']>3000,grid_best)
    check('full action approximation errors decrease',all(reduction['rows'][index+1]['max_fractional_expansion_difference']<reduction['rows'][index]['max_fractional_expansion_difference'] for index in range(2)))
    check('full action closest test reproduces approximate likelihood',abs(reduction['rows'][-1]['delta_chi2_from_adiabatic'])<.001)
    check('full action tighter integration agrees',abs(reduction['tighter_solver_delta_chi2'])<1e-5,reduction['tighter_solver_delta_chi2'])
    inputs=[]
    script_hashes={digest(path) for path in ROOT.glob('*.py')}
    for path in ROOT.glob('results/*/status.json'):
        report=read_json(path)
        assert report['state']=='complete' and report['script_sha256'] in script_hashes,path
        for source,expected in report['input_hashes'].items():
            assert Path(source).is_file() and digest(source)==expected,(path,source)
        inputs.append(path)
    check('input hashes unchanged',True)
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(),str(path),'exec')
    check('no bytecode caches',not list(ROOT.rglob('__pycache__')))
    save('validation',Path(__file__),dict(checks=checks,validation_checks=len(checks),dense_fraction_profiles=profile_checks,
        no_Lambda_grid_best=grid_best,no_Lambda_grid_evaluations=len(grid),
        review_status='Ready within reviewed scope: conditional late-time homogeneous/adiabatic SN+BAO screening; no posterior or universal MTS exclusion.',
        all_models_converged=all(row['optimizer_converged'] for row in comparison['fits']),
        dataset_is_actual_observations=True,fit_is_not_derivation=True,
        early_universe_sound_horizon_predicted=False,formation_history_proved=False,closed_candidate_bath_matching_proved=False,
        parent_framework_replaced=False),inputs)
    print(dict(checks=len(checks),grid_best=grid_best,profile_resolution_checks=profile_checks,full_action_tolerance_shift=reduction['tighter_solver_delta_chi2']),flush=True)


if __name__=='__main__':
    main()
