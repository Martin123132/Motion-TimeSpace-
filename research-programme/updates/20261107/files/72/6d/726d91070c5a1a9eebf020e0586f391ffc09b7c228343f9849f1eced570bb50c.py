from join_common import *


def main():
    modest()
    controls=sorted((ROOT/'results').glob('time-control-n*/status.json'),key=lambda path:int(path.parent.name.split('-n')[-1]))
    assert controls
    control_path=controls[-1]
    control=json.loads(control_path.read_text())
    steps=control['steps']
    folder=ROOT/'results/refined-attribution'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[*ladder.inputs,control_path,ROOT/'ORTHOGONAL-WINDOW-BUDGET.md']
    checks=[dict(name='Finest component timestep refinement satisfies original NET gate',passed=control['all_checks_passed'])]
    models={}
    norm=lambda value:np.sqrt(np.sum(basis.measure[:,None]*value**2,axis=0))
    for model in ['heavy','cold']:
        cases,parts=[],[]
        for upper in UPPERS:
            path=ROOT/'results'/f'response-o8-q32-n{steps}'/f'{model}-m{int(upper*1000)}.npz'
            response=read_npz(path)
            inputs.extend([path,path.parent/'status.json'])
            cases.append(response)
            pieces=[basis.values@response['photon'][-1,:,offset:offset+3] for offset in [3,6,9]]+[response['unresolved_change']]
            parts.append(pieces)
            error=norm(sum(pieces)-response['physical_change'])/np.maximum(sum(norm(value) for value in pieces),1e-300)
            checks.append(check(f'Finest physical-component reconstruction:{model}:{upper}',max(error),1e-10))
        high,low=cases
        total=low['physical_change']-high['physical_change']
        changes=[lower-higher for lower,higher in zip(parts[1],parts[0])]
        total_norm=norm(total)
        shares=np.array([np.sum(basis.measure[:,None]*value*total,axis=0)/total_norm**2 for value in changes])
        checks.append(check('Finest signed projections sum to one:'+model,max(abs(shares.sum(axis=0)-1)),1e-8))
        resolved=low['resolved_change']-high['resolved_change']
        unresolved=low['unresolved_change']-high['unresolved_change']
        resolved2,unresolved2,total2=norm(resolved)**2,norm(unresolved)**2,total_norm**2
        cross=2*np.sum(basis.measure[:,None]*resolved*unresolved,axis=0)
        checks.append(check('Finest resolved/unresolved orthogonality:'+model,max(abs(cross)/total2),1e-10))
        checks.append(check('Finest Pythagorean budget:'+model,max(abs(total2-resolved2-unresolved2)/total2),1e-10))
        old_path=ROOT/'results/response-o8-q32-n1024'/f'{model}-m40.npz'
        old=read_npz(old_path)
        inputs.append(old_path)
        models[model]=dict(signed_projection_share=shares.tolist(),
            component_norm_over_window_difference=[(norm(value)/total_norm).tolist() for value in changes],
            window_cancellation_factor=(sum(norm(value) for value in changes)/total_norm).tolist(),
            resolved_squared_norm_fraction=(resolved2/total2).tolist(),
            unresolved_squared_norm_fraction=(unresolved2/total2).tolist(),
            final_feedback_fraction_of_saved=(norm(high['physical_change'])/norm(high['saved_potential'])).tolist(),
            refined_vs1024_total_over1024_net=(norm(high['physical_change']-old['physical_change'])/norm(old['physical_change'])).tolist(),
            dropped_join_would_change_net_by=(norm(parts[0][1])/norm(high['physical_change'])).tolist(),
            window_difference_over_fine_net=(total_norm/norm(high['physical_change'])).tolist())
    finish(folder,dict(checks=checks,models=models,steps=steps,
        authoritative_response_packet=f'response-o8-q32-n{steps}',
        columns=['baseline','join1','join2'],components=['bulk','joining','remainder','unresolved'],
        joining_term_retained=True,parent_raw_gas_relative_flags_not_promoted=True),__file__,inputs)
    print(json.dumps(dict(steps=steps,checks=checks,models=models)),flush=True)


if __name__=='__main__':
    main()

