from finer_common import *


def main():
    modest()
    folder=ROOT/'results/grid-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=list(ladder.inputs)
    checks,rows=[],[]
    for upper,event_order in [(.04,8),(.02,6)]:
        for model in ['heavy','cold']:
            fine_path=PARENT/'results'/f'response-fine-p4-n5120-o{event_order}-q32-m{int(upper*1000)}-r2048'/(model+'.npz')
            coarse_path=PARENT/'results'/f'response-space-p4-n5120-o{event_order}-q32-m{int(upper*1000)}-r2048'/(model+'.npz')
            finer_path=ROOT/'results'/f'feedback-m{int(upper*1000)}-n5120'/(model+'-response.npz')
            fields={}
            for name,path in [('coarse',coarse_path),('fine',fine_path),('finer',finer_path)]:
                local_packet(path.parent)
                fields[name]=read_npz(path)
                inputs.extend([path,path.parent/'status.json'])
            coarse,fine,finer=fields['coarse'],fields['fine'],fields['finer']
            sampled=finer['saved_step_indices'][::16]
            assert len(sampled)==129 and np.allclose(finer['coordinate'][sampled],fine['coordinate'],atol=1e-14,rtol=0)
            old_delta=norm(fine['physical_change']-coarse['physical_change'],basis.measure)
            new_delta=norm(finer['physical_change']-fine['physical_change'],basis.measure)
            scale=norm(finer['physical_change'],basis.measure)
            relative=new_delta/np.maximum(scale,1e-300)
            contraction=new_delta/np.maximum(old_delta,1e-300)
            gas_old=abs(fine['gas'][:,:3]-coarse['gas'][:,:3]).max(axis=0)
            gas_new=abs(finer['gas'][sampled,:3]-fine['gas'][:,:3]).max(axis=0)
            gas_relative=gas_new/np.maximum(abs(finer['gas'][sampled,:3]).max(axis=0),1e-300)
            gas_contraction=gas_new/np.maximum(gas_old,1e-300)
            old_resolved=photon_norm(fine['photon'][:,:,:3]-coarse['photon'][:,:,:3],basis.mass).max(axis=0)
            new_resolved=photon_norm(finer['photon'][sampled,:,:3]-fine['photon'][:,:,:3],basis.mass).max(axis=0)
            for name,value,limit in [('Final radiation1percent',relative,.01),('Radiation contraction',contraction,1.),
                    ('Peak gas1percent',gas_relative,.01),('Gas contraction',gas_contraction,1.)]:
                checks.extend(check(f'{model}:m{int(upper*1000)}:{name}:{branch}',result,limit) for branch,result in zip(['baseline','join1','join2'],value))
            inner_fields={}
            for name,path in [('coarse',PARENT/'results'/f'inner-{model}-space-p4-n5120/prediction.npz'),
                    ('fine',PARENT/'results'/f'inner-{model}-fine-p4-n5120/prediction.npz'),
                    ('finer',ROOT/'results'/f'inner-{model}-n5120/prediction.npz')]:
                saved=read_npz(path)
                inputs.append(path)
                inner_fields[name]=np.stack([compact_defect(basis.nodes,saved['frequency'],values,upper) for values in saved['defect']])
            old_inner_delta=norm(inner_fields['fine']-inner_fields['coarse'],basis.measure).max(axis=0)
            new_inner_delta=norm(inner_fields['finer']-inner_fields['fine'],basis.measure).max(axis=0)
            inner_relative=new_inner_delta/np.maximum(norm(inner_fields['finer'],basis.measure).max(axis=0),1e-300)
            inner_contraction=new_inner_delta/np.maximum(old_inner_delta,1e-300)
            checks.extend(check(f'{model}:m{int(upper*1000)}:Inner1percent:{branch}',result,.01) for branch,result in zip(['baseline','join1','join2'],inner_relative))
            checks.extend(check(f'{model}:m{int(upper*1000)}:Inner contraction:{branch}',result,1.) for branch,result in zip(['baseline','join1','join2'],inner_contraction))
            source_status=local_packet(finer_path.parent)
            rows.append(dict(model=model,upper=upper,final_radiation_relative_change=relative.tolist(),
                radiation_contraction=contraction.tolist(),radiation_observed_order=(-np.log2(np.maximum(contraction,1e-300))).tolist(),
                gas_peak_relative_change=gas_relative.tolist(),gas_contraction=gas_contraction.tolist(),
                resolved_peak_contraction=(new_resolved/np.maximum(old_resolved,1e-300)).tolist(),
                inner_peak_relative_change=inner_relative.tolist(),inner_contraction=inner_contraction.tolist(),
                finer_metrics=source_status['models'][model]['metrics'],
                gas_ratio_finer_over_fine=(finer['gas'][-1,:3]/fine['gas'][-1,:3]).tolist()))
    finish(folder,dict(checks=checks,rows=rows,grid_sizes=[659,1317,2633],inner_steps=5120,response_steps=2048,
        same_events_rates_boundaries_and_histories=True,extrapolated_value_promoted=False,
        columns=['baseline','join1','join2']),__file__,inputs)
    print(json.dumps(dict(rows=rows,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
