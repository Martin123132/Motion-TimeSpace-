from repair_common import *
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
        assert packet['script_sha256'] in script_hashes,path
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
        checks.append(dict(name='Complete,unchanged,finite result packet:'+path.parent.name,passed=True))
    assert failures==review['expected_failed_by_packet']
    assert (scientific,passing)==(review['scientific_checks'],review['passing_scientific_checks'])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    inputs.extend(ladder.inputs)
    consumed.update(ladder.inputs)
    basis=ladder.basis
    for model in ['heavy','cold']:
        baseline,window,history_inputs=load_histories(model)
        inputs.extend(history_inputs)
        consumed.update(history_inputs)
        driver,normalization=make_drivers(basis,baseline,window,np.array([basis.minimum]),.1)
        for path in sorted((ROOT/'results').glob(f'inner-{model}-*/prediction.npz')):
            saved=read_npz(path)
            status=json.loads((path.parent/'status.json').read_text())
            assert saved['frequency'][0]==basis.minimum and saved['frequency'][-1]>.05
            assert len(saved['coordinate'])==65 and not np.count_nonzero(saved['defect'][0])
            assert status['physical_lower_target_retained'] and status['saved_high_exterior_retained']
            assert status['boundary_order_reduction_maximum_frequency']<2e-5
            spacing=math.log(saved['frequency'][1]/saved['frequency'][0])
            margin=int(max(abs(saved['offsets'])))
            ghost=saved['frequency'][0]*np.exp(spacing*np.arange(-margin,0))
            bank_at=interpolate.interp1d(saved['coefficient_knots'],saved['coefficient_bank'],axis=0,bounds_error=True)
            outer_values=basis.evaluate(saved['frequency'])/saved['frequency'][:,None]
            outer_output_difference=0.
            outer_roundoff_usage=0.
            for epoch,position in enumerate(saved['coordinate']):
                coefficients=bank_at(position)
                count=len(saved['offsets'])
                dc=coefficients[count+1]/ghost**2
                br=coefficients[count+3:count+3+margin]
                drives=driver(float(position))[:,:3]
                target=(dc[:,None]*drives[1]+br[:,None]*drives[0])/(dc+br)[:,None]
                assert np.allclose(saved['lower_target'][epoch],target,rtol=1e-12,atol=0)
                outer=outer_values@saved['profiles'][epoch]
                scale=np.maximum(abs(outer).max(axis=0),1e-300)
                difference=abs(saved['outer_slope'][epoch]-outer)
                outer_output_difference=max(outer_output_difference,float(np.max(difference/scale)))
                operand=abs(outer_values)@abs(saved['profiles'][epoch])
                allowance=128*np.finfo(float).eps*np.maximum(operand,1e-300)
                usage=float(np.max(difference/allowance))
                outer_roundoff_usage=max(outer_roundoff_usage,usage)
                assert usage<=1.,(path,epoch,usage)
            scale=np.maximum(abs(saved['slope']).max(axis=(0,1)),1e-300)
            assert np.max(abs(saved['slope']-saved['outer_slope']-saved['defect'])/scale)<1e-12
            checks.append(dict(name='Independent original boundary,outer driver and defect check:'+path.parent.name,
                maximum_alternative_outer_output_relative_difference=outer_output_difference,
                maximum_dot_roundoff_allowance_usage=outer_roundoff_usage,passed=True))
    for path in sorted((ROOT/'results').glob('sources-*/status.json')):
        packet=json.loads(path.read_text())
        assert packet['stored_small_defect_used'] and packet['dc_br_recalculated'] and not packet['joining_term_discarded']
        for model in ['heavy','cold']:
            saved=read_npz(path.parent/(model+'.npz'))
            inner=read_npz(ROOT/'results'/str(saved['inner_packet'])/'prediction.npz')
            raw=compact_defect(basis.nodes,inner['frequency'],inner['defect'][-1],float(saved['match_upper']))
            moment=(basis.values.T*basis.measure)@raw
            assert np.allclose(saved['replacement_moments'][-1],moment,rtol=1e-12,atol=0)
            scale=np.maximum(abs(saved['raw_source']).max(axis=(0,1,2))+abs(saved['overlap_source']).max(axis=(0,1,2)),1e-300)
            assert np.max(abs(saved['source']-saved['raw_source']+saved['overlap_source'])/scale)<1e-12
        checks.append(dict(name='Independent direct-defect moments and represented subtraction:'+path.parent.name,passed=True))
    for path in sorted((ROOT/'results').glob('response-*/status.json')):
        packet=json.loads(path.read_text())
        assert packet['paired_gas_exchange'] and packet['expansion_work_included'] and not packet['parent_history_rerun']
        assert packet['residuals_checked_every_step'] and packet['saved_snapshots_not_adjacent_steps']
        for model in ['heavy','cold']:
            saved=read_npz(path.parent/(model+'.npz'))
            assert len(saved['coordinate'])==129 and saved['saved_step_indices'][-1]==packet['steps']
            assert np.allclose(saved['physical_change'],saved['resolved_change']+saved['unresolved_change'],rtol=1e-12,atol=0)
            background=thermal_wave.thermal.ThermalBackground(model)
            energy_scale=np.maximum((abs(saved['energy'])+background.chi*abs(saved['gas'])+abs(saved['work'])).max(axis=0),1e-300)
            assert np.max(abs(saved['energy']+background.chi*saved['gas']+saved['work'])/energy_scale)<1e-7
        checks.append(dict(name='Independent radiation readout,paired gas and expansion-work ledger:'+path.parent.name,passed=True))
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
    assert inherited_count==203591,inherited_count
    checks.append(dict(name='Immediate parent,consumed sources and seal chain verified',rehashed=len(rehashed),inherited_count=inherited_count,passed=True))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Compilation,citations,folder size and bytecode controls',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=scientific-passing,retained_failure_names=failures,compiled_scripts=len(scripts),
        checked_science_packets=len(packets),accepted_scope_verified=True,largest_direct_file_count=maximum,
        local_citations=[str(path) for path in sorted(citations)],inherited_payload_count=inherited_count,
        prior_archive_full_rehash_performed=False,
        consumed_and_immediate_rehashed={str(path):checked_hash(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(science=scientific,passes=passing,retained_failures=scientific-passing,validation_checks=len(checks),rehashed_prior_files=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
