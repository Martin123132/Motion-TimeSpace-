from __future__ import annotations

from velocity_common import *


def main():
    modest()
    folder=ROOT/'results/velocity-fits'
    folder.mkdir(parents=True,exist_ok=False)
    parent=json.loads((PARENT/'results/diagnostic-fits/status.json').read_text())
    rows=[]
    for label in ['heavy','cold','lcdm']:
        angular=AngularResponse(label)
        for family in FAMILIES:
            for cap in ['NGC','SGC']:
                packet=np.load(ROOT/'results/response-tables'/(label+'-'+family+'-'+cap+'.npz'))
                survey=np.load(PARENT/'results/prepared'/(cap+'.npz'))
                for kmax,ells in [(.1,(0,2)),(.08,(0,2)),(.12,(0,2)),(.1,(0,2,4))]:
                    indices=previous.select(kmax,ells)
                    covariance=survey['covariance'][np.ix_(indices,indices)]
                    fit=fit_response(packet['grid'],packet['basis'][:,:,indices],survey['data'][indices],covariance)
                    poles=angular.poles(fit['variance'],family)
                    direct=convolved(poles,survey['operator'])
                    prediction=model(direct,fit['bias'],fit['noise'])
                    delta=prediction[indices]-np.array(fit['prediction'])
                    error=previous.covariance_norm(delta,covariance)
                    direct_residual=prediction[indices]-survey['data'][indices]
                    direct_score=float(direct_residual@linalg.solve(covariance,direct_residual,assume_a='pos'))
                    baseline=next(row for row in parent['rows'] if row['branch']==label and row['cap']==cap and row['kmax']==kmax and row['ells']==list(ells))
                    total_poles=fit['bias']**2*poles[0]+fit['bias']*poles[1]+poles[2]
                    band=(KIN>.02)&(KIN<kmax)
                    higher=float(np.max(abs(total_poles[3:,band])/abs(total_poles[0,band])))
                    tail=poles.copy();tail[:,:,KIN<=.2]=0.
                    tail_basis=convolved(tail,survey['operator']);tail_basis[3]=0.
                    tail_error=previous.covariance_norm(model(tail_basis,fit['bias'],0)[indices],covariance)
                    conversion=angular.geometry['model_H_km_s_Mpc']/(1+previous.REDSHIFT)/HUNIT
                    rows.append(dict(branch=label,family=family,cap=cap,kmax=kmax,ells=list(ells),fit=fit,
                        direct_interpolation_distance=error,direct_chi2_raw=direct_score,
                        improvement_over_no_smearing=baseline['fit']['chi2_hartlap']-fit['chi2_hartlap'],
                        residual_sigma_velocity_km_s=conversion*fit['sigma_displacement'],
                        omitted_ell6_8_over_monopole=higher,tail_100percent_covariance_distance=tail_error,
                        coefficient_parent_derived=False,formal_model_preference=False))
                    np.savez_compressed(folder/f'{label}-{family}-{cap}-{kmax:g}-{len(ells)}.npz',
                        prediction=prediction,indices=indices,poles=total_poles)
                    print(label,family,cap,kmax,ells,'score',fit['chi2_hartlap'],'s2',fit['variance'],flush=True)
    summaries=[]
    for family in FAMILIES:
        for kmax,ells in [(.1,[0,2]),(.08,[0,2]),(.12,[0,2]),(.1,[0,2,4])]:
            for label in ['heavy','cold','lcdm']:
                picked=[row for row in rows if row['branch']==label and row['family']==family and row['kmax']==kmax and row['ells']==ells]
                summaries.append(dict(branch=label,family=family,kmax=kmax,ells=ells,
                    chi2_hartlap=sum(row['fit']['chi2_hartlap'] for row in picked),
                    chi2_raw=sum(row['fit']['chi2_raw'] for row in picked),data_count=sum(row['fit']['bins'] for row in picked),
                    tracer_parameters=6,upper_or_other_edge=any(row['fit']['upper_variance_boundary'] or row['fit']['other_boundary'] for row in picked)))
    finish(folder,dict(rows=rows,summaries=summaries,coefficient_parent_derived=False,formal_model_preference=False,
        overlap_scores_added=False,scope='Independent residual-displacement stress test; not full nonlinear galaxy dynamics.'),
        __file__,[ROOT/'results/response-tables/status.json',PARENT/'results/diagnostic-fits/status.json',
            *sorted((ROOT/'results/response-tables').glob('*.npz')),
            *[PARENT/'results/prepared'/(cap+'.npz') for cap in ['NGC','SGC']],*folder.glob('*.npz')])


if __name__=='__main__':
    main()
