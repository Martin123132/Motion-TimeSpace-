from stage164_common import *
from assemble_repair import decimal_array


def cardinal_weights(phase,route):
    warm=bubble(phase,route)
    cold=cold_bubble(phase,route)
    warm_at_cold=bubble(.75,route)
    basic=np.array([(1-phase)*(1-2*phase)-.375*warm,warm,4*phase*(1-phase)-.75*warm,0.,phase*(2*phase-1)+.125*warm])
    at_cold=np.array([-.125-.375*warm_at_cold,warm_at_cold,.75-.75*warm_at_cold,0.,.375+.125*warm_at_cold])
    basic-=cold*at_cold
    basic[3]=cold
    return basic


def coordinate_source(exact,temperature):
    result=exact.copy()
    others=[index for index in range(96) if index!=1]
    for column in range(exact.shape[1]):
        result[2,column]=(exact[0,column]-sum((Decimal.from_float(float(temperature[index]))*exact[index+1,column]
            for index in others),Decimal(0)))/Decimal.from_float(float(temperature[1]))
        result[-1,column]=-exact[0,column]
    return result


def measure_phases(anchors,route,temperature,coordinates,changes):
    maxima={key:0. for key in ['full_old_pair','full_old_moment','full_old_rewrite','full_new_pair','full_new_moment','full_new_rewrite',
        'physical_pair','physical_moment','physical_rewrite','numerical_replay_rewrite']}
    for phase in np.linspace(0,1,2049):
        weights=cardinal_weights(phase,route)
        full=stable_sum(weights[:,None,None]*anchors)
        reference=stable_sum(weights[:,None,None]*changes['raw_reference'])
        newfull=full+reference
        for label,values in [('full_old',full),('full_new',newfull)]:
            scale=np.maximum(abs(values[0]),1e-300)
            maxima[label+'_pair']=max(maxima[label+'_pair'],float(max(abs(values[0]+values[-1])/scale)))
            maxima[label+'_moment']=max(maxima[label+'_moment'],float(max(abs(temperature@values[1:-1]-values[0])/scale)))
            maxima[label+'_rewrite']=max(maxima[label+'_rewrite'],coordinates.source(values)[3]['relative_change'])
        physical=[stable_sum(weights[:,None,None]*changes[step]) for step in ['54','65','64']]
        values=np.column_stack(physical)
        scale=np.maximum(abs(values[0]),1e-300)
        maxima['physical_pair']=max(maxima['physical_pair'],float(max(abs(values[0]+values[-1])/scale)))
        maxima['physical_moment']=max(maxima['physical_moment'],float(max(abs(temperature@values[1:-1]-values[0])/scale)))
        maxima['physical_rewrite']=max(maxima['physical_rewrite'],coordinates.source(values)[3]['relative_change'])
        replay=stable_sum(weights[:,None,None]*changes['coordinate_reference'])
        maxima['numerical_replay_rewrite']=max(maxima['numerical_replay_rewrite'],coordinates.source(replay)[3]['relative_change'])
    return maxima


