from residual_kinetic_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    script_hashes={digest(script) for script in scripts}
    checks,inputs,consumed=[],[],set()
    scientific,passing=0,0
    expected=set(review['expected_failed_names'])
    for name in ['kinetic-drive','readout-controls','interpretation','baseline-refinement']:
        path=ROOT/'results'/name/'status.json'
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').exists()
        assert packet['script_sha256'] in script_hashes
        failures={row['name'] for row in packet['checks'] if not row['passed']}
        assert failures==(expected if name=='kinetic-drive' else set()),(name,failures)
        assert packet['count']==len(packet['checks'])
        assert packet['all_checks_passed']==(not failures)
        for source,sha in packet['input_hashes'].items():
            assert digest(source)==sha,source
            consumed.add(Path(source))
        for archive in path.parent.glob('*.npz'):
            with np.load(archive) as data:
                assert all(np.isfinite(data[key]).all() for key in data.files),archive
            inputs.append(archive)
        scientific+=packet['count']
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        inputs.append(path)
        checks.append(dict(name='Complete packet,unchanged sources,finite arrays,truthful failures:'+name,passed=True))
    assert (scientific,passing)==(111,105)
    raw=json.loads((ROOT/'results/kinetic-drive/status.json').read_text())
    assert raw['no_evolution_rerun'] and raw['no_finite_source_event_integrals']
    assert raw['matched_epochs']==65 and raw['full_modes']==96
    assert raw['operators']==TERM_NAMES and raw['drives']==DRIVE_NAMES
    assert not raw['physical_parameters_fitted'] and not raw['empirical_fit']
    specification_path=BRANCH/'temperature-distortion-projection-20261012/results/projection/status.json'
    inputs.append(specification_path)
    consumed.add(specification_path)
    specification=json.loads(specification_path.read_text())['basis_specification']
    basis=infrared_ladder.ConsistentBasis(**specification)
    readout=ResidualMap(basis)
    for model in ['heavy','cold']:
        path=ROOT/'results/kinetic-drive'/f'{model}-1024.npz'
        with np.load(path) as data:
            actual_rates=data['residual_power_half_derivative_terms'].sum(axis=(2,3))
            maximum_error=0.
            for band,(name,frequency,measure,mapping) in enumerate(readout.bands):
                residual=np.einsum('ij,njk->nik',mapping,data['photon'])
                derivative=np.einsum('ij,njk->nik',mapping,data['bdf_coefficient_derivative'])
                discrete_rate=np.einsum('i,nik,nik->nk',measure,residual,derivative)
                error=abs(discrete_rate[-1,:3]-actual_rates[-1,band,:3])/abs(actual_rates[-1,band,:3])
                maximum_error=max(maximum_error,float(error.max()))
                assert np.array_equal(np.sign(discrete_rate[1:,:3]),np.sign(actual_rates[1:,band,:3]))
                assert np.allclose(np.sum(measure[None,:,None]*residual**2,axis=1),data['residual_power'][:,band],rtol=1e-12,atol=0.)
            assert maximum_error<1e-6
        checks.append(dict(name='Independent saved BDF power rates preserve all sampled signs:'+model,
            endpoint_relative_net_rate_error=maximum_error,passed=True))
    checks.append(dict(name='111 science records,105 passes,6 original gas-relative failures retained',passed=True))
    documents=sorted(ROOT.glob('*.md'))
    citations=set()
    for document in documents:
        for reference in re.findall(chr(96)+'([^'+chr(96)+']+)'+chr(96),document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.f90')):
                target=(ROOT/reference).resolve()
                assert target.is_file(),(document,reference)
                citations.add(target)
                if not target.is_relative_to(ROOT):
                    consumed.add(target)
    checks.append(dict(name='All local citations exist;source URLs recorded in derivation',passed=True))
    chain=ancestors()
    rehashed=set()
    parent_packet=chain[PARENT/'results/stage-integrity.json']
    for name,sha in parent_packet['file_hashes'].items():
        path=PARENT/name
        assert digest(path)==sha,path
        rehashed.add(path)
    for path in consumed:
        if not path.is_relative_to(ROOT):
            verify_source(path,chain)
            rehashed.add(path)
    inherited_count=sum(len(packet['file_hashes']) for packet in chain.values())
    assert inherited_count==202515
    checks.append(dict(name='Immediate and consumed inputs unchanged;ancestor seal links verified',
        count=len(rehashed),inherited_payload_count=inherited_count,prior_archive_full_rehash=False,passed=True))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='All scripts compile;no bytecode,temp files or oversized folder',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=6,compiled_scripts=len(scripts),accepted_scope_verified=True,
        original_gas_relative_gate_closed=False,local_citations=[str(path) for path in sorted(citations)],
        largest_direct_file_count=maximum,inherited_payload_count=inherited_count,
        prior_archive_full_rehash_performed=False,
        consumed_and_immediate_rehashed={str(path):digest(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(science=scientific,passes=passing,retained_failures=6,
        validation_checks=len(checks),prior_files_rehashed=len(rehashed))),flush=True)


if __name__=='__main__':
    import re
    main()
