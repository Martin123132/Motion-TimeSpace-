from response_time_common import *
from audit_response_equations import physical_residuals,SELECTED
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
    comparison=json.loads((ROOT/'results/response-comparison/status.json').read_text())
    audit=json.loads((ROOT/'results/equation-audit/status.json').read_text())
    inner_comparison_path=PARENT/'results/time-comparison/status.json'
    inner_comparison=json.loads(inner_comparison_path.read_text())
    inputs.append(inner_comparison_path)
    consumed.add(inner_comparison_path)
    assert comparison['response_steps']==[2048,4096]
    assert comparison['fixed_inner_steps']==10240 and comparison['fixed_frequency_nodes']==5265
    assert comparison['source_epochs']==65 and len(comparison['rows'])==4
    assert audit['selected_steps']==SELECTED
    for row in comparison['rows']:
        model,upper=row['model'],row['upper']
        inner_path=PARENT/'results'/f'inner-{model}-n10240/prediction.npz'
        source_path=PARENT/'results'/f'feedback-m{int(upper*1000)}-n10240'/(model+'-source.npz')
        old_path=source_path.parent/(model+'-response.npz')
        new_path=ROOT/'results'/f'response-m{int(upper*1000)}-r4096'/(model+'-response.npz')
        inner,source,previous,current=[read_npz(path) for path in [inner_path,source_path,old_path,new_path]]
        inputs.extend([inner_path,source_path,old_path,new_path])
        consumed.update([inner_path,source_path,old_path])
        assert int(inner['steps'])==10240 and len(inner['frequency'])==5265
        assert np.array_equal(inner['coordinate'],source['coordinate']) and len(source['coordinate'])==65
        assert np.array_equal(source['profiles'],inner['profiles']) and np.array_equal(source['gas'],inner['gas'])
        assert np.array_equal(previous['coordinate'],current['coordinate'][::2])
        assert np.array_equal(current['saved_step_indices'],np.arange(4097))
        assert int(current['integration_steps'])==4096 and bool(current['all_steps_saved'])
        assert len(current['coordinate'])==4097 and len(previous['coordinate'])==2049
        for key in ['frequency','measure','replacement','unresolved_change','saved_potential','saved_residual']:
            assert np.array_equal(previous[key],current[key]),(model,upper,key)
        response_status=json.loads((new_path.parent/'status.json').read_text())
        for fixed in [inner_path,source_path]:
            assert response_status['input_hashes'][str(fixed.resolve())]==hashed(fixed)
        checks.append(dict(name='Source identity, fixed inner evolution, common epochs:'+model+':'+str(upper),passed=True))
        replacement=compact_defect(basis.nodes,inner['frequency'],inner['defect'][-1],upper)
        assert np.allclose(source['replacement_moments'][-1],(basis.values.T*basis.measure)@replacement,atol=0,rtol=1e-12)
        total=basis.values@current['photon'][-1,:,:3]+replacement-basis.values@source['projected_replacement'][-1]
        assert np.max(norm(total-current['physical_change'],basis.measure)/norm(current['physical_change'],basis.measure))<1e-10
        background=thermal_wave.thermal.ThermalBackground(model)
        scale=np.maximum((abs(current['energy'])+background.chi*abs(current['gas'])+abs(current['work'])).max(axis=0),1e-300)
        assert np.max(abs(current['energy']+background.chi*current['gas']+current['work'])/scale)<1e-7
        checks.append(dict(name='Physical readout and paired energy bookkeeping:'+model+':'+str(upper),passed=True))
        old_gas,new_gas=previous['gas'][:,:3],current['gas'][:,:3]
        difference=new_gas[::2]-old_gas
        full_peak=abs(new_gas).max(axis=0)
        late_peak=abs(new_gas[3072:]).max(axis=0)
        endpoint=abs(new_gas[-1])
        inner_row=next(item for item in inner_comparison['rows'] if item['model']==model and item['upper']==upper)
        expected={
            'radiation_relative_change':norm(current['physical_change']-previous['physical_change'],basis.measure)/norm(current['physical_change'],basis.measure),
            'gas_peak_relative_change':abs(difference).max(axis=0)/full_peak,
            'gas_late_relative_change':abs(difference[1536:]).max(axis=0)/late_peak,
            'gas_endpoint_relative_change':abs(difference[-1])/np.maximum(endpoint,1e-300),
            'gas_old_endpoint':old_gas[-1],'gas_new_endpoint':new_gas[-1],
            'gas_endpoint_difference':difference[-1],'gas_full_peak_denominator':full_peak,
            'gas_late_peak_denominator':late_peak,'gas_endpoint_denominator':endpoint,
            'gas_peak_absolute_difference':abs(difference).max(axis=0),
            'gas_late_absolute_difference':abs(difference[1536:]).max(axis=0),
            'gas_peak_amplitude_change_over_refined_peak':(abs(new_gas).max(axis=0)-abs(old_gas).max(axis=0))/full_peak,
            'response_over_inner_endpoint_change':abs(difference[-1])/np.maximum(abs(np.array(inner_row['gas_endpoint_difference'])),1e-300),
            'response_over_inner_peak_change':abs(difference).max(axis=0)/np.maximum(inner_row['gas_peak_absolute_difference'],1e-300),
            'response_endpoint_change_over_stage119_endpoint':abs(difference[-1])/np.maximum(abs(np.array(inner_row['gas_new_endpoint'])),1e-300),
            'inner_endpoint_change_over_stage119_endpoint':abs(np.array(inner_row['gas_endpoint_difference']))/np.maximum(abs(np.array(inner_row['gas_new_endpoint'])),1e-300)}
        for name,values in expected.items():
            assert np.allclose(row[name],values,rtol=1e-12,atol=0),(model,upper,name)
            checks.append(dict(name='Independent comparison:'+model+':'+str(upper)+':'+name,passed=True))
        assert row['gas_endpoint_near_zero']==(endpoint<=1e-6*full_peak).tolist()
        assert row['late_old_index']==1536 and row['late_new_index']==3072
        assert row['late_start_coordinate']==float(current['coordinate'][3072])
        assert row['compared_epochs']==2049 and row['refined_peak_epochs']==4097
        assert row['endpoint_sign_preserved']==(np.sign(old_gas[-1])==np.sign(new_gas[-1])).tolist()
        difference_path=ROOT/'results/response-comparison'/f'{model}-m{int(upper*1000)}-gas-difference.npz'
        differences=read_npz(difference_path)
        assert np.array_equal(differences['gas_difference'],difference)
        assert np.array_equal(differences['gas_new_all'],new_gas)
        inputs.append(difference_path)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend(emission.inputs)
        consumed.update(emission.inputs)
        regenerated=physical_residuals(current,source,ladder,emission,background)
        saved_audit=next(item for item in audit['rows'] if item['model']==model and item['upper']==upper)
        for regenerated_row,saved_row in zip(regenerated,saved_audit['records']):
            assert regenerated_row['step']==saved_row['step']
            for key in ['photon','gas','work']:
                assert np.allclose(regenerated_row[key],saved_row[key],rtol=1e-12,atol=1e-18)
        for key in ['photon','gas','work']:
            maximum=float(np.max([item[key] for item in regenerated]))
            assert np.isclose(maximum,saved_audit['maximum'][key],rtol=1e-12,atol=1e-18)
        checks.append(dict(name='Physical recurrence audit reproduced with failed flags retained:'+model+':'+str(upper),passed=True))
    for row in comparison['window_rows']:
        model=row['model']
        wide=read_npz(ROOT/'results/response-m40-r4096'/(model+'-response.npz'))
        narrow=read_npz(ROOT/'results/response-m20-r4096'/(model+'-response.npz'))
        assert np.allclose(row['radiation_window_difference_over_wide'],
            norm(narrow['physical_change']-wide['physical_change'],basis.measure)/norm(wide['physical_change'],basis.measure),atol=0,rtol=1e-12)
        assert np.allclose(row['gas_endpoint_narrow_over_wide'],narrow['gas'][-1,:3]/wide['gas'][-1,:3],atol=0,rtol=1e-12)
        checks.append(dict(name='Independent joining-window comparison:'+model,passed=True))
    assert len(packets)==6
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
    assert inherited_count==204512,inherited_count
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
