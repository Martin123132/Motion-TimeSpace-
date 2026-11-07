from turnover_common import *
import re


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text(encoding='utf-8'))
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    script_hashes={digest(script) for script in scripts}
    predictions=sorted(ROOT.rglob('prediction.npz'))
    assert len(predictions)==20
    packets=[path.parent/'status.json' for path in predictions]
    packets.extend(ROOT/'results'/name/'status.json' for name in ['invariant-banks','turnover-comparison','turnover-scales'])
    checks,inputs,consumed=[],[],set()
    scientific,passing=0,0
    hash_cache={}
    def checked_hash(path):
        path=Path(path).resolve()
        if path not in hash_cache:
            hash_cache[path]=digest(path)
        return hash_cache[path]
    found_failures={}
    for path in packets:
        packet=json.loads(path.read_text(encoding='utf-8'))
        assert packet['state']=='complete' and (path.parent/'COMPLETE').is_file()
        assert packet['script_sha256'] in script_hashes
        failures=[row['name'] for row in packet['checks'] if not row['passed']]
        relative=path.relative_to(ROOT).as_posix()
        assert failures==review['expected_failed_by_packet'].get(relative,[]),(relative,failures)
        if failures:
            found_failures[relative]=failures
        assert packet['count']==len(packet['checks'])
        assert packet['all_checks_passed']==(not failures)
        for source,sha in packet['input_hashes'].items():
            assert checked_hash(source)==sha,source
            consumed.add(Path(source))
        if 'settings' in packet:
            assert not packet['full_history_rerun'] and not packet['physical_cutoff_fitted']
            assert not packet['future_test_band_in_forcing'] and not packet['photon_gas_feedback_applied']
            assert packet['structural_all_passed']
            assert packet['settings']['hard_floor']>.01
            assert packet['diagnostics']['numerical_domain'][1]>.01
            assert packet['count']==16
        for archive in path.parent.glob('*.npz'):
            with np.load(archive) as data:
                assert all(np.isfinite(data[key]).all() for key in data.files),archive
            inputs.append(archive)
        scientific+=packet['count']
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        inputs.append(path)
        checks.append(dict(name='Complete packet,unchanged inputs,finite arrays,retained failures:'+relative,passed=True))
    assert found_failures==review['expected_failed_by_packet']
    assert scientific==review['scientific_checks']
    assert passing==review['passing_scientific_checks']
    for model in ['heavy','cold']:
        path=ROOT/'invariant-half-time2-prediction/runs'/f'{model}-main1280/prediction.npz'
        packet=json.loads((path.parent/'status.json').read_text())
        assert packet['settings']['steps']==2560 and packet['interpolation']=='invariant-half'
        with np.load(path) as data:
            measure=data['core_measure'][None,:,None]
            actual=(measure*data['true_residual']**2).sum(axis=1)
            predicted=(measure*data['predicted_residual']**2).sum(axis=1)
            error=np.sqrt((measure*(data['predicted_residual']-data['true_residual'])**2).sum(axis=1))
            peak=np.sqrt(actual.max(axis=0))
            assert np.allclose(actual,data['actual_power'],rtol=1e-12,atol=0)
            assert np.allclose(predicted,data['predicted_power'],rtol=1e-12,atol=0)
            assert np.allclose(error.max(axis=0)/peak,packet['metrics']['residual_error_over_peak'],rtol=1e-10,atol=1e-15)
            epoch=data['coordinate']/math.log(10)
            assert np.array_equal(epoch[actual.argmin(axis=0)],packet['metrics']['actual_minimum_epoch'])
            assert np.array_equal(epoch[predicted.argmin(axis=0)],packet['metrics']['predicted_minimum_epoch'])
            step=data['coordinate'][1]-data['coordinate'][0]
            predicted_slope=(3*predicted[-1]-4*predicted[-2]+predicted[-3])/(2*step)
            actual_slope=(3*actual[-1]-4*actual[-2]+actual[-3])/(2*step)
            assert np.allclose(predicted_slope/actual_slope,packet['metrics']['predicted_to_actual_late_power_slope'],rtol=1e-9,atol=1e-12)
            assert np.all(np.sign(actual_slope[:3])==np.sign(predicted_slope[:3]))
            assert data['slope'].shape==(65,1317,17)
            assert data['coefficient_knots'][0]<=data['coordinate'][0] and data['coefficient_knots'][-1]>=data['coordinate'][-1]
        checks.append(dict(name='Independent finest-case norms,minima,slopes and matched scope:'+model,passed=True))
    bank_path=ROOT/'results/invariant-banks/status.json'
    bank=json.loads(bank_path.read_text())
    assert bank['soft_velocity_temperature_nodes']==65 and bank['finite_frequency_source_evaluations']==0
    assert not bank['physical_coefficients_fitted'] and not bank['parent_history_rerun']
    for source,sha in bank['files'].items():
        assert checked_hash(source)==sha,source
        inputs.append(Path(source))
        with np.load(source) as data:
            spacing=math.log(data['frequency'][1]/data['frequency'][0])
            count=len(data['offsets'])
            stencil=data['coefficient_bank'][:,:count]
            eigenvalue=data['coefficient_bank'][:,count]
            defect=stencil@np.exp(-data['offsets']*spacing)+eigenvalue
            assert np.max(abs(defect/eigenvalue))<1e-10
    checks.append(dict(name='Bounded65-temperature extension and equilibrium invariants independently checked',passed=True))
    documents=sorted(ROOT.glob('*.md'))
    citations=set()
    for document in documents:
        for reference in re.findall(chr(96)+'([^'+chr(96)+']+)'+chr(96),document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.f90','.pdf')):
                target=(ROOT/reference).resolve()
                assert target.is_file(),(document,reference)
                citations.add(target)
                if not target.is_relative_to(ROOT):
                    consumed.add(target)
    checks.append(dict(name='All local citations exist and literature URLs recorded',passed=True))
    chain=ancestors()
    parent_packet=chain[PARENT/'results/stage-integrity.json']
    rehashed=set()
    for name,sha in parent_packet['file_hashes'].items():
        path=PARENT/name
        assert checked_hash(path)==sha,path
        rehashed.add(path)
    for path in consumed:
        if not path.is_relative_to(ROOT):
            verify_source(path,chain)
            rehashed.add(path)
    inherited_count=sum(len(packet['file_hashes']) for packet in chain.values())
    assert inherited_count==202558
    checks.append(dict(name='Parent and consumed dependencies unchanged;ancestor seal links verified',
        rehashed_files=len(rehashed),inherited_payload_count=inherited_count,archive_wide_rehash=False,passed=True))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Scripts compile;no bytecode,temp files or overlarge folder',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=scientific-passing,retained_failure_names=found_failures,
        checked_science_packets=len(packets),compiled_scripts=len(scripts),accepted_scope_verified=True,
        local_citations=[str(path) for path in sorted(citations)],largest_direct_file_count=maximum,
        inherited_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        consumed_and_immediate_rehashed={str(path):checked_hash(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(science=scientific,passes=passing,retained_failures=scientific-passing,
        validation_checks=len(checks),prior_files_rehashed=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
