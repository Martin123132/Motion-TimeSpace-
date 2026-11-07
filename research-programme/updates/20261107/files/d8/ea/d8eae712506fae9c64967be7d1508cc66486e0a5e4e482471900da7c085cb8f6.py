from stage160_common import *
import argparse


def reconstruct(data,registry,checks,folder):
    banks={}
    used_events=0
    for order in [5,6]:
        sites=[]
        virtual=registry.read(SOURCE157/'results/analysis'/f'order{order}-frequency.npz')
        for site_index,site in enumerate(SITES):
            location=bank_folder(site,order)
            config_path=location/'configuration.json'
            registry.add(config_path)
            config=json.loads(config_path.read_text())
            theta=config['theta']
            nodes=list(integration_nodes(theta,order))
            assert len(nodes)==7*order*36
            frequencies=[value for value,weight in incoming_rule(order,BOUNDARIES[0],BOUNDARIES[-1])]
            slots={value:index for index,value in enumerate(frequencies)}
            terms=[[[] for component in COMPONENTS] for value in frequencies]
            for node in nodes:
                path,original,reused=node_path(site,order,node,config,theta)
                saved=registry.read(path)
                assert json.loads(str(saved['identity']))==original
                assert event_signature(original)==event_signature(node)
                parameters,weight=parameters_and_weight(theta,node)
                original_parameters,original_weight=parameters_and_weight(theta,original)
                assert weight>0 and float(saved['weight'])==original_weight
                loop_path=Path(str(saved['loop_path']))
                registry.add(loop_path)
                loop=json.loads(loop_path.read_text())
                assert loop['identity']==event_owner.inherited.virtual_identity(parameters)
                assert loop['finite'] and loop['scalar']==float(saved['loop_scalar'])
                for component_index,component in enumerate(COMPONENTS):
                    value=saved[component]
                    assert value.shape==(98,4) and np.isfinite(value).all()
                    terms[slots[node['frequency']]][component_index].append(-weight*value)
                used_events+=1
            values=np.asarray([[stable_sum(group) for group in frequency] for frequency in terms])
            assert all(len(group)==36 for frequency in terms for group in frequency)
            panels=np.asarray([[stable_sum(values[panel*order:(panel+1)*order,component])
                for component in range(3)] for panel in range(7)])
            scale=SourceNorm(data['mass'])(data['actual'])
            measure=SourceNorm(data['mass'])
            for component_index,component in enumerate(COMPONENTS):
                expected=full_component(data,site,order,component)
                test(checks,f'Full saved component replay:{site}:{order}:{component}',
                    float(np.max(measure(stable_sum(panels[:,component_index])-expected)/scale)),1e-10)
            test(checks,f'Independent virtual panel replay:{site}:{order}',
                float(np.max(measure(panels[:,1]-virtual['panels'][site_index])/scale)),1e-10)
            if order==6:
                test(checks,f'Independent selected order6 panels:{site}',
                    float(np.max(measure(panels[[3,4]]-data['old_panels'][:,site_index])/scale)),1e-10)
            np.savez_compressed(folder/f'{site}-order{order}-panels.npz',panels=panels,
                frequency_values=values,frequencies=frequencies,theta=theta)
            sites.append(panels)
            print(json.dumps(dict(reconstructed=site,order=order,saved_events=len(nodes))),flush=True)
        banks[order]=np.swapaxes(np.asarray(sites),0,1)
    assert used_events==8316
    return banks,used_events


