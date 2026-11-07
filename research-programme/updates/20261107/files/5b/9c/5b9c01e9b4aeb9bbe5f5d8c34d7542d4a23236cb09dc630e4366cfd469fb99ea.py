from __future__ import annotations

from precision_common import *
import refit_primary as primary


def main():
    modest()
    folder=ROOT/'results/production-primary-refit'
    folder.mkdir(parents=True,exist_ok=False)
    old=json.loads((ROOT/'results/primary-refit/status.json').read_text())
    rows=[]
    paths=[ROOT/'refit_primary.py',ROOT/'EMPIRICAL-CHECK.md',ROOT/'results/primary-refit/status.json',ROOT/'results/production-spectrum/status.json']
    for label in ['heavy','cold','lcdm']:
        input_path=(SPECTRUM/'results/spectrum' if label=='lcdm' else ROOT/'results/production-spectrum')/(label+'.npz')
        packet=np.load(input_path)
        epoch=int(np.argmin(abs(packet['scales']-1/1.38)))
        transfer=(interpolate.CubicSpline(np.log(packet['modes']),np.log(packet['delta_cb'][:,epoch])),
            interpolate.CubicSpline(np.log(packet['modes']),np.log(packet['velocity_cb'][:,epoch])))
        original_function=primary.velocity.previous.transfer
        try:
            primary.velocity.previous.transfer=lambda selected_label,method='cubic',template=False: transfer
            angular=primary.angular_for(label)
        finally:
            primary.velocity.previous.transfer=original_function
        paths.append(input_path)
        for family in ['gaussian','laplace']:
            for cap in ['NGC','SGC']:
                survey_path=primary.SURVEY/'results/prepared'/(cap+'.npz')
                survey=np.load(survey_path)
                indices=primary.velocity.previous.select(.1,(0,2))
                covariance=survey['covariance'][np.ix_(indices,indices)]
                basis=np.array([primary.velocity.convolved(angular.poles(variance,family),survey['operator']) for variance in primary.velocity.VARIANCE_GRID])
                fit=primary.velocity.fit_response(primary.velocity.VARIANCE_GRID,basis[:,:,indices],survey['data'][indices],covariance)
                reference=next(row for row in old['rows'] if row['branch']==label and row['family']==family and row['cap']==cap)
                direct=primary.velocity.model(primary.velocity.convolved(angular.poles(fit['variance'],family),survey['operator']),fit['bias'],fit['noise'])
                distance=primary.velocity.previous.covariance_norm(direct[indices]-np.array(fit['prediction']),covariance)
                rows.append(dict(branch=label,family=family,cap=cap,fit=fit,
                    change_from_intermediate=fit['chi2_hartlap']-reference['fit']['chi2_hartlap'],
                    change_from_stage58=fit['chi2_hartlap']-reference['prior_chi2_hartlap'],
                    direct_grid_interpolation_distance=distance))
                output=folder/(label+'-'+family+'-'+cap+'.npz')
                np.savez_compressed(output,indices=indices,prediction=direct)
                paths.extend([survey_path,output])
    summaries=[]
    checks=[]
    for row in rows:
        fit=row['fit']
        checks.append(dict(name=' '.join([row['branch'],row['family'],row['cap']])+' fit and interpolation',
            passed=bool(fit['converged'] and all(item['success'] for item in fit['starts']) and not(fit['lower_variance_boundary'] or fit['upper_variance_boundary'] or fit['other_boundary']) and row['direct_grid_interpolation_distance']<1e-3)))
    for label in ['heavy','cold','lcdm']:
        for family in ['gaussian','laplace']:
            picked=[row for row in rows if row['branch']==label and row['family']==family]
            summaries.append(dict(branch=label,family=family,chi2_hartlap=sum(row['fit']['chi2_hartlap'] for row in picked),
                change_from_stage58=sum(row['change_from_stage58'] for row in picked),data_count=32,tracer_parameters=6))
    finish(folder,dict(rows=rows,summaries=summaries,checks=checks,all_checks_passed=all(row['passed'] for row in checks),
        field_parameters_refitted=False,production_spectra_used=True,formal_model_preference=False),__file__,paths)
    print(json.dumps(summaries),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