def main():
    modest()
    folder=ROOT/'results/reference'
    folder.mkdir(parents=True,exist_ok=False)
    source_packet=verify_packet(ROOT/'results/sources')
    legacy=verify_packet(ROOT/'results/legacy-update')
    data=read_npz(ROOT/'results/sources/source.npz')
    prior_path=BRANCH/'saved-event-precision-repair-20261016/results/repaired-readiness/source.npz'
    previous=read_npz(prior_path)
    assert np.array_equal(previous['end'],data['start'])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    coordinates=EnergyCoordinates(ladder.basis)
    inputs=[ROOT/'REFERENCE-CONTRACT.md',ROOT/'results/sources/status.json',ROOT/'results/legacy-update/status.json',ROOT/'results/sources/source.npz',prior_path,*ladder.inputs]
    checks,records,arrays=[],{},dict(mass=data['mass'],temperature=data['temperature'])
    with localcontext() as context:
        context.prec=60
        for endpoint in ENDPOINTS:
            exacts={}
            for order in [4,6]:
                path=ROOT/'results/sources'/f'{endpoint}-source{order}-exact.json'
                packet=json.loads(path.read_text())
                exacts[order]={key:np.array([Decimal(value) for value in packet[key]],dtype=object).reshape(4,4) for key in ['full','update','saved']}
                inputs.append(path)
            old=decimal_array(data[endpoint])
            raw_arithmetic=decimal_array(data[f'soft_{endpoint}_update4'])
            raw_arithmetic[[0,1,2,97]]=exacts[4]['update']
            new=old+raw_arithmetic
            computational_old=coordinate_source(old,data['temperature'])
            computational_new=coordinate_source(new,data['temperature'])
            replay=coordinate_source(raw_arithmetic,data['temperature'])
            difference=computational_new-computational_old-replay
            scale=max(max(abs(value) for value in replay.flat),Decimal('1e-300'))
            test(checks,'Historical coordinate-map linearity:'+endpoint,float(max(abs(value) for value in difference.flat)/scale),1e-10)
            raw_change=exacts[6]['update']
            physical=exacts[6]['full']-exacts[4]['full']
            arithmetic=exacts[4]['update']
            physical_full=decimal_array(data[f'soft_{endpoint}_total64'])
            physical_full[[0,1,2,97]]=physical
            direct_coordinate=coordinate_source(new+physical_full,data['temperature'])
            recovered_coordinate=computational_old+replay+coordinate_source(physical_full,data['temperature'])
            coordinate_scale=max(max(abs(value) for value in direct_coordinate.flat),Decimal('1e-300'))
            test(checks,'Direct repaired6 coordinate source equals reference plus physical:'+endpoint,
                float(max(abs(value) for value in (direct_coordinate-recovered_coordinate).flat)/coordinate_scale),1e-10)
            scale=max(max(abs(value) for value in raw_change.flat),Decimal('1e-300'))
            test(checks,'Exact reference plus physical source telescope:'+endpoint,
                float(max(abs(value) for value in (raw_change-arithmetic-physical).flat)/scale),1e-10)
            defects={}
            for name,values in [('old',exacts[4]['saved']),('repaired4',exacts[4]['full']),('repaired6',exacts[6]['full']),
                ('arithmetic',arithmetic),('physical64',physical),('legacy64',raw_change)]:
                pair=values[0]+values[-1]
                moment=Decimal.from_float(float(data['temperature'][0]))*values[1]+Decimal.from_float(float(data['temperature'][1]))*values[2]-values[0]
                defects[name]=dict(pair=[str(value) for value in pair],moment=[str(value) for value in moment])
            for diagnostic in ['pair','moment']:
                residual=np.array([Decimal(value) for value in defects['legacy64'][diagnostic]],dtype=object)
                parts=sum(np.array([Decimal(value) for value in defects[name][diagnostic]],dtype=object) for name in ['arithmetic','physical64'])
                scale=max(max(abs(value) for value in residual),Decimal('1e-300'))
                test(checks,'Independent defect ledger:'+endpoint+':'+diagnostic,float(max(abs(value) for value in residual-parts)/scale),1e-10)
            arrays[f'{endpoint}_raw_reference']=np.asarray(raw_arithmetic,dtype=float)
            arrays[f'{endpoint}_coordinate_reference']=np.asarray(replay,dtype=float)
            arrays[f'{endpoint}_coordinate_old']=np.asarray(computational_old,dtype=float)
            arrays[f'{endpoint}_coordinate_new']=np.asarray(computational_new,dtype=float)
            records[endpoint]=dict(defects=defects,arithmetic_relative_source=(SourceNorm(data['mass'])(np.asarray(raw_arithmetic,dtype=float))/SourceNorm(data['mass'])(data[endpoint])).tolist(),
                numerical_replay_is_not_physical_source=True)
    old_warm=previous['warm_defect']+.375*previous['start']+.75*previous['centre']-.125*previous['end']
    old_anchors=np.stack([previous['start'],old_warm,previous['centre'],previous['actual'],previous['end']])
    current=data['after_band820_full']
    new_anchors=np.stack([data['start'],current[1],current[2],current[0],data['end']])
    arrays['earlier_anchors']=old_anchors
    arrays['terminal_anchors']=new_anchors
    phase_records={}
    phase_checks=[]
    for window,anchors in [('earlier',old_anchors),('terminal',new_anchors)]:
        changes={name:np.zeros_like(anchors) for name in ['raw_reference','coordinate_reference','54','65','64']}
        for endpoint,index in ([('start',4)] if window=='earlier' else [('start',0),('end',4)]):
            changes['raw_reference'][index]=arrays[endpoint+'_raw_reference']
            changes['coordinate_reference'][index]=arrays[endpoint+'_coordinate_reference']
            for step in ['54','65','64']:
                changes[step][index]=data[f'soft_{endpoint}_total{step}']
        for name,values in changes.items():
            arrays[window+'_'+name]=values
        for route in ['local','cubic']:
            for phase_index,phase in enumerate([0.,.25,.5,.75,1.]):
                close(checks,f'Frozen cardinal anchor:{window}:{route}:{phase}',cardinal_weights(phase,route),np.eye(5)[phase_index],1e-12)
            maxima=measure_phases(anchors,route,data['temperature'],coordinates,changes)
            phase_records[window+'-'+route]=maxima
            for quantity,value in maxima.items():
                test(phase_checks,'Unchanged phase gate:'+window+':'+route+':'+quantity,value,1e-10)
    checks.extend(phase_checks)
    np.savez_compressed(folder/'reference.npz',**arrays)
    allowed=source_packet['all_checks_passed'] and all(row['passed'] for row in checks)
    report=dict(checks=checks,records=records,phase_records=phase_records,phases_per_route=2049,
        source_reconciliation_completed=True,saved_history_replayed=False,reference_replay_qualified=allowed,
        physical_source_checks_passed=source_packet['all_checks_passed'],
        legacy_failed_checks=[row for row in legacy['checks'] if not row['passed']],
        legacy_raw_update_reclassified=False,coordinate_reference_is_numerical_not_physical=True,
        shared_endpoint_included_in_both_windows=True,temperature_curve_changed=False)
    finish(folder,report,__file__,[*inputs,folder/'reference.npz'])
    print(json.dumps(dict(qualified=allowed,checks=len(checks),failed=[row for row in checks if not row['passed']],phase_records=phase_records)),flush=True)


if __name__=='__main__':
    main()