def source_analysis(data,banks,checks,folder):
    measure=SourceNorm(data['mass'])
    scale=measure(data['actual'])
    delta65=banks[6]-banks[5]
    latest=delta65.copy()
    latest[3]=data['order8_delta']
    latest[4]=data['delta_panels'][1]
    previous=delta65.copy()
    previous[3]=data['delta_panels'][0]
    for site_index,site in enumerate(SITES):
        for component_index,component in enumerate(COMPONENTS):
            expected=data[('delta6_' if site=='cold' else site+'_delta6_')+component]
            test(checks,'Panel65 telescope:'+site+':'+component,
                float(max(measure(sum(delta65[:,site_index,component_index])-expected)/scale)),1e-10)
    current=data['after_order8_full']
    original=np.asarray([parent159.parent158.original_full(data,site) for site in SITES])
    close(checks,'Full mixed-order source telescope',original+data['delta_panels'].sum(axis=(0,2))+data['order8_delta'].sum(axis=1),current,1e-10)
    magnitudes=measure(latest)/scale
    previous_magnitudes=measure(previous)/scale
    older_magnitudes=measure(delta65)/scale
    ratios=magnitudes[[3,4]]/np.maximum(previous_magnitudes[[3,4]],1e-300)
    ratios[0]=np.maximum(ratios[0],previous_magnitudes[3]/np.maximum(older_magnitudes[3],1e-300))
    contraction_available=bool(np.isfinite(ratios).all() and np.all(ratios<1))
    radii=magnitudes.copy()
    if contraction_available:
        radii[[3,4]]=magnitudes[[3,4]]*ratios/(1-ratios)
    routes={}
    arrays=dict(mass=data['mass'],scale=scale,panels5=banks[5],panels6=banks[6],
        delta65=delta65,latest_steps=latest,previous_steps=previous,latest_sources=current,
        observed_ratio_caps=ratios,latest_component_magnitudes=magnitudes,
        conditional_geometric_component_radii=radii if contraction_available else np.empty(0))
    for route in ['local','cubic']:
        weights=weights_for(route)
        prediction=latest_prediction(data,route)
        error=current[0]-prediction
        if route=='cubic':
            close(checks,'Independent current cubic predictor',prediction,
                data['start']/4-current[1]+1.5*current[2]+data['end']/4,1e-12)
        old_error=data['source6']-data[route+'_diagnostic_prediction6']
        adopted_shift=np.einsum('s,scij->ij',weights,data['delta_panels'].sum(axis=0)+data['order8_delta'])
        close(checks,'Source discrepancy telescope:'+route,old_error+adopted_shift,error,1e-10)
        joint=np.einsum('s,pscij->pij',weights,latest)
        panel_budget=measure(joint)/scale
        independent=(abs(weights)[None,:,None,None]*magnitudes).sum(axis=(0,1,2))
        cold_radius=magnitudes[:,0].sum(axis=(0,1))
        coherent=panel_budget.sum(axis=0)
        test(checks,'Panel versus independent triangle:'+route,float(np.max(coherent/independent)),1+1e-12)
        numerator=measure(error)/scale
        denominator=measure(current[0])/scale
        scenarios={}
        scenarios['matched_panel_last_step']=conditional_radius(numerator,denominator,coherent,cold_radius)
        scenarios['independent_last_step']=conditional_radius(numerator,denominator,independent,cold_radius)
        twice=magnitudes.copy()
        twice[[3,4]]+=previous_magnitudes[[3,4]]
        twice_radius=(abs(weights)[None,:,None,None]*twice).sum(axis=(0,1,2))
        scenarios['independent_two_selected_steps']=conditional_radius(numerator,denominator,
            twice_radius,twice[:,0].sum(axis=(0,1)))
        if contraction_available:
            geometric=(abs(weights)[None,:,None,None]*radii).sum(axis=(0,1,2))
            scenarios['selected_geometric_other_last_step']=conditional_radius(numerator,denominator,
                geometric,radii[:,0].sum(axis=(0,1)))
        else:
            scenarios['selected_geometric_other_last_step']=dict(available=False,certified=False,
                reason='At least one observed component ratio is not below one',endpoint_and_other_axis_radius=None)
        observed=[]
        for panel in range(7):
            separate=(abs(weights)[:,None,None]*magnitudes[panel]).sum(axis=(0,1))
            observed.append(dict(panel=panel,bounds=BOUNDARIES[panel:panel+2].tolist(),
                latest_order=8 if panel==3 else 7 if panel==4 else 6,
                matched_step=panel_budget[panel].tolist(),independent_step=separate.tolist(),
                share_of_independent_budget=(separate/independent).tolist()))
        directions=list(joint)+[np.einsum('s,scij->ij',weights,previous[panel]) for panel in [3,4]]
        shapes={str(cutoff):stage156_parent.projected_shape(error,directions,measure.whiten,cutoff,checks,
            route+':nine_observed_panel_steps') for cutoff in SHAPE_CUTOFFS}
        routes[route]=dict(error_fixed_scale=numerator.tolist(),cold_fixed_scale=denominator.tolist(),
            relative_error=(numerator/denominator).tolist(),weights=weights.tolist(),
            independent_allowance_factor_to_cover_error=(numerator/independent).tolist(),
            scenarios=scenarios,ranked_panels=sorted(observed,key=lambda item:max(item['independent_step']),reverse=True),
            remaining_error_shape_outside_observed_steps=shapes,unresolved_axes=unresolved_axes(),
            global_error_bound=None,pure_interpolation_error_identified=False)
        arrays[route+'_prediction']=prediction
        arrays[route+'_error']=error
        arrays[route+'_panel_steps']=joint
    np.savez_compressed(folder/'source-allowance.npz',**arrays)
    return dict(routes=routes,selected_observed_ratio_caps=ratios.tolist(),
        geometric_scenario_available=contraction_available,all_radii_conditional=True,
        adopted_temperature_curve_changed=False,new_physical_events=0,
        mixed_incoming_orders=[6,6,6,8,7,6,6],endpoint_and_other_axis_radii_certified=False)


