from join_common import *


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--steps',type=int,choices=[2048,4096,8192,16384],required=True)
    args=parser.parse_args()
    modest()
    folder=ROOT/'results'/f'time-control-n{args.steps}'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[*ladder.inputs,ROOT/'TIME-REFINEMENT-ADDENDUM.md']
    checks,models=[],{}
    norm=lambda value:np.sqrt(np.sum(basis.measure[:,None]*value**2,axis=0))
    for model in ['heavy','cold']:
        denominator_path=ROOT/'results/response-o8-q32-n1024'/f'{model}-m40.npz'
        denominator=np.maximum(norm(read_npz(denominator_path)['physical_change']),1e-300)
        inputs.append(denominator_path)
        for upper in UPPERS:
            label=f'{model}-m{int(upper*1000)}'
            previous_path=ROOT/'results'/f'response-o8-q32-n{args.steps//2}'/(label+'.npz')
            current_path=ROOT/'results'/f'response-o8-q32-n{args.steps}'/(label+'.npz')
            previous,current=read_npz(previous_path),read_npz(current_path)
            inputs.extend([previous_path,current_path,previous_path.parent/'status.json',current_path.parent/'status.json'])
            component=np.array([norm(basis.values@(current['photon'][-1,:,offset:offset+3]-previous['photon'][-1,:,offset:offset+3]))/denominator for offset in [3,6,9]])
            total=norm(current['physical_change']-previous['physical_change'])/denominator
            checks.extend([check('Component refinement versus NET:'+label,np.max(component),.01),
                check('Total refinement:'+label,max(total),.01)])
            models[label]=dict(component_difference_over_reference_net=component.tolist(),total_difference_over_reference_net=total.tolist())
    finish(folder,dict(checks=checks,models=models,steps=args.steps,previous_steps=args.steps//2,
        reference_scale='unchanged1024-step,m40 net response',original_failed_gates_retained=True),__file__,inputs)
    print(json.dumps(dict(steps=args.steps,passed=all(row['passed'] for row in checks),models=models)),flush=True)


if __name__=='__main__':
    main()

