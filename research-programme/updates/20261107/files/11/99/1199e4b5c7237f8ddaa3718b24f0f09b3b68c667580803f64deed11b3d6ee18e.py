from inner_contraction_common import *
import re


def main():
    modest()
    folder=ROOT/'results/validation'
    assert not (ROOT/'results/stage-integrity.json').exists()
    assert not (folder/'status.json').exists()
    folder.mkdir(parents=True,exist_ok=True)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    script_hashes={digest(script) for script in scripts}
    inputs,consumed,checks=[],set(),[]
    hashes,failures={},{}
    scientific,passing=0,0
    def hashed(path):
        path=Path(path).resolve()
        if path not in hashes:
            hashes[path]=digest(path)
        return hashes[path]
    packets=sorted(path for path in (ROOT/'results').glob('*/status.json') if path.parent!=folder)
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').is_file()
        assert packet['script_sha256'] in script_hashes,path
        failed=[row['name'] for row in packet['checks'] if not row['passed']]
        assert failed==review['expected_failed_by_packet'].get(path.parent.name,[]),(path,failed)
        assert packet['count']==len(packet['checks']) and packet['all_checks_passed']==(not failed)
        if failed:
            failures[path.parent.name]=failed
        for source,sha in packet['input_hashes'].items():
            assert hashed(source)==sha,source
            consumed.add(Path(source))
        for archive in path.parent.glob('*.npz'):
            with np.load(archive) as saved:
                for key in saved.files:
                    if saved[key].dtype.kind not in ['U','S']:
                        assert np.isfinite(saved[key]).all(),(archive,key)
            inputs.append(archive)
        inputs.append(path)
        scientific+=packet['count']
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        checks.append(dict(name='Complete finite sourced packet:'+path.parent.name,passed=True))
    assert failures==review['expected_failed_by_packet']
    assert (scientific,passing)==(review['scientific_checks'],review['passing_scientific_checks'])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs.extend(ladder.inputs)
    consumed.update(ladder.inputs)
    for model in ['heavy','cold']:
        path=ROOT/'results'/f'inner-{model}-n20480/prediction.npz'
        saved=read_npz(path)
        assert len(saved['frequency'])==5265 and saved['frequency'][0]==basis.minimum
        assert len(saved['coordinate'])==65 and not np.count_nonzero(saved['defect'][0])
        baseline,window,history_inputs=load_histories(model)
        inputs.extend(history_inputs)
        consumed.update(history_inputs)
        driver,unused=make_drivers(basis,baseline,window,np.array([basis.minimum]),.1)
        margin=int(max(abs(saved['offsets'])))
        spacing=math.log(saved['frequency'][-1]/saved['frequency'][0])/(len(saved['frequency'])-1)
        ghosts=saved['frequency'][0]*np.exp(spacing*np.arange(-margin,0))
        for epoch,coordinate in enumerate(saved['coordinate']):
            coefficient=saved['coefficient_bank'][epoch]
            dc=coefficient[len(saved['offsets'])+1]/ghosts**2
            br=coefficient[len(saved['offsets'])+3:len(saved['offsets'])+3+margin]
            drive=driver(float(coordinate))[:,:3]
            target=(dc[:,None]*drive[1]+br[:,None]*drive[0])/(dc+br)[:,None]
            assert np.allclose(saved['lower_target'][epoch],target,rtol=1e-12,atol=0)
        checks.append(dict(name='Independent fixed grid and original lower-boundary law:'+model,passed=True))
        for upper in [.04,.02]:
            response_folder=ROOT/'results'/f'feedback-m{int(upper*1000)}-n20480'
            source=read_npz(response_folder/(model+'-source.npz'))
            response=read_npz(response_folder/(model+'-response.npz'))
            assert len(response['coordinate'])==2049 and np.array_equal(response['saved_step_indices'],np.arange(2049))
            replacement=compact_defect(basis.nodes,saved['frequency'],saved['defect'][-1],upper)
            assert np.allclose(source['replacement_moments'][-1],(basis.values.T*basis.measure)@replacement,rtol=1e-12,atol=0)
            total=basis.values@response['photon'][-1,:,:3]+replacement-basis.values@source['projected_replacement'][-1]
            assert np.max(norm(total-response['physical_change'],basis.measure)/norm(response['physical_change'],basis.measure))<1e-10
            background=thermal_wave.thermal.ThermalBackground(model)
            scale=np.maximum((abs(response['energy'])+background.chi*abs(response['gas'])+abs(response['work'])).max(axis=0),1e-300)
            assert np.max(abs(response['energy']+background.chi*response['gas']+response['work'])/scale)<1e-7
            checks.append(dict(name='Independent total radiation and paired energy bookkeeping:'+model+':'+str(upper),passed=True))
    comparison=json.loads((ROOT/'results/inner-contraction/status.json').read_text())
    assert comparison['inner_steps']==[5120,10240,20480] and comparison['response_steps']==2048
    assert comparison['fixed_frequency_nodes']==5265 and comparison['source_epochs']==65
    assert len(comparison['rows'])==4 and len(comparison['window_rows'])==2
    restart_count=0
    for model in ['heavy','cold']:
        current_path=ROOT/'results'/f'inner-{model}-n20480/prediction.npz'
        current=read_npz(current_path)
        for owner,steps in [(COARSE_PARENT,5120),(INNER_PARENT,10240)]:
            prior_path=owner/'results'/f'inner-{model}-n{steps}/prediction.npz'
            previous=read_npz(prior_path)
            inputs.append(prior_path)
            consumed.add(prior_path)
            assert int(previous['steps'])==steps and int(current['steps'])==20480
            for key in ['frequency','offsets','coefficient_knots','coefficient_bank','coordinate',
                    'profiles','gas','outer_slope','lower_target']:
                assert np.array_equal(current[key],previous[key]),(model,steps,key)
            checks.append(dict(name='All inner inputs fixed relative to:'+model+':'+str(steps),passed=True))
        records=sorted((current_path.parent/'checkpoints').glob('restart-*.json'))
        assert len(records)==9
        first_inputs=None
        for record_path in records:
            record=json.loads(record_path.read_text())
            archive=record_path.parent/record['archive']
            assert hashed(archive)==record['archive_sha256']
            assert record['script_sha256']==hashed(ROOT/'refine_inner_again.py')
            assert record['steps']==20480
            snapshot=read_npz(archive)
            completed=int(snapshot['completed_step'])
            assert completed==record['completed_step']
            assert completed in range(0,20481,2560)
            length=completed//320+1
            for key in ['coordinate','slope','outer_slope','defect','lower_target']:
                assert np.array_equal(snapshot['saved_'+key],current[key][:length]),(record_path,key)
            assert np.array_equal(snapshot['error'],snapshot['saved_defect'][-1])
            assert np.array_equal(snapshot['old_outer'],snapshot['saved_outer_slope'][-1])
            assert snapshot['previous_error'].shape==snapshot['error'].shape
            assert snapshot['older_outer'].shape==snapshot['old_outer'].shape
            assert all(np.isfinite(value).all() for value in snapshot.values())
            if first_inputs is None:
                first_inputs=record['input_hashes']
            assert record['input_hashes']==first_inputs
            for path,sha in record['input_hashes'].items():
                assert hashed(path)==sha,path
                consumed.add(Path(path))
            inputs.extend([archive,record_path])
            checks.append(dict(name='Complete restart state and saved-prefix identity:'+model+':'+str(completed),passed=True))
            restart_count+=1
    for row in comparison['rows']:
        model,upper=row['model'],row['upper']
        response_fields,inner_fields={},{}
        for label,owner,steps in [('coarse',COARSE_PARENT,5120),('previous',INNER_PARENT,10240),('refined',ROOT,20480)]:
            response_path=owner/'results'/f'feedback-m{int(upper*1000)}-n{steps}'/(model+'-response.npz')
            inner_path=owner/'results'/f'inner-{model}-n{steps}/prediction.npz'
            response_fields[label]=read_npz(response_path)
            inner=read_npz(inner_path)
            inner_fields[label]=np.stack([compact_defect(basis.nodes,inner['frequency'],value,upper) for value in inner['defect']])
            inputs.extend([response_path,inner_path])
            consumed.update([response_path,inner_path])
            assert int(response_fields[label]['integration_steps'])==2048
        coarse,previous,refined=[response_fields[label] for label in ['coarse','previous','refined']]
        assert np.array_equal(coarse['coordinate'],previous['coordinate'])
        assert np.array_equal(previous['coordinate'],refined['coordinate'])
        gases=[item['gas'][:,:3] for item in [coarse,previous,refined]]
        old_delta,new_delta=gases[1]-gases[0],gases[2]-gases[1]
        amplitudes={
            'gas_peak':[abs(values).max(axis=0) for values in gases],
            'gas_late':[abs(values[1536:]).max(axis=0) for values in gases],
            'gas_endpoint':[abs(values[-1]) for values in gases],
            'radiation':[norm(values['physical_change'],basis.measure) for values in [coarse,previous,refined]],
            'inner':[norm(inner_fields[label],basis.measure).max(axis=0) for label in ['coarse','previous','refined']]}
        differences={
            'gas_peak':(abs(old_delta).max(axis=0),abs(new_delta).max(axis=0)),
            'gas_late':(abs(old_delta[1536:]).max(axis=0),abs(new_delta[1536:]).max(axis=0)),
            'gas_endpoint':(abs(old_delta[-1]),abs(new_delta[-1])),
            'radiation':(norm(previous['physical_change']-coarse['physical_change'],basis.measure),
                norm(refined['physical_change']-previous['physical_change'],basis.measure)),
            'inner':(norm(inner_fields['previous']-inner_fields['coarse'],basis.measure).max(axis=0),
                norm(inner_fields['refined']-inner_fields['previous'],basis.measure).max(axis=0))}
        for metric,(old_difference,new_difference) in differences.items():
            relative=new_difference/np.maximum(amplitudes[metric][-1],1e-300)
            record=row['contractions'][metric]
            floor=100*np.finfo(float).eps*np.maximum(np.max(amplitudes[metric],axis=0),1e-300)
            resolved=old_difference>floor
            assert np.allclose(relative,row['relative_change'][metric],rtol=1e-12,atol=0)
            assert np.allclose(old_difference,record['old_absolute'],rtol=1e-12,atol=0)
            assert np.allclose(new_difference,record['new_absolute'],rtol=1e-12,atol=0)
            assert np.array_equal(resolved,record['denominator_resolved'])
            assert np.allclose(floor,record['resolution_floor'],rtol=1e-12,atol=0)
            for index in range(3):
                ratio=record['ratio'][index]
                order=record['effective_order'][index]
                if not resolved[index]:
                    assert ratio is None and order is None
                else:
                    assert np.isclose(ratio,new_difference[index]/old_difference[index],rtol=1e-12,atol=0)
                    if ratio>0:
                        assert np.isclose(order,-np.log2(ratio),rtol=1e-12,atol=1e-14)
                    else:
                        assert order is None
            checks.append(dict(name='Independent relative difference and absolute contraction:'+model+':'+str(upper)+':'+metric,passed=True))
        assert np.array_equal(row['gas_coarse_endpoint'],gases[0][-1])
        assert np.array_equal(row['gas_previous_endpoint'],gases[1][-1])
        assert np.array_equal(row['gas_refined_endpoint'],gases[2][-1])
        assert np.array_equal(row['gas_old_endpoint_increment'],old_delta[-1])
        assert np.array_equal(row['gas_new_endpoint_increment'],new_delta[-1])
        assert row['endpoint_increment_direction_preserved']==(np.sign(old_delta[-1])==np.sign(new_delta[-1])).tolist()
        assert row['endpoint_response_sign_preserved']==(np.sign(gases[1][-1])==np.sign(gases[2][-1])).tolist()
        assert row['endpoint_near_zero']==(amplitudes['gas_endpoint'][-1]<=1e-6*amplitudes['gas_peak'][-1]).tolist()
        assert row['compared_epochs']==2049 and row['late_start_index']==1536
        assert row['late_start_coordinate']==float(refined['coordinate'][1536])
        packet_path=ROOT/'results/inner-contraction'/f'{model}-m{int(upper*1000)}-gas-differences.npz'
        saved_difference=read_npz(packet_path)
        assert np.array_equal(saved_difference['old_difference'],old_delta)
        assert np.array_equal(saved_difference['new_difference'],new_delta)
        inputs.append(packet_path)
        old_cache=INNER_PARENT/'results'/f'feedback-m{int(upper*1000)}-n10240/source-cache.npz'
        new_cache=ROOT/'results'/f'feedback-m{int(upper*1000)}-n20480/source-cache.npz'
        saved_cache,current_cache=read_npz(old_cache),read_npz(new_cache)
        assert all(np.array_equal(saved_cache[key],current_cache[key]) for key in saved_cache)
        inputs.extend([old_cache,new_cache])
        consumed.add(old_cache)
        checks.append(dict(name='Fixed source operator and signed endpoint comparisons:'+model+':'+str(upper),passed=True))
    for row in comparison['window_rows']:
        model=row['model']
        wide=read_npz(ROOT/'results/feedback-m40-n20480'/(model+'-response.npz'))
        narrow=read_npz(ROOT/'results/feedback-m20-n20480'/(model+'-response.npz'))
        assert np.allclose(row['radiation_window_difference_over_wide'],
            norm(narrow['physical_change']-wide['physical_change'],basis.measure)/norm(wide['physical_change'],basis.measure),atol=0,rtol=1e-12)
        assert np.allclose(row['gas_endpoint_narrow_over_wide'],narrow['gas'][-1,:3]/wide['gas'][-1,:3],atol=0,rtol=1e-12)
        checks.append(dict(name='Independent window comparison:'+model,passed=True))
    assert restart_count==18 and len(packets)==7
    documents=sorted(ROOT.glob('*.md'))
    citations=set()
    for document in documents:
        for reference in re.findall(chr(96)+'([^'+chr(96)+']+)'+chr(96),document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.pdf')):
                path=(ROOT/reference).resolve()
                assert path.is_file(),(document,reference)
                citations.add(path)
                if not path.is_relative_to(ROOT):
                    consumed.add(path)
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
    assert inherited_count==204549,inherited_count
    checks.append(dict(name='Immediate parent and consumed dependencies unchanged',passed=True,rehashed=len(rehashed)))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Compilation,citations,bytecode and directory capacity',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=scientific-passing,retained_failure_names=failures,compiled_scripts=len(scripts),
        checked_science_packets=len(packets),accepted_scope_verified=True,largest_direct_file_count=maximum,
        new_precision_segments=0,previous_precision_scope_preserved=True,restart_snapshots_verified=restart_count,
        inherited_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        consumed_and_immediate_rehashed={str(path):hashed(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(science=scientific,passes=passing,failures=scientific-passing,validation_checks=len(checks),rehashed=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
