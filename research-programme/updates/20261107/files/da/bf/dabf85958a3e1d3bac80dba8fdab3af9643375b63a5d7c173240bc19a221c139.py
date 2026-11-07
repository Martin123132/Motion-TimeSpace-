from complete_history_common import *
from evaluate_source_probes import sources,response_metrics
from propagate_matched_feedback import solve_response
from propagate_repaired_feedback import readout
import argparse
import time


def expand_source(previous,coordinate):
    result={}
    positions=np.searchsorted(coordinate,previous['coordinate'])
    for key,value in previous.items():
        if value.ndim>0 and value.shape[0]==len(previous['coordinate']):
            result[key]=interpolate.interp1d(previous['coordinate'],value,axis=0,bounds_error=True)(coordinate)
            result[key][positions]=value
        else:
            result[key]=value.copy()
    result['coordinate']=coordinate.copy()
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--upper',type=float,choices=[.02,.04],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'feedback-{args.model}-m{int(args.upper*1000)}'
    folder.mkdir(parents=True,exist_ok=False)
    replay_path=ROOT/'results'/f'evolution-{args.model}-carry/prediction.npz'
    prefix_path=P132/'results'/f'replay-{args.model}-cubic/prediction.npz'
    middle_path=P133/'results'/f'evolution-{args.model}-carry/prediction.npz'
    extended_path=P134/'results'/f'evolution-{args.model}-carry/prediction.npz'
    quarter_path=P135/'results'/f'evolution-{args.model}-carry/prediction.npz'
    recent_path=P136/'results'/f'evolution-{args.model}-carry/prediction.npz'
    half_path=P137/'results'/f'evolution-{args.model}-carry/prediction.npz'
    beyond_path=P138/'results'/f'evolution-{args.model}-carry/prediction.npz'
    three_quarter_path=P139/'results'/f'evolution-{args.model}-carry/prediction.npz'
    seven_eighths_path=PARENT/'results'/f'evolution-{args.model}-carry/prediction.npz'
    replay,prefix,middle,extended,quarter,recent,half,beyond,three_quarter,seven_eighths=map(read_npz,
        [replay_path,prefix_path,middle_path,extended_path,quarter_path,recent_path,half_path,beyond_path,three_quarter_path,seven_eighths_path])
    for block in [middle,extended,quarter,recent,half,beyond,three_quarter,seven_eighths]:
        assert np.array_equal(prefix['frequency'],block['frequency'])
        for key in ['coordinate','slope','outer_slope','defect','lower_target','profiles','gas']:
            assert np.array_equal(prefix[key][-1],block[key][0]),key
            prefix[key]=np.concatenate([prefix[key],block[key][1:]])
    assert local_packet(replay_path.parent)['all_checks_passed']
    for key in ['frequency']:
        assert np.array_equal(replay[key],prefix[key])
    for key in ['defect','slope','outer_slope','lower_target']:
        assert np.array_equal(replay[key][0],prefix[key][-1])
    inner_path=refined_owner(args.model)/'results'/f'inner-{args.model}-n40960/prediction.npz'
    cache_path=refined_owner(args.model)/'results'/f'feedback-m{int(args.upper*1000)}-n40960/source-cache.npz'
    inner,cache=map(read_npz,[inner_path,cache_path])
    prediction=dict(inner)
    for key in ['coordinate','defect','profiles','gas','slope','outer_slope','lower_target']:
        prediction[key]=np.concatenate([prefix[key],replay[key][1:]])
    previous_sites=FIRST_STEP//20+1
    total_sites=LAST_STEP//20+1
    assert len(prefix['coordinate'])==previous_sites
    assert len(prediction['coordinate'])==total_sites
    assert total_sites==2049
    endpoint=dict(frequency=prediction['frequency'],
        **{key:prediction[key][-1:].copy() for key in ['coordinate','defect','profiles','gas','slope','outer_slope','lower_target']})
    for key in ['coordinate','defect','profiles','gas','slope','outer_slope','lower_target']:
        assert np.array_equal(endpoint[key][0],replay[key][-1]),key
    np.savez_compressed(folder/'corrected-readout-state.npz',**endpoint)
    operator_path=ROOT/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    prefix_operator_path=P132/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    middle_operator_path=P133/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    extended_operator_path=P134/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    quarter_operator_path=P135/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    recent_operator_path=P136/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    half_operator_path=P137/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    beyond_operator_path=P138/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    three_quarter_operator_path=P139/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    seven_eighths_operator_path=PARENT/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    operators,prefix_operators,middle_operators,extended_operators,quarter_operators,recent_operators,half_operators,beyond_operators,three_quarter_operators,seven_eighths_operators=map(read_npz,
        [operator_path,prefix_operator_path,middle_operator_path,extended_operator_path,quarter_operator_path,recent_operator_path,half_operator_path,beyond_operator_path,three_quarter_operator_path,seven_eighths_operator_path])
    for block in [middle_operators,extended_operators,quarter_operators,recent_operators,half_operators,beyond_operators,three_quarter_operators,seven_eighths_operators]:
        for key in ['frequency','weights']:
            assert np.array_equal(prefix_operators[key],block[key]),key
        for key in ['coordinate','physical','cubic']:
            assert np.array_equal(prefix_operators[key][-1],block[key][0]),key
            prefix_operators[key]=np.concatenate([prefix_operators[key],block[key][1:]])
    for key in ['physical','cubic']:
        assert np.array_equal(operators[key][0],prefix_operators[key][-1])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    background=thermal_wave.thermal.ThermalBackground(args.model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    free_free=FreeFree(background,cache['frequency'])
    parent_folder=PARENT/'results'/f'feedback-{args.model}-m{int(args.upper*1000)}'
    template_path=parent_folder/'physical-source.npz'
    template=read_npz(template_path)
    reference_path=parent_folder/'physical-response.npz'
    reference=read_npz(reference_path)
    start,end=inner['coordinate'][[0,-1]]
    assert LAST_STEP==40960 and prediction['coordinate'][0]==start and prediction['coordinate'][-1]==end
    assert np.isin(template['coordinate'],prediction['coordinate']).all()
    coordinate=prediction['coordinate'].copy()
    assert len(coordinate)==2049 and np.all(np.diff(coordinate)>0)
    positions=np.searchsorted(coordinate,prediction['coordinate'])
    assert np.array_equal(coordinate[positions],prediction['coordinate'])
    prefix_positions=positions[:previous_sites]
    new_positions=positions[previous_sites:]
    reference_expanded=expand_source(template,coordinate)
    np.savez_compressed(folder/'previous-expanded-source.npz',**reference_expanded)
    response_grid=np.array([float(start+(end-start)*index/2048) for index in range(2049)])
    old_forcing=interpolate.interp1d(template['coordinate'],template['source'],axis=0,bounds_error=True)(response_grid)
    expanded_forcing=interpolate.interp1d(coordinate,reference_expanded['source'],axis=0,bounds_error=True)(response_grid)
    expansion_error=float(np.max(abs(expanded_forcing-old_forcing))/max(np.max(abs(old_forcing)),1e-300))
    checks=[check('Unchanged reference forcing under grid expansion',expansion_error,1e-12)]
    rows,source_sets,response_sets={},{},{}
    inputs=[replay_path,replay_path.parent/'status.json',prefix_path,prefix_path.parent/'status.json',middle_path,middle_path.parent/'status.json',extended_path,extended_path.parent/'status.json',quarter_path,quarter_path.parent/'status.json',recent_path,recent_path.parent/'status.json',half_path,half_path.parent/'status.json',beyond_path,beyond_path.parent/'status.json',three_quarter_path,three_quarter_path.parent/'status.json',seven_eighths_path,seven_eighths_path.parent/'status.json',inner_path,cache_path,
        operator_path,operator_path.parent/'status.json',prefix_operator_path,prefix_operator_path.parent/'status.json',middle_operator_path,middle_operator_path.parent/'status.json',extended_operator_path,extended_operator_path.parent/'status.json',quarter_operator_path,quarter_operator_path.parent/'status.json',recent_operator_path,recent_operator_path.parent/'status.json',half_operator_path,half_operator_path.parent/'status.json',beyond_operator_path,beyond_operator_path.parent/'status.json',three_quarter_operator_path,three_quarter_operator_path.parent/'status.json',seven_eighths_operator_path,seven_eighths_operator_path.parent/'status.json',
        template_path,reference_path,parent_folder/'status.json',*ladder.inputs,*emission.inputs,*free_free.inputs,
        background.parent.source,background.native_constants]
    for label in ['physical','cubic']:
        parent_source_path=parent_folder/(label+'-source.npz')
        previous=read_npz(parent_source_path)
        inputs.append(parent_source_path)
        action=np.concatenate([prefix_operators[label],operators[label][1:]])
        assert np.array_equal(np.r_[prefix_operators['coordinate'],operators['coordinate'][1:]],prediction['coordinate'])
        events=dict(frequency=operators['frequency'],adjoint=action)
        fresh,source_checks,source_errors=sources(basis,ladder,prediction,cache,events,background,emission,free_free,args.upper)
        checks.extend(dict(row,name='Source:'+label+':'+row['name']) for row in source_checks)
        candidate=expand_source(previous,coordinate)
        scale=max(float(np.max(abs(candidate['raw_source'][prefix_positions]))),1e-300)
        prefix_difference=float(np.max(abs(fresh['source'][:previous_sites]-candidate['source'][prefix_positions]))/scale)
        checks.append(check('Unchanged prefix independently recomputed:'+label,prefix_difference,1e-12))
        for key,value in fresh.items():
            if isinstance(value,np.ndarray) and value.ndim>0 and value.shape[0]==total_sites and key!='coordinate':
                candidate[key][new_positions]=value[previous_sites:]
        unaffected=np.ones(len(coordinate),dtype=bool)
        unaffected[new_positions]=False
        expanded_previous=expand_source(previous,coordinate)
        for key in ['source','raw_source','energy_source','number_source','overlap_source']:
            assert np.array_equal(candidate[key][unaffected],expanded_previous[key][unaffected])
        checks.append(dict(name='Earlier corrected prefix unchanged:'+label,passed=True))
        np.savez_compressed(folder/(label+'-source.npz'),**candidate)
        solution,errors=solve_response(args.model,candidate,2048,ladder,emission,background)
        metrics,view=readout(basis,prediction,candidate,solution,args.upper)
        response={**solution,**view}
        np.savez_compressed(folder/(label+'-response.npz'),**{key:value for key,value in response.items() if key!='photon'},
            photon_final=solution['photon'][-1],integration_steps=2048)
        checks.extend(check('Response:'+label+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
        checks.append(check('Unresolved moments:'+label,metrics['unresolved_energy_number_defect'],1e-10))
        comparator=reference if label=='physical' else response_sets['physical']
        rows[label]=dict(comparison=response_metrics(response,comparator,basis),source_errors=source_errors,response_errors=errors)
        source_sets[label],response_sets[label]=candidate,response
    assert np.array_equal(source_sets['cubic']['source'][:,1:],source_sets['physical']['source'][:,1:])
    checks.append(dict(name='Physical/common comparison changes only Compton source',passed=True))
    for label,current_source,old_source,current_response,old_response in [
        ('continuation',source_sets['physical'],reference_expanded,response_sets['physical'],reference),
        ('discretization',source_sets['cubic'],source_sets['physical'],response_sets['cubic'],response_sets['physical'])]:
        packet=dict(coordinate=coordinate,source=current_source['source']-old_source['source'])
        if label=='continuation':
            assert not np.count_nonzero(packet['source'][unaffected])
        else:
            assert not np.count_nonzero(packet['source'][:,1:])
        np.savez_compressed(folder/(label+'-source.npz'),**packet)
        residual,errors=solve_response(args.model,packet,2048,ladder,emission,background)
        if label=='continuation':
            continuation_solution=residual
        np.savez_compressed(folder/(label+'-response.npz'),**{key:value for key,value in residual.items() if key!='photon'},
            photon_final=residual['photon'][-1],integration_steps=2048)
        checks.extend(check('Response:'+label+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
        gas=residual['gas'][:,:3]
        old_gas=old_response['gas'][:,:3]
        peak=np.max(abs(gas),axis=0)
        relative_peak=peak/np.maximum(np.max(abs(old_gas),axis=0),1e-300)
        relative_late=np.max(abs(gas[1536:]),axis=0)/np.maximum(np.max(abs(old_gas[1536:]),axis=0),1e-300)
        relative_endpoint=abs(gas[-1])/np.maximum(abs(old_gas[-1]),1e-300)
        discrepancy=np.max(abs(current_response['gas'][:,:3]-old_gas-gas),axis=0)
        superposition=discrepancy/np.maximum(peak,1e-300)
        for metric,values in [('peak',relative_peak),('late',relative_late),('endpoint',relative_endpoint)]:
            checks.extend(check('Sensitivity1percent:'+label+':'+metric+':'+column,value,.01)
                for column,value in zip(['baseline','join1','join2'],values))
        checks.extend(check('Superposition:'+label+':'+column,value,1e-4)
            for column,value in zip(['baseline','join1','join2'],superposition))
        rows[label]=dict(response_errors=errors,relative_peak=relative_peak.tolist(),relative_late=relative_late.tolist(),
            relative_endpoint=relative_endpoint.tolist(),superposition_relative=superposition.tolist(),gas_endpoint=gas[-1].tolist())
    current=response_sets['physical']
    total_delta=current['physical_change']-reference['physical_change']
    resolved_delta=current['resolved_change']-reference['resolved_change']
    unresolved_delta=current['unresolved_change']-reference['unresolved_change']
    raw_delta=current['replacement']-reference['replacement']
    projection_delta=basis.values@(source_sets['physical']['projected_replacement'][-1]-template['projected_replacement'][-1])
    independent_resolved=basis.values@continuation_solution['photon'][-1,:,:3]
    operand_scale=np.maximum(norm(current['physical_change'],basis.measure)+norm(reference['physical_change'],basis.measure),1e-300)
    split_error=norm(total_delta-resolved_delta-unresolved_delta,basis.measure)/operand_scale
    endpoint_scale=np.maximum(norm(current['replacement'],basis.measure)+norm(reference['replacement'],basis.measure),1e-300)
    endpoint_error=norm(unresolved_delta-raw_delta+projection_delta,basis.measure)/endpoint_scale
    independent_error=norm(resolved_delta-independent_resolved,basis.measure)/np.maximum(norm(independent_resolved,basis.measure),1e-300)
    checks.append(dict(name='Complete corrected source grid and final readout endpoint',passed=True,source_sites=2049,restore_step=None))
    for column,split_value,endpoint_value,independent_value in zip(['baseline','join1','join2'],split_error,endpoint_error,independent_error):
        checks.extend([check('Final readout split:'+column,float(split_value),1e-12),
            check('Final endpoint replacement identity:'+column,float(endpoint_value),1e-12),
            check('Superposition:final resolved readout:'+column,float(independent_value),1e-4)])
    denominator=np.maximum(norm(reference['physical_change'],basis.measure),1e-300)
    decomposition=dict(total_relative=(norm(total_delta,basis.measure)/denominator).tolist(),
        resolved_relative=(norm(resolved_delta,basis.measure)/denominator).tolist(),
        endpoint_unresolved_relative=(norm(unresolved_delta,basis.measure)/denominator).tolist(),
        raw_endpoint_relative=(norm(raw_delta,basis.measure)/denominator).tolist(),
        projection_endpoint_relative=(norm(projection_delta,basis.measure)/denominator).tolist(),
        split_identity_error=split_error.tolist(),endpoint_identity_error=endpoint_error.tolist(),
        independent_resolved_error=independent_error.tolist())
    np.savez_compressed(folder/'final-readout-decomposition.npz',total_delta=total_delta,
        resolved_delta=resolved_delta,unresolved_delta=unresolved_delta,raw_endpoint_delta=raw_delta,
        projected_endpoint_delta=projection_delta,independent_resolved_delta=independent_resolved,
        reference_norm=denominator)
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    assert all(row['passed'] for row in checks if not row['name'].startswith(('Response:','Superposition:','Sensitivity1percent:')))
    finish(folder,dict(checks=checks,model=args.model,upper=args.upper,variants=rows,readout_decomposition=decomposition,
        source_knots=len(coordinate),continuous_inner_stop=LAST_STEP,continuous_source_sites=total_sites,
        restore_step=None,new_source_sites=total_sites-previous_sites,frequency_nodes=5265,response_steps=2048,
        full_history_recomputed=True,full_parent_history_rerun=False,corrected_final_readout=True,previous_prefix_preserved=True,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(model=args.model,upper=args.upper,source_knots=len(coordinate),seconds=time.monotonic()-started,
        endpoints={label:rows[label]['relative_endpoint'] for label in ['continuation','discretization']},
        failures=[row['name'] for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
