from __future__ import annotations

from window_common import *


def main():
    modest()
    folder=ROOT/'results/diagnostic-fits'
    folder.mkdir(parents=True,exist_ok=False)
    rows=[]
    for kmax,ells in [(.1,(0,2)),(.08,(0,2)),(.12,(0,2)),(.1,(0,2,4))]:
        indices=select(kmax,ells)
        for label in ['heavy','cold','lcdm']:
            for cap in ['NGC','SGC']:
                survey=np.load(ROOT/'results/prepared'/(cap+'.npz'))
                response=np.load(ROOT/'results/response'/(label+'-'+cap+'.npz'))
                covariance=survey['covariance'][np.ix_(indices,indices)]
                basis=response['basis'][:,indices]
                fit=fit_nuisance(basis,survey['data'][indices],covariance)
                bias,noise=fit['bias'],fit['noise']
                variants={}
                central=physical_vector(basis,bias,noise)
                for name in ['pchip_basis','angular32_basis','identity_basis','no_window_basis']:
                    candidate=physical_vector(response[name][:,indices],bias,noise)
                    variants[name]=covariance_norm(candidate-central,covariance)
                tail=physical_vector(response['tail_basis'][:,indices],bias)
                tail_norm=covariance_norm(tail,covariance)
                poles=response['poles']
                total_poles=bias**2*poles[0]+bias*poles[1]+poles[2]
                diagnostic_band=(KIN>.02)&(KIN<kmax)
                higher=float(np.max(abs(total_poles[3:,diagnostic_band])/abs(total_poles[0,diagnostic_band])))
                full_prediction=physical_vector(response['basis'],bias,noise)
                np.savez_compressed(folder/f'{label}-{cap}-{kmax:g}-{len(ells)}.npz',
                    indices=indices,prediction=full_prediction,data=survey['data'],covariance=survey['covariance'])
                rows.append(dict(branch=label,cap=cap,kmin=.02,kmax=kmax,ells=list(ells),fit=fit,
                    numerical_and_ablated_distance=variants,tail_100percent_covariance_distance=tail_norm,
                    omitted_ell6_8_over_monopole_max=higher,formal_model_selection=False))
    summaries=[]
    for kmax,ells in [(.1,[0,2]),(.08,[0,2]),(.12,[0,2]),(.1,[0,2,4])]:
        for label in ['heavy','cold','lcdm']:
            picked=[row for row in rows if row['branch']==label and row['kmax']==kmax and row['ells']==ells]
            assert len(picked)==2
            summaries.append(dict(branch=label,kmax=kmax,ells=ells,data_count=sum(row['fit']['bins'] for row in picked),
                tracer_parameters=4,chi2_raw=sum(row['fit']['chi2_raw'] for row in picked),
                chi2_hartlap=sum(row['fit']['chi2_hartlap'] for row in picked),
                boundary_hit=any(row['fit']['boundary_hit'] for row in picked)))
    finish(folder,dict(rows=rows,summaries=summaries,parameter_policy='Same bias and white-noise residual per cap; all field/cosmological parameters held fixed.',
        finite_covariance_policy='Hartlap factor after selecting each cap covariance; raw score also retained.',
        covariance_not_added_to_stage56=True,nonlinear_model_validated=False,formal_model_selection=False),
        __file__,[ROOT/'results/response/status.json',ROOT/'results/prepared/status.json',
            *sorted((ROOT/'results/response').glob('*.npz')),*sorted((ROOT/'results/prepared').glob('*.npz')),*folder.glob('*.npz')])
    print(json.dumps(dict(summaries=summaries,primary=[row for row in rows if row['kmax']==.1 and row['ells']==[0,2]]),indent=2))


if __name__=='__main__':
    main()
