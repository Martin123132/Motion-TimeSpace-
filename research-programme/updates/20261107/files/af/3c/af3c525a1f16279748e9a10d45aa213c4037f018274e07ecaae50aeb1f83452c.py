from __future__ import annotations

from precision_common import *

VELOCITY=BRANCH/'shared-velocity-response-20261007'
SURVEY=BRANCH/'survey-window-forward-model-20261007'
sys.path.insert(0,str(VELOCITY))
import velocity_common as velocity


def angular_for(label):
    previous_root=velocity.previous.PARENT
    try:
        velocity.previous.PARENT=SPECTRUM if label=='lcdm' else ROOT
        return velocity.AngularResponse(label)
    finally:
        velocity.previous.PARENT=previous_root


def main():
    modest()
    folder=ROOT/'results/primary-refit'
    folder.mkdir(parents=True,exist_ok=False)
    prior_path=VELOCITY/'results/velocity-fits/status.json'
    prior=json.loads(prior_path.read_text())
    rows=[]
    paths=[prior_path,ROOT/'EMPIRICAL-CHECK.md',VELOCITY/'velocity_common.py',SURVEY/'window_common.py',ROOT/'results/spectrum/status.json']
    for label in ['heavy','cold','lcdm']:
        angular=angular_for(label)
        for family in ['gaussian','laplace']:
            for cap in ['NGC','SGC']:
                survey_path=SURVEY/'results/prepared'/(cap+'.npz')
                survey=np.load(survey_path)
                indices=velocity.previous.select(.1,(0,2))
                covariance=survey['covariance'][np.ix_(indices,indices)]
                basis=np.array([velocity.convolved(angular.poles(variance,family),survey['operator']) for variance in velocity.VARIANCE_GRID])
                fit=velocity.fit_response(velocity.VARIANCE_GRID,basis[:,:,indices],survey['data'][indices],covariance)
                direct=velocity.model(velocity.convolved(angular.poles(fit['variance'],family),survey['operator']),fit['bias'],fit['noise'])
                interpolation_distance=velocity.previous.covariance_norm(direct[indices]-np.array(fit['prediction']),covariance)
                old=next(row for row in prior['rows'] if row['branch']==label and row['family']==family and row['cap']==cap and row['kmax']==.1 and row['ells']==[0,2])
                old_parameters=old['fit']
                fixed=velocity.model(velocity.convolved(angular.poles(old_parameters['variance'],family),survey['operator']),old_parameters['bias'],old_parameters['noise'])
                distance=velocity.previous.covariance_norm(fixed[indices]-np.array(old_parameters['prediction']),covariance)
                row=dict(branch=label,family=family,cap=cap,fit=fit,prior_chi2_hartlap=old_parameters['chi2_hartlap'],
                    chi2_change=fit['chi2_hartlap']-old_parameters['chi2_hartlap'],fixed_nuisance_covariance_distance=distance,
                    direct_grid_interpolation_distance=interpolation_distance)
                rows.append(row)
                output=folder/(label+'-'+family+'-'+cap+'.npz')
                np.savez_compressed(output,indices=indices,prediction=direct,fixed_nuisance_prediction=fixed,grid=velocity.VARIANCE_GRID,basis=basis)
                paths.extend([survey_path,output])
                print(json.dumps({key:row[key] for key in ['branch','family','cap','chi2_change','fixed_nuisance_covariance_distance']}),flush=True)
        source_root=SPECTRUM if label=='lcdm' else ROOT
        paths.extend([source_root/'results/spectrum'/(label+'.npz'),source_root/'runs'/label/'background.npz'])
    summaries=[]
    for label in ['heavy','cold','lcdm']:
        for family in ['gaussian','laplace']:
            selected=[row for row in rows if row['branch']==label and row['family']==family]
            summaries.append(dict(branch=label,family=family,chi2_hartlap=sum(row['fit']['chi2_hartlap'] for row in selected),
                change_from_stage58=sum(row['chi2_change'] for row in selected),data_count=sum(row['fit']['bins'] for row in selected),
                tracer_parameters=6,all_converged=all(row['fit']['converged'] for row in selected),
                any_edge=any(row['fit']['upper_variance_boundary'] or row['fit']['other_boundary'] or row['fit']['lower_variance_boundary'] for row in selected)))
    finish(folder,dict(rows=rows,summaries=summaries,field_parameters_refitted=False,formal_model_preference=False,
        same_primary_data_and_nuisances=True,unchanged_residual_closure_assumptions=True),__file__,sorted(set(paths)))
    print(json.dumps(summaries),flush=True)


if __name__=='__main__':
    main()
