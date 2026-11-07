from stage156_common import *
import argparse


def source_analysis(data,checks,folder):
    factor=np.linalg.cholesky(data['mass'])
    whiten=lambda value:np.linalg.solve(factor,value[1:-1])
    norm=lambda value:np.linalg.norm(whiten(value),axis=0)
    scale=norm(data['actual'])
    current=norm(data['source6'])/scale
    increments={}
    for order in [5,6]:
        increments[order]={'cold':[data[f'delta{order}_'+key] for key in COMPONENTS]}
        for anchor in ANCHORS:
            prefix=anchor+('_delta_' if order==5 else '_delta6_')
            increments[order][anchor]=[data[prefix+key] for key in COMPONENTS]
    ladder={}
    tails={}
    for site in ['cold','warm','centre']:
        previous=np.asarray([norm(value) for value in increments[5][site]])/scale
        latest=np.asarray([norm(value) for value in increments[6][site]])/scale
        ratio=latest/np.maximum(previous,1e-300)
        bounded=bool(np.all(ratio<1))
        tail=latest*ratio/(1-ratio) if bounded else None
        tails[site]=tail
        ladder[site]=dict(previous=previous.tolist(),latest=latest.tolist(),ratios=ratio.tolist(),
            geometric_tail=None if tail is None else tail.tolist(),
            uniform_future_contraction_proven=False,scenario_available=bounded)
    saved=dict(mass=data['mass'],scale=scale,cold_norm=current,cold_source6=data['source6'])
    records={}
    for route in ['local','cubic']:
        weights={'cold':1.,'warm':-predictor_basis(.75,route,'warm'),
            'centre':-predictor_basis(.75,route,'centre')}
        predictions={4:data['prediction_'+route],5:data[route+'_diagnostic_prediction'],
            6:data[route+'_diagnostic_prediction6']}
        errors={order:data['actual' if order==4 else 'source'+str(order)]-predictions[order] for order in [4,5,6]}
        changes={order:sum(weights[site]*sum(increments[order][site]) for site in weights) for order in [5,6]}
        close(checks,'Matched54 source identity:'+route,errors[5]-errors[4],changes[5],1e-10)
        close(checks,'Matched65 source identity:'+route,errors[6]-errors[5],changes[6],1e-10)
        close(checks,'Complete matched telescope:'+route,errors[4]+changes[5]+changes[6],errors[6],1e-11)
        if route=='cubic':
            for order in [4,5,6]:
                predicted=data['start']/4-data['warm_source'+str(order)]+1.5*data['centre_source'+str(order)]+data['end']/4
                close(checks,'Independent matched cubic anchors:'+str(order),predicted,predictions[order],1e-12)
        budgets={order:sum(abs(weights[site])*sum(norm(part) for part in increments[order][site]) for site in weights)/scale for order in [5,6]}
        error_norm=norm(errors[6])/scale
        coherent={order:norm(changes[order])/scale for order in [5,6]}
        ratio=coherent[6]/np.maximum(coherent[5],1e-300)
        def cosine(first,second):
            return np.sum(whiten(first)*whiten(second),axis=0)/np.maximum(norm(first)*norm(second),1e-300)
        per_order={}
        for order in [4,5,6]:
            source=data['actual' if order==4 else 'source'+str(order)]
            relative=norm(errors[order])/norm(source)
            per_order[str(order)]=dict(fixed_scale=(norm(errors[order])/scale).tolist(),own_source=relative.tolist())
            for column,label in enumerate(COLUMN_NAMES):
                test(checks,'MATCHED_FORECAST:'+route+':'+str(order)+':'+label,float(relative[column]),THRESHOLD)
        last_cold=sum(norm(part) for part in increments[6]['cold'])/scale
        previous_cold=sum(norm(part) for part in increments[5]['cold'])/scale
        scenarios={}
        for name,cold_radius,error_radius in [('observed_last_step_as_radius',last_cold,budgets[6]),
                ('observed_two_steps_as_radius',last_cold+previous_cold,budgets[5]+budgets[6])]:
            scenarios[name]=dict(cold_radius=cold_radius.tolist(),tested_error_radius=error_radius.tolist(),
                **conditional_bound(error_norm,current,cold_radius,error_radius),
                assumption='Unknown post6 remainder is bounded by this observed-step budget;not established.')
        ranked=[]
        if all(value is not None for value in tails.values()):
            cold_radius=tails['cold'].sum(axis=0)
            error_radius=sum(abs(weights[site])*tails[site].sum(axis=0) for site in weights)
            scenarios['independent_component_geometric']=dict(cold_radius=cold_radius.tolist(),
                tested_error_radius=error_radius.tolist(),**conditional_bound(error_norm,current,cold_radius,error_radius),
                assumption='Each observed component ratio bounds every future increment at that site;endpoint and other-axis errors excluded.')
            for site in weights:
                for position,key in enumerate(COMPONENTS):
                    amount=abs(weights[site])*tails[site][position]
                    ranked.append(dict(site=site,component=key,radius_over_coldS4=amount.tolist(),
                        share_of_tested_radius=(amount/error_radius).tolist()))
            if np.all(ratio<1):
                coherent_tail=coherent[6]*ratio/(1-ratio)
                scenarios['coherent_matched_geometric']=dict(cold_radius=cold_radius.tolist(),
                    tested_error_radius=coherent_tail.tolist(),**conditional_bound(error_norm,current,cold_radius,coherent_tail),
                    assumption='Matched dE contraction persists uniformly in future,including anchor correlations;separate cold component tail assumed for denominator;endpoints/other axes excluded.')
        directions=[weights[site]*value for order in [5,6] for site in weights for value in increments[order][site]]
        shapes={}
        for name,values in [('two_coherent_steps',[changes[5],changes[6]]),('all_component_steps',directions)]:
            shapes[name]={str(cutoff):projected_shape(errors[6],values,whiten,cutoff,checks,route+':'+name) for cutoff in SHAPE_CUTOFFS}
        records[route]=dict(matched_errors=per_order,weights=weights,
            observed_component_budgets={str(order):value.tolist() for order,value in budgets.items()},
            coherent_step_norms={str(order):value.tolist() for order,value in coherent.items()},
            observed_coherent_ratio=ratio.tolist(),
            latest_step_cosine_with_error=cosine(changes[6],errors[6]).tolist(),
            consecutive_step_cosine=cosine(changes[5],changes[6]).tolist(),
            scenarios=scenarios,ranked_independent_tail_components=sorted(ranked,key=lambda item:max(item['radius_over_coldS4']),reverse=True),
            shape_projections=shapes,endpoint_and_other_axis_radius=None,
            pure_interpolation_error_identified=False)
        for order in [4,5,6]:
            saved[f'{route}_error{order}']=errors[order]
        for order in [5,6]:
            saved[f'{route}_change{order}']=changes[order]
    for order in [5,6]:
        for site in increments[order]:
            for key,value in zip(COMPONENTS,increments[order][site]):
                saved[f'{site}_{key}_{order}']=value
    np.savez_compressed(folder/'source-separation.npz',**saved)
    return dict(scale='same cold order4 mass-dual source norm',cold_source6_norm=current.tolist(),
        incoming_component_ladders=ladder,routes=records)


