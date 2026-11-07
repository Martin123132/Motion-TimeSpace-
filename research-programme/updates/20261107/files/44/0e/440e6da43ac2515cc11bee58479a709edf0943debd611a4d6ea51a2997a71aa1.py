from shape_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    if folder.exists():
        assert not any(folder.iterdir()),'Validation output must be empty before a recovery run'
    else:
        folder.mkdir(parents=True,exist_ok=False)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    expected={name:set(values) for name,values in review['retained_failed_checks'].items()}
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    hashes={digest(path) for path in scripts}
    packets=[ROOT/'results'/name/'status.json' for name in ['decomposition','finite-band-controls','residual-readout']]
    checks,inputs,failures=[],[],[]
    scientific,passed=0,0
    consumed=set()
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').exists()
        assert packet['count']==len(packet['checks']) and packet['script_sha256'] in hashes
        missing={row['name'] for row in packet['checks'] if not row['passed']}
        name=path.parent.relative_to(ROOT).as_posix()
        assert missing==expected.get(name,set()),(name,missing)
        assert packet['all_checks_passed']==(not missing)
        for source,sha in packet['input_hashes'].items():
            assert digest(source)==sha,source
            consumed.add(Path(source))
        for data in path.parent.glob('*.npz'):
            with np.load(data) as saved:
                assert all(np.isfinite(saved[key]).all() for key in saved.files),(data,saved.files)
            inputs.append(data)
        scientific+=packet['count']
        passed+=sum(bool(row['passed']) for row in packet['checks'])
        failures.extend(dict(packet=name,test=test) for test in sorted(missing))
        checks.append(dict(name='Completed packet hashes,finite arrays and truthful failure record:'+name,passed=True))
        inputs.append(path)
    assert (scientific,passed,len(failures))==(308,305,3)
    raw,boundary,readout=[json.loads(path.read_text()) for path in packets]
    assert boundary['all_checks_passed'] and readout['all_checks_passed']
    assert boundary['failed_initial_zero_moment_assumption_corrected']
    assert not boundary['templates_changed'] and not boundary['thresholds_relaxed']
    checks.append(dict(name='Finite-band number-control error explained without changing spectra or thresholds',passed=True))
    for model in ['heavy','cold']:
        path=ROOT/'results/decomposition'/f'{model}-main-1024-canonical.npz'
        definition=ROOT/'results/decomposition/canonical700-definition.npz'
        with np.load(path) as data,np.load(definition) as grid:
            measure=grid['measure']
            distortion_power=np.sum(measure[:,None]*data['distortion']**2,axis=0)
            residual_power=np.sum(measure[:,None]*data['residual']**2,axis=0)
            joint_power=np.sum(measure[:,None]*data['joint']**2,axis=0)
            declared=raw['models'][model]['bands']['canonical700']
            assert np.max(abs(joint_power[:3]/distortion_power[:3]-np.array(declared['jointly_captured_squared_norm_fraction'])))<1e-12
            assert np.max(abs(residual_power[:3]/distortion_power[:3]+np.array(declared['jointly_captured_squared_norm_fraction'])-1))<1e-12
            fractions=np.array(readout['models'][model]['residual_squared_norm_fraction_by_bin'])
            assert fractions.shape==(6,3) and np.all(fractions>=0)
            assert np.max(abs(fractions.sum(axis=0)-1))<1e-8
            assert np.max(abs(fractions[:3].sum(axis=0)-readout['models'][model]['residual_squared_norm_below_point1']))<1e-12
        checks.append(dict(name='Independent norm fractions and fixed-template bin partition:'+model,passed=True))
    for key in ['source_evaluations']:
        assert raw[key]==0
    for key in ['evolution_rerun','physical_parameters_fitted','empirical_fit','instrument_metric',
                'new_physical_model','github_action','infrared_continuation_derived','later_time_transfer_derived',
                'continuum_error_bounded']:
        assert raw[key] is False and review[key] is False,key
    for key in ['same_readout_for_baseline_and_window','full_96_mode_input_retained','orthogonal_residual_retained',
                'mu_y_component_powers_not_added','restricted_band_uses_own_energy','primary_independent_energy_retained']:
        assert raw[key] is True and review[key] is True,key
    checks.append(dict(name='Matched baseline/correction comparison;no source rerun,fit or claimed outside-domain prediction',passed=True))
    documents=sorted(ROOT.glob('*.md'))
    citations=set()
    for document in documents:
        for reference in re.findall(chr(96)+'([^'+chr(96)+']+)'+chr(96),document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.f90')):
                target=(ROOT/reference).resolve()
                assert target.is_file(),(document,reference)
                citations.add(target)
    assert all(url in (ROOT/'SOURCES.md').read_text() for url in URLS)
    checks.append(dict(name='All cited local files and primary source URLs recorded',passed=True))
    chain=ancestors()
    rehashed=set()
    for seal in [PARENT/'results/stage-integrity.json',inherited.PARENT/'results/stage-integrity.json']:
        for name,sha in chain[seal]['file_hashes'].items():
            path=seal.parent.parent/name
            assert digest(path)==sha,path
            rehashed.add(path)
    for path in consumed:
        if not path.is_relative_to(ROOT):
            if path in chain:
                assert chain[path]['state']=='complete',path
            else:
                inherited.inherited.verify_reference(path,chain)
            rehashed.add(path)
    assert sum(len(packet['file_hashes']) for packet in chain.values())==202450
    checks.append(dict(name='Immediate38+48 payloads and consumed dependencies unchanged;prior seal links valid',
        rehashed_unique_files=len(rehashed),inherited_payload_count=202450,passed=True))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Scripts compile;no bytecode or temp writes;direct folder sizes below1000',value=maximum,passed=True))
    finish(folder,dict(checks=checks,checked_packets=3,scientific_checks=scientific,passing_scientific_checks=passed,
        retained_failed_scientific_checks=3,retained_failure_records=failures,compiled_scripts=len(scripts),
        largest_direct_file_count=maximum,local_citations=[str(path) for path in sorted(citations)],
        accepted_current_scope_verified=True,recorded_web_urls=URLS,
        inherited_payload_count=202450,prior_archive_full_rehash_performed=False,
        consumed_and_immediate_rehashed={str(path):digest(path) for path in sorted(rehashed)},
        prior_archive_verification_seal_sha256=PARENT_SEAL),__file__,
        [*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(scientific=scientific,passed=passed,retained=3,validation_checks=len(checks),
        prior_files_rehashed=len(rehashed),prior_archive_full_rehash=False)),flush=True)


if __name__=='__main__':
    main()

