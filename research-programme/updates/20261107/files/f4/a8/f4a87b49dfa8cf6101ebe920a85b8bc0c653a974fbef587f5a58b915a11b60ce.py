from coefficient_common import *
from interpolation_common import load_inputs as load_operator_inputs
import hashlib
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
    checks,inputs,consumed=[],[],set()
    failed={}
    science=passing=0
    packets=sorted(path for path in (ROOT/'results').glob('*/status.json') if path.parent!=folder)
    assert len(packets)==12
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').exists()
        assert packet['script_sha256'] in {hashed(script) for script in ROOT.glob('*.py')}
        names=[row['name'] for row in packet['checks'] if not row['passed']]
        assert all(name.startswith(('Low exact moment:','Sensitivity1percent:')) or (name.startswith('Response:') and name.endswith(':gas')) for name in names),names
        if names:
            failed[path.parent.name]=names
        assert packet['count']==len(packet['checks']) and packet['all_checks_passed']==(not names)
        science+=len(packet['checks'])
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        for name,sha in packet['input_hashes'].items():
            assert hashed(name)==sha,name
            consumed.add(Path(name))
        for archive in path.parent.glob('*.npz'):
            values=read_npz(archive)
            assert all(np.isfinite(value).all() for value in values.values() if value.dtype.kind not in ['U','S'])
            inputs.append(archive)
        inputs.append(path)
        checks.append(dict(name='Sourced finite packet:'+path.parent.name,passed=True))
    assert science==review['scientific_checks'] and passing==review['passing_scientific_checks']
    assert failed==review['expected_failed_by_packet']
    raw=read_npz(ROOT/'results/coefficients/bank.npz')
    repaired=read_npz(ROOT/'results/balanced-coefficients/bank.npz')
    repair_status=json.loads((ROOT/'results/balanced-coefficients/status.json').read_text())
    offsets,spacing=raw['offsets'],float(raw['spacing'])
    center=int(np.flatnonzero(offsets==0)[0])
    old_root=BRANCH/'direct-doppler-compton-feedback-20261012/results/bank-o6-q32-m40'
    event_paths=[old_root/'epoch-00.npz',*[SITES/'results/operator-m20'/f'event-{step:05d}.npz' for step in range(20,640,20)],old_root/'epoch-01.npz']
    for index,path in enumerate(event_paths):
        event=read_npz(path)
        ratio,rates=event['ratios'],event['rates']
        eigen=float(np.sum(rates*(-np.expm1(-np.log(ratio)))))
        moment=float(np.sum(rates*(ratio-1)**2*(ratio+1)/ratio**3))
        assert abs(eigen-raw['eigenvalue'][index])/eigen<1e-12
        assert abs(moment-2*eigen)/eigen<1e-8
        lower=np.floor(np.log(ratio)/spacing).astype(int)
        high_u=np.exp(-lower*spacing)
        low_u=np.exp(-(lower+1)*spacing)
        variance=(1/ratio-low_u)*(high_u-1/ratio)
        bias=np.array([rates@variance,rates@(variance*(low_u+high_u+1/ratio))])
        actual=np.array([raw['low'][index]@np.expm1(power*offsets*spacing)-rates@np.expm1(power*np.log(ratio)) for power in [-2,-3]])
        assert np.max(abs(actual-bias))/eigen<1e-9
        assert np.all(bias>0)
        values=repaired['low'][index]
        assert np.all(values[np.arange(len(values))!=center]>=0)
        ratios=np.exp(offsets[center+1:]*spacing)
        assert np.allclose(values[:center][::-1],values[center+1:]/ratios**3,rtol=1e-14,atol=0)
        total=raw['low'][index,center+1:]+raw['low'][index,:center][::-1]
        assert np.allclose(values[center+1:]+values[:center][::-1],repaired['normalization'][index]*total,rtol=1e-14,atol=0)
        for power,target in [(-1,0.),(-2,0.),(-3,eigen)]:
            observed=values@np.expm1(power*offsets*spacing)+eigen
            assert abs(observed-target)/eigen<1e-9
        assert abs(values.sum())<1e-12
        rate_change=np.sum(abs(values-raw['low'][index]))/np.sum(abs(raw['low'][index]))
        assert np.isclose(rate_change,repair_status['rows'][index]['rate_change_l1_relative'],rtol=1e-14)
        consumed.add(path)
    checks.append(dict(name='Independent reciprocal repair and Jensen moment-bias identities',passed=True))
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    consumed.update(ladder.inputs)
    for model in ['heavy','cold']:
        old_path=SITES/'results'/f'replay-{model}-s00000/prediction.npz'
        original=read_npz(old_path)
        consumed.add(old_path)
        for variant in ['control','dense','balanced']:
            current=ROOT/'results'/f'replay-{model}-{variant}'
            prediction=read_npz(current/'prediction.npz')
            assert np.array_equal(prediction['saved_step_indices'],np.arange(0,641,20))
            for key in ['frequency','coordinate','outer_slope','lower_target','profiles','gas']:
                assert np.array_equal(prediction[key],original[key]),key
            if variant=='control':
                assert np.array_equal(prediction['defect'],original['defect'])
            assert np.array_equal(prediction['defect'][0],original['defect'][0])
            fingerprint=json.loads((current/'INPUTS.json').read_text())
            fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
            for name,sha in fingerprint.items():
                assert hashed(name)==sha,name
                consumed.add(Path(name))
            receipts=sorted((current/'checkpoints').glob('restart-*.json'))
            assert len(receipts)==8
            for receipt in receipts:
                record=json.loads(receipt.read_text())
                assert record['fingerprint_sha256']==fingerprint_hash
                archive=receipt.parent/record['archive']
                assert hashed(archive)==record['archive_sha256']
                state=read_npz(archive)
                assert int(state['completed_step'])==record['completed_step']
                assert np.array_equal(state['defect'],prediction['defect'][:len(state['defect'])])
                assert np.array_equal(state['error'],state['defect'][-1])
            final=read_npz(current/'checkpoints/restart-00640.npz')
            assert final['previous_error'].shape==final['error'].shape
            checks.append(dict(name='Verified control/state/input and restart chain:'+model+':'+variant,passed=True))
        background=thermal_wave.thermal.ThermalBackground(model)
        for upper in [.04,.02]:
            current=ROOT/'results'/f'feedback-{model}-m{int(upper*1000)}'
            packet=json.loads((current/'status.json').read_text())
            data=load_operator_inputs(model,upper,basis)
            consumed.update(data['inputs'])
            original_source=data['sources']['direct-sites32-source']
            retabulated=read_npz(current/'retabulated-source.npz')
            responses={'saved':read_npz(current/'retabulated-response.npz')}
            source_indices=np.searchsorted(retabulated['coordinate'],data['coordinate'])
            untouched=np.ones(139,dtype=bool)
            untouched[source_indices]=False
            fraction=(data['coordinate']-data['coordinate'][0])/(data['coordinate'][-1]-data['coordinate'][0])
            moments=data['moments']
            factored=moments[:,None,None]*((1-fraction[:,None,None])*data['operators'][0]/moments[0]+fraction[:,None,None]*data['operators'][-1]/moments[-1])
            for variant in ['control','dense','balanced']:
                prediction=read_npz(ROOT/'results'/f'replay-{model}-{variant}/prediction.npz')
                for branch,operators in [('direct',data['operators']),('factored',factored)]:
                    label=variant+'-'+branch
                    source=read_npz(current/(label+'-source.npz'))
                    response=read_npz(current/(label+'-response.npz'))
                    field=np.array([compact_defect(data['frequency'],prediction['frequency'],values,upper) for values in prediction['defect']])
                    expected=operators@field
                    scale=np.maximum(abs(expected).max(axis=0),1e-300)
                    assert np.max(abs(source['raw_source'][source_indices,0]-expected)/scale)<1e-10
                    assert np.array_equal(source['source'][source_indices],source['raw_source'][source_indices]-source['overlap_source'][source_indices])
                    for key in ['source','raw_source','energy_source','number_source','overlap_source']:
                        assert np.array_equal(source[key][untouched],retabulated[key][untouched])
                    assert np.array_equal(source['coordinate'],retabulated['coordinate'])
                    if branch=='factored':
                        direct=read_npz(current/(variant+'-direct-source.npz'))
                        assert np.array_equal(source['source'][:,1:],direct['source'][:,1:])
                    assert int(response['integration_steps'])==2048
                    assert np.array_equal(response['unresolved_change'],responses['saved']['unresolved_change'])
                    assert np.array_equal(response['physical_change'],basis.values@response['photon_final'][:,:3]+response['unresolved_change'])
                    energy_scale=np.maximum((abs(response['energy'])+background.chi*abs(response['gas'])+abs(response['work'])).max(axis=0),1e-300)
                    assert np.max(abs(response['energy']+background.chi*response['gas']+response['work'])/energy_scale)<1e-7
                    reference=responses[packet['variants'][label]['reference']]
                    metric=packet['variants'][label]['comparison']
                    delta=response['gas'][:,:3]-reference['gas'][:,:3]
                    for key,selection in [('gas_peak_relative',slice(None)),('gas_late_relative',slice(1536,None))]:
                        value=abs(delta[selection]).max(axis=0)/np.maximum(abs(reference['gas'][selection,:3]).max(axis=0),1e-300)
                        assert np.allclose(value,metric[key],rtol=1e-12,atol=0)
                    assert np.array_equal(metric['gas_endpoint_signed_difference'],delta[-1])
                    assert np.allclose(abs(delta[-1])/abs(reference['gas'][-1,:3]),metric['gas_endpoint_relative'],rtol=1e-12,atol=0)
                    radiation=norm(response['physical_change']-reference['physical_change'],basis.measure)/norm(reference['physical_change'],basis.measure)
                    assert np.allclose(radiation,metric['radiation_relative'],rtol=1e-12,atol=0)
                    forcing=interpolate.interp1d(source['coordinate'],source['source'],axis=0)(response['coordinate'][33:])
                    original_forcing=interpolate.interp1d(original_source['coordinate'],original_source['source'],axis=0)(response['coordinate'][33:])
                    assert max_relative(forcing-original_forcing,[original_forcing])<1e-12
                    responses[label]=response
            assert packet['local_splice_only'] and not packet['later_state_carried']
            checks.append(dict(name='Independent saved-state sources,local splice and paired response:'+model+':'+str(upper),passed=True))
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==205956
    rehashed=set()
    for name,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
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
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    workbench=POST.parent/'formalization-workbench'
    assert workbench.is_dir() and not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Provenance/compiler/capacity/protected-workbench audit',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=science,passing_scientific_checks=passing,
        retained_failed_checks=science-passing,compiled_scripts=len(scripts),checked_science_packets=12,
        accepted_scope_verified=True,largest_direct_file_count=maximum,inherited_payload_count=205956,
        independent_replayed_steps=0,solver_residuals_from_recorded_runs=True,
        consumed_and_immediate_rehashed={str(path):hashed(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,ROOT/'ACCURACY-REVIEW.json',ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(science=science,passes=passing,failures=science-passing,validation_checks=len(checks),rehashed=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
