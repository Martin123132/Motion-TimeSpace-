from repair_common import *
from matched_feedback_common import CompactCorrection


def main():
    modest()
    folder=ROOT/'results/inner-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=list(ladder.inputs)
    checks,rows=[],[]
    cases={'reference':'fine-p4-n5120','time':'fine-p4-n10240','space':'space-p4-n5120','forcing':'fine-p6-n5120'}
    for model in ['heavy','cold']:
        predictions={}
        for name,case in cases.items():
            path=ROOT/'results'/f'inner-{model}-{case}'/'prediction.npz'
            local_packet(path.parent)
            predictions[name]=read_npz(path)
            inputs.extend([path,path.parent/'status.json'])
        old,profiles,gas,dependencies=read_prediction(model,'fine')
        inputs.extend(dependencies)
        for upper in [.04,.02]:
            values={name:np.stack([compact_defect(basis.nodes,saved['frequency'],field,upper) for field in saved['defect']]) for name,saved in predictions.items()}
            correction=CompactCorrection(basis,old['frequency'],upper)
            correction.register('canonical',basis.nodes)
            old_values=np.stack([correction.at('canonical',interpolate.CubicSpline(np.log(old['frequency']),slope,axis=0),profile) for slope,profile in zip(old['slope'],profiles)])
            old_values[0]=0
            reference=values['reference']
            new_scale=np.maximum(norm(reference,basis.measure).max(axis=0),1e-300)
            old_scale=np.maximum(norm(old_values,basis.measure).max(axis=0),1e-300)
            comparisons={}
            for name in ['time','space','forcing']:
                change=norm(values[name]-reference,basis.measure)
                relative=change.max(axis=0)/new_scale
                comparisons[name]=dict(peak_change_over_repaired_peak=relative.tolist(),
                    peak_change_over_old_peak=(change.max(axis=0)/old_scale).tolist(),
                    final_change_over_repaired_final=(change[-1]/np.maximum(norm(reference[-1],basis.measure),1e-300)).tolist())
                checks.extend(check(f'{model}:m{int(upper*1000)}:{name}:{branch}',value,.01) for branch,value in zip(['baseline','join1','join2'],relative))
            rows.append(dict(model=model,upper=upper,repaired_peak=new_scale.tolist(),old_peak=old_scale.tolist(),
                repaired_final=norm(reference[-1],basis.measure).tolist(),old_final=norm(old_values[-1],basis.measure).tolist(),
                repaired_peak_over_old_peak=(new_scale/old_scale).tolist(),comparisons=comparisons))
            np.savez_compressed(folder/f'{model}-m{int(upper*1000)}.npz',coordinate=old['coordinate'],frequency=basis.nodes,
                measure=basis.measure,old_replacement=old_values,**values)
    finish(folder,dict(checks=checks,rows=rows,normalization='peak norm of repaired difference per physical column; old scale separate',
        old_initial_interpolation_residual_set_zero=True,source_columns=['baseline','join1','join2']),__file__,inputs)
    print(json.dumps(dict(rows=rows,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
