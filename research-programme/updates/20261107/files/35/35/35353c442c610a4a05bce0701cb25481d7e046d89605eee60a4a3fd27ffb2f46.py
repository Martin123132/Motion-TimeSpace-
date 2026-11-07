from repair_common import *


def main():
    modest()
    folder=ROOT/'results/source-rule-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[*ladder.inputs,ROOT/'SOURCE-RULE-CONTROL.md']
    rows,checks=[],[]
    for model in ['heavy','cold']:
        windows={}
        for upper,order in [(.04,8),(.02,6)]:
            fields={}
            for rule in [32,48]:
                path=ROOT/'results'/f'response-fine-p4-n5120-o{order}-q{rule}-m{int(upper*1000)}-r2048'/(model+'.npz')
                local_packet(path.parent)
                fields[rule]=read_npz(path)
                inputs.extend([path,path.parent/'status.json'])
            reference,refined=fields[32],fields[48]
            windows[upper]=reference
            radiation=norm(refined['physical_change']-reference['physical_change'],basis.measure)/norm(reference['physical_change'],basis.measure)
            gas=abs(refined['gas'][:,:3]-reference['gas'][:,:3]).max(axis=0)/np.maximum(abs(reference['gas'][:,:3]).max(axis=0),1e-300)
            for quantity,values in [('radiation',radiation),('gas',gas)]:
                checks.extend(check(f'{model}:m{int(upper*1000)}:{quantity}:{branch}',value,.01) for branch,value in zip(['baseline','join1','join2'],values))
            rows.append(dict(model=model,upper=upper,radiation_relative_change=radiation.tolist(),gas_peak_relative_change=gas.tolist()))
        old={}
        for upper in [.04,.02]:
            path=BRANCH/'physical-join-flux-decomposition-20261012/results/response-o8-q32-n8192'/f'{model}-m{int(upper*1000)}.npz'
            old[upper]=read_npz(path)
            inputs.append(path)
        rows.append(dict(model=model,kind='window-change',
            old_radiation_window_difference_over_wide= (norm(old[.02]['physical_change']-old[.04]['physical_change'],basis.measure)/norm(old[.04]['physical_change'],basis.measure)).tolist(),
            repaired_radiation_window_difference_over_wide=(norm(windows[.02]['physical_change']-windows[.04]['physical_change'],basis.measure)/norm(windows[.04]['physical_change'],basis.measure)).tolist()))
    finish(folder,dict(checks=checks,rows=rows,dc_br_rule32to48=True,compton_rule_unchanged=32,
        physical_parameters_unchanged=True,reference_packet_unchanged=True),__file__,inputs)
    print(json.dumps(dict(rows=rows,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
