from stage153_separation_common import *
import argparse


def source_analysis(data,warm,checks,folder):
    mass=data['mass']
    factor=np.linalg.cholesky(mass)
    def whiten(value):
        return np.linalg.solve(factor,value[1:-1])
    def norm(value):
        return np.linalg.norm(whiten(value),axis=0)
    scale=norm(data['actual'])
    current=norm(data['source6'])/scale
    nodes=[Fraction(0),Fraction(1,4),Fraction(1,2),Fraction(1)]
    target=Fraction(3,4)
    weights=[]
    for position,node in enumerate(nodes):
        weight=Fraction(1)
        for other_position,other in enumerate(nodes):
            if position!=other_position:
                weight*=(target-other)/(node-other)
        weights.append(weight)
    assert weights==[Fraction(1,4),Fraction(-1),Fraction(3,2),Fraction(1,4)]
    for degree in range(4):
        assert sum(weight*node**degree for weight,node in zip(weights,nodes))==target**degree
    checks.append(dict(name='Exact cubic weights and degree0-to3 reproduction',passed=True))
    anchors=[data['start'],warm['actual'],data['centre'],data['end']]
    assert np.array_equal(data['mass'],warm['mass'])
    predicted=sum(float(weight)*anchor for weight,anchor in zip(weights,anchors))
    close(checks,'Frozen cubic equals independent barycentric anchors',predicted,data['prediction_cubic'],1e-12)
    close(checks,'Independent saved warm defect',warm['defect'],data['warm_defect'],1e-12)
    summed65=sum(norm(data['delta6_'+key]) for key in COMPONENTS)/scale
    summed54=sum(norm(data['delta5_'+key]) for key in COMPONENTS)/scale
    summed43=sum(norm(data['delta3_'+key]) for key in COMPONENTS)/scale
    output=dict(denominator='fixed order4 full finite-remainder mass-dual norm',
        source6_norm=current.tolist(),component_sum_65=summed65.tolist(),
        component_sum_54=summed54.tolist(),component_sum_43=summed43.tolist(),
        barycentric_weights=[str(weight) for weight in weights],anchor_norms_over_S4=[(norm(anchor)/scale).tolist() for anchor in anchors],
        anchor_weight_absolute_sum=float(sum(abs(weight) for weight in weights)),routes={})
    saved=dict(mass=mass,scale=scale,source6_norm=current,weights=np.asarray(weights,dtype=float),
        source6=data['source6'],source4=data['actual'],radius65=summed65,radius54=summed54,
        anchors=np.asarray(anchors))
    for route in ['local','cubic']:
        prediction=data['prediction_'+route]
        error6=data['source6']-prediction
        error4=data['actual']-prediction
        incremental=error4+data['delta5_total']+data['delta6_total']
        close(checks,'Source telescoping identity:'+route,incremental,error6,1e-11)
        magnitudes={}
        self_relative={}
        for order,key in [(3,'source3'),(4,'actual'),(5,'source5'),(6,'source6')]:
            defect=data[key]-prediction
            magnitudes[str(order)]=(norm(defect)/scale).tolist()
            self_relative[str(order)]=(norm(defect)/norm(data[key])).tolist()
            for column,label in enumerate(COLUMN_NAMES):
                test(checks,'FROZEN_FORECAST:'+route+':order'+str(order)+':'+label,
                    self_relative[str(order)][column],.01)
        error_norm=norm(error6)/scale
        shift=data['delta6_total']
        cosine=np.sum(whiten(error6)*whiten(shift),axis=0)/(norm(error6)*norm(shift))
        test(checks,'Cauchy bound:'+route,float(max(abs(cosine))),1.+1e-12)
        parallel=np.sum(whiten(error6)*whiten(shift),axis=0)/norm(shift)
        orthogonal=np.sqrt(np.maximum(norm(error6)**2-parallel**2,0.))/scale
        threshold=.01
        center=prediction/(1-threshold**2)
        radius=threshold*norm(prediction)/(1-threshold**2)
        offset=data['source6']-center
        offset_norm=norm(offset)
        displacement=np.maximum(offset_norm-radius,0.)/scale
        nearest=center+offset*(radius/offset_norm)
        close(checks,'Exact nearest1percent boundary:'+route,norm(nearest-prediction)/norm(nearest),
            np.full(4,threshold),1e-9)
        close(checks,'Exact nearest-boundary distance:'+route,norm(nearest-data['source6'])/scale,displacement,1e-10)
        record=dict(error_norm_over_S4=magnitudes,self_relative_error=self_relative,
            latest_shift_cosine=cosine.tolist(),orthogonal_to_latest_shift_over_S4=orthogonal.tolist(),
            observed_last_ball=ball_diagnostics(error_norm,current,summed65),
            two_observed_steps_ball=ball_diagnostics(error_norm,current,summed65+summed54),
            exact_displacement_to1percent_over_S4=displacement.tolist(),
            displacement_over_observed_last_radius=(displacement/summed65).tolist(),
            continuum_interpolation_error_identified=False)
        if route=='cubic':
            remaining=error_norm-summed65-threshold*(current+summed65)
            weighted_anchor_norm=sum(abs(float(weight))*norm(anchor)/scale for weight,anchor in zip(weights,anchors))
            record.update(conditional_weighted_anchor_budget_to_keep_miss=remaining.tolist(),
                conditional_common_anchor_relative_radius_limit=(remaining/weighted_anchor_norm).tolist(),
                conditional_assumptions=['Cold continuum error <= observed b65,not established',
                    'All anchor radii separately controlled in same norm'],
                certified_cold_radius=None,certified_anchor_radii=[None]*4)
        output['routes'][route]=record
        saved['prediction_'+route]=prediction
        saved['error6_'+route]=error6
    np.savez_compressed(folder/'source-separation.npz',**saved)
    return output