def response_analysis(checks,folder,inputs):
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    inputs.extend(ladder.inputs)
    reader=ShapeReadout(ladder.basis,canonical=True)
    records={}
    maximum_precision=maximum_svd=0.
    quantities=['photon','gas','energy','work','number','integrated_number_source']
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            steps={}
            for count in COUNTS:
                packets=[read_npz(location(stage,model,route,count)/'response.npz')
                    for stage in [STAGE150,STAGE151,SOURCE152,SOURCE154,PARENT]]
                original,cold5,cold6,anchor5,anchor6=packets
                metadata=verify_packet(location(PARENT,model,route,count))
                heat=metadata['heat']
                for packet in packets[1:]:
                    assert np.array_equal(original['coordinate'],packet['coordinate'])
                total,initial,latest,previous={},{},{},{}
                component_last,component_previous={},{}
                for quantity in quantities:
                    initial[quantity]=original[quantity][...,4:6]
                    previous[quantity]=cold5[quantity][...,4:6]+anchor5[quantity][...,4:6]
                    latest[quantity]=cold6[quantity][...,4:6]+anchor6[quantity][...,4:6]
                    total[quantity]=initial[quantity]+previous[quantity]+latest[quantity]
                    direct=anchor6[quantity][...,2:4]-original[quantity][...,0:2]
                    close(checks,'Matched trajectory telescope:'+model+':'+route+':'+str(count)+':'+quantity,direct,total[quantity],1e-8)
                    component_last[quantity]=[cold6[quantity][...,start:start+2] for start in range(12,18,2)]+[anchor6[quantity][...,start:start+2] for start in range(12,24,2)]
                    component_previous[quantity]=[cold5[quantity][...,start:start+2] for start in range(12,18,2)]+[anchor5[quantity][...,start:start+2] for start in range(12,24,2)]
                    close(checks,'Nine latest component sum:'+model+':'+route+':'+str(count)+':'+quantity,sum(component_last[quantity]),latest[quantity],1e-8)
                    close(checks,'Nine previous component sum:'+model+':'+route+':'+str(count)+':'+quantity,sum(component_previous[quantity]),previous[quantity],1e-8)
                    assert not np.any(anchor6[quantity][...,6:8])
                    assert np.array_equal(original[quantity][...,8:10],anchor6[quantity][...,8:10])
                balance=total['energy']+heat*total['gas']+total['work']
                denominator=np.maximum(np.max(abs(total['energy'])+abs(heat*total['gas'])+abs(total['work']),axis=0),1e-300)
                test(checks,'Reconstructed trajectory energy/work:'+model+':'+route+':'+str(count),
                    float(np.max(abs(balance-balance[0])/denominator)),1e-7)
                budgets={}
                norms={}
                for quantity in ['photon','gas']:
                    measure=lambda values:state_norm(values,ladder.basis.mass) if quantity=='photon' else abs(values)
                    reference=measure(original[quantity][...,10:12])
                    observed=measure(total[quantity])
                    last_budget=sum(measure(value) for value in component_last[quantity])
                    old_budget=sum(measure(value) for value in component_previous[quantity])
                    endpoint=reference[-1] if quantity=='photon' else reference.max(axis=0)
                    peak=reference.max(axis=0)
                    budgets[quantity]=dict(original_prediction_gap_endpoint=(observed[-1]/endpoint).tolist(),
                        original_prediction_gap_history=(observed.max(axis=0)/peak).tolist(),
                        latest_component_budget_endpoint=(last_budget[-1]/endpoint).tolist(),
                        latest_component_budget_history=(last_budget.max(axis=0)/peak).tolist(),
                        last_two_component_budgets_endpoint=((old_budget[-1]+last_budget[-1])/endpoint).tolist(),
                        latest_coherent_change_endpoint=(measure(latest[quantity])[-1]/endpoint).tolist(),
                        conditional_last_radius_lower_endpoint=(np.maximum(observed[-1]-last_budget[-1],0)/endpoint).tolist(),
                        denominator='original accumulated coldS4 response;history/gas use peak',
                        conditional_radius_certified=False)
                    norms[quantity+'_gap']=observed
                    norms[quantity+'_last_budget']=last_budget
                    norms[quantity+'_previous_budget']=old_budget
                    norms[quantity+'_reference']=reference
                label=f'{model}-{route}-{count}'
                np.savez_compressed(folder/(label+'-history.npz'),coordinate=original['coordinate'],**norms)
                steps[count]={quantity:total[quantity] for quantity in ['photon','gas']}
                readouts={}
                for match in [20,40]:
                    old=read_npz(STAGE150/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz')
                    last=read_npz(PARENT/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz')
                    assert np.array_equal(old['potential'][:,:3],last['potential'][:,:3])
                    assert np.array_equal(old['amplitudes'][:,:1],last['amplitudes'][:,:1])
                    baseline=old['potential'][:,:1]
                    frozen=old['potential'][:,7:9]
                    resolved=last['potential'][:,9:11]
                    gap=reader.values@total['photon'][-1]
                    parts=[reader.values@value[-1] for value in component_last['photon']]
                    potential=np.column_stack([baseline,frozen,resolved,baseline+frozen,baseline+resolved,gap,*parts])
                    energy=np.r_[old['energy'][:1],old['energy'][7:9],last['energy'][9:11],
                        old['energy'][:1]+old['energy'][7:9],old['energy'][:1]+last['energy'][9:11],
                        total['energy'][-1],*[value[-1] for value in component_last['energy']]]
                    split=reader.split_values(potential,energy)
                    name=label+'-m'+str(match)
                    inherited.invariants(checks,reader,split,name)
                    close(checks,'Independent frozen-to-resolved small spectrum:'+name,resolved-frozen,gap,1e-8)
                    assert np.array_equal(split['amplitudes'][:,:1],old['amplitudes'][:,:1])
                    precise=precise_readout(dict(potential=potential,energy=energy),reader)
                    maximum_precision=max(maximum_precision,precise['same_baseline_cancellation'])
                    test(checks,'60digit matched baseline/MTS cancellation:'+name,precise['same_baseline_cancellation'],1e-8)
                    close(checks,'60digit direct gap amplitudes:'+name,precise['amplitudes'][:,3:5],split['amplitudes'][:,9:11],1e-8)
                    close(checks,'60digit same baseline amplitudes:'+name,precise['amplitudes'][:,:1],split['amplitudes'][:,:1],1e-10)
                    close(checks,'60digit direct gap residual:'+name,precise['residual'][:,3:5],split['residual'][:,9:11],1e-10)
                    alternate=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                        np.sqrt(reader.measure)[:,None]*split['distortion'],rcond=None)[0]
                    difference=reader.templates@(alternate-split['amplitudes'])
                    numerator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*difference,axis=0)
                    denominator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*split['distortion'],axis=0)
                    maximum_svd=max(maximum_svd,float(max(numerator/np.maximum(denominator,1e-300))))
                    rows={}
                    for position,quantity in enumerate(['mu','y']):
                        amplitudes=heat*split['amplitudes'][position]
                        denominator=abs(heat*old['amplitudes'][position,9:11])
                        gap_magnitude=abs(amplitudes[9:11])
                        budget=sum(abs(amplitudes[start:start+2]) for start in range(11,29,2))
                        rows[quantity]=dict(gap_over_S4=(gap_magnitude/denominator).tolist(),
                            latest_budget_over_S4=(budget/denominator).tolist(),
                            gap_over_last_budget=(gap_magnitude/np.maximum(budget,1e-300)).tolist(),
                            conditional_last_radius_lower_over_S4=(np.maximum(gap_magnitude-budget,0)/denominator).tolist())
                    for quantity in ['distortion_norm','residual_norm']:
                        denominator=old[quantity][9:11]
                        gap_magnitude=split[quantity][9:11]
                        budget=sum(split[quantity][start:start+2] for start in range(11,29,2))
                        rows[quantity]=dict(gap_over_S4=(gap_magnitude/denominator).tolist(),
                            latest_budget_over_S4=(budget/denominator).tolist(),
                            gap_over_last_budget=(gap_magnitude/np.maximum(budget,1e-300)).tolist(),
                            conditional_last_radius_lower_over_S4=(np.maximum(gap_magnitude-budget,0)/denominator).tolist())
                    np.savez_compressed(folder/(name+'-readout.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=heat)
                    readouts[str(match)]=rows
                records[label]=dict(state=budgets,readouts=readouts,
                    response_scope='Saved R6(W6,C6,H6) minus ORIGINAL P4;not separately the updated cold-point cubic-defect response',
                    updated_pure_cubic_defect_response_available=False)
                print(json.dumps(dict(response_reused=label)),flush=True)
            step_checks={}
            for quantity in ['photon','gas']:
                coarse,fine=steps[2048][quantity],steps[4096][quantity]
                measure=lambda values:state_norm(values,ladder.basis.mass) if quantity=='photon' else abs(values)
                change=measure(fine[::2]-coarse).max(axis=0)/measure(fine).max(axis=0)
                step_checks[quantity]=change.tolist()
                test(checks,'CONVERGENCE:matched trajectory gap:'+model+':'+route+':'+quantity,float(max(change)),.01)
            records[model+'-'+route+'-steps']=step_checks
    test(checks,'Independent weightedSVD',maximum_svd,1e-10)
    return dict(records=records,maximum_precision_cancellation=maximum_precision,
        maximum_independent_svd=maximum_svd,baseline_reused=True,baseline_inner_rerun=False,
        new_response_evolutions=0,updated_defect_response_not_fabricated=True)


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    inputs=planned_inputs()
    assert all(path.is_file() for path in inputs)
    if args.dry_run:
        print(json.dumps(dict(paths=len(inputs),all_exist=True,new_physical_events=0,new_trajectories=0,outputs_written=False)))
        return
    folder=ROOT/'results/analysis'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    for filename,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert digest(PARENT/filename)==sha,filename
    for path in inputs:
        inherited.inherited.verify_source(path,chain)
    checks=[dict(name='Immediate Stage155 and consumed source provenance verified',passed=True)]
    data=read_npz(PARENT/'results/anchor-sources/source.npz')
    source=source_analysis(data,checks,folder)
    response=response_analysis(checks,folder,inputs)
    numerical=all(row['passed'] for row in checks if not row['name'].startswith(('MATCHED_FORECAST:','CONVERGENCE:')))
    summary=dict(stage=156,source=source,response=response,numerical_integrity_passed=numerical,
        time_steps_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:')),
        new_physical_events=0,new_response_evolutions=0,temperature_curve_changed=False,
        numerical_remainder_certified=False,endpoint_radii_certified=False,other_axis_radii_certified=False,
        next_target='Use the saved component ranking and correlation dependence to choose a targeted error-control calculation;do not blindly increase all quadrature orders or alter the temperature curve.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    finish(folder,dict(checks=checks,numerical_integrity_passed=numerical,new_events=0,new_trajectories=0,
        baseline_preserved=True,temperature_curve_changed=False),__file__,
        [*inputs,*folder.glob('*.npz'),ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(checks=len(checks),numerical=numerical,failed=[row for row in checks if not row['passed']])),flush=True)
    assert numerical


if __name__=='__main__':
    main()
