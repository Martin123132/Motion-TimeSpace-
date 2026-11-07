from projection_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    expected={name:set(values) for name,values in review['retained_failed_checks'].items()}
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    hashes={digest(script) for script in scripts}
    checks,inputs,failures=[],[],[]
    scientific,passed=0,0
    statuses=[ROOT/'results/projection/status.json',ROOT/'results/stable-readout/status.json']
    for path in statuses:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').exists()
        assert packet['count']==len(packet['checks']) and packet['script_sha256'] in hashes
        missed={row['name'] for row in packet['checks'] if not row['passed']}
        name=path.parent.relative_to(ROOT).as_posix()
        assert missed==expected.get(name,set()),(name,missed)
        assert packet['all_checks_passed']==(not missed)
        for source,sha in packet['input_hashes'].items():
            assert digest(source)==sha,source
        scientific+=packet['count']
        passed+=sum(bool(row['passed']) for row in packet['checks'])
        failures.extend(dict(packet=name,test=test) for test in sorted(missed))
        for data in path.parent.glob('*.npz'):
            with np.load(data) as saved:
                assert all(np.isfinite(saved[key]).all() for key in saved.files)
            inputs.append(data)
        checks.append(dict(name='Completed packet hashes and truthful failure ledger:'+name,passed=True))
        inputs.append(path)
    raw=json.loads(statuses[0].read_text())
    stable=json.loads(statuses[1].read_text())
    assert stable['all_checks_passed'] and not stable['thresholds_relaxed']
    assert stable['stable_pointwise_readout_authoritative'] and stable['old_float64_pointwise_readout_retained']
    assert scientific==174 and passed==171 and len(failures)==3
    for model in ['heavy','cold']:
        value=stable['models'][model]['template_floating_coefficient_defect_relative']
        assert value<1e-11
        checks.append(dict(name='High precision temperature basis passes original1e-11 relative gate:'+model,value=value,passed=True))
        projected_path=ROOT/'results/projection'/f'{model}-main-1024-projected.npz'
        source_path=PARENT/'results/window-transfer'/f'{model}-main-1024.npz'
        with np.load(projected_path) as projected,np.load(source_path) as source,np.load(ROOT/'results/projection/projection-definition.npz') as definition:
            capacity=float(definition['energy_capacity'])
            expected_eta=source['energy'][-1]/capacity
            assert np.array_equal(expected_eta,projected['eta'])
            assert np.array_equal(source['photon'][-1],projected['photon'])
            for key in ['gas','work','number']:
                assert np.array_equal(source[key][-1],projected[key]),key
            heat=raw['models'][model]['metadata']['heat']
            claimed=np.array(raw['models'][model]['cases']['main-1024']['fractional_temperature'])
            assert np.array_equal(claimed,heat*expected_eta)
            check_energy=np.array([math.fsum(float(coefficient)*float(value) for coefficient,value in zip(definition['energy_row'],column)) for column in projected['distortion'].T])
            assert np.max(abs(check_energy)/projected['cancellation_allowance'])<1
            assert np.max(abs(projected['distortion']+projected['temperature']-source['photon'][-1]))<1e-18
        checks.append(dict(name='Independent saved-state, physical chi and compensated residual-energy crosscheck:'+model,passed=True))
    for key in ['physical_source_recomputed','new_empirical_fit','new_evolution','source_continuum_error_bounded',
                'infrared_increment_continuation_computed','outside_window_source_assumed_zero','current_epoch_today',
                'instrument_temperature_fit','github_action']:
        assert review[key] is False and raw[key] is False,key
    assert review['source_evaluations']==0 and review['kinetic_modes_discarded']==0
    checks.append(dict(name='Scoped known window and represented band;no physical fit,extra integration or mode deletion',passed=True))
    documents=[ROOT/name for name in ['RESULTS.md','DERIVATION.md','SOURCES.md','RESUME.md','DEVELOPMENT-NOTES.md','STABLE-READOUT.md','ACCEPTANCE.md']]
    citations=set()
    for document in documents:
        for reference in re.findall(chr(96)+'([^'+chr(96)+']+)'+chr(96),document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.f90')):
                target=(ROOT/reference).resolve()
                assert target.is_file(),(document,reference)
                citations.add(target)
    source_text=(ROOT/'SOURCES.md').read_text()
    assert all(url in source_text for url in URLS)
    checks.append(dict(name='Every cited local file exists and primary web URLs recorded',passed=True))
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SEAL
    for name,sha in parent['file_hashes'].items():
        assert digest(PARENT/name)==sha,name
    checks.append(dict(name='All48 Stage107 payloads and seal unchanged',passed=True))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    assert not (ROOT/'virtual-cache').exists()
    checks.append(dict(name='Scripts compile;no bytecode,temp files or source cache;folder sizes safe',value=maximum,passed=True))
    finish(folder,dict(checks=checks,checked_packets=2,scientific_checks=scientific,passing_scientific_checks=passed,
        retained_failed_scientific_checks=scientific-passed,retained_failure_records=failures,
        compiled_scripts=len(scripts),largest_direct_file_count=maximum,local_citations=[str(path) for path in sorted(citations)],
        accepted_current_scope_verified=True,recorded_web_urls=URLS,
        authority=dict(coefficient_projection=str(statuses[0]),physical_readout=str(statuses[1]))),
        __file__,[*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(packets=2,scientific=scientific,passed=passed,retained_failures=3,validation_checks=len(checks))),flush=True)


if __name__=='__main__':
    main()