def response_analysis(data,checks,folder,inputs):
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    inputs.extend(ladder.inputs)
    reader=ShapeReadout(ladder.basis,canonical=True)
    records={}
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            steps={}
            for count in COUNTS:
                packets=[read_npz(response_location(stage,model,route,count)/'response.npz')
                    for stage in [STAGE150,STAGE151,PARENT]]
                first,middle,last=packets
                metadata=json.loads((response_location(PARENT,model,route,count)/'status.json').read_text())
                heat=metadata['heat']
                assert metadata['all_checks_passed']
                assert np.array_equal(first['coordinate'],middle['coordinate'])
                assert np.array_equal(first['coordinate'],last['coordinate'])
                total={}
                norms={}
                budgets={}
                for quantity in ['photon','gas','energy','work','number','integrated_number_source']:
                    total[quantity]=first[quantity][...,4:6]+middle[quantity][...,4:6]+last[quantity][...,4:6]
                    direct=last[quantity][...,2:4]-first[quantity][...,0:2]
                    close(checks,'Saved frozen-to-order6 telescope:'+model+':'+route+':'+str(count)+':'+quantity,
                        direct,total[quantity],1e-8)
                    assert not np.any(first[quantity][...,6:8])
                    assert not np.any(last[quantity][...,6:8])
                    assert np.array_equal(first[quantity][...,8:10],last[quantity][...,8:10])
                balance=total['energy']+heat*total['gas']+total['work']
                denominator=np.maximum(np.max(abs(total['energy'])+abs(heat*total['gas'])+abs(total['work']),axis=0),1e-300)
                test(checks,'Frozen-defect energy/work:'+model+':'+route+':'+str(count),
                    float(np.max(abs(balance-balance[0])/denominator)),1e-7)
                for quantity in ['photon','gas']:
                    norm=lambda values:state_norm(values,ladder.basis.mass) if quantity=='photon' else abs(values)
                    observed=norm(total[quantity])
                    bound=sum(norm(last[quantity][...,selection]) for selection in [slice(12,14),slice(14,16),slice(16,18)])
                    reference=norm(first[quantity][...,10:12])
                    endpoint_scale=reference[-1] if quantity=='photon' else reference.max(axis=0)
                    peak_scale=reference.max(axis=0)
                    assert np.all(endpoint_scale>0) and np.all(peak_scale>0)
                    norms[quantity+'_defect']=observed
                    norms[quantity+'_step65']=bound
                    norms[quantity+'_reference']=reference
                    budgets[quantity]=dict(defect_endpoint_over_S4=(observed[-1]/endpoint_scale).tolist(),
                        last_budget_endpoint_over_S4=(bound[-1]/endpoint_scale).tolist(),
                        defect_history_over_S4_peak=(observed.max(axis=0)/peak_scale).tolist(),
                        last_budget_history_over_S4_peak=(bound.max(axis=0)/peak_scale).tolist(),
                        conditional_endpoint_lower_over_S4=(np.maximum(observed[-1]-bound[-1],0)/endpoint_scale).tolist(),
                        conditional_history_lower_over_S4_peak=(np.maximum(observed-bound,0).max(axis=0)/peak_scale).tolist(),
                        endpoint_defect_over_last_step=(observed[-1]/bound[-1]).tolist())
                steps[count]=dict(photon=total['photon'],gas=total['gas'])
                np.savez_compressed(folder/f'{model}-{route}-{count}-history-norms.npz',
                    coordinate=first['coordinate'],**norms)
                readouts={}
                for match in [20,40]:
                    old=read_npz(comparison_path(STAGE150,model,route,count,match))
                    latest=read_npz(comparison_path(PARENT,model,route,count,match))
                    assert np.array_equal(old['frequency'],reader.frequency)
                    assert np.array_equal(old['measure'],reader.measure)
                    assert np.array_equal(old['potential'][:,:3],latest['potential'][:,:3])
                    baseline=old['potential'][:,:1]
                    frozen=old['potential'][:,7:9]
                    revised=latest['potential'][:,9:11]
                    defect=reader.values@total['photon'][-1]
                    components=[reader.values@last['photon'][-1,:,selection] for selection in [slice(12,14),slice(14,16),slice(16,18)]]
                    potential=np.column_stack([baseline,frozen,revised,baseline+frozen,baseline+revised,defect,*components])
                    energy=np.r_[old['energy'][:1],old['energy'][7:9],latest['energy'][9:11],
                        old['energy'][:1]+old['energy'][7:9],old['energy'][:1]+latest['energy'][9:11],
                        total['energy'][-1],*[last['energy'][-1,selection] for selection in [slice(12,14),slice(14,16),slice(16,18)]]]
                    split=reader.split_values(potential,energy)
                    label=f'{model}-{route}-{count}-m{match}'
                    inherited.invariants(checks,reader,split,label)
                    assert np.array_equal(split['potential'][:,:1],old['potential'][:,:1])
                    assert np.array_equal(split['amplitudes'][:,:1],old['amplitudes'][:,:1])
                    close(checks,'Frozen MTS replay:'+label,split['amplitudes'][:,1:3],old['amplitudes'][:,7:9],1e-10)
                    close(checks,'Order6 MTS replay:'+label,split['amplitudes'][:,3:5],latest['amplitudes'][:,9:11],1e-10)
                    for key in ['potential','distortion','residual','amplitudes']:
                        close(checks,'Same baseline cancellation:'+key+':'+label,
                            split[key][:,7:9]-split[key][:,5:7],split[key][:,9:11],1e-8)
                    rows={}
                    for position,name in enumerate(['mu','y']):
                        physical=heat*split['amplitudes'][position]
                        reference=abs(heat*old['amplitudes'][position,9:11])
                        miss=abs(physical[9:11])
                        budget=sum(abs(physical[selection]) for selection in [slice(11,13),slice(13,15),slice(15,17)])
                        rows[name]=dict(signed_frozen_defect=physical[9:11].tolist(),
                            defect_over_S4=(miss/reference).tolist(),last_budget_over_S4=(budget/reference).tolist(),
                            defect_over_last_step=(miss/budget).tolist(),
                            conditional_lower_over_S4=(np.maximum(miss-budget,0)/reference).tolist())
                    for name in ['distortion_norm','residual_norm']:
                        reference=old[name][9:11]
                        miss=split[name][9:11]
                        budget=sum(split[name][selection] for selection in [slice(11,13),slice(13,15),slice(15,17)])
                        rows[name]=dict(defect_over_S4=(miss/reference).tolist(),
                            last_budget_over_S4=(budget/reference).tolist(),
                            defect_over_last_step=(miss/budget).tolist(),
                            conditional_lower_over_S4=(np.maximum(miss-budget,0)/reference).tolist())
                    readouts[str(match)]=rows
                    np.savez_compressed(folder/(label+'-readout.npz'),**split,
                        frequency=reader.frequency,measure=reader.measure,heat=heat)
                records[f'{model}-{route}-{count}']=dict(state=budgets,readouts=readouts)
            step_record={}
            for quantity in ['photon','gas']:
                coarse=steps[2048][quantity]
                fine=steps[4096][quantity]
                difference=fine[::2]-coarse
                norm=lambda values:state_norm(values,ladder.basis.mass) if quantity=='photon' else abs(values)
                relative=norm(difference).max(axis=0)/norm(fine).max(axis=0)
                step_record[quantity]=relative.tolist()
                test(checks,'CONVERGENCE:reconstructed defect:'+model+':'+route+':'+quantity,float(max(relative)),.01)
            records[f'{model}-{route}-steps']=step_record
    return records


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
    checks=[dict(name='Stage152 immediate payloads and all consumed prior paths verified',passed=True)]
    data=read_npz(PARENT/'results/integration-source/source.npz')
    warm=read_npz(STAGE149/'results/holdout-source/source.npz')
    source=source_analysis(data,warm,checks,folder)
    source_report=json.loads((PARENT/'results/integration-source/status.json').read_text())
    close(checks,'Reuse Stage152 source norm budget',source['component_sum_65'],
        source_report['metrics']['6']['source_component_sum'],1e-10)
    responses=response_analysis(data,checks,folder,inputs)
    numerical=all(row['passed'] for row in checks if not row['name'].startswith(('FROZEN_FORECAST:','CONVERGENCE:')))
    summary=dict(stage=153,source=source,responses=responses,
        numerical_integrity_passed=numerical,
        response_steps_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:')),
        forecast_failures_retained=[row['name'] for row in checks if row['name'].startswith('FROZEN_FORECAST:') and not row['passed']],
        new_physical_events=0,new_response_evolutions=0,temperature_curve_changed=False,
        baseline_preserved=True,baseline_inner_history_refined=False,
        incoming_continuum_error_certified=False,predictor_anchor_errors_certified=False,
        next_target='Audit the saved integration evidence for the four cubic predictor anchors, especially the centre(weight1.5) and warm quarter(weight-1); use their weighted budgets to choose the smallest targeted refinement before changing the temperature curve.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    outputs=list(folder.glob('*.npz'))
    finish(folder,dict(checks=checks,numerical_integrity_passed=numerical,
        source_component_sum_gate_unchanged=.01,baseline_preserved=True,temperature_curve_changed=False,
        new_events=0,new_trajectories=0),__file__,[*inputs,*outputs,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
        cubic=source['routes']['cubic'],numerical=numerical)),flush=True)
    assert numerical


if __name__=='__main__':
    main()