def response_analysis(registry,checks,folder):
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    for path in ladder.inputs:
        registry.add(path)
    reader=ShapeReadout(ladder.basis,canonical=True)
    records={}
    precision_max=svd_max=0.
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            steps={}
            for count in COUNTS:
                label=f'{model}-{route}-{count}'
                original=registry.read(response_path(STAGE150,model,route,count))
                order6=registry.read(response_path(SOURCE155,model,route,count))
                first=registry.read(response_path(SOURCE158,model,route,count))
                last=registry.read(response_path(PARENT,model,route,count))
                old_metrics=registry.read(SOURCE156/'results/analysis'/(label+'-history.npz'))
                status_path=response_path(PARENT,model,route,count).parent/'status.json'
                registry.add(status_path)
                heat=json.loads(status_path.read_text())['heat']
                assert np.array_equal(first['coordinate'],last['coordinate'])
                assert np.array_equal(original['coordinate'],last['coordinate'])
                assert np.array_equal(order6['coordinate'],last['coordinate'])
                gap={}
                parts={}
                for quantity in QUANTITIES:
                    gap[quantity]=order6[quantity][...,2:4]-original[quantity][...,:2]+first[quantity][...,2:4]+last[quantity][...,2:4]
                    parts[quantity]=[last[quantity][...,start:start+2] for start in [12,14,16]]+[first[quantity][...,start:start+2] for start in [18,20,22]]
                    close(checks,'Targeted response sum:'+label+':'+quantity,sum(parts[quantity]),
                        last[quantity][...,2:4]+first[quantity][...,4:6],1e-8)
                balance=gap['energy']+heat*gap['gas']+gap['work']
                scale=np.maximum((abs(gap['energy'])+abs(heat*gap['gas'])+abs(gap['work'])).max(axis=0),1e-300)
                test(checks,'Updated original-P4 gap energy/work:'+label,float(max(abs(balance-balance[0]).max(axis=0)/scale)),1e-7)
                state={}
                arrays={}
                for quantity in ['photon','gas']:
                    measure=lambda value:state_norm(value,ladder.basis.mass) if quantity=='photon' else abs(value)
                    old_gap=order6[quantity][...,2:4]-original[quantity][...,:2]
                    close(checks,'Independent Stage156 gap replay:'+label+':'+quantity,measure(old_gap),old_metrics[quantity+'_gap'],1e-8)
                    gap_norm=measure(gap[quantity])
                    target_budget=sum(measure(value) for value in parts[quantity])
                    overlap_budget=old_metrics[quantity+'_last_budget']+target_budget
                    reference=old_metrics[quantity+'_reference']
                    endpoint_scale=reference[-1] if quantity=='photon' else reference.max(axis=0)
                    state[quantity]=dict(gap_endpoint_over_saved_reference=(gap_norm[-1]/endpoint_scale).tolist(),
                        targeted_step_budget_endpoint=(target_budget[-1]/endpoint_scale).tolist(),
                        overlapping_full65_plus_targeted_budget_endpoint=(overlap_budget[-1]/endpoint_scale).tolist(),
                        gap_over_overlapping_budget_endpoint=(gap_norm[-1]/np.maximum(overlap_budget[-1],1e-300)).tolist(),
                        future_error_radius_certified=False)
                    arrays[quantity+'_gap_norm']=gap_norm
                    arrays[quantity+'_target_budget']=target_budget
                    arrays[quantity+'_overlap_budget']=overlap_budget
                np.savez_compressed(folder/(label+'-history.npz'),coordinate=last['coordinate'],**arrays)
                steps[count]={quantity:gap[quantity] for quantity in ['photon','gas']}
                readouts={}
                for match in [20,40]:
                    name=label+f'-m{match}'
                    old=registry.read(SOURCE156/'results/analysis'/(name+'-readout.npz'))
                    current=registry.read(PARENT/'results/comparison'/(name+'.npz'))
                    baseline=current['potential'][:,:1]
                    frozen=old['potential'][:,1:3]
                    resolved=current['potential'][:,3:5]
                    assert np.array_equal(baseline,old['potential'][:,:1])
                    assert np.array_equal(current['amplitudes'][:,:1],old['amplitudes'][:,:1])
                    increment=reader.values@(first['photon'][-1,:,2:4]+last['photon'][-1,:,2:4])
                    gap_values=old['potential'][:,9:11]+increment
                    gap_energy=old['energy'][9:11]+first['energy'][-1,2:4]+last['energy'][-1,2:4]
                    projected_parts=[reader.values@value[-1] for value in parts['photon']]
                    potential=np.column_stack([baseline,frozen,resolved,baseline+frozen,baseline+resolved,gap_values,*projected_parts])
                    energy=np.r_[current['energy'][:1],old['energy'][1:3],current['energy'][3:5],
                        current['energy'][:1]+old['energy'][1:3],current['energy'][:1]+current['energy'][3:5],
                        gap_energy,*[value[-1] for value in parts['energy']]]
                    split=reader.split_values(potential,energy)
                    inherited.invariants(checks,reader,split,name)
                    close(checks,'Latest saved readout minus frozen predictor:'+name,resolved-frozen,gap_values,1e-8)
                    assert np.array_equal(split['amplitudes'][:,:1],current['amplitudes'][:,:1])
                    close(checks,'Saved MTS shape amplitude replay:'+name,split['amplitudes'][:,3:5],current['amplitudes'][:,3:5],1e-10)
                    precise=precise_readout(dict(potential=potential,energy=energy),reader)
                    precision_max=max(precision_max,precise['same_baseline_cancellation'])
                    test(checks,'60digit paired baseline:'+name,precise['same_baseline_cancellation'],1e-8)
                    close(checks,'60digit gap shapes:'+name,precise['amplitudes'][:,3:5],split['amplitudes'][:,9:11],1e-8)
                    close(checks,'60digit gap residual:'+name,precise['residual'][:,3:5],split['residual'][:,9:11],1e-10)
                    alternate=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                        np.sqrt(reader.measure)[:,None]*split['distortion'],rcond=None)[0]
                    numerator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*(reader.templates@(alternate-split['amplitudes'])),axis=0)
                    denominator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*split['distortion'],axis=0)
                    svd_max=max(svd_max,float(max(numerator/np.maximum(denominator,1e-300))))
                    rows={}
                    for position,quantity in enumerate(['mu','y','residual_norm']):
                        observed=abs(split['amplitudes'][position]) if position<2 else split['residual_norm']
                        earlier=abs(old['amplitudes'][position]) if position<2 else old['residual_norm']
                        targeted=sum(observed[start:start+2] for start in range(11,23,2))
                        older=sum(earlier[start:start+2] for start in range(11,29,2))
                        total_budget=targeted+older
                        rows[quantity]=dict(gap_over_overlapping_budget=(observed[9:11]/np.maximum(total_budget,1e-300)).tolist(),
                            targeted_budget_over_gap=(targeted/np.maximum(observed[9:11],1e-300)).tolist(),
                            future_error_radius_certified=False)
                    readouts[str(match)]=rows
                    np.savez_compressed(folder/(name+'-readout.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=heat)
                records[label]=dict(state=state,readouts=readouts,baseline_preserved=True,
                    response_scope='Gap to ORIGINAL P4,not isolated latest pointwise cubic-defect evolution',
                    overlap_budget_scope='Old full-order65 component budget plus latest targeted site steps;overlaps refined bands',
                    new_response_evolutions=0)
                print(json.dumps(dict(saved_response_checked=label)),flush=True)
            step_metrics={}
            for quantity in ['photon','gas']:
                measure=lambda value:state_norm(value,ladder.basis.mass) if quantity=='photon' else abs(value)
                coarse,fine=steps[2048][quantity],steps[4096][quantity]
                ratio=measure(fine[::2]-coarse).max(axis=0)/measure(fine).max(axis=0)
                step_metrics[quantity]=ratio.tolist()
                test(checks,'CONVERGENCE:originalP4 gap:'+model+':'+route+':'+quantity,float(max(ratio)),.01)
            records[model+'-'+route+'-steps']=step_metrics
    test(checks,'Independent weighted SVD',svd_max,1e-10)
    return dict(records=records,maximum_precision_cancellation=precision_max,maximum_independent_svd=svd_max,
        baseline_inner_rerun=False,new_response_evolutions=0,pure_latest_defect_response_available=False,
        unresolved_response_radius=None)


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    if args.dry_run:
        paths=[PARENT/'results/sources/source.npz',SOURCE157/'results/analysis/order6-frequency.npz',
            SOURCE156/'results/analysis/heavy-cubic-4096-history.npz']
        assert all(path.is_file() for path in paths)
        print(json.dumps(dict(new_events=0,new_responses=0,saved_event_records_to_reconstruct=8316,
            temperature_curve_changed=False,outputs_written=False)))
        return
    folder=ROOT/'results/analysis'
    folder.mkdir(parents=True,exist_ok=False)
    registry=Registry()
    for filename in registry.chain[PARENT/'results/stage-integrity.json']['file_hashes']:
        registry.add(PARENT/filename)
    checks=[dict(name='All immediate Stage159 payloads verified',passed=True)]
    data=registry.read(PARENT/'results/sources/source.npz')
    banks,event_count=reconstruct(data,registry,checks,folder)
    source=source_analysis(data,banks,checks,folder)
    response=response_analysis(registry,checks,folder)
    numerical=all(row['passed'] for row in checks if not row['name'].startswith('CONVERGENCE:'))
    summary=dict(stage=160,source=source,response=response,numerical_integrity_passed=numerical,
        convergence_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:')),
        temperature_curve_changed=False,new_physical_events=0,new_response_evolutions=0,
        reused_order5_6_event_records=event_count,numerical_remainder_certified=False,
        next_target='Use the ranked independent panel budget to select the smallest missing accuracy test or physical temperature-law derivation;do not refit the temperature curve or equate the saved original-P4 response gap with the isolated updated pointwise defect.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    finish(folder,dict(checks=checks,numerical_integrity_passed=numerical,consumed_prior_hashes=registry.hashes,
        rehashed_prior_files=len(registry.hashes),new_events=0,new_trajectories=0,
        reused_event_records=event_count,temperature_curve_changed=False),__file__,
        [*map(Path,registry.hashes),*folder.glob('*.npz'),ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(checks=len(checks),numerical=numerical,
        failed=[row for row in checks if not row['passed']],prior_files=len(registry.hashes))),flush=True)
    assert numerical


if __name__=='__main__':
    main()
