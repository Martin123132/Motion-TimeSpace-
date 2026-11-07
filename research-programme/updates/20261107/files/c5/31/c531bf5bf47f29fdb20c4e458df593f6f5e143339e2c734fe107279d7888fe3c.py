from join_common import *
import re


def main():
    modest()
    folder=ROOT/'results/validation'
    if folder.exists():
        assert not any(folder.iterdir()),folder
    folder.mkdir(parents=True,exist_ok=True)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text(encoding='utf-8'))
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    script_hashes={digest(script) for script in scripts}
    packets=sorted(path for path in (ROOT/'results').glob('*/status.json') if path.parent!=folder)
    checks,inputs,consumed=[],[],set()
    scientific,passing=0,0
    found={}
    hashes={}
    def checked_hash(path):
        path=Path(path).resolve()
        if path not in hashes:
            hashes[path]=digest(path)
        return hashes[path]
    for path in packets:
        packet=json.loads(path.read_text(encoding='utf-8'))
        assert packet['state']=='complete' and (path.parent/'COMPLETE').is_file()
        assert packet['script_sha256'] in script_hashes,path
        failures=[row['name'] for row in packet['checks'] if not row['passed']]
        assert failures==review['expected_failed_by_packet'].get(path.parent.name,[]),(path,failures)
        if failures:
            found[path.parent.name]=failures
        assert packet['count']==len(packet['checks']) and packet['all_checks_passed']==(not failures)
        for source,sha in packet['input_hashes'].items():
            assert checked_hash(source)==sha,source
            consumed.add(Path(source))
        for archive in path.parent.glob('*.npz'):
            with np.load(archive) as data:
                for key in data.files:
                    if data[key].dtype.kind not in ['U','S']:
                        assert np.isfinite(data[key]).all(),(archive,key)
            inputs.append(archive)
        inputs.append(path)
        scientific+=packet['count']
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        checks.append(dict(name='Complete packet,unchanged inputs,finite arrays,truthful gates:'+path.parent.name,passed=True))
    assert found==review['expected_failed_by_packet']
    assert (scientific,passing)==(review['scientific_checks'],review['passing_scientific_checks'])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    consumed.update(ladder.inputs)
    inputs.extend(ladder.inputs)
    for source_folder in sorted((ROOT/'results').glob('sources-*')):
        status=json.loads((source_folder/'status.json').read_text())
        for upper in UPPERS:
            for model in ['heavy','cold']:
                source=read_npz(source_folder/f'{model}-m{int(upper*1000)}.npz')
                old_label=f"fine-o{status['event_order']}-q{status['source_panel_order']}-m40" if upper==.04 else 'fine-o6-q32-m20'
                parent_path=PARENT/'results'/('sources-'+old_label)/(model+'.npz')
                parent=read_npz(parent_path)
                consumed.add(parent_path)
                for key in ['overlap_source','projected_replacement','replacement_moments','profiles','gas']:
                    assert np.array_equal(source[key],parent[key]),(source_folder,key)
                assert np.array_equal(source['raw_source'][:,1:],parent['raw_source'][:,1:])
                total=source['source'].sum(axis=1)
                expected=source['physical_process_source'].sum(axis=1)
                scale=np.maximum(np.linalg.norm(source['source'],axis=2).sum(axis=1)+np.linalg.norm(source['physical_process_source'],axis=2).sum(axis=1),1e-300)
                assert np.max(np.linalg.norm(total-expected,axis=1)/scale)<1e-10
                assert np.count_nonzero(source['source'][0])==0
                assert np.count_nonzero(np.einsum('i,ntik->ntk',basis.chemical,source['source'][:,:2]))==0
        checks.append(dict(name='Independent source regrouping,number and unchanged parent arrays:'+source_folder.name,passed=True))
    identities=json.loads((ROOT/'results/identities/status.json').read_text())
    equal_test=[row for row in identities['rows'] if row['h_degree']==row['test_degree']]
    assert equal_test and all(row['bulk']<=0 for row in equal_test)
    assert (ROOT/'DISSIPATION-CLARIFICATION.md').is_file()
    checks.append(dict(name='Corrected bulk dissipation statement checked for matching test functions',passed=True))
    independent={}
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        consumed.update([background.parent.source,background.native_constants])
        for upper in UPPERS:
            label=f'{model}-m{int(upper*1000)}'
            response=read_npz(ROOT/'results'/review['authoritative_response_packet']/(label+'.npz'))
            parts=[basis.values@response['photon'][-1,:,offset:offset+3] for offset in [3,6,9]]
            reconstructed=sum(parts)+response['unresolved_change']
            scale=np.maximum(sum(np.linalg.norm(part,axis=0) for part in parts)+np.linalg.norm(response['unresolved_change'],axis=0),1e-300)
            assert np.max(np.linalg.norm(reconstructed-response['physical_change'],axis=0)/scale)<1e-10
            balance=response['energy']+background.chi*response['gas']+response['work']
            denominator=np.maximum((abs(response['energy'])+background.chi*abs(response['gas'])+abs(response['work'])).max(axis=0),1e-300)
            value=float(np.max(abs(balance)/denominator))
            assert value<1e-7
            independent[label]=dict(energy_work_relative=value)
            checks.append(dict(name='Independent spectral contributions and energy-work:'+label,passed=True))
    documents=sorted(ROOT.glob('*.md'))
    citations=set()
    for document in documents:
        for reference in re.findall(chr(96)+'([^'+chr(96)+']+)'+chr(96),document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.pdf','.f90')):
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
        assert checked_hash(path)==sha,path
        rehashed.add(path)
    for path in consumed:
        if not path.is_relative_to(ROOT):
            verify_source(path,chain)
            rehashed.add(path)
    inherited_count=sum(len(packet['file_hashes']) for packet in chain.values())
    assert inherited_count==203164
    checks.append(dict(name='Immediate parent,consumed dependencies and seal-chain verified',rehashed=len(rehashed),inherited_count=inherited_count,passed=True))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Compilation,local citations,folder size and bytecode controls',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=scientific-passing,retained_failure_names=found,compiled_scripts=len(scripts),
        checked_science_packets=len(packets),accepted_scope_verified=True,independent_readout=independent,
        largest_direct_file_count=maximum,local_citations=[str(path) for path in sorted(citations)],
        inherited_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        consumed_and_immediate_rehashed={str(path):checked_hash(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(science=scientific,passes=passing,retained_failures=scientific-passing,
        validation_checks=len(checks),rehashed_prior_files=len(rehashed))),flush=True)


if __name__=='__main__':
    main()

