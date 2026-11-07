from interpolation_common import *
import re


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        if path not in hashes:
            hashes[path]=digest(path)
        return hashes[path]
    consumed,inputs,checks=set(),[],[]
    failed={}
    science=passing=0
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    consumed.update(ladder.inputs)
    for path in sorted((ROOT/'results').glob('case-*/status.json')):
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').exists()
        assert packet['script_sha256']==hashed(ROOT/'evaluate_interpolation.py')
        names=[row['name'] for row in packet['checks'] if not row['passed']]
        assert all(name.startswith('Factored1percent:') or (name.startswith('Response:') and name.endswith(':gas')) for name in names),names
        if names:
            failed[path.parent.name]=names
        science+=len(packet['checks'])
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        assert packet['count']==len(packet['checks']) and packet['all_checks_passed']==(not names)
        for name,sha in packet['input_hashes'].items():
            assert hashed(name)==sha,name
            consumed.add(Path(name))
        archives={archive.stem:read_npz(archive) for archive in path.parent.glob('*.npz')}
        assert all(np.isfinite(value).all() for archive in archives.values() for value in archive.values() if value.dtype.kind not in ['U','S'])
        inputs.extend(path.parent.glob('*.npz'))
        inputs.append(path)
        saved=archives['decomposition']
        source_data=load_inputs(packet['model'],packet['upper'],basis)
        consumed.update(source_data['inputs'])
        for key in ['coordinate','frequency','weights','operators','moments','field','temperature']:
            assert np.array_equal(saved[key],source_data[key]),key
        fraction=saved['fraction']
        assert np.array_equal(fraction,(saved['coordinate']-saved['coordinate'][0])/(saved['coordinate'][-1]-saved['coordinate'][0]))
        operators,field,moments=saved['operators'],saved['field'],saved['moments']
        operator_chord=operators[0]+fraction[:,None,None]*(operators[-1]-operators[0])
        field_chord=field[0]+fraction[:,None,None]*(field[-1]-field[0])
        raw=operators@field
        chord_raw=raw[0]+fraction[:,None,None]*(raw[-1]-raw[0])
        independent=dict(total=raw-chord_raw,operator=(operators-operator_chord)@field,
            state=operator_chord@(field-field_chord),
            cross=operator_chord@field_chord-chord_raw)
        normalized=operators/moments[:,None,None]
        normalized_chord=normalized[0]+fraction[:,None,None]*(normalized[-1]-normalized[0])
        moment_chord=moments[0]+fraction*(moments[-1]-moments[0])
        corrected=moments[:,None,None]*normalized_chord
        independent['moment']=((moments-moment_chord)[:,None,None]*normalized_chord)@field
        independent['shape']=operators@field-corrected@field
        independent['moment_cross']=(moment_chord[:,None,None]*normalized_chord-operator_chord)@field
        for name,value in independent.items():
            scale=np.maximum(abs(raw).max(axis=0),1e-300)
            assert np.max(abs(saved[name]-value)/scale)<1e-10,name
            assert not np.count_nonzero(saved[name][[0,-1]])
        checks.append(dict(name='Independent source/moment product decomposition:'+path.parent.name,passed=True))
        label=int(packet['upper']*1000)
        order=8 if packet['upper']==.04 else 6
        old=BRANCH/'direct-doppler-compton-feedback-20261012/results'/f'bank-o{order}-q32-m{label}'
        event_paths=[old/'epoch-00.npz',*[SITES/'results'/f'operator-m{label}'/f'event-{step:05d}.npz' for step in range(20,640,20)],old/'epoch-01.npz']
        for index,event_path in enumerate(event_paths):
            event=read_npz(event_path)
            ratio,rates=event['ratios'],event['rates']
            moment=np.sum(rates*(ratio-1)**2*(ratio+1)/ratio**3)
            assert abs(moment-moments[index])/moments[index]<1e-14
            assert np.all(rates>0) and np.all(ratio>0)
            consumed.add(event_path)
        expected=moments[:,None]*saved['weights']*saved['frequency']/(2*I3)
        assert np.max(abs(np.einsum('i,nif->nf',basis.temperature,saved['corrected_operator'])-expected)/abs(expected))<1e-10
        assert np.max(abs(np.einsum('i,nif->nf',basis.chemical,saved['corrected_operator'])))<1e-14
        checks.append(dict(name='Positive sourced moment and exact candidate energy/number:'+path.parent.name,passed=True))
        original=source_data['sources']['direct-sites32-source']
        original_response=source_data['sources']['direct-sites32-response']
        indices=saved['source_indices']
        assert np.array_equal(original['coordinate'][indices],saved['coordinate'])
        untouched=np.ones(len(original['coordinate']),dtype=bool)
        untouched[indices[1:-1]]=False
        for name,raw_expected in [('control',raw),('chord',operator_chord@field),('factored',corrected@field)]:
            candidate=archives[name+'-source']
            if name=='control':
                assert all(np.array_equal(value,original[key]) for key,value in candidate.items())
            else:
                for key in ['source','raw_source','energy_source','number_source']:
                    assert np.array_equal(candidate[key][untouched],original[key][untouched])
                    assert np.array_equal(candidate[key][:,1:],original[key][:,1:])
                for key in ['coordinate','overlap_source','profiles','gas','projected_replacement']:
                    assert np.array_equal(candidate[key],original[key])
                scale=np.maximum(abs(raw_expected).max(axis=0),1e-300)
                assert np.max(abs(candidate['raw_source'][indices[1:-1],0]-raw_expected[1:-1])/scale)<1e-10
                assert np.array_equal(candidate['source'][indices[1:-1],0],candidate['raw_source'][indices[1:-1],0]-candidate['overlap_source'][indices[1:-1],0])
                assert np.allclose(candidate['energy_source'][indices[1:-1],0],np.einsum('i,nik->nk',basis.temperature,candidate['source'][indices[1:-1],0]),rtol=1e-14,atol=0)
            response=archives[name+'-response']
            assert np.array_equal(response['gas'][:,6:],original_response['gas'][:,6:])
            assert np.array_equal(response['unresolved_change'],original_response['unresolved_change'])
            assert np.array_equal(response['physical_change'],basis.values@response['photon_final'][:,:3]+response['unresolved_change'])
        checks.append(dict(name='Only intended first-interval Compton sources changed:'+path.parent.name,passed=True))
        background=thermal_wave.thermal.ThermalBackground(packet['model'])
        for name in [*PARTS,'control','chord','factored']:
            response=archives[name+'-response']
            assert int(response['integration_steps'])==2048
            assert np.array_equal(response['coordinate'],original_response['coordinate'])
            scale=np.maximum((abs(response['energy'])+background.chi*abs(response['gas'])+abs(response['work'])).max(axis=0),1e-300)
            assert np.max(abs(response['energy']+background.chi*response['gas']+response['work'])/scale)<1e-7
            if name in PARTS:
                assert not np.count_nonzero(response['gas'][:,6:])
                assert np.array_equal(packet['endpoint'][name],response['gas'][-1,:3])
        for target,pieces in [('total',['operator','state','cross']),('operator',['moment','shape','moment_cross'])]:
            for quantity in ['gas','energy','work']:
                operands=[archives[target+'-response'][quantity],*[archives[key+'-response'][quantity] for key in pieces]]
                scale=np.maximum(np.sum(np.abs(operands),axis=0).max(axis=0),1e-300)
                assert np.max(abs(operands[0]-np.sum(operands[1:],axis=0))/scale)<1e-7
        for name,part in [('chord','operator'),('factored','shape')]:
            for quantity in ['gas','energy','work']:
                operands=[archives['control-response'][quantity],archives[name+'-response'][quantity],archives[part+'-response'][quantity]]
                scale=np.maximum(np.sum(np.abs(operands),axis=0).max(axis=0),1e-300)
                assert np.max(abs(operands[0]-operands[1]-operands[2])/scale)<1e-7
        checks.append(dict(name='Independent response conservation and superposition:'+path.parent.name,passed=True))
        control=archives['control-response']
        for name in ['chord','factored']:
            response=archives[name+'-response']
            delta=response['gas'][:,:3]-control['gas'][:,:3]
            metric=packet['candidate_comparisons'][name]
            for label_name,selection in [('gas_peak_relative',slice(None)),('gas_late_relative',slice(1536,None))]:
                ratio=abs(delta[selection]).max(axis=0)/np.maximum(abs(control['gas'][selection,:3]).max(axis=0),1e-300)
                assert np.allclose(metric[label_name],ratio,rtol=1e-12,atol=0)
            assert np.array_equal(metric['gas_endpoint_signed_difference'],delta[-1])
            assert np.allclose(metric['gas_endpoint_relative'],abs(delta[-1])/abs(control['gas'][-1,:3]),rtol=1e-12,atol=0)
            radiation=norm(response['physical_change']-control['physical_change'],basis.measure)/norm(control['physical_change'],basis.measure)
            assert np.allclose(metric['radiation_relative'],radiation,rtol=1e-12,atol=0)
        operator_endpoint=archives['operator-response']['gas'][-1,:3]
        for name in ['moment','shape','moment_cross']:
            assert np.array_equal(packet['operator_signed_fractions'][name],archives[name+'-response']['gas'][-1,:3]/operator_endpoint)
        residual=abs(archives['shape-response']['gas'][-1,:3]/operator_endpoint)
        assert np.array_equal(packet['factored_operator_endpoint_residual_ratio'],residual)
        checks.append(dict(name='Independent fractions and paired comparison metrics:'+path.parent.name,passed=True))
    assert len(list((ROOT/'results').glob('case-*/status.json')))==4
    assert science==review['scientific_checks'] and passing==review['passing_scientific_checks']
    assert failed==review['expected_failed_by_packet']
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==205877
    rehashed=set()
    parent=chain[PARENT/'results/stage-integrity.json']
    for name,sha in parent['file_hashes'].items():
        path=PARENT/name
        assert hashed(path)==sha,path
        rehashed.add(path)
    for path in consumed:
        if not path.is_relative_to(ROOT):
            verify_source(path,chain)
            rehashed.add(path)
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    documents=sorted(ROOT.glob('*.md'))
    for document in documents:
        for reference in re.findall(chr(96)+'([^'+chr(96)+']+)'+chr(96),document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.pdf')):
                assert (ROOT/reference).resolve().is_file(),reference
    assert not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000
    workbench=POST.parent/'formalization-workbench'
    assert workbench.is_dir() and not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Parent/provenance/compiler/capacity/protected-workbench verification',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=science,passing_scientific_checks=passing,
        retained_failed_checks=science-passing,compiled_scripts=len(scripts),checked_science_packets=4,
        accepted_scope_verified=True,largest_direct_file_count=maximum,inherited_payload_count=205877,
        consumed_and_immediate_rehashed={str(path):hashed(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,ROOT/'ACCURACY-REVIEW.json',ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(science=science,passes=passing,failures=science-passing,validation_checks=len(checks),rehashed=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
