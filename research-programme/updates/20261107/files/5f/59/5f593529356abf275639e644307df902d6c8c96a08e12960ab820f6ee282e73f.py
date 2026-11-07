from overlap_common import *
import argparse


def evaluate(case,basis,prediction,profiles):
    saved=read_npz(case/'overlap.npz')
    assert np.allclose(saved['coordinate'],prediction['coordinate'],rtol=0,atol=2e-15)
    frequency=basis.nodes
    selected=(frequency>.01)&(frequency<.04)
    nodes=frequency[selected]
    inner=np.stack([nodes[:,None]*interpolate.CubicSpline(np.log(prediction['frequency']),values,axis=0,extrapolate=False)(np.log(nodes))
                    for values in prediction['slope']])
    overlap=np.stack([nodes[:,None]*interpolate.CubicSpline(np.log(saved['frequency']),values,axis=0,extrapolate=False)(np.log(nodes))
                      for values in saved['slope']])
    outer=np.einsum('fi,nik->nfk',basis.values[selected],profiles)
    old=np.zeros((len(profiles),len(frequency),3))
    residual=np.zeros_like(old)
    bridge=np.zeros_like(old)
    old[:,selected]=inner-outer
    residual[:,selected]=inner-overlap
    bridge[:,selected]=overlap-outer
    old[0]=0.
    residual[0]=0.
    bridge[0]=0.
    windows=np.array([matching_weight(frequency,upper) for upper in [.04,.02]])
    delta_window=windows[0]-windows[1]
    assert not np.any(delta_window[~selected])
    checks=[]
    outputs=dict(frequency=frequency,coordinate=saved['coordinate'],inner=inner,outer=outer,overlap=overlap,band_nodes=nodes)
    for name,value in [('old',old),('residual',residual),('bridge',bridge)]:
        raw=delta_window[None,:,None]*value
        unresolved=projected(raw,basis)
        represented=raw-unresolved
        raw_norm=norm(raw,basis.measure)
        norm_unresolved=norm(unresolved,basis.measure)
        full_norm=norm(value,basis.measure)
        projected_orthogonality=np.einsum('fi,f,nfk->nik',basis.values,basis.measure,unresolved)
        scale=np.maximum(raw_norm.max(axis=0),1e-300)
        checks.extend([
            check('Orthogonal projection:'+name,np.max(np.linalg.norm(projected_orthogonality,axis=1)/scale),1e-9),
            check('Projection contraction:'+name,np.max(np.maximum(norm_unresolved-raw_norm,0)/scale),1e-9),
            check('Window contraction:'+name,np.max(np.maximum(raw_norm-full_norm,0)/scale),1e-9),
            check('Orthogonal norm identity:'+name,
                  np.max(abs(raw_norm**2-norm_unresolved**2-norm(represented,basis.measure)**2)/scale**2),1e-9)])
        per_window=np.stack([projected(window[None,:,None]*value,basis) for window in windows])
        checks.append(check('Both fixed windows give same difference:'+name,
            np.max(norm(per_window[0]-per_window[1]-unresolved,basis.measure)/scale),1e-9))
        outputs.update({name+'_band':value,name+'_unresolved_delta':unresolved,name+'_band_norm':full_norm,
                        name+'_delta_norm':norm_unresolved,name+'_window_band':per_window})
    scale=np.maximum(outputs['old_band_norm'].max(axis=0),1e-300)
    checks.append(check('Complete physical mismatch split',
        np.max(norm(old-residual-bridge,basis.measure)/scale),1e-9))
    checks.append(check('Complete projected mismatch split',
        np.max(norm(outputs['old_unresolved_delta']-outputs['residual_unresolved_delta']-outputs['bridge_unresolved_delta'],basis.measure)/scale),1e-9))
    checks.append(check('Direct overlap change equals saved defect correction',
        np.max(abs(saved['slope']-saved['outer_slope']-saved['defect_correction']))/
        max(float(np.max(abs(saved['defect_correction']))),1e-300),1e-8))
    rows=[]
    for column,label in enumerate(['baseline','join1','join2']):
        old_final=outputs['old_band_norm'][-1,column]
        delta_final=outputs['old_delta_norm'][-1,column]
        rows.append(dict(branch=label,
            final_old_band_norm=float(old_final),
            final_remaining_band_ratio=float(outputs['residual_band_norm'][-1,column]/old_final),
            peak_remaining_over_old_peak=float(outputs['residual_band_norm'][:,column].max()/scale[column]),
            final_remaining_unresolved_ratio=float(outputs['residual_delta_norm'][-1,column]/delta_final),
            final_bridge_unresolved_ratio=float(outputs['bridge_delta_norm'][-1,column]/delta_final),
            final_old_unresolved_delta_norm=float(delta_final)))
    return outputs,checks,rows


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--pilot',action='store_true')
    args=parser.parse_args()
    modest()
    folder=ROOT/'results'/('pilot-comparison' if args.pilot else 'comparison')
    if folder.exists():
        assert not any(folder.iterdir()),folder
    folder.mkdir(parents=True,exist_ok=True)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=list(ladder.inputs)
    checks,rows=[],[]
    cases={}
    for model in (['heavy'] if args.pilot else ['heavy','cold']):
        prediction,profiles,unused_gas,dependencies=read_prediction(model,'fine')
        inputs.extend(dependencies)
        for case in sorted((ROOT/'results').glob(model+'-*/overlap.npz')):
            values,local_checks,local_rows=evaluate(case.parent,basis,prediction,profiles)
            for row in local_checks:
                row['name']=case.parent.name+':'+row['name']
            checks.extend(local_checks)
            rows.append(dict(case=case.parent.name,branches=local_rows))
            cases[case.parent.name]=values
            inputs.extend([case,case.parent/'status.json'])
            np.savez_compressed(folder/(case.parent.name+'.npz'),**values)
    refinement=[]
    if not args.pilot:
        for model in ['heavy','cold']:
            reference=cases[model+'-fine-lo25-n5120']
            scale=np.maximum(reference['old_band_norm'].max(axis=0),1e-300)
            for other_name,kind in [(model+'-fine-lo25-n2560','time'),
                                    (model+'-space-lo25-n5120','space'),
                                    (model+'-fine-lo50-n5120','boundary')]:
                other=cases[other_name]
                difference=reference['residual_band']-other['residual_band']
                magnitude=norm(difference,basis.measure)
                values=magnitude.max(axis=0)/scale
                unresolved=norm(reference['residual_unresolved_delta']-other['residual_unresolved_delta'],basis.measure)
                refinement.append(dict(model=model,kind=kind,peak_difference_over_old_peak=values.tolist(),
                    final_unresolved_difference_over_old=(unresolved[-1]/reference['old_delta_norm'][-1]).tolist()))
                if kind!='boundary':
                    for column,label in enumerate(['baseline','join1','join2']):
                        checks.append(check(kind+' refinement:'+model+':'+label,values[column],.01))
    finish(folder,dict(checks=checks,rows=rows,refinement=refinement,
        candidate_scope='conditional common soft band with two-sided saved outer exterior',
        no_total_feedback_reduction_claim=True,no_gas_response_replaced=True,
        old_mismatch_reconstructed_including_bridge=True,
        old_matched_physical_response_unchanged=True),__file__,inputs)
    print(json.dumps(dict(rows=rows,refinement=refinement,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
