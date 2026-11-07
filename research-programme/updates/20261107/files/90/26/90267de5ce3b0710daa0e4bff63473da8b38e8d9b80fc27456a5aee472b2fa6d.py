from join_common import *


def main():
    modest()
    folder=ROOT/'results/orthogonal-budget'
    folder.mkdir(parents=True,exist_ok=False)
    checks,models,inputs=[],{},[]
    for model in ['heavy','cold']:
        for steps in [512,1024]:
            responses=[]
            for upper in UPPERS:
                path=ROOT/'results'/f'response-o8-q32-n{steps}'/f'{model}-m{int(upper*1000)}.npz'
                responses.append(read_npz(path))
                inputs.extend([path,path.parent/'status.json'])
            high,low=responses
            measure=high['measure']
            resolved=low['resolved_change']-high['resolved_change']
            unresolved=low['unresolved_change']-high['unresolved_change']
            total=low['physical_change']-high['physical_change']
            square=lambda value:np.sum(measure[:,None]*value**2,axis=0)
            resolved2,unresolved2,total2=[square(value) for value in [resolved,unresolved,total]]
            cross=np.sum(measure[:,None]*resolved*unresolved,axis=0)
            denominator=np.maximum(resolved2+unresolved2,1e-300)
            label=f'{model}:{steps}'
            checks.extend([check('Resolved/unresolved orthogonality:'+label,max(abs(2*cross)/denominator),1e-10),
                check('Pythagorean window budget:'+label,max(abs(total2-denominator)/denominator),1e-10)])
            models[label]=dict(resolved_squared_norm_fraction=(resolved2/total2).tolist(),
                unresolved_squared_norm_fraction=(unresolved2/total2).tolist(),
                resolved_norm=np.sqrt(resolved2).tolist(),unresolved_norm=np.sqrt(unresolved2).tolist(),
                total_norm=np.sqrt(total2).tolist(),cross_term_over_squared_norm=(2*cross/denominator).tolist())
    finish(folder,dict(checks=checks,models=models,columns=['baseline','join1','join2'],
        scope='Unfiltered full-spectrum norm;not energy fractions or residual-shape fractions.'),__file__,inputs)
    print(json.dumps(dict(checks=checks,models=models)),flush=True)


if __name__=='__main__':
    main()

