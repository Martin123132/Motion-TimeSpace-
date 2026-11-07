from direct_common import *


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    names=['fine-o6-q32-m40-n1024','fine-o8-q32-m40-n1024','fine-o6-q48-m40-n1024',
        'fine-o6-q32-m20-n1024','fine-o8-q32-m40-n512','space-o8-q32-m40-n1024','time-o8-q32-m40-n1024']
    old_names=['fine-q32-m40-n1024','fine-space-transport-n1024','space-fine-transport-n1024','space-q32-m40-n1024']
    checks,inputs,models=[],[],{}
    for model in ['heavy','cold']:
        cases={}
        for name in names:
            path=ROOT/'results'/('response-'+name)/(model+'.npz')
            cases[name]=read_npz(path)
            inputs.extend([path,path.parent/'status.json'])
        old={}
        for name in old_names:
            path=PARENT/'results'/('response-'+name)/(model+'.npz')
            old[name]=read_npz(path)
            inputs.extend([path,path.parent/'status.json'])
        fine=cases['fine-o8-q32-m40-n1024']
        measure=fine['measure']
        norm=lambda value:np.sqrt(np.sum(measure[:,None]*value**2,axis=0))
        fine_norm=norm(fine['physical_change'])
        saved_norm=norm(fine['saved_potential'])
        residual_norm=norm(fine['saved_residual'])
        def difference(first,second):
            value=norm(first['physical_change']-second['physical_change'])
            return dict(absolute_norm=value.tolist(),over_direct_response=(value/np.maximum(fine_norm,1e-300)).tolist(),
                over_saved_spectrum=(value/np.maximum(saved_norm,1e-300)).tolist())
        refinements={}
        for label,first,second in [
            ('events6to8',cases['fine-o6-q32-m40-n1024'],fine),
            ('compton_panels32to48',cases['fine-o6-q32-m40-n1024'],cases['fine-o6-q48-m40-n1024']),
            ('response_steps512to1024',cases['fine-o8-q32-m40-n512'],fine)]:
            result=difference(first,second)
            refinements[label]=result
            checks.append(check(label+':'+model,max(result['over_direct_response']),.01))
        sensitivity={}
        for label,first,second in [
            ('same_fine_profile_old_fine_stencil',old['fine-q32-m40-n1024'],fine),
            ('same_fine_profile_old_coarse_stencil',old['fine-space-transport-n1024'],fine),
            ('remaining_profile_space',cases['space-o8-q32-m40-n1024'],fine),
            ('remaining_profile_time',cases['time-o8-q32-m40-n1024'],fine),
            ('matching_upper04to02',cases['fine-o6-q32-m20-n1024'],cases['fine-o6-q32-m40-n1024'])]:
            sensitivity[label]=difference(first,second)
        previous_profile=norm(old['space-fine-transport-n1024']['physical_change']-old['fine-q32-m40-n1024']['physical_change'])
        direct_profile=norm(cases['space-o8-q32-m40-n1024']['physical_change']-fine['physical_change'])
        old_combined=norm(old['space-q32-m40-n1024']['physical_change']-old['fine-q32-m40-n1024']['physical_change'])
        old_transport=norm(old['fine-space-transport-n1024']['physical_change']-old['fine-q32-m40-n1024']['physical_change'])
        models[model]=dict(final_direct_norm=fine_norm.tolist(),
            final_change_over_saved=(fine_norm/saved_norm).tolist(),
            final_residual_change_over_saved_residual=(norm(fine['residual_change'])/residual_norm).tolist(),
            event_panel_time_refinements=refinements,sensitivities=sensitivity,
            remaining_profile_difference_over_previous_profile_difference=(direct_profile/previous_profile).tolist(),
            remaining_profile_difference_over_previous_combined_difference=(direct_profile/old_combined).tolist(),
            previous_same_profile_transport_spread_absolute=old_transport.tolist(),
            direct_event_refinement_over_previous_transport_spread=(norm(cases['fine-o6-q32-m40-n1024']['physical_change']-fine['physical_change'])/old_transport).tolist(),
            physical_profile_difference_still_present=bool(np.any(direct_profile/fine_norm>.01)))
        print(json.dumps(dict(model=model,**models[model])),flush=True)
    finish(folder,dict(checks=checks,models=models,columns=['baseline','join1','join2'],
        parent_history_rerun=False,physical_shift_deposition_removed_from_compact_source=True,
        physical_shift_deposition_removed_from_saved_tail_profiles=False,
        finite_planck_recoil_remainder_bounded=False),__file__,inputs)


if __name__=='__main__':
    main()

