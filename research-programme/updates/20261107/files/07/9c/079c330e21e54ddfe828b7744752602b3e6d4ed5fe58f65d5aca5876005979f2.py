from consecutive_common import *


def main():
    modest()
    folder=ROOT/'results/grid-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    previous=BRANCH/'repaired-inner-radiation-gas-feedback-20261013'
    checks,rows,inputs=[],[],list(ladder.inputs)
    for upper,event_order in [(.04,8),(.02,6)]:
        for model in ['heavy','cold']:
            coarse_path=previous/'results'/f'response-fine-p4-n5120-o{event_order}-q32-m{int(upper*1000)}-r2048'/(model+'.npz')
            fine_path=PARENT/'results'/f'feedback-m{int(upper*1000)}-n5120'/(model+'-response.npz')
            finer_path=ROOT/'results'/f'feedback-m{int(upper*1000)}-n5120'/(model+'-response.npz')
            fields={}
            for name,path in [('coarse',coarse_path),('fine',fine_path),('finer',finer_path)]:
                local_packet(path.parent)
                fields[name]=read_npz(path)
                inputs.extend([path,path.parent/'status.json'])
            coarse,fine,finer=fields['coarse'],fields['fine'],fields['finer']
            assert np.array_equal(fine['coordinate'],finer['coordinate'])
            assert np.allclose(finer['coordinate'][::16],coarse['coordinate'],atol=1e-14,rtol=0)
            old_delta=norm(fine['physical_change']-coarse['physical_change'],basis.measure)
            new_delta=norm(finer['physical_change']-fine['physical_change'],basis.measure)
            relative=new_delta/np.maximum(norm(finer['physical_change'],basis.measure),1e-300)
            contraction=new_delta/np.maximum(old_delta,1e-300)
            gas_old=abs(fine['gas'][::16,:3]-coarse['gas'][:,:3]).max(axis=0)
            gas_new=abs(finer['gas'][:,:3]-fine['gas'][:,:3]).max(axis=0)
            gas_sampled=abs(finer['gas'][::16,:3]-fine['gas'][::16,:3]).max(axis=0)
            gas_relative=gas_new/np.maximum(abs(finer['gas'][:,:3]).max(axis=0),1e-300)
            gas_contraction=gas_sampled/np.maximum(gas_old,1e-300)
            for name,value,limit in [('Final radiation1percent',relative,.01),('Radiation contraction',contraction,1.),
                    ('Full-history peak gas1percent',gas_relative,.01),('Common-cadence gas contraction',gas_contraction,1.)]:
                checks.extend(check(f'{model}:m{int(upper*1000)}:{name}:{branch}',result,limit)
                    for branch,result in zip(['baseline','join1','join2'],value))
            inner_fields={}
            for name,path in [('coarse',previous/'results'/f'inner-{model}-fine-p4-n5120/prediction.npz'),
                    ('fine',PARENT/'results'/f'inner-{model}-n5120/prediction.npz'),
                    ('finer',ROOT/'results'/f'inner-{model}-n5120/prediction.npz')]:
                saved=read_npz(path)
                inputs.append(path)
                inner_fields[name]=np.stack([compact_defect(basis.nodes,saved['frequency'],values,upper) for values in saved['defect']])
            old_inner=norm(inner_fields['fine']-inner_fields['coarse'],basis.measure).max(axis=0)
            new_inner=norm(inner_fields['finer']-inner_fields['fine'],basis.measure).max(axis=0)
            inner_relative=new_inner/np.maximum(norm(inner_fields['finer'],basis.measure).max(axis=0),1e-300)
            inner_contraction=new_inner/np.maximum(old_inner,1e-300)
            for name,value,limit in [('Inner1percent',inner_relative,.01),('Inner contraction',inner_contraction,1.)]:
                checks.extend(check(f'{model}:m{int(upper*1000)}:{name}:{branch}',result,limit)
                    for branch,result in zip(['baseline','join1','join2'],value))
            rows.append(dict(model=model,upper=upper,final_radiation_relative_change=relative.tolist(),
                radiation_contraction=contraction.tolist(),radiation_observed_order=(-np.log2(np.maximum(contraction,1e-300))).tolist(),
                gas_peak_relative_change=gas_relative.tolist(),gas_contraction_common129=gas_contraction.tolist(),
                gas_peak_cadence=2049,contraction_cadence=129,
                inner_peak_relative_change=inner_relative.tolist(),inner_contraction=inner_contraction.tolist(),
                gas_ratio_finer_over_fine=(finer['gas'][-1,:3]/fine['gas'][-1,:3]).tolist()))
    finish(folder,dict(checks=checks,rows=rows,grid_sizes=[1317,2633,5265],inner_steps=5120,response_steps=2048,
        physical_inputs_unchanged=True,extrapolated_value_promoted=False,columns=['baseline','join1','join2']),__file__,inputs)
    print(json.dumps(dict(rows=rows,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
