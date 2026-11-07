from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy import optimize

from cosmology_common import ROOT, inherited, modest_process, save, read_json, archived_parameters, evaluate, independent_likelihood, candidate_profile, charged_shape


def main():
    modest_process()
    assert read_json(ROOT/'results/preflight/status.json')['likelihood_run_authorized_after_preflight']
    folder=ROOT/'runs/observational-smoke'
    folder.mkdir(parents=True,exist_ok=False)
    started=time.monotonic()
    deadline=started+3600

    def log(payload):
        line=json.dumps(dict(time_utc=datetime.now(timezone.utc).isoformat(),**payload),allow_nan=False)
        with (folder/'log.txt').open('a',encoding='utf-8') as handle:
            handle.write(line+'\n')
        print(line,flush=True)

    data=inherited.load_likelihood_data()
    archived=archived_parameters()
    fits=[]

    def fit(model, priors, starts, fixed=None, label=None):
        names=list(priors)
        bounds=list(priors.values())
        fixed={} if fixed is None else fixed
        evaluations=0
        failures=0

        def objective(vector):
            nonlocal evaluations,failures
            if time.monotonic()>deadline:
                raise TimeoutError('Bounded one-hour fitting budget reached; completed rows are in the log.')
            evaluations+=1
            parameters=dict(fixed,**dict(zip(names,map(float,vector))))
            try:
                score=float(evaluate(model,parameters,data)['chi2_total'])
                if not np.isfinite(score):
                    raise ValueError('nonfinite score')
                return score
            except (ValueError,OverflowError,FloatingPointError):
                failures+=1
                return 1e30

        attempts=[]
        for initial in starts:
            start=np.array([np.clip(initial[name],*priors[name]) for name in names])
            initial_score=objective(start)
            result=optimize.minimize(objective,start,method='Powell',bounds=bounds,
                options=dict(maxiter=45,maxfev=350,xtol=2e-6,ftol=2e-9))
            attempts.append(dict(parameters=result.x.tolist(),chi2=float(result.fun),success=bool(result.success),message=str(result.message),evaluations=int(result.nfev)))
            if initial_score<result.fun:
                attempts.append(dict(parameters=start.tolist(),chi2=initial_score,success=False,message='Retained better input candidate',evaluations=1))
        best=min(attempts,key=lambda item:item['chi2'])
        parameters=dict(fixed,**dict(zip(names,best['parameters'])))
        result=evaluate(model,parameters,data)
        n_points=len(data.sn['z'])+len(data.bao['rows'])
        count=len(names)+2
        score=result['chi2_total']
        edges=[dict(parameter=name,value=parameters[name],lower=bounds[index][0],upper=bounds[index][1],
            fractional_distance=min(parameters[name]-bounds[index][0],bounds[index][1]-parameters[name])/(bounds[index][1]-bounds[index][0])) for index,name in enumerate(names)]
        converged=any(attempt['success'] and abs(attempt['chi2']-score)<2e-4 for attempt in attempts)
        row=dict(model=label or model,evaluator=model,parameters=parameters,priors=priors,fixed=fixed,
            chi2_total=score,chi2_SN=result['chi2_SN'],chi2_BAO=result['chi2_BAO'],
            k=count,n=n_points,AIC=score+2*count,BIC=score+count*math.log(n_points),
            optimizer_converged=converged,status='bounded_fit_converged' if converged else 'bounded_search_not_converged',
            edges=edges,prior_edge_flag=any(edge['fractional_distance']<.01 for edge in edges),
            evaluations=evaluations,invalid_evaluations=failures,attempts=attempts,
            sn_offset=result['sn_offset'],bao_alpha=result['bao_alpha'])
        if 'candidate' in result:
            candidate=result['candidate']
            row.update(Omega_C=candidate['Omega_C'],Omega_pressureless=candidate['Omega_pressureless'],Omega_Lambda=candidate['Omega_Lambda'],q0=float(candidate['q'][0]),w0=float(candidate['w'][0]),
                interpretation='Conditional adiabatic charged-sector prediction; microphysical preparation, bath matching and CMB/growth not established.',
                identifiable=parameters['f_condensate']>1e-5,
                information_criteria_caveat='Nominal parameter count; mixture boundary and unidentified y0 at zero fraction make regular likelihood-ratio/AIC asymptotics unreliable.')
        log(dict(event='fit_complete',**{key:value for key,value in row.items() if key!='attempts'}))
        return row,result

    for model in ['LCDM','wCDM','CPL','ParentScalar_Lambda_free','ParentScalar_Lambda_zero']:
        priors=inherited.MODEL_PRIORS[model]
        seed=archived[model]
        perturbed=dict(seed,Omega_m=np.clip(seed['Omega_m']+.025,*priors['Omega_m']))
        fixed={'f_scalar':1.} if model=='ParentScalar_Lambda_zero' else {}
        row,result=fit(model,priors,[seed,perturbed],fixed)
        fits.append(row)
    priors=dict(Omega_m=(.05,.6),f_condensate=(0.,1.),log10_y0=(0.,3.))
    starts=[dict(Omega_m=.3,f_condensate=fraction,log10_y0=state) for fraction,state in [(0.,0.),(.15,0.),(.6,.5),(1.,2.)]]
    row,result=fit('Condensate_Lambda_free',priors,starts)
    fits.append(row)
    no_lambda=dict(f_condensate=(0.,1.),log10_y0=(0.,3.))
    row,result=fit('Condensate_Lambda_zero',no_lambda,[dict(f_condensate=fraction,log10_y0=state) for fraction,state in [(0.,0.),(.5,0.),(1.,2.)]])
    fits.append(row)
    metastable=dict(f_condensate=(0.,1.),log10_y0=(-math.log10(3)+1e-4,3.))
    row,result=fit('Condensate_Lambda_zero',metastable,[dict(f_condensate=fraction,log10_y0=-math.log10(3)+1e-4) for fraction in [.1,.7,1.]],label='Condensate_metastable_Lambda_zero')
    fits.append(row)
    profiles=[]
    for fraction in [0.,.01,.03,.1,.3,.6,1.]:
        row,result=fit('Condensate_Lambda_free',dict(Omega_m=(.05,.6),log10_y0=(0.,3.)),
            [dict(Omega_m=.3,log10_y0=0.),dict(Omega_m=.2,log10_y0=1.)],
            dict(f_condensate=fraction),label='fraction='+str(fraction))
        profiles.append(row)
    dense=replace(data,z_grid=np.linspace(0,data.z_grid[-1],8*(len(data.z_grid)-1)+1))
    checks=[]
    residuals=[]
    backgrounds=[]
    for row in fits:
        prediction=evaluate(row['evaluator'],row['parameters'],data)
        independent=independent_likelihood(prediction['E'],data)
        refined=evaluate(row['evaluator'],row['parameters'],dense)
        checks.append(dict(model=row['model'],inverse_vs_cholesky=independent['chi2_total']-prediction['chi2_total'],
            dense_grid_chi2=refined['chi2_total'],dense_minus_matched=refined['chi2_total']-prediction['chi2_total']))
        residuals.append(dict(model=row['model'],SN_z=data.sn['z'].tolist(),SN_residual=prediction['sn_residual'].tolist(),
            SN_diagonal_sigma=np.sqrt(np.diag(data.sn['covariance'])).tolist(),
            BAO_rows=[dict(**datum,residual=float(residual),predicted=float(predicted),sigma=float(sigma)) for datum,residual,predicted,sigma in zip(data.bao['rows'],prediction['bao_residual'],prediction['bao_predicted'],np.sqrt(np.diag(data.bao['covariance'])))],
            note='Diagonal error bars are descriptive only; full correlated covariance defines the scores.'))
        sampled=np.linspace(0,data.z_grid[-1],81)
        backgrounds.append(dict(model=row['model'],redshift=sampled.tolist(),E=np.interp(sampled,data.z_grid,prediction['E']).tolist()))
    reference=next(row for row in fits if row['model']=='LCDM')
    for row in fits:
        row.update(delta_chi2_LCDM=row['chi2_total']-reference['chi2_total'],delta_AIC_LCDM=row['AIC']-reference['AIC'],delta_BIC_LCDM=row['BIC']-reference['BIC'])
    for row in profiles:
        row['delta_chi2_LCDM']=row['chi2_total']-reference['chi2_total']
    write_inputs=[ROOT/'results/preflight/status.json']
    report=save('comparison',Path(__file__),dict(fits=fits,fraction_profiles=profiles,numerical_checks=checks,
        residuals=residuals,backgrounds=backgrounds,elapsed_seconds=time.monotonic()-started,
        coexistence_limit='When finite bodies form a dilute conserved population with negligible interaction/velocity pressure, rho_C scales as a^-3. Replacing a fraction of dust is exactly degenerate with LCDM in this background-only likelihood. Formation and abundance are additional unsolved questions.',
        data_are_observations=True,new_data_acquired=False,claim='Scoped observed SN+BAO comparison, conditional on stated homogeneous adiabatic reduction; not posterior inference or empirical validation of the entire MTS framework.'),write_inputs)
    (folder/'COMPLETE').write_text(report['time_utc']+'\n',encoding='utf-8')
    log(dict(event='complete',elapsed_seconds=report['elapsed_seconds']))


if __name__=='__main__':
    main()
