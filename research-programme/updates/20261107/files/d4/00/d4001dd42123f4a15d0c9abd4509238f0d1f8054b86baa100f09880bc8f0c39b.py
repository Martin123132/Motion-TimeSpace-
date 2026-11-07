from matched_feedback_common import *
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
    assert len(packets)==20
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
        assert packet['script_sha256'] in script_hashes
        failures=[row['name'] for row in packet['checks'] if not row['passed']]
        assert failures==review['expected_failed_by_packet'].get(path.parent.name,[]),(path,failures)
        if failures:
            found[path.parent.name]=failures
        assert packet['count']==len(packet['checks'])
        assert packet['all_checks_passed']==(not failures)
        for source,sha in packet['input_hashes'].items():
            assert checked_hash(source)==sha,source
            consumed.add(Path(source))
        for archive in path.parent.glob('*.npz'):
            with np.load(archive) as data:
                for key in data.files:
                    value=data[key]
                    if value.dtype.kind not in ['U','S']:
                        assert np.isfinite(value).all(),(archive,key)
            inputs.append(archive)
        inputs.append(path)
        scientific+=packet['count']
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        checks.append(dict(name='Complete packet,unchanged inputs,finite arrays,truthful failures:'+path.parent.name,passed=True))
    assert found==review['expected_failed_by_packet']
    assert (scientific,passing)==(review['scientific_checks'],review['passing_scientific_checks'])==(250,232)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    consumed.update(ladder.inputs)
    inputs.extend(ladder.inputs)
    maxima={}
    for model in ['heavy','cold']:
        source_path=ROOT/'results/sources-fine-q32-m40'/(model+'.npz')
        response_path=ROOT/'results/response-fine-q32-m40-n1024'/(model+'.npz')
        status=json.loads((response_path.parent/'status.json').read_text())
        with np.load(source_path) as source,np.load(response_path) as response:
            assert np.array_equal(source['source'],source['raw_source']-source['overlap_source'])
            assert np.count_nonzero(source['source'][0])==0
            reconstructed_moments=np.einsum('ij,njk->nik',basis.mass,source['projected_replacement'])
            moment_residual=np.linalg.norm(reconstructed_moments-source['replacement_moments'],axis=1)
            moment_operands=np.linalg.norm(reconstructed_moments,axis=1)+np.linalg.norm(source['replacement_moments'],axis=1)
            assert np.max(moment_residual/np.maximum(moment_operands,1e-300))<1e-10
            assert np.allclose(response['physical_change'],response['resolved_change']+response['unresolved_change'],rtol=1e-12,atol=0.)
            assert np.allclose(response['resolved_change'],basis.values@response['photon'][-1,:,:3],rtol=1e-12,atol=0.)
            norm=lambda value:np.sqrt((response['measure'][:,None]*value**2).sum(axis=0))
            metrics=status['models'][model]['metrics']
            expected=norm(response['physical_change'])/norm(response['saved_potential'])
            assert np.allclose(expected,metrics['final_photon_change_over_saved_norm'],rtol=1e-12)
            background=thermal_wave.thermal.ThermalBackground(model)
            inputs.extend([background.parent.source,background.native_constants])
            consumed.update([background.parent.source,background.native_constants])
            balance=response['energy']+background.chi*response['gas']+response['work']
            denominator=np.maximum((abs(response['energy'])+background.chi*abs(response['gas'])+abs(response['work'])).max(axis=0),1e-300)
            value=float(np.max(abs(balance)/denominator))
            assert value<3e-14,value
            source_energy=np.einsum('i,nik->nk',basis.temperature,source['raw_source'][:,1])
            source_scale=np.maximum(np.einsum('i,nik->nk',abs(basis.temperature),abs(source['raw_source'][:,1])),1e-300)
            assert np.max(abs(source_energy)/source_scale)<1e-10
            maxima[model]=dict(energy_work_relative=value,final_relative_change=expected.tolist())
        checks.append(dict(name='Independent matched subtraction,stored moments,final spectrum and energy balance:'+model,passed=True))
    for model in ['heavy','cold']:
        path=ROOT/'results/transport-attribution/status.json'
        result=json.loads(path.read_text())['models'][model]
        assert min(result['transport_only']['over_fine_response'])>1
        assert min(result['profile_only']['over_fine_response'])>1
    checks.append(dict(name='Net amplitude not promoted despite dominant transport/profile sensitivity',passed=True))
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
    assert inherited_count==202673
    checks.append(dict(name='Immediate parent,consumed dependencies and ancestor seal links verified',rehashed=len(rehashed),inherited_count=inherited_count,passed=True))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Compilation,local citations,folder size and bytecode controls pass',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=scientific-passing,retained_failure_names=found,compiled_scripts=len(scripts),
        checked_science_packets=len(packets),accepted_scope_verified=True,gas_relative_gate_closed=False,
        net_physical_shift_precision_established=False,independent_readout=maxima,
        largest_direct_file_count=maximum,local_citations=[str(path) for path in sorted(citations)],
        inherited_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        consumed_and_immediate_rehashed={str(path):checked_hash(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(science=scientific,passes=passing,retained_failures=scientific-passing,
        validation_checks=len(checks),rehashed_prior_files=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
