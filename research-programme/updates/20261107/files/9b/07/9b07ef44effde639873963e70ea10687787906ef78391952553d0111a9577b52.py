from source_probe_common import *
from direct_common import direct_adjoint
import re


def independent_dual(values,basis):
    moved=np.moveaxis(values,-2,-1)
    flat=moved.reshape(-1,basis.count)
    solved=linalg.solve(basis.mass,flat.T,assume_a='pos').T
    return np.sqrt(np.maximum(np.sum(flat*solved,axis=1),0)).reshape(moved.shape[:-1])


def main():
    modest()
    folder=ROOT/'results/validation'
    assert not (ROOT/'results/stage-integrity.json').exists()
    folder.mkdir(parents=True,exist_ok=False)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    script_hashes={digest(script) for script in scripts}
    checks,inputs,consumed=[],[],set()
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        if path not in hashes:
            hashes[path]=digest(path)
        return hashes[path]
    packets=sorted(path for path in (ROOT/'results').glob('*/status.json') if path.parent!=folder)
    failures={}
    scientific,passing=0,0
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').is_file()
        assert packet['script_sha256'] in script_hashes
        failed=[row['name'] for row in packet['checks'] if not row['passed']]
        assert all(name.startswith(('Source diagnostic1percent:','Sampled response1percent:')) or
            (name.startswith('Response:') and name.endswith(':gas')) for name in failed),(path,failed)
        if failed:
            failures[path.parent.name]=failed
        assert packet['count']==len(packet['checks'])
        assert packet['all_checks_passed']==(not failed)
        for source,sha in packet['input_hashes'].items():
            assert hashed(source)==sha,source
            consumed.add(Path(source))
        for archive in path.parent.glob('*.npz'):
            values=read_npz(archive)
            assert all(np.isfinite(value).all() for value in values.values() if value.dtype.kind not in ['U','S'])
            inputs.append(archive)
        inputs.append(path)
        scientific+=len(packet['checks'])
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        checks.append(dict(name='Finite sourced packet:'+path.parent.name,passed=True))
    assert len(packets)==25
    assert failures==review['expected_failed_by_packet']
    assert scientific==review['scientific_checks'] and passing==review['passing_scientific_checks']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs.extend(ladder.inputs)
    consumed.update(ladder.inputs)
    replayed_steps=0
    for model in ['heavy','cold']:
        parent_path=refined_owner(model)/'results'/f'inner-{model}-n40960/prediction.npz'
        parent=read_npz(parent_path)
        inputs.append(parent_path)
        consumed.add(parent_path)
        fresh_steps=[]
        for restart in RESTART_STEPS:
            replay_folder=ROOT/'results'/f'replay-{model}-s{restart:05d}'
            replay=read_npz(replay_folder/'prediction.npz')
            status=json.loads((replay_folder/'status.json').read_text())
            record_path=Path(status['original_restart'])
            record=json.loads(record_path.read_text())
            snapshot_path=record_path.parent/record['archive']
            assert hashed(snapshot_path)==record['archive_sha256']
            snapshot=read_npz(snapshot_path)
            assert int(snapshot['completed_step'])==restart
            assert np.array_equal(replay['defect'][0],snapshot['error'])
            assert np.array_equal(replay['outer_slope'][0],snapshot['old_outer'])
            expected_stop=40960 if restart==35840 else restart+640
            assert np.array_equal(replay['saved_step_indices'],np.arange(restart,expected_stop+1,160))
            assert int(replay['steps'])==40960 and len(replay['frequency'])==5265
            for key in ['frequency','coefficient_knots','coefficient_bank','offsets']:
                assert np.array_equal(replay[key],parent[key]),key
            for index,step in enumerate(replay['saved_step_indices']):
                expected=parent['coordinate'][0]+(parent['coordinate'][-1]-parent['coordinate'][0])*step/40960
                assert replay['coordinate'][index]==expected
                if step%640==0:
                    for key in ['defect','outer_slope','lower_target','slope']:
                        assert np.array_equal(replay[key][index],parent[key][step//640]),(model,step,key)
                else:
                    fresh_steps.append(int(step))
            replayed_steps+=expected_stop-restart
            inputs.extend([record_path,snapshot_path])
            consumed.update([record_path,snapshot_path])
            checks.append(dict(name='Restored state,fixed inputs and bitwise old endpoints:'+model+':'+str(restart),passed=True))
        assert fresh_steps==[interval*640+offset for interval in PROBE_INTERVALS for offset in [160,320,480]]
    assert replayed_steps==19200
    for upper in [.04,.02]:
        bank_folder=ROOT/'results'/f'operator-m{int(upper*1000)}'
        bank=read_npz(bank_folder/'bank.npz')
        assert len(bank['steps'])==45
        for index,step in enumerate(bank['steps']):
            event=read_npz(bank_folder/f'event-{step:05d}.npz')
            assert np.array_equal(event['adjoint'],bank['adjoint'][index])
            assert np.all(event['rates']>0) and np.all(event['ratios']>0)
            moment=np.sum(event['rates']*(event['ratios']-1)**2*(event['ratios']+1)/event['ratios']**3)
            target=bank['weights']*bank['frequency']*moment/(2*I3)
            assert np.linalg.norm(basis.temperature@event['adjoint']-target)/np.linalg.norm(target)<1e-10
            assert np.max(abs(basis.chemical@event['adjoint']))<1e-14
            temperatures=[thermal_wave.thermal.ThermalBackground(model).at(float(event['coordinate']))['thermal_parameter'] for model in ['heavy','cold']]
            assert temperatures[0]==temperatures[1]==float(event['theta'])
            if index in [0,22,44]:
                recalculated,unused=direct_adjoint(basis,bank['frequency'],bank['weights'],event['ratios'],event['rates'])
                assert np.array_equal(recalculated,event['adjoint'])
        checks.append(dict(name='Fresh Doppler bank,invariants,shared temperature and three recomputations:'+str(upper),passed=True))
    combined_original_failures={}
    for model in ['heavy','cold']:
        owner=refined_owner(model)
        parent=read_npz(owner/'results'/f'inner-{model}-n40960/prediction.npz')
        background=thermal_wave.thermal.ThermalBackground(model)
        for upper in [.04,.02]:
            probe_folder=ROOT/'results'/f'probe-{model}-m{int(upper*1000)}'
            status=json.loads((probe_folder/'status.json').read_text())
            assert status['sampled_intervals']==PROBE_INTERVALS and not status['full_history_source_refinement']
            assert status['frequency_nodes']==5265 and status['inner_steps']==40960 and status['response_steps']==2048
            points=read_npz(probe_folder/'point-sources.npz')
            sampled=read_npz(probe_folder/'sampled-states.npz')
            old_folder=owner/'results'/f'feedback-m{int(upper*1000)}-n40960'
            old_source=read_npz(old_folder/(model+'-source.npz'))
            old_response=read_npz(old_folder/(model+'-response.npz'))
            old_status=json.loads((old_folder/'status.json').read_text())
            original_failures=[row for row in old_status['checks'] if not row['passed']]
            assert status['original_response_failures']==original_failures
            combined_original_failures[f'{model}:m{int(upper*1000)}']=original_failures
            consumed.update([old_folder/'status.json',old_folder/(model+'-source.npz'),old_folder/(model+'-response.npz')])
            old_interpolation=interpolate.interp1d(old_source['coordinate'],old_source['source'],axis=0,bounds_error=True)(points['coordinate'])
            assert np.array_equal(old_interpolation,points['linear'])
            direct=read_npz(probe_folder/'direct-evaluated.npz')
            assembled=read_npz(probe_folder/'assembled-evaluated.npz')
            selection=sampled['steps']%640!=0
            for label,values in [('direct',direct),('assembled',assembled)]:
                assert np.array_equal(points[label],values['source'][selection])
                assert np.array_equal(values['source'],values['raw_source']-values['overlap_source'])
            order=8 if upper==.04 else 6
            old_bank_path=BRANCH/'direct-doppler-compton-feedback-20261012/results'/f'bank-o{order}-q32-m{int(upper*1000)}/bank.npz'
            old_bank=read_npz(old_bank_path)
            fresh=read_npz(ROOT/'results'/f'operator-m{int(upper*1000)}/bank.npz')
            old_adjoint=interpolate.interp1d(old_bank['coordinate'],old_bank['adjoint'],axis=0,bounds_error=True)(points['coordinate'])
            event_values=np.stack([compact_defect(fresh['frequency'],parent['frequency'],value,upper) for value in sampled['defect'][selection]])
            predicted=np.einsum('nij,njk->nik',fresh['adjoint']-old_adjoint,event_values)
            observed=points['direct'][:,0]-points['assembled'][:,0]
            scale=np.maximum(independent_dual(points['direct'][:,0],basis)+independent_dual(points['assembled'][:,0],basis),1e-300)
            assert np.max(independent_dual(predicted-observed,basis)/scale)<1e-9
            assert np.array_equal(points['direct'][:,1:],points['assembled'][:,1:])
            consumed.add(old_bank_path)
            for row in status['diagnostics']:
                label=row['label']
                current,reference=(points['assembled'],points['linear']) if label=='assembly_vs_linear' else ((points['direct'],points['linear']) if label=='direct_vs_linear' else (points['direct'],points['assembled']))
                delta=current-reference
                absolute=independent_dual(delta.sum(axis=1),basis)
                total_scale=np.maximum(independent_dual(current.sum(axis=1),basis),independent_dual(reference.sum(axis=1),basis))
                component_scale=np.maximum(independent_dual(current,basis).sum(axis=1),independent_dual(reference,basis).sum(axis=1))
                assert np.allclose(row['difference_absolute'],absolute,rtol=1e-8,atol=0)
                assert np.allclose(row['relative_to_total'],absolute/np.maximum(total_scale,1e-300),rtol=1e-8,atol=0)
                assert np.allclose(row['relative_to_components'],absolute/np.maximum(component_scale,1e-300),rtol=1e-8,atol=0)
                assert np.allclose(row['energy_moment'],np.einsum('i,ntik->ntk',basis.temperature,delta),rtol=1e-12,atol=0)
                assert np.allclose(row['number_moment'],np.einsum('i,ntik->ntk',basis.chemical,delta),rtol=1e-12,atol=0)
            for variant in ['linear','assembled','direct']:
                source=read_npz(probe_folder/(variant+'-source.npz'))
                response=read_npz(probe_folder/(variant+'-response.npz'))
                assert len(source['coordinate'])==110 and np.all(np.diff(source['coordinate'])>0)
                old_indices=np.searchsorted(source['coordinate'],old_source['coordinate'])
                for key,value in old_source.items():
                    if value.ndim>0 and value.shape[0]==65:
                        assert np.array_equal(source[key][old_indices],value)
                assert len(response['coordinate'])==2049 and int(response['integration_steps'])==2048
                assert np.array_equal(response['coordinate'],old_response['coordinate'])
                assert np.array_equal(response['unresolved_change'],old_response['unresolved_change'])
                scale=np.maximum((abs(response['energy'])+background.chi*abs(response['gas'])+abs(response['work'])).max(axis=0),1e-300)
                assert np.max(abs(response['energy']+background.chi*response['gas']+response['work'])/scale)<1e-7
                total=basis.values@response['photon'][-1,:,:3]+response['unresolved_change']
                assert np.array_equal(total,response['physical_change'])
                metric=status['variants'][variant]['comparison']
                difference=response['gas'][:,:3]-old_response['gas'][:,:3]
                for key,selected in [('gas_peak_relative',slice(None)),('gas_late_relative',slice(1536,None))]:
                    relative=abs(difference[selected]).max(axis=0)/np.maximum(abs(old_response['gas'][selected,:3]).max(axis=0),1e-300)
                    assert np.allclose(metric[key],relative,atol=0,rtol=1e-12)
                assert np.array_equal(metric['gas_endpoint_signed_difference'],difference[-1])
                assert np.allclose(metric['gas_endpoint_relative'],abs(difference[-1])/np.maximum(abs(old_response['gas'][-1,:3]),1e-300),atol=0,rtol=1e-12)
                radiation=norm(response['physical_change']-old_response['physical_change'],basis.measure)/np.maximum(norm(old_response['physical_change'],basis.measure),1e-300)
                assert np.allclose(metric['radiation_relative'],radiation,atol=0,rtol=1e-12)
                if variant=='linear':
                    assert max(metric['gas_peak_relative'])<1e-7 and max(metric['radiation_relative'])<1e-7
            checks.append(dict(name='Independent source decomposition,norms,unchanged knots,paired responses and control:'+model+':'+str(upper),passed=True))
    assert combined_original_failures==review['combined_original_response_failures']
    attribution_path=ROOT/'results/source-attribution/status.json'
    attribution=json.loads(attribution_path.read_text())
    assert attribution['all_checks_passed'] and attribution['diagnostic_added_after_source_probe']
    assert len(attribution['rows'])==4
    for row in attribution['rows']:
        model,upper=row['model'],row['upper']
        probe=ROOT/'results'/f'probe-{model}-m{int(upper*1000)}'
        sources={label:read_npz(probe/(label+'-source.npz')) for label in ['linear','assembled','direct']}
        responses={label:read_npz(probe/(label+'-response.npz')) for label in sources}
        deltas={label:read_npz(ROOT/'results/source-attribution'/f'{model}-m{int(upper*1000)}-{label}.npz') for label in ['first','remaining','operator']}
        assert np.array_equal(deltas['first']['source']+deltas['remaining']['source'],sources['direct']['source']-sources['linear']['source'])
        assert np.array_equal(deltas['operator']['source'],sources['direct']['source']-sources['assembled']['source'])
        assert not np.count_nonzero(deltas['operator']['source'][:,1:])
        assert np.array_equal(responses['direct']['gas'][:,6:],responses['assembled']['gas'][:,6:])
        old_source=read_npz(refined_owner(model)/'results'/f'feedback-m{int(upper*1000)}-n40960'/(model+'-source.npz'))
        first_mask=deltas['first']['coordinate']<old_source['coordinate'][1]
        assert not np.count_nonzero(deltas['first']['source'][~first_mask])
        assert not np.count_nonzero(deltas['remaining']['source'][first_mask])
        for label in deltas:
            assert len(deltas[label]['response_coordinate'])==2049
            assert np.array_equal(deltas[label]['response_coordinate'],responses['linear']['coordinate'])
            field={'first':'first_interval_endpoint','remaining':'remaining_intervals_endpoint','operator':'operator_increment_endpoint'}[label]
            assert np.array_equal(row[field],deltas[label]['gas'][-1,:3])
        closure=responses['direct']['gas']-responses['linear']['gas']-deltas['first']['gas']-deltas['remaining']['gas']
        scale=np.maximum((abs(responses['direct']['gas'])+abs(responses['linear']['gas'])+abs(deltas['first']['gas'])+abs(deltas['remaining']['gas'])).max(axis=0),1e-300)
        error=float(np.max(abs(closure)/scale))
        assert error<1e-7 and np.isclose(error,row['first_split_gas_closure'],rtol=1e-12,atol=0)
        for label,response in responses.items():
            parts=np.stack([response['gas'][-1,offset:offset+3] for offset in [3,6,9]])
            component_scale=abs(parts).sum(axis=0)
            factor=component_scale/np.maximum(abs(response['gas'][-1,:3]),1e-300)
            assert np.array_equal(row['conditioning'][label]['component_endpoints'],parts)
            assert np.array_equal(row['conditioning'][label]['cancellation_factor'],factor)
        checks.append(dict(name='Independent initial-interval attribution and gas-component cancellation:'+model+':'+str(upper),passed=True))
    chain=ancestors()
    parent=chain[PARENT/'results/stage-integrity.json']
    rehashed=set()
    for name,sha in parent['file_hashes'].items():
        path=PARENT/name
        assert hashed(path)==sha
        rehashed.add(path)
    for path in consumed:
        if not path.is_relative_to(ROOT):
            verify_source(path,chain)
            rehashed.add(path)
    inherited_count=sum(len(packet['file_hashes']) for packet in chain.values())
    assert inherited_count==204746
    documents=sorted(ROOT.glob('*.md'))
    for document in documents:
        for reference in re.findall(chr(96)+'([^'+chr(96)+']+)'+chr(96),document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.pdf')):
                assert (ROOT/reference).resolve().is_file(),reference
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Parent,consumed sources,citations and directory capacity',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=scientific-passing,retained_failure_names=failures,compiled_scripts=len(scripts),
        checked_science_packets=len(packets),accepted_scope_verified=True,largest_direct_file_count=maximum,
        inherited_payload_count=inherited_count,replayed_steps=replayed_steps,completed_backgrounds=['heavy','cold'],
        consumed_and_immediate_rehashed={str(path):hashed(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(science=scientific,passes=passing,failures=scientific-passing,
        validation_checks=len(checks),rehashed=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
