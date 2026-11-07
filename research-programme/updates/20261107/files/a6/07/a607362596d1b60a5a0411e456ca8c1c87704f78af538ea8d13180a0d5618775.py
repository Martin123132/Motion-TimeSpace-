from overlap_common import *


def main():
    modest()
    folder=ROOT/'results/balanced-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[*ladder.inputs,ROOT/'WELL-BALANCED-EXTENSION.md']
    checks,rows=[],[]
    for model in ['heavy','cold']:
        root=ROOT/'results'/f'balanced-{model}-fine-p4-n5120'
        reference=read_npz(root/'readout.npz')
        inputs.extend([root/'readout.npz',root/'status.json'])
        denominator=np.maximum(reference['old_band_norm'].max(axis=0),1e-300)
        for label,kind in [(f'balanced-{model}-fine-p4-n10240','time'),
                           (f'balanced-{model}-space-p4-n5120','space'),
                           (f'balanced-{model}-fine-p6-n5120','forcing')]:
            other_root=ROOT/'results'/label
            other=read_npz(other_root/'readout.npz')
            inputs.extend([other_root/'readout.npz',other_root/'status.json'])
            difference=reference['residual_band']-other['residual_band']
            relative=norm(difference,basis.measure).max(axis=0)/denominator
            rows.append(dict(model=model,control=kind,peak_difference_over_old_peak=relative.tolist(),
                reference_final_residual_ratio=(reference['residual_band_norm'][-1]/reference['old_band_norm'][-1]).tolist(),
                reference_final_bridge_ratio=(reference['bridge_band_norm'][-1]/reference['old_band_norm'][-1]).tolist()))
            for branch,value in zip(['baseline','join1','join2'],relative):
                checks.append(check(kind+':'+model+':'+branch,value,.01))
    finish(folder,dict(checks=checks,rows=rows,physical_signal_claim=False,
        comparison_scale='original inner-minus-outer band norm;not total spectrum',parent_response_unchanged=True),__file__,inputs)
    print(json.dumps(dict(rows=rows,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
