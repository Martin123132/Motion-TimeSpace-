from time_refinement_common import *
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
        path=ROOT/'results'/f'inner-{model}-n10240/prediction.npz'
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
            response_folder=ROOT/'results'/f'feedback-m{int(upper*1000)}-n10240'
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
    comparison=json.loads((ROOT/'results/time-comparison/status.json').read_text())
    assert comparison['inner_steps']==[5120,10240] and comparison['response_steps']==2048
    assert comparison['fixed_frequency_nodes']==5265 and comparison['source_epochs']==65
    assert len(comparison['rows'])==4 and len(comparison['window_rows'])==2
    for model in ['heavy','cold']:
        old_path=PARENT/'results'/f'inner-{model}-n5120/prediction.npz'
        new_path=ROOT/'results'/f'inner-{model}-n10240/prediction.npz'
        previous,current=read_npz(old_path),read_npz(new_path)
        inputs.extend([old_path,new_path])
        consumed.add(old_path)
        assert int(previous['steps'])==5120 and int(current['steps'])==10240
        for key in ['frequency','offsets','coefficient_knots','coefficient_bank','coordinate',
                'profiles','gas','outer_slope','lower_target']:
            assert np.array_equal(current[key],previous[key]),(model,key)
            checks.append(dict(name='Independent unchanged input:'+model+':'+key,passed=True))
    for row in comparison['rows']:
        model,upper=row['model'],row['upper']
        old_path=PARENT/'results'/f'feedback-m{int(upper*1000)}-n5120'/(model+'-response.npz')
        new_path=ROOT/'results'/f'feedback-m{int(upper*1000)}-n10240'/(model+'-response.npz')
        previous,current=read_npz(old_path),read_npz(new_path)
        inputs.extend([old_path,new_path])
        consumed.add(old_path)
        assert np.array_equal(previous['coordinate'],current['coordinate'])
        old_cache_path=old_path.parent/'source-cache.npz'
        new_cache_path=new_path.parent/'source-cache.npz'
        old_cache,new_cache=read_npz(old_cache_path),read_npz(new_cache_path)
        for key in old_cache:
            assert np.array_equal(old_cache[key],new_cache[key]),key
        inputs.extend([old_cache_path,new_cache_path])
        consumed.add(old_cache_path)
        checks.append(dict(name='Independent reused source cache:'+model+':'+str(upper),passed=True))
        old_gas,current_gas=previous['gas'][:,:3],current['gas'][:,:3]
        difference=current_gas-old_gas
        full_peak=np.max(abs(current_gas),axis=0)
        late_peak=np.max(abs(current_gas[1536:]),axis=0)
        endpoint=abs(current_gas[-1])
        expected={
            'gas_peak_relative_change':abs(difference).max(axis=0)/full_peak,
            'gas_late_relative_change':abs(difference[1536:]).max(axis=0)/late_peak,
            'gas_endpoint_relative_change':abs(difference[-1])/np.maximum(endpoint,1e-300),
            'gas_old_endpoint':old_gas[-1],'gas_new_endpoint':current_gas[-1],
            'gas_endpoint_difference':difference[-1],'gas_full_peak_denominator':full_peak,
            'gas_late_peak_denominator':late_peak,'gas_endpoint_denominator':endpoint,
            'gas_peak_absolute_difference':abs(difference).max(axis=0),
            'gas_late_absolute_difference':abs(difference[1536:]).max(axis=0),
            'final_radiation_relative_change':norm(current['physical_change']-previous['physical_change'],basis.measure)/norm(current['physical_change'],basis.measure)}
        old_inner=read_npz(PARENT/'results'/f'inner-{model}-n5120/prediction.npz')
        new_inner=read_npz(ROOT/'results'/f'inner-{model}-n10240/prediction.npz')
        old_defects=np.stack([compact_defect(basis.nodes,old_inner['frequency'],values,upper) for values in old_inner['defect']])
        new_defects=np.stack([compact_defect(basis.nodes,new_inner['frequency'],values,upper) for values in new_inner['defect']])
        expected['inner_peak_relative_change']=norm(new_defects-old_defects,basis.measure).max(axis=0)/norm(new_defects,basis.measure).max(axis=0)
        for name,values in expected.items():
            assert np.allclose(values,row[name],atol=0,rtol=1e-12),(name,row)
            checks.append(dict(name='Independent comparison:'+model+':'+str(upper)+':'+name,passed=True))
        assert row['gas_endpoint_near_zero']==(endpoint<=1e-6*full_peak).tolist()
        assert row['late_start_index']==1536
        assert row['late_start_coordinate']==float(current['coordinate'][1536])
        assert row['all_response_states_compared']==2049
        difference_path=ROOT/'results/time-comparison'/f'{model}-m{int(upper*1000)}-gas-difference.npz'
        difference_packet=read_npz(difference_path)
        assert np.array_equal(difference_packet['gas_difference'],difference)
        assert np.array_equal(difference_packet['gas_old'],old_gas)
        assert np.array_equal(difference_packet['gas_new'],current_gas)
        inputs.append(difference_path)
    for row in comparison['window_rows']:
        model=row['model']
        wide=read_npz(ROOT/'results/feedback-m40-n10240'/(model+'-response.npz'))
        narrow=read_npz(ROOT/'results/feedback-m20-n10240'/(model+'-response.npz'))
        assert np.allclose(row['radiation_window_difference_over_wide'],
            norm(narrow['physical_change']-wide['physical_change'],basis.measure)/norm(wide['physical_change'],basis.measure),atol=0,rtol=1e-12)
        assert np.allclose(row['gas_endpoint_narrow_over_wide'],narrow['gas'][-1,:3]/wide['gas'][-1,:3],atol=0,rtol=1e-12)
        checks.append(dict(name='Independent window comparison:'+model,passed=True))
    assert len(packets)==7
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
    assert inherited_count==204463,inherited_count
    checks.append(dict(name='Immediate parent and consumed dependencies unchanged',passed=True,rehashed=len(rehashed)))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Compilation,citations,bytecode and directory capacity',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=scientific-passing,retained_failure_names=failures,compiled_scripts=len(scripts),
        checked_science_packets=len(packets),accepted_scope_verified=True,largest_direct_file_count=maximum,
        new_precision_segments=0,previous_precision_scope_preserved=True,
        inherited_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        consumed_and_immediate_rehashed={str(path):hashed(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(science=scientific,passes=passing,failures=scientific-passing,validation_checks=len(checks),rehashed=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
