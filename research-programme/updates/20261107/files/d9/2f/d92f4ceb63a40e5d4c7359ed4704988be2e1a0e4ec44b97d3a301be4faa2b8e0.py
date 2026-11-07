from response_sites_common import *
from validate_source_probe import independent_dual
import re


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
    inputs,consumed,checks=[],set(),[]
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        if path not in hashes:
            hashes[path]=digest(path)
        return hashes[path]
    packets=sorted(path for path in (ROOT/'results').glob('*/status.json') if path.parent!=folder)
    failures={}
    scientific=passing=0
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').is_file()
        assert packet['script_sha256'] in script_hashes
        failed=[row['name'] for row in packet['checks'] if not row['passed']]
        assert all(name.startswith(('Refinement1percent:','Source1percent:')) or
            (name.startswith('Response:') and name.endswith(':gas')) for name in failed),(path,failed)
        if failed:
            failures[path.parent.name]=failed
        assert packet['count']==len(packet['checks']) and packet['all_checks_passed']==(not failed)
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
    assert len(packets)==11
    assert failures==review['expected_failed_by_packet']
    assert scientific==review['scientific_checks'] and passing==review['passing_scientific_checks']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs.extend(ladder.inputs)
    consumed.update(ladder.inputs)
    for model in ['heavy','cold']:
        owner=refined_owner(model)
        old_path=owner/'results'/f'inner-{model}-n40960/prediction.npz'
        parent=read_npz(old_path)
        previous_path=PARENT/'results'/f'replay-{model}-s00000/prediction.npz'
        previous=read_npz(previous_path)
        replay_folder=ROOT/'results'/f'replay-{model}-s00000'
        replay=read_npz(replay_folder/'prediction.npz')
        status=json.loads((replay_folder/'status.json').read_text())
        record_path=Path(status['original_restart'])
        record=json.loads(record_path.read_text())
        snapshot_path=record_path.parent/record['archive']
        assert hashed(snapshot_path)==record['archive_sha256']
        snapshot=read_npz(snapshot_path)
        assert int(snapshot['completed_step'])==0 and not np.count_nonzero(snapshot['error'])
        assert np.array_equal(replay['defect'][0],snapshot['error'])
        assert np.array_equal(replay['outer_slope'][0],snapshot['old_outer'])
        assert np.array_equal(replay['saved_step_indices'],np.arange(0,641,20))
        for key in ['frequency','coefficient_knots','coefficient_bank','offsets']:
            assert np.array_equal(replay[key],parent[key]),key
        count=0
        for old_index,step in enumerate(previous['saved_step_indices']):
            if step%20:
                continue
            selected=int(step//20)
            for key in ['defect','outer_slope','slope','lower_target','coordinate']:
                assert np.array_equal(replay[key][selected],previous[key][old_index]),(model,step,key)
            count+=1
        assert count==18
        assert int(replay['steps'])==40960 and int(replay['stop_step'])==640
        inputs.extend([old_path,previous_path,record_path,snapshot_path])
        consumed.update([old_path,previous_path,record_path,snapshot_path])
        checks.append(dict(name='All18 overlapping saved states and fixed inner controls:'+model,passed=True))
    for upper in [.04,.02]:
        label=int(upper*1000)
        bank_folder=ROOT/'results'/f'operator-m{label}'
        bank=read_npz(bank_folder/'bank.npz')
        status=json.loads((bank_folder/'status.json').read_text())
        prior_path=PARENT/'results'/f'operator-m{label}/bank.npz'
        prior=read_npz(prior_path)
        assert status['new_soft_temperature_evaluations']==16 and status['reused_temperature_evaluations']==15
        assert sum(row['reused'] for row in status['rows'])==15
        assert np.array_equal(bank['steps'],np.arange(20,640,20))
        for index,step in enumerate(bank['steps']):
            event=read_npz(bank_folder/f'event-{step:05d}.npz')
            assert np.array_equal(event['adjoint'],bank['adjoint'][index])
            assert np.all(event['ratios']>0) and np.all(event['rates']>0)
            moment=np.sum(event['rates']*(event['ratios']-1)**2*(event['ratios']+1)/event['ratios']**3)
            expected=bank['weights']*bank['frequency']*moment/(2*I3)
            assert np.linalg.norm(basis.temperature@event['adjoint']-expected)/np.linalg.norm(expected)<1e-10
            if step%40==0:
                selected=int(np.flatnonzero(prior['steps']==step)[0])
                assert np.array_equal(bank['adjoint'][index],prior['adjoint'][selected])
        inputs.append(prior_path)
        consumed.add(prior_path)
        checks.append(dict(name='32fresh/30reused operators,energy and positive-kernel checks:'+str(upper),passed=True))
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        for upper in [.04,.02]:
            label=int(upper*1000)
            packet_folder=ROOT/'results'/f'sites-{model}-m{label}'
            old_folder=PARENT/'results'/f'transient-{model}-m{label}'
            status=json.loads((packet_folder/'status.json').read_text())
            assert not status['inner_coefficients_resampled'] and not status['other_source_intervals_changed']
            assert not status['initial_state_tuned'] and status['source_knot_counts']==[122,138]
            evaluated={variant:read_npz(packet_folder/(variant+'-evaluated.npz')) for variant in ['assembled','direct']}
            assert np.array_equal(evaluated['assembled']['source'][:,1:],evaluated['direct']['source'][:,1:])
            for variant in ['assembled','direct']:
                previous_eval_path=old_folder/(variant+'-evaluated.npz')
                previous_eval=read_npz(previous_eval_path)
                fresh=read_npz(packet_folder/(variant+'-fresh.npz'))
                current=evaluated[variant]
                assert len(current['coordinate'])==33 and len(fresh['coordinate'])==18
                for key,value in previous_eval.items():
                    if value.ndim>0 and value.shape[0]==17:
                        assert np.array_equal(current[key][::2],value),key
                        assert np.array_equal(current[key][1::2],fresh[key][1:-1]),key
                old_source_path=old_folder/f'{variant}-16-source.npz'
                old_response_path=old_folder/f'{variant}-16-response.npz'
                earlier_response_path=old_folder/f'{variant}-8-response.npz'
                old_source,old_response=read_npz(old_source_path),read_npz(old_response_path)
                earlier_response=read_npz(earlier_response_path)
                inputs.extend([previous_eval_path,old_source_path,old_response_path,earlier_response_path])
                consumed.update([previous_eval_path,old_source_path,old_response_path,earlier_response_path])
                diagnostic=status['source_differences'][variant]
                old_at=interpolate.interp1d(old_source['coordinate'],old_source['source'],axis=0)(current['coordinate'])
                difference=current['source']-old_at
                components=np.maximum(independent_dual(current['source'],basis).sum(axis=1),independent_dual(old_at,basis).sum(axis=1))
                expected=independent_dual(difference.sum(axis=1),basis)/np.maximum(components,1e-300)
                assert np.allclose(diagnostic['relative_to_components'],expected,rtol=1e-8,atol=0)
                refined_response=read_npz(packet_folder/f'{variant}-sites32-response.npz')
                for representation in ['control','sites32','collocated']:
                    source=read_npz(packet_folder/f'{variant}-{representation}-source.npz')
                    response=read_npz(packet_folder/f'{variant}-{representation}-response.npz')
                    reference=refined_response if representation=='collocated' else old_response
                    if representation!='collocated':
                        assert len(source['coordinate'])==138 and np.all(np.diff(source['coordinate'])>0)
                        selected=np.searchsorted(source['coordinate'],old_source['coordinate'])
                        for key,value in old_source.items():
                            if value.ndim>0 and value.shape[0]==122:
                                assert np.array_equal(source[key][selected],value),key
                        extra=np.ones(len(source['coordinate']),dtype=bool)
                        extra[selected]=False
                        assert np.count_nonzero(extra)==16
                        assert np.all(source['coordinate'][extra]<current['coordinate'][-1])
                        if representation=='control':
                            expected=interpolate.interp1d(old_source['coordinate'],old_source['source'],axis=0)(source['coordinate'])
                            assert np.array_equal(source['source'][extra],expected[extra])
                        else:
                            assert np.array_equal(source['source'][extra],fresh['source'][1:-1])
                    else:
                        start,end=old_source['coordinate'][[0,-1]]
                        sites=np.array([float(start+(end-start)*index/2048) for index in range(2049)])
                        assert np.array_equal(source['coordinate'],sites)
                        assert np.array_equal(source['source'][:33],current['source'])
                    assert np.array_equal(response['coordinate'],old_response['coordinate'])
                    assert len(response['coordinate'])==2049 and int(response['integration_steps'])==2048
                    assert np.array_equal(response['unresolved_change'],old_response['unresolved_change'])
                    assert bool(response['all_photon_steps_saved'])==(representation=='sites32')
                    if representation=='sites32':
                        assert np.array_equal(response['photon_final'],response['photon'][-1])
                    total=basis.values@response['photon_final'][:,:3]+response['unresolved_change']
                    assert np.array_equal(total,response['physical_change'])
                    scale=np.maximum((abs(response['energy'])+background.chi*abs(response['gas'])+abs(response['work'])).max(axis=0),1e-300)
                    assert np.max(abs(response['energy']+background.chi*response['gas']+response['work'])/scale)<1e-7
                    metric=status['comparisons'][variant][representation]['comparison']
                    delta=response['gas'][:,:3]-reference['gas'][:,:3]
                    assert np.array_equal(metric['gas_endpoint_signed_difference'],delta[-1])
                    for key,selection in [('gas_peak_relative',slice(None)),('gas_late_relative',slice(1536,None))]:
                        expected=abs(delta[selection]).max(axis=0)/np.maximum(abs(reference['gas'][selection,:3]).max(axis=0),1e-300)
                        assert np.allclose(metric[key],expected,atol=0,rtol=1e-12)
                    expected=abs(delta[-1])/np.maximum(abs(reference['gas'][-1,:3]),1e-300)
                    assert np.allclose(metric['gas_endpoint_relative'],expected,atol=0,rtol=1e-12)
                    radiation=norm(response['physical_change']-reference['physical_change'],basis.measure)/np.maximum(norm(reference['physical_change'],basis.measure),1e-300)
                    assert np.allclose(metric['radiation_relative'],radiation,atol=0,rtol=1e-12)
                    parts=np.stack([response['gas'][-1,offset:offset+3] for offset in [3,6,9]])
                    assert np.array_equal(metric['gas_endpoint_components'],parts)
                    if representation!='sites32':
                        assert max(metric['gas_peak_relative'])<1e-7 and max(metric['radiation_relative'])<1e-7
                    checks.append(dict(name='Independent source,component and response metrics:'+model+':'+str(upper)+':'+variant+':'+representation,passed=True))
                fine=refined_response['gas'][:,:3]-old_response['gas'][:,:3]
                coarse=old_response['gas'][:,:3]-earlier_response['gas'][:,:3]
                expected=abs(fine[-1])/np.maximum(abs(coarse[-1]),1e-300)
                assert np.allclose(status['convergence'][variant]['endpoint_difference_ratio'],expected,atol=0,rtol=1e-12)
                contract=read_npz(packet_folder/(variant+'-sampling-contract.npz'))
                sampled=independent_dual(contract['interpolated_forcing']-contract['direct_forcing'],basis)
                denominator=np.maximum(independent_dual(contract['direct_forcing'],basis).max(axis=0),1e-300)
                assert np.max(sampled/denominator)<1e-10
                null_at=interpolate.interp1d(contract['null_coordinate'],contract['null_values'])
                assert np.max(abs(null_at(contract['response_coordinate'][:33])))<1e-14
                assert np.max(contract['null_values'])==1.
                assert status['sampling'][variant]['remaining_unsupplied_initial_response_sites']==0
                assert not status['sampling'][variant]['physical_time_accuracy_certified']
                checks.append(dict(name='Complete32-site forcing and explicit sampling-nullspace:'+model+':'+str(upper)+':'+variant,passed=True))
            for representation in ['control','sites32','collocated']:
                assembled=read_npz(packet_folder/f'assembled-{representation}-response.npz')
                direct=read_npz(packet_folder/f'direct-{representation}-response.npz')
                assert np.array_equal(assembled['gas'][:,6:],direct['gas'][:,6:])
            checks.append(dict(name='Unchanged DC/BR responses:'+model+':'+str(upper),passed=True))
    attribution_path=ROOT/'results/site-attribution/status.json'
    attribution=json.loads(attribution_path.read_text())
    assert attribution['diagnostic_added_after_main_result'] and len(attribution['rows'])==4
    for row in attribution['rows']:
        model,upper=row['model'],row['upper']
        label=int(upper*1000)
        packet_folder=ROOT/'results'/f'sites-{model}-m{label}'
        source={key:read_npz(packet_folder/(key+'-source.npz')) for key in
            ['direct-sites32','direct-control','assembled-sites32','assembled-control']}
        response={key:read_npz(packet_folder/(key+'-response.npz')) for key in source}
        delta={key:read_npz(ROOT/'results/site-attribution'/f'{model}-m{label}-{key}.npz')
            for key in ['first','remaining','operator']}
        direct=source['direct-sites32']['source']-source['direct-control']['source']
        assembled=source['assembled-sites32']['source']-source['assembled-control']['source']
        assert np.array_equal(delta['first']['source']+delta['remaining']['source'],direct)
        assert np.array_equal(delta['operator']['source'],direct-assembled)
        assert not np.count_nonzero(delta['operator']['source'][:,1:])
        assert np.count_nonzero(np.any(delta['first']['source']!=0,axis=(1,2,3)))==1
        assert np.count_nonzero(np.any(delta['remaining']['source']!=0,axis=(1,2,3)))==15
        selected=int(np.flatnonzero(np.any(delta['first']['source']!=0,axis=(1,2,3)))[0])
        assert delta['first']['coordinate'][selected]==delta['first']['response_coordinate'][1]
        gas=response['direct-sites32']['gas']-response['direct-control']['gas']
        assembled_gas=response['assembled-sites32']['gas']-response['assembled-control']['gas']
        scale=np.maximum((abs(response['direct-sites32']['gas'])+abs(response['direct-control']['gas'])
            +abs(delta['first']['gas'])+abs(delta['remaining']['gas'])).max(axis=0),1e-300)
        error=float(np.max(abs(gas-delta['first']['gas']-delta['remaining']['gas'])/scale))
        assert error<1e-7 and np.isclose(error,row['first_rest_closure'],rtol=1e-12,atol=0)
        operator_scale=np.maximum((abs(response['direct-sites32']['gas'])+abs(response['direct-control']['gas'])
            +abs(response['assembled-sites32']['gas'])+abs(response['assembled-control']['gas'])
            +abs(delta['operator']['gas'])).max(axis=0),1e-300)
        operator_error=float(np.max(abs(gas-assembled_gas-delta['operator']['gas'])/operator_scale))
        assert operator_error<1e-7 and np.isclose(operator_error,row['operator_closure'],rtol=1e-12,atol=0)
        assert not np.count_nonzero(delta['operator']['gas'][:,6:])
        assert np.array_equal(row['direct_endpoint_increment'],gas[-1,:3])
        for split in ['first','remaining','operator']:
            assert np.array_equal(row[split+'_endpoint'],delta[split]['gas'][-1,:3])
        assert np.array_equal(row['first_signed_fraction'],delta['first']['gas'][-1,:3]/gas[-1,:3])
        assert np.array_equal(row['operator_signed_fraction'],delta['operator']['gas'][-1,:3]/gas[-1,:3])
        photon=response['direct-sites32']['photon_final']-response['direct-control']['photon_final']
        photon_error=photon-delta['first']['photon_final']-delta['remaining']['photon_final']
        denominator=np.maximum(photon_norm(response['direct-sites32']['photon_final'],basis.mass)
            +photon_norm(response['direct-control']['photon_final'],basis.mass)
            +photon_norm(delta['first']['photon_final'],basis.mass)
            +photon_norm(delta['remaining']['photon_final'],basis.mass),1e-300)
        assert np.max(photon_norm(photon_error,basis.mass)/denominator)<1e-7
        checks.append(dict(name='Independent first-site/operator gas and photon attribution:'+model+':'+str(upper),passed=True))
    chain=ancestors()
    parent=chain[PARENT/'results/stage-integrity.json']
    rehashed=set()
    for name,sha in parent['file_hashes'].items():
        path=PARENT/name
        assert hashed(path)==sha,path
        rehashed.add(path)
    for path in consumed:
        if not path.is_relative_to(ROOT):
            verify_source(path,chain)
            rehashed.add(path)
    inherited_count=sum(len(packet['file_hashes']) for packet in chain.values())
    assert inherited_count==205148
    documents=sorted(ROOT.glob('*.md'))
    for document in documents:
        for reference in re.findall(chr(96)+'([^'+chr(96)+']+)'+chr(96),document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.pdf')):
                assert (ROOT/reference).resolve().is_file(),reference
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    workbench=POST.parent/'formalization-workbench'
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert workbench.is_dir() and not changed,changed
    checks.append(dict(name='Parent,consumed sources,citations,capacity and protected-workbench scan',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=scientific-passing,retained_failure_names=failures,compiled_scripts=len(scripts),
        checked_science_packets=len(packets),accepted_scope_verified=True,largest_direct_file_count=maximum,
        inherited_payload_count=inherited_count,replayed_steps=1280,completed_backgrounds=['heavy','cold'],
        consumed_and_immediate_rehashed={str(path):hashed(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,ROOT/'ACCURACY-REVIEW.json',ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(science=scientific,passes=passing,failures=scientific-passing,
        validation_checks=len(checks),rehashed=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
