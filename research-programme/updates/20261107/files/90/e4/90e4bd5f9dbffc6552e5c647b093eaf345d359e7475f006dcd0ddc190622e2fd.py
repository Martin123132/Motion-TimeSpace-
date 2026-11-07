from repair_common import *


def main():
    modest()
    folder=ROOT/'results/feedback-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=list(ladder.inputs)
    checks,rows=[],[]
    for upper,order in [(.04,8),(.02,6)]:
        window=f'm{int(upper*1000)}'
        reference=f'fine-p4-n5120-o{order}-q32-{window}-r2048'
        cases=dict(response_time=f'fine-p4-n5120-o{order}-q32-{window}-r1024',
            reconstruction_time=f'fine-p4-n10240-o{order}-q32-{window}-r2048',
            reconstruction_space=f'space-p4-n5120-o{order}-q32-{window}-r2048',
            forcing_order=f'fine-p6-n5120-o{order}-q32-{window}-r2048')
        if upper==.04:
            cases['compton_order']='fine-p4-n5120-o6-q32-m40-r2048'
        for model in ['heavy','cold']:
            path=ROOT/'results'/('response-'+reference)/(model+'.npz')
            status=local_packet(path.parent)
            saved=read_npz(path)
            inputs.extend([path,path.parent/'status.json'])
            photon_scale=np.maximum(norm(saved['physical_change'],basis.measure),1e-300)
            gas_scale=np.maximum(abs(saved['gas'][:,:3]).max(axis=0),1e-300)
            source_path=ROOT/'results'/status['source_packet']/(model+'.npz')
            source=read_npz(source_path)
            inputs.append(source_path)
            comparisons={}
            for name,case in cases.items():
                other_path=ROOT/'results'/('response-'+case)/(model+'.npz')
                local_packet(other_path.parent)
                other=read_npz(other_path)
                inputs.extend([other_path,other_path.parent/'status.json'])
                assert np.allclose(saved['coordinate'],other['coordinate'],rtol=0,atol=1e-14)
                radiation=norm(other['physical_change']-saved['physical_change'],basis.measure)/photon_scale
                residual=norm(other['residual_change']-saved['residual_change'],basis.measure)/np.maximum(norm(saved['residual_change'],basis.measure),1e-300)
                gas=abs(other['gas'][:,:3]-saved['gas'][:,:3]).max(axis=0)/gas_scale
                resolved=photon_norm(other['photon'][:,:,:3]-saved['photon'][:,:,:3],basis.mass).max(axis=0)/np.maximum(photon_norm(saved['photon'][:,:,:3],basis.mass).max(axis=0),1e-300)
                comparisons[name]=dict(final_radiation_relative_change=radiation.tolist(),final_distortion_relative_change=residual.tolist(),
                    peak_gas_relative_change=gas.tolist(),peak_resolved_radiation_relative_change=resolved.tolist())
                for quantity,values in [('radiation',radiation),('gas',gas),('distortion',residual),('resolved',resolved)]:
                    checks.extend(check(f'{model}:{window}:{name}:{quantity}:{branch}',value,.01) for branch,value in zip(['baseline','join1','join2'],values))
            old_path=BRANCH/'physical-join-flux-decomposition-20261012/results/response-o8-q32-n8192'/f'{model}-{window}.npz'
            old=read_npz(old_path)
            inputs.append(old_path)
            row=dict(model=model,upper=upper,metrics=status['models'][model]['metrics'],comparisons=comparisons,
                repaired_over_old_radiation=(photon_scale/np.maximum(norm(old['physical_change'],basis.measure),1e-300)).tolist(),
                repaired_over_old_final_gas=(abs(saved['gas'][-1,:3])/np.maximum(abs(old['gas'][-1,:3]),1e-300)).tolist(),
                signed_gas_old=old['gas'][-1,:3].tolist(),signed_gas_new=saved['gas'][-1,:3].tolist(),
                old_radiation_norm=norm(old['physical_change'],basis.measure).tolist(),
                maximum_projection_rule_difference=(photon_norm(source['projection_quadrature_difference'],basis.mass).max(axis=0)/np.maximum(source['replacement_norm'].max(axis=0),1e-300)).tolist())
            rows.append(row)
    finish(folder,dict(checks=checks,rows=rows,same_controls_for_baseline_and_corrections=True,
        relative_controls_normalized_to_repaired_signal=True,
        old_raw_gas_failures_retained=True,old_comparison_packet='Stage114 response-o8-q32-n8192'),__file__,inputs)
    print(json.dumps(dict(rows=rows,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
