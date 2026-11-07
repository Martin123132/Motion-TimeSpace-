from join_common import *
from matched_feedback_common import ShapeReadout


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    reader=ShapeReadout(basis,canonical=True)
    inputs=[*ladder.inputs]
    checks,models=[],{}
    norm=lambda value:np.sqrt(np.sum(basis.measure[:,None]*value**2,axis=0))
    def residual(value):
        eta=(reader.measure*reader.frequency)@value/reader.capacity
        return value-reader.frequency[:,None]*eta-reader.templates@(reader.amplitude_matrix@value)
    def components(case):
        return [basis.values@case['photon'][-1,:,offset:offset+3] for offset in [3,6,9]]+[case['unresolved_change']]
    for model in ['heavy','cold']:
        cases={}
        for rule in ['o6-q32-n1024','o8-q32-n1024','o6-q48-n1024','o8-q32-n512']:
            for upper in UPPERS:
                path=ROOT/'results'/('response-'+rule)/f'{model}-m{int(upper*1000)}.npz'
                cases[rule,upper]=read_npz(path)
                inputs.extend([path,path.parent/'status.json'])
        reference=cases['o8-q32-n1024',.04]
        denominator=np.maximum(norm(reference['physical_change']),1e-300)
        saved_norm=np.maximum(norm(reference['saved_potential']),1e-300)
        control_rows={}
        for upper in UPPERS:
            fine=cases['o8-q32-n1024',upper]
            parts=components(fine)
            closure=norm(sum(parts)-fine['physical_change'])/np.maximum(sum(norm(part) for part in parts),1e-300)
            checks.append(check(f'Four physical contributions reconstruct:{model}:{upper}',np.max(closure),1e-10))
            discrepancy=norm(residual(fine['physical_change'])-fine['residual_change'])/np.maximum(norm(fine['residual_change']),1e-300)
            checks.append(check(f'Independent residual-shape map:{model}:{upper}',np.max(discrepancy),1e-10))
            old_rule='fine-o8-q32-m40-n1024' if upper==.04 else 'fine-o6-q32-m20-n1024'
            old_path=PARENT/'results'/('response-'+old_rule)/(model+'.npz')
            old=read_npz(old_path)
            inputs.extend([old_path,old_path.parent/'status.json'])
            difference=norm(fine['physical_change']-old['physical_change'])/np.maximum(norm(old['physical_change']),1e-300)
            checks.append(check(f'Unchanged recombined Stage113 response:{model}:{upper}',max(difference),1e-4))
            rows={'against_stage113':difference.tolist()}
            for label,first,second in [
                ('event6to8',cases['o6-q32-n1024',upper],fine),
                ('panels32to48',cases['o6-q32-n1024',upper],cases['o6-q48-n1024',upper]),
                ('steps512to1024',cases['o8-q32-n512',upper],fine)]:
                first_parts,second_parts=components(first),components(second)
                component_changes=np.array([norm(before-after)/denominator for before,after in zip(first_parts,second_parts)])
                total_change=norm(first['physical_change']-second['physical_change'])/denominator
                rows[label]=dict(component_difference_over_reference_net=component_changes.tolist(),
                    total_difference_over_reference_net=total_change.tolist())
                checks.append(check(f'Component refinement versus NET:{label}:{model}:{upper}',np.max(component_changes),.01))
                checks.append(check(f'Total refinement:{label}:{model}:{upper}',max(total_change),.01))
            rows['component_norm_over_net']=[(norm(part)/denominator).tolist() for part in parts]
            control_rows[str(upper)]=rows
        upper_case,lower_case=cases['o8-q32-n1024',.04],cases['o8-q32-n1024',.02]
        changes=[low-high for low,high in zip(components(lower_case),components(upper_case))]
        difference=lower_case['physical_change']-upper_case['physical_change']
        attribution={}
        for view,transform in [('full_spectrum',lambda value:value),('residual_shape',residual)]:
            transformed=[transform(change) for change in changes]
            total=transform(difference)
            total_norm=norm(total)
            component_norms=np.array([norm(value) for value in transformed])
            signed=np.array([np.sum(basis.measure[:,None]*value*total,axis=0)/np.maximum(total_norm**2,1e-300) for value in transformed])
            reconstruction=norm(sum(transformed)-total)/np.maximum(component_norms.sum(axis=0),1e-300)
            checks.append(check(f'Window-difference vector reconstruction:{view}:{model}',max(reconstruction),1e-10))
            checks.append(check(f'Signed projections sum to one:{view}:{model}',max(abs(signed.sum(axis=0)-1)),1e-8))
            attribution[view]=dict(component_norm_over_total=(component_norms/np.maximum(total_norm,1e-300)).tolist(),
                signed_projection_share=signed.tolist(),cancellation_factor=(component_norms.sum(axis=0)/np.maximum(total_norm,1e-300)).tolist(),
                total_difference_norm=total_norm.tolist())
        models[model]=dict(controls=control_rows,window_attribution=attribution,
            final_feedback_fraction_of_saved=(norm(reference['physical_change'])/saved_norm).tolist(),
            window_difference_over_reference_net=(norm(difference)/denominator).tolist(),
            window_difference_over_saved=(norm(difference)/saved_norm).tolist())
        print(json.dumps(dict(model=model,**models[model])),flush=True)
    finish(folder,dict(checks=checks,models=models,component_labels=['bulk','joining','remainder','unresolved'],
        columns=['baseline','join1','join2'],new_physical_prediction=False,common_full_frequency_overlap_closed=False,
        exact_product_decomposition=True,join_discarded=False),__file__,inputs)


if __name__=='__main__':
    main()

