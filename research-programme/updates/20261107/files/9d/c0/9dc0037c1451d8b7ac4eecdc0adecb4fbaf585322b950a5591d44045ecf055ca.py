from half_history_common import *
from evaluate_half_feedback import expand_source
import hashlib


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        if path not in hashes:
            hashes[path]=digest(path)
        return hashes[path]
    parent_path=PARENT/'results/stage-integrity.json'
    assert hashed(parent_path)==PARENT_SEAL
    parent=json.loads(parent_path.read_text())
    for name,sha in parent['file_hashes'].items():
        assert hashed(PARENT/name)==sha,name
    checks=[dict(name='All immediate Stage136 payloads unchanged',passed=True)]
    inputs=[]
    count=passed=0
    failures={}
    for name in summary['packet_names']:
        path=ROOT/'results'/name/'status.json'
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').exists()
        script='build_half_coefficients.py' if name=='coefficients' else 'evolve_half_history.py' if name.startswith('evolution-') else 'build_half_sources.py' if name.startswith('weak-') else 'evaluate_half_feedback.py'
        assert packet['script_sha256']==hashed(ROOT/script)
        bad=[row['name'] for row in packet['checks'] if not row['passed']]
        assert all(item.startswith(('Sensitivity1percent:','Superposition:')) or (item.startswith('Response:') and item.endswith(':gas')) for item in bad),bad
        assert packet['count']==len(packet['checks']) and packet['all_checks_passed']==(not bad)
        count+=packet['count']
        passed+=sum(row['passed'] for row in packet['checks'])
        if bad:
            failures[name]=bad
        for source,sha in packet['input_hashes'].items():
            assert hashed(source)==sha,source
        for archive in path.parent.glob('*.npz'):
            values=read_npz(archive)
            assert all(np.isfinite(value).all() for value in values.values() if value.dtype.kind not in ['U','S'])
            inputs.append(archive)
        inputs.append(path)
        checks.append(dict(name='Finite sourced packet:'+name,passed=True))
    assert count==summary['scientific_checks'] and passed==summary['passing_scientific_checks'] and failures==summary['failed_by_packet']
    coefficient=read_npz(ROOT/'results/coefficients/bank.npz')
    coefficient_status=local_packet(ROOT/'results/coefficients')
    previous=read_npz(PARENT/'results/coefficients/bank.npz')
    assert len(coefficient['coordinate'])==len(SOURCE_STEPS) and np.array_equal(coefficient['steps'],SOURCE_STEPS)
    for index,step in enumerate(SOURCE_STEPS):
        row=coefficient_status['rows'][index]
        assert hashed(row['event_path'])==row['event_sha256']
        event=read_npz(row['event_path'])
        raw,unused_weights,unused_errors=deposit_cubic(event['ratios'],event['rates'],coefficient['offsets'],float(coefficient['spacing']))
        assert np.array_equal(raw,coefficient['raw'][index])
        stencil=pair_cubic(raw,coefficient['offsets'],float(coefficient['spacing']))
        assert np.array_equal(stencil,coefficient['stencil'][index])
        assert symbol_bound(stencil,coefficient['offsets'],float(coefficient['spacing']),float(coefficient['eigenvalue'][index]))==row['bound']
    assert np.array_equal(coefficient['stencil'][0],previous['stencil'][-1])
    checks.append(dict(name='All257physical event sources,cubic construction and Stage136 endpoint identity',passed=True))
    restart_count=0
    for model in ['heavy','cold']:
        original=read_npz(refined_owner(model)/'results'/f'inner-{model}-n40960/prediction.npz')
        previous_prediction=read_npz(PARENT/'results'/f'evolution-{model}-carry/prediction.npz')
        evolution_folder=ROOT/'results'/f'evolution-{model}-carry'
        prediction=read_npz(evolution_folder/'prediction.npz')
        assert np.array_equal(prediction['saved_step_indices'],SOURCE_STEPS)
        fingerprint=json.loads((evolution_folder/'INPUTS.json').read_text())
        for source,sha in fingerprint.items():
            assert hashed(source)==sha,source
        fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
        records=sorted((evolution_folder/'checkpoints').glob('restart-*.json'))
        assert len(records)==(LAST_STEP-FIRST_STEP)//80
        for step,record_path in zip(range(FIRST_STEP+80,LAST_STEP+1,80),records):
            record=json.loads(record_path.read_text())
            archive=record_path.parent/record['archive']
            assert record['fingerprint_sha256']==fingerprint_hash and hashed(archive)==record['archive_sha256']
            state=read_npz(archive)
            assert record['completed_step']==step and int(state['completed_step'])==step
            assert state['error'].shape==state['previous_error'].shape==(5265,3)
            assert all(np.isfinite(value).all() for value in state.values())
            assert np.array_equal(state['error'],prediction['defect'][(step-FIRST_STEP)//20])
            restart_count+=1
        assert prediction['budget'].shape==(LAST_STEP-FIRST_STEP,7,3) and np.all(prediction['budget'][:,2]<=0)
        assert np.max(prediction['budget'][:,5:])<1e-8
        for key in ['coordinate','slope','outer_slope','defect','lower_target','profiles','gas']:
            assert np.array_equal(prediction[key][0],previous_prediction[key][-1])
        for key in ['outer_slope','lower_target']:
            assert np.array_equal(prediction[key][-1],original[key][LAST_STEP//640])
        checks.append(dict(name='Unbroken corrected origin and all64both-level restarts:'+model,passed=True))
    assert restart_count==2*(LAST_STEP-FIRST_STEP)//80
    weak_count=0
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    for window in [20,40]:
        weak_folder=ROOT/'results'/f'weak-m{window}'
        bank=read_npz(weak_folder/'bank.npz')
        prefix_bank=read_npz(PARENT/'results'/f'weak-m{window}/bank.npz')
        unit=read_npz(P133/'results/linear-source-cache'/f'unit-m{window}.npz')
        active=coefficient['offsets']!=0
        cache=np.einsum('tj,jkl->tkl',coefficient['stencil'][:,active],unit['unit_adjoint'],optimize=True)
        fingerprint=json.loads((weak_folder/'INPUTS.json').read_text())
        fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
        for source,sha in fingerprint.items():
            assert hashed(source)==sha,source
        for index in range(len(SOURCE_STEPS)):
            record=json.loads((weak_folder/f'epoch-{index:03d}.json').read_text())
            archive=weak_folder/record['archive']
            assert record['fingerprint_sha256']==fingerprint_hash and hashed(archive)==record['archive_sha256']
            values=read_npz(archive)
            for key in ['physical','cubic']:
                assert np.array_equal(bank[key][index],values[key])
                expected=bank['weights']*bank['frequency']*coefficient['eigenvalue'][index]/I3
                assert np.linalg.norm(basis.temperature@values[key]-expected)/np.linalg.norm(expected)<1e-9
                assert not np.count_nonzero(basis.chemical@values[key])
            if index:
                assert np.array_equal(bank['cubic'][index],cache[index])
                assert record['raw_physical_energy_error'] is not None
            weak_count+=1
        for key in ['physical','cubic']:
            assert np.array_equal(bank[key][0],prefix_bank[key][-1])
        assert len(bank['coordinate'])==len(SOURCE_STEPS)
        assert np.array_equal(bank['coordinate'],coefficient['coordinate'])
        assert np.array_equal(bank['steps'],SOURCE_STEPS)
    assert weak_count==2*len(SOURCE_STEPS)
    checks.append(dict(name='Every514source record,physical evaluation,moments and exact cached contraction',passed=True))
    for model in ['heavy','cold']:
        for window in [20,40]:
            feedback_folder=ROOT/'results'/f'feedback-{model}-m{window}'
            physical=read_npz(feedback_folder/'physical-source.npz')
            cubic=read_npz(feedback_folder/'cubic-source.npz')
            prior=read_npz(PARENT/'results'/f'feedback-{model}-m{window}/physical-source.npz')
            reference=expand_source(prior,physical['coordinate'])
            assert np.array_equal(reference['source'],read_npz(feedback_folder/'previous-expanded-source.npz')['source'])
            assert np.array_equal(physical['source'][:,1:],cubic['source'][:,1:])
            new_positions=np.searchsorted(physical['coordinate'],coefficient['coordinate'][1:])
            unaffected=np.ones(len(physical['coordinate']),dtype=bool)
            unaffected[new_positions]=False
            for label,current in [('physical',physical),('cubic',cubic)]:
                previous_source=read_npz(PARENT/'results'/f'feedback-{model}-m{window}'/(label+'-source.npz'))
                expanded=expand_source(previous_source,current['coordinate'])
                for key in ['source','raw_source','energy_source','number_source','overlap_source']:
                    assert np.array_equal(current[key][unaffected],expanded[key][unaffected])
            for label,current,old in [('continuation',physical,reference),('discretization',cubic,physical)]:
                packet=read_npz(feedback_folder/(label+'-source.npz'))
                assert np.array_equal(packet['source'],current['source']-old['source'])
                response=read_npz(feedback_folder/(label+'-response.npz'))
                assert len(response['coordinate'])==2049 and int(response['integration_steps'])==2048
    checks.append(dict(name='Extended prefix,unchanged previous sites/tail and exact independent difference forcing',passed=True))
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for unused,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert workbench.is_dir() and not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Scripts compile;no caches;folder limits;protected mtime zero',passed=True))
    consumed={str(path):sha for path,sha in hashes.items() if not path.is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=True,scientific_checks=count,passing_scientific_checks=passed,
        retained_failed_checks=count-passed,retained_failure_names=failures,compiled_scripts=len(scripts),
        rehashed_prior_files=len(consumed),consumed_and_immediate_rehashed=consumed,restart_records_verified=restart_count,
        weak_records_verified=weak_count,largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0),
        __file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json',*ladder.inputs])
    print(json.dumps(dict(validation_checks=len(checks),science=count,passed=passed,failed=count-passed,prior_rehashed=len(consumed))),flush=True)


if __name__=='__main__':
    main()
