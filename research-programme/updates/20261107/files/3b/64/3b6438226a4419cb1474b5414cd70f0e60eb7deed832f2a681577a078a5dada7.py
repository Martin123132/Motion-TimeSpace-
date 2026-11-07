from connection208 import *


def validate():
    config=protocol()
    parent=read(PARENT/'results/stage-integrity.json')
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SHA
    primary_path=ROOT/'results/assessment-036.json'
    primary=read(primary_path)
    assert primary['state']=='forecast_rejected' and len(primary['failed_checks'])==96
    assert all(row['category']=='prediction' for row in primary['failed_checks'])
    assert not primary['permission_to_propagate'] and not primary['complete_band']
    diagnostic=read(ROOT/'diagnostic/assessment.json')
    assert diagnostic['post_test_diagnostic'] and not diagnostic['failed_checks']
    assert diagnostic['original_forecast_still_rejected'] and not diagnostic['permission_to_propagate']
    rows=[dict(row,name='source:'+row['name']) for row in primary['checks'] if row['category']!='prediction']
    rows.extend(dict(row,name='diagnostic:'+row['name']) for row in diagnostic['checks'])
    inputs=read(ROOT/'inputs.json')
    inputs.update(read(ROOT/'diagnostic/configuration.json')['input_hashes'])
    for name,value in inputs.items():assert digest(name)==value,name
    check(rows,'consumed and immediate inputs unchanged',0,0,'integrity')
    manifest=read(ROOT/'frozen/prediction-manifest.json')
    assert manifest['configuration_sha256']==digest(ROOT/'configuration.json')
    check(rows,'all252 event predictions remain frozen',len(list((ROOT/'frozen').glob('frequency-*/event-*.npz')))-252,0,'integrity')
    actual_paths=sorted((ROOT/'events').rglob('event-*.npz'))
    diagnostic_paths=sorted((ROOT/'diagnostic/events').glob('event-*.npz'))
    check(rows,'central physical events complete',len(actual_paths)-36,0,'integrity')
    check(rows,'diagnostic events complete',len(diagnostic_paths)-36,0,'integrity')
    acquired=0
    for path in actual_paths+diagnostic_paths:
        record=read(path.with_suffix('.json'))
        assert digest(path)==record['sha256'] and not record['failed_checks']
        assert digest(record['loop_path'])==record['loop_sha256']
        if path.is_relative_to(ROOT/'events'):
            assert datetime.fromisoformat(record['started_at'])>datetime.fromisoformat(manifest['frozen_at'])
            acquired+=int(record['new_virtual_integral'])
        else:assert record['new_virtual_integrals']==0
    check(rows,'only36 new virtual inputs, diagnostic none',acquired-36,0,'integrity')
    check(rows,'isolated new virtual cache complete',len(list((ROOT/'virtual-cache').rglob('*.json')))-36,0,'integrity')
    values=packet(ROOT/'diagnostic/decomposition.npz')
    energy_records=[]
    for method in ('quadratic','linear'):
        for term in ('error','history','remaining'):
            high,low=values[method+'_'+term+'_high'],values[method+'_'+term+'_low']
            energy=high[...,0,:]+low[...,0,:]
            gas=high[...,-1,:]+low[...,-1,:]
            residual=abs(energy+gas)/np.maximum(np.maximum(abs(energy),abs(gas)),1e-300)
            maximum=float(residual.max())
            check(rows,method+':'+term+':energy exchange',maximum,1e-10,'identity')
            energy_records.append(dict(method=method,term=term,relative=maximum))
    history_generator=np.array([[0,1],[0,0]],dtype=int)
    source_map=np.array([[1,0],[-1,0]],dtype=int)
    hidden=np.array([0,1],dtype=int)
    zero=np.zeros(2,dtype=int)
    check(rows,'closure counterexample same source',np.max(abs(source_map@hidden-source_map@zero)),0,'exact_algebra')
    check(rows,'closure counterexample different derivative',int(np.array_equal(source_map@history_generator@hidden,source_map@history_generator@zero)),0,'exact_algebra')
    check(rows,'closure counterexample conserves energy',np.max(abs(np.array([1,1])@source_map)),0,'exact_algebra')
    for path in ROOT.rglob('*.py'):compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'no bytecode or unfinished writes',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial')))+len(list(ROOT.rglob('*.tmp'))),0,'integrity')
    for name,value in config['bookmarks'].items():assert digest(name)==value,name
    protected=BRANCH.parent.parent/'formalization-workbench'
    started=datetime.fromisoformat(config['started_at']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    check(rows,'protected workbench recent-mtime count',len(changed),0,'integrity')
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/final-validation.json',dict(checks=rows,failed_checks=failed,integrity_and_diagnostic_validation_passed=not failed,
        retained_prediction_failures=primary['failed_checks'],forecast_qualified=False,permission_to_propagate=False,
        full_new_temperature_band_evaluated=False,inputs_rehashed=len(inputs),consumed_and_immediate_rehashed=inputs,
        new_physical_events=36,new_diagnostic_events=36,new_virtual_inputs=acquired,
        energy_error_decomposition=energy_records,source_assessment_sha256=digest(primary_path),
        diagnostic_assessment_sha256=digest(ROOT/'diagnostic/assessment.json'),
        protected_workbench_recent_modified_file_count=len(changed),protected_scope='recent mtime guard, not a separate full-tree hash'))
    print(json.dumps(dict(validation_checks=len(rows),validation_failed=failed,retained_prediction_failures=96,
        inputs_rehashed=len(inputs),energy_decomposition=energy_records)),flush=True)


def seal():
    config=protocol()
    validation=read(ROOT/'results/final-validation.json')
    assert validation['integrity_and_diagnostic_validation_passed']
    assert digest(ROOT/'results/assessment-036.json')==validation['source_assessment_sha256']
    assert digest(ROOT/'diagnostic/assessment.json')==validation['diagnostic_assessment_sha256']
    for name,value in validation['consumed_and_immediate_rehashed'].items():assert digest(name)==value,name
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md','DERIVED-TRANSPORT.md'):assert (ROOT/name).exists()
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            path=Path(name);before=archive.read(path.name)
            assert hashlib.sha256(before).hexdigest()==value and path.read_bytes().endswith(before)
            bookmarks.append(dict(path=name,previous_sha256=value,current_sha256=digest(path),previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='complete',outcome='central_temperature_forecast_rejected_and_diagnosed',
        forecast_qualified=False,permission_to_propagate=False,completed_physical_events=36,total_frozen_events=252,
        remaining_frequency_events_deferred=216,active_workers=0))
    destination=ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(stage=208,state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),
        outcome='central_temperature_forecast_rejected_and_diagnosed',forecast_qualified=False,permission_to_propagate=False,
        parent_seal_sha256=PARENT_SHA,parent_seal_path=str(PARENT/'results/stage-integrity.json'),
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        file_hashes=hashes,consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],
        retained_prediction_failures=96,new_physical_events=36,new_diagnostic_events=36,new_virtual_inputs=36,
        total_frozen_events=252,full_new_temperature_band_evaluated=False,
        original_bank_changed=False,global_curve_changed=False,grids_changed=False,tolerances_changed=False,
        maximum_concurrent_event_workers=2,numerical_threads_per_worker=1,active_workers_at_seal=0,
        github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md'),
        protected_workbench_recent_modified_file_count=validation['protected_workbench_recent_modified_file_count']))
    print(json.dumps(dict(seal=str(destination),sha256=digest(destination),payloads=len(hashes))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['validate','seal'])
    args=parser.parse_args()
    {'validate':validate,'seal':seal}[args.phase]()
