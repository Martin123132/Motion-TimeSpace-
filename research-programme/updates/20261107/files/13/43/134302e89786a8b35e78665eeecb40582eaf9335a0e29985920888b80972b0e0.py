from overlap_common import *
import re


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text(encoding='utf-8'))
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    scripts_by_hash={digest(script):script for script in scripts}
    packets=sorted(path for path in (ROOT/'results').glob('*/status.json') if path.parent!=folder)
    inputs,consumed,checks=[],set(),[]
    hashes={}
    scientific,passing=0,0
    failures={}
    def checked_hash(path):
        path=Path(path).resolve()
        if path not in hashes:
            hashes[path]=digest(path)
        return hashes[path]
    for path in packets:
        packet=json.loads(path.read_text(encoding='utf-8'))
        assert packet['state']=='complete' and (path.parent/'COMPLETE').is_file()
        assert packet['script_sha256'] in scripts_by_hash,path
        failed=[row['name'] for row in packet['checks'] if not row['passed']]
        assert failed==review['expected_failed_by_packet'].get(path.parent.name,[]),(path,failed)
        assert packet['count']==len(packet['checks']) and packet['all_checks_passed']==(not failed)
        if failed:
            failures[path.parent.name]=failed
        for source,sha in packet['input_hashes'].items():
            assert checked_hash(source)==sha,source
            consumed.add(Path(source))
        for archive in path.parent.glob('*.npz'):
            with np.load(archive) as saved:
                for key in saved.files:
                    if saved[key].dtype.kind not in ['U','S']:
                        assert np.isfinite(saved[key]).all(),(archive,key)
            inputs.append(archive)
        inputs.append(path)
        scientific+=len(packet['checks'])
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        checks.append(dict(name='Complete packet,unchanged provenance,finite arrays:'+path.parent.name,passed=True))
    assert failures==review['expected_failed_by_packet']
    assert (scientific,passing)==(review['scientific_checks'],review['passing_scientific_checks'])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    inputs.extend(ladder.inputs)
    consumed.update(ladder.inputs)
    basis=ladder.basis
    for model in ['heavy','cold']:
        for case in sorted((ROOT/'results').glob(model+'-*/overlap.npz')):
            saved=read_npz(case)
            status=json.loads((case.parent/'status.json').read_text())
            assert status['future_inner_spectrum_used_as_driver'] is False
            assert saved['frequency'][0]<.01 and saved['frequency'][-1]>.04
            assert len(saved['coordinate'])==65
            assert np.count_nonzero(saved['defect_correction'][0])==0
            scale=np.maximum(np.max(abs(saved['defect_correction']),axis=(0,1)),1e-300)
            assert np.all(np.max(abs(saved['slope']-saved['outer_slope']-saved['defect_correction']),axis=(0,1))/scale<1e-8)
            assert np.all(np.min(saved['envelope'],axis=(0,1))>=-1e-10*scale)
            assert np.all(np.max(abs(saved['defect_correction'])-saved['envelope'],axis=(0,1))<=1e-10*scale)
            checks.append(dict(name='Independent saved envelope and defect equality:'+case.parent.name,passed=True))
        path=ROOT/'results/comparison'/f'{model}-fine-lo25-n5120.npz'
        saved=read_npz(path)
        full=saved['old_unresolved_delta']
        parts=saved['residual_unresolved_delta']+saved['bridge_unresolved_delta']
        scale=np.maximum(norm(full,basis.measure).max(axis=0),1e-300)
        assert np.max(norm(full-parts,basis.measure)/scale)<1e-9
        assert np.max(abs(np.einsum('fi,f,nfk->nik',basis.values,basis.measure,parts))/scale)<1e-9
        checks.append(dict(name='Independent complete window mismatch incl bridge:'+model,passed=True))
    for path in sorted((ROOT/'results').glob('balanced-*/overlap.npz')):
        saved=read_npz(path)
        status=json.loads((path.parent/'status.json').read_text())
        assert not status['positive_BE_envelope_claim']
        assert not status['future_inner_spectrum_used_as_driver']
        assert status['small_defect_only_evolved'] and status['new_scattering_events']==0
        assert len(saved['coordinate'])==65
        assert np.count_nonzero(saved['defect_correction'][0])==0
        scale=np.maximum(np.max(abs(saved['defect_correction']),axis=(0,1)),1e-300)
        assert np.all(np.max(abs(saved['slope']-saved['outer_slope']-saved['defect_correction']),axis=(0,1))/scale<1e-8)
        assert np.max(abs(saved['high_stencils'].sum(axis=1)))<1e-12
        readout=read_npz(path.parent/'readout.npz')
        total=readout['old_unresolved_delta']
        parts=readout['residual_unresolved_delta']+readout['bridge_unresolved_delta']
        scale=np.maximum(norm(total,basis.measure).max(axis=0),1e-300)
        assert np.max(norm(total-parts,basis.measure)/scale)<1e-9
        checks.append(dict(name='Independent balanced-state and complete mismatch checks:'+path.parent.name,passed=True))
    physical=json.loads((ROOT/'results/background-scattering/status.json').read_text())
    assert physical['exact_physical_shift_spot_check'] and physical['no_shift_deposition_in_reference']
    assert len(physical['rows'])==6 and physical['all_checks_passed']
    checks.append(dict(name='Physical-shift reference independently tests low/high-order background scattering',passed=True))
    planck=json.loads((ROOT/'results/planck-remainder/status.json').read_text())
    assert len(planck['rows'])==65 and len(planck['contrasts'])==6
    assert not planck['recoil_included'] and not planck['full_juttner_tail_certified']
    assert planck['new_thermal_events']==0
    for row in planck['contrasts']:
        assert np.array_equal(np.array(row['planck_change']),-np.array(row['opposite_gas_change']))
        assert np.max(row['bound_usage'])<=1+1e-10
    checks.append(dict(name='Finite-event Planck bound and opposite gas energy diagnostic',passed=True))
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
        assert checked_hash(path)==sha,path
        rehashed.add(path)
    for path in consumed:
        if not path.is_relative_to(ROOT):
            verify_source(path,chain)
            rehashed.add(path)
    inherited_count=sum(len(packet['file_hashes']) for packet in chain.values())
    assert inherited_count==203486,inherited_count
    checks.append(dict(name='Immediate parent,consumed sources and seal-chain verified',
        rehashed=len(rehashed),inherited_count=inherited_count,passed=True))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Compilation,citation paths,folder size and bytecode controls',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=scientific-passing,retained_failure_names=failures,compiled_scripts=len(scripts),
        checked_science_packets=len(packets),accepted_scope_verified=True,
        largest_direct_file_count=maximum,local_citations=[str(path) for path in sorted(citations)],
        inherited_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        consumed_and_immediate_rehashed={str(path):checked_hash(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(science=scientific,passes=passing,retained_failures=scientific-passing,
        validation_checks=len(checks),rehashed_prior_files=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
