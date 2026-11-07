from quadrature_common import *
from direct_common import source_grid
from validate_source_probe import independent_dual
import hashlib
import re


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    assert not (ROOT/'results/stage-integrity.json').exists()
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    script_hashes={digest(script) for script in scripts}
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        if path not in hashes:
            hashes[path]=digest(path)
        return hashes[path]
    packets=sorted(path for path in (ROOT/'results').glob('*/status.json') if path.parent!=folder)
    checks,inputs,consumed=[],[],set()
    failures={}
    scientific=passing=0
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').is_file()
        assert packet['script_sha256'] in script_hashes
        failed=[row['name'] for row in packet['checks'] if not row['passed']]
        assert all(name.startswith(('Source1percent:','Sensitivity1percent:')) or
            (name.startswith('Response:') and name.endswith(':gas')) for name in failed),(path,failed)
        if failed:
            failures[path.parent.name]=failed
        assert packet['count']==len(packet['checks']) and packet['all_checks_passed']==(not failed)
        for source,sha in packet['input_hashes'].items():
            assert hashed(source)==sha,source
            consumed.add(Path(source))
        for archive in path.parent.glob('*.npz'):
            values=read_npz(archive)
            assert all(np.isfinite(value).all() for value in values.values() if value.dtype.kind not in ['U','S'])
            inputs.append(archive)
        inputs.append(path)
        scientific+=len(packet['checks'])
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        checks.append(dict(name='Finite sourced packet:'+path.parent.name,passed=True))
    assert len(packets)==17
    assert scientific==review['scientific_checks'] and passing==review['passing_scientific_checks']
    assert failures==review['expected_failed_by_packet']
    proof=json.loads((ROOT/'results/arithmetic-proof/status.json').read_text())
    proof_values=read_npz(ROOT/'results/arithmetic-proof/comparison.npz')
    assert proof['all_checks_passed'] and proof['decimal_digits']==80
    assert not np.count_nonzero(proof_values['paired'][proof_values['ratios']==1])
    assert not np.count_nonzero(proof_values['paired'][:,:,0])
    for index,row in enumerate(proof['rows']):
        ratio_index,frequency_index=divmod(index,len(proof_values['frequency']))
        reference=proof_values['reference'][ratio_index,frequency_index]
        denominator=max(float(np.max(abs(reference))),1e-300)
        observed=float(np.max(abs(proof_values['paired'][ratio_index,frequency_index]-reference))/denominator)
        assert observed<1e-8 and abs(observed-row['paired_relative_error'])<8*np.finfo(float).eps
    checks.append(dict(name='Independent stored80digit arithmetic comparison',passed=True))
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs.extend(ladder.inputs)
    consumed.update(ladder.inputs)
    for upper in [.04,.02]:
        label=int(upper*1000)
        old_bank_path=PARENT/'results'/f'operator-m{label}/bank.npz'
        old_bank=read_npz(old_bank_path)
        for variant in VARIANTS:
            bank_folder=ROOT/'results'/f'bank-{variant}-m{label}'
            bank=read_npz(bank_folder/'bank.npz')
            packet=json.loads((bank_folder/'status.json').read_text())
            order,panels=specification(upper,variant)
            assert packet['event_order']==order and packet['frequency_panel_order']==panels
            assert np.array_equal(bank['steps'],ODD_STEPS) and len(packet['rows'])==16
            frequency,weights=source_grid(upper,panels)
            assert np.array_equal(bank['frequency'],frequency) and np.array_equal(bank['weights'],weights)
            fingerprint=json.loads((bank_folder/'INPUTS.json').read_text())
            fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
            for path,sha in fingerprint.items():
                assert hashed(path)==sha,path
                consumed.add(Path(path))
            for index,step in enumerate(ODD_STEPS):
                event_path=bank_folder/f'event-{step:05d}.npz'
                receipt=json.loads((bank_folder/f'event-{step:05d}.json').read_text())
                assert receipt['archive_sha256']==hashed(event_path)
                assert receipt['input_fingerprint_sha256']==fingerprint_hash
                assert receipt['row']==packet['rows'][index]
                event=read_npz(event_path)
                assert np.array_equal(event['adjoint'],bank['adjoint'][index])
                assert np.all(event['rates']>0) and np.all(event['ratios']>0)
                moment=np.sum(event['rates']*(event['ratios']-1)**2*(event['ratios']+1)/event['ratios']**3)
                expected=weights*frequency*moment/(2*I3)
                assert np.linalg.norm(basis.temperature@event['adjoint']-expected)/np.linalg.norm(expected)<1e-10
                assert np.max(abs(basis.chemical@event['adjoint']))<1e-14
                audit=receipt['row']['diagnostics']
                forward=event['ratios'][:,None]*frequency
                backward=frequency/event['ratios'][:,None]
                outside=(forward<basis.minimum)|(forward>basis.maximum)|(backward<basis.minimum)|(backward>basis.maximum)
                assert np.count_nonzero(outside)==audit['domain_crossing_pairs']
                integration_weight=(event['rates']/event['ratios'])[:,None]*weights
                fraction=float(np.sum(integration_weight*outside)/np.sum(integration_weight))
                assert np.isclose(fraction,audit['positive_weight_crossing_fraction'],rtol=1e-12,atol=1e-15)
                if variant=='stable':
                    old_index=int(np.flatnonzero(old_bank['steps']==step)[0])
                    assert np.array_equal(bank['adjoint'][index,:2],old_bank['adjoint'][old_index,:2])
            checks.append(dict(name='Reproducible receipt,quadrature,moments and domain audit:'+variant+':'+str(upper),passed=True))
        inputs.append(old_bank_path)
        consumed.add(old_bank_path)
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        for upper in [.04,.02]:
            label=int(upper*1000)
            comparison_folder=ROOT/'results'/f'comparison-{model}-m{label}'
            status=json.loads((comparison_folder/'status.json').read_text())
            prior=PARENT/'results'/f'sites-{model}-m{label}'
            source_path=prior/'direct-sites32-source.npz'
            response_path=prior/'direct-sites32-response.npz'
            original_source=read_npz(source_path)
            original_response=read_npz(response_path)
            replay_path=PARENT/'results'/f'replay-{model}-s00000/prediction.npz'
            replay=read_npz(replay_path)
            mask=replay['saved_step_indices']%40==20
            source_indices=np.searchsorted(original_source['coordinate'],replay['coordinate'][mask])
            changed=np.zeros(138,dtype=bool)
            changed[source_indices]=True
            inputs.extend([source_path,response_path,replay_path])
            consumed.update([source_path,response_path,replay_path])
            sources={'legacy':original_source}
            responses={'legacy':original_response}
            control=read_npz(comparison_folder/'legacy-control-response.npz')
            for metric,values in [('gas_peak_relative',abs(control['gas'][:,:3]-original_response['gas'][:,:3]).max(axis=0)/np.maximum(abs(original_response['gas'][:,:3]).max(axis=0),1e-300)),
                    ('radiation_relative',norm(control['physical_change']-original_response['physical_change'],basis.measure)/np.maximum(norm(original_response['physical_change'],basis.measure),1e-300))]:
                assert np.max(values)<1e-7
                assert np.allclose(values,status['legacy_control']['comparison'][metric],rtol=1e-12,atol=0)
            for variant in VARIANTS:
                source=read_npz(comparison_folder/(variant+'-source.npz'))
                response=read_npz(comparison_folder/(variant+'-response.npz'))
                bank=read_npz(ROOT/'results'/f'bank-{variant}-m{label}/bank.npz')
                assert np.array_equal(source['coordinate'],original_source['coordinate']) and len(source['coordinate'])==138
                for key in ['source','raw_source','energy_source','number_source']:
                    assert np.array_equal(source[key][~changed],original_source[key][~changed])
                    assert np.array_equal(source[key][:,1:],original_source[key][:,1:])
                for key in ['overlap_source','projected_replacement','replacement_moments','profiles','gas']:
                    assert np.array_equal(source[key],original_source[key]),key
                for selected,index in enumerate(source_indices):
                    field=compact_defect(bank['frequency'],replay['frequency'],replay['defect'][mask][selected],upper)
                    expected=bank['adjoint'][selected]@field
                    assert np.array_equal(source['raw_source'][index,0],expected)
                    assert np.array_equal(source['source'][index,0],expected-source['overlap_source'][index,0])
                assert np.array_equal(response['coordinate'],original_response['coordinate'])
                assert int(response['integration_steps'])==2048
                assert np.array_equal(response['unresolved_change'],original_response['unresolved_change'])
                assert np.array_equal(response['gas'][:,6:],original_response['gas'][:,6:])
                assert np.array_equal(response['physical_change'],basis.values@response['photon_final'][:,:3]+response['unresolved_change'])
                scale=np.maximum((abs(response['energy'])+background.chi*abs(response['gas'])+abs(response['work'])).max(axis=0),1e-300)
                assert np.max(abs(response['energy']+background.chi*response['gas']+response['work'])/scale)<1e-7
                for reference,metric in status['variants'][variant]['comparisons'].items():
                    old=responses[reference]
                    delta=response['gas'][:,:3]-old['gas'][:,:3]
                    assert np.array_equal(metric['gas_endpoint_signed_difference'],delta[-1])
                    for key,selection in [('gas_peak_relative',slice(None)),('gas_late_relative',slice(1536,None))]:
                        expected=abs(delta[selection]).max(axis=0)/np.maximum(abs(old['gas'][selection,:3]).max(axis=0),1e-300)
                        assert np.allclose(metric[key],expected,atol=0,rtol=1e-12)
                    expected=abs(delta[-1])/np.maximum(abs(old['gas'][-1,:3]),1e-300)
                    assert np.allclose(metric['gas_endpoint_relative'],expected,atol=0,rtol=1e-12)
                    radiation=norm(response['physical_change']-old['physical_change'],basis.measure)/np.maximum(norm(old['physical_change'],basis.measure),1e-300)
                    assert np.allclose(metric['radiation_relative'],radiation,atol=0,rtol=1e-12)
                    current=source['source'][source_indices]
                    previous=sources[reference]['source'][source_indices]
                    component_scale=np.maximum(independent_dual(current,basis).sum(axis=1),independent_dual(previous,basis).sum(axis=1))
                    relative=independent_dual((current-previous).sum(axis=1),basis)/np.maximum(component_scale,1e-300)
                    diagnostic=status['variants'][variant]['source_comparisons'][reference]
                    assert np.allclose(diagnostic['relative_to_components'],relative,rtol=1e-8,atol=0)
                sources[variant],responses[variant]=source,response
                checks.append(dict(name='Independent unchanged inputs,physical-source replacement and response:'+model+':'+str(upper)+':'+variant,passed=True))
            for kind,levels in [('event',['stable','event1','event2']),('frequency',['stable','frequency1','frequency2'])]:
                first=responses[levels[1]]['gas'][:,:3]-responses[levels[0]]['gas'][:,:3]
                second=responses[levels[2]]['gas'][:,:3]-responses[levels[1]]['gas'][:,:3]
                expected=abs(second[-1])/np.maximum(abs(first[-1]),1e-300)
                assert np.allclose(status['refinement'][kind]['endpoint_difference_ratio'],expected,rtol=1e-12,atol=0)
            interaction=responses['joint']['gas'][:,:3]-responses['event1']['gas'][:,:3]-responses['frequency1']['gas'][:,:3]+responses['stable']['gas'][:,:3]
            assert np.array_equal(status['interaction_endpoint'],interaction[-1])
            checks.append(dict(name='Event/frequency ladders and mixed interaction:'+model+':'+str(upper),passed=True))
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
    assert inherited_count==205345
    documents=sorted(ROOT.glob('*.md'))
    for document in documents:
        for reference in re.findall(chr(96)+'([^'+chr(96)+']+)'+chr(96),document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.pdf')):
                assert (ROOT/reference).resolve().is_file(),reference
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    workbench=POST.parent/'formalization-workbench'
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert workbench.is_dir() and not changed,changed
    checks.append(dict(name='Parent,consumed sources,citations,capacity and protected-workbench scan',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=scientific-passing,retained_failure_names=failures,compiled_scripts=len(scripts),
        checked_science_packets=len(packets),accepted_scope_verified=True,largest_direct_file_count=maximum,
        inherited_payload_count=inherited_count,replayed_steps=0,completed_backgrounds=['heavy','cold'],
        consumed_and_immediate_rehashed={str(path):hashed(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,ROOT/'ACCURACY-REVIEW.json',ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(science=scientific,passes=passing,failures=scientific-passing,
        validation_checks=len(checks),rehashed=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
