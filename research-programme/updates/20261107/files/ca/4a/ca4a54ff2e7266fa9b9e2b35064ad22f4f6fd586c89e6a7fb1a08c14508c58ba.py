from bridge215 import *


def validate():
    config=protocol()
    manifest=read(ROOT/'frozen/prediction-manifest.json')
    assessment=read(ROOT/'results/assessment.json')
    assert digest(ROOT/'assess215.py')==read(ROOT/'frozen/analysis-contract.json')['sha256']
    rows=list(assessment['checks'])
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    check(rows,'all consumed and immediate inputs unchanged',0,0,'integrity')
    for name,value in manifest['files'].items():
        assert digest(ROOT/name)==value,name
    by_label={label:[] for label in LABELS}
    for row in config['events']:
        values,report=verify_event(row)
        assert report['scalar_precision']==60 and report['protected_precision']==80
        assert report['new_virtual_integrals']==0
        parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
        assert weight==row['weight']
        assert digest(row['loop_path'])==row['loop_sha256']
        loop=read(row['loop_path'])
        assert loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
        by_label[row['label']].append((values['high'],values['low']))
    check(rows,'all108 event matrices authenticated',len(list((ROOT/'events').rglob('event-*.npz')))-108,0,'integrity')
    check(rows,'no new virtual cache created',int((ROOT/'virtual-cache').exists()),0,'integrity')
    for name in ('history-coefficients.npz','basis-metric.npz'):
        check(rows,name+':byte-identical reuse',int(digest(ROOT/'frozen'/name)!=digest(PARENT/'frozen'/name)),0,'integrity')
    sampled=[]
    with mp.workdps(100):
        totals=[packet(ROOT/f'results/operator-{label}.npz') for label in LABELS]
        predicted=packet(ROOT/'frozen/predicted-operator.npz')
        for component,row,index,join in ((0,0,0,0),(1,1,48,1),(2,97,96,0),(3,42,63,1),(4,83,47,0),(5,0,96,1)):
            members=[component] if component<4 else [1,2,3] if component==4 else [0,1,2,3]
            exact_anchors=[]
            for label,total in zip(LABELS,totals):
                exact=mp.fsum(mp.mpf(float(high[member,row,index,join]))+mp.mpf(float(low[member,row,index,join]))
                    for high,low in by_label[label] for member in members)
                exact_anchors.append(exact)
                value=mp.mpf(float(total['high'][component,row,index,join]))+mp.mpf(float(total['low'][component,row,index,join]))
                error=float(abs(value-exact)/max(abs(exact),mp.mpf('1e-300')))
                sampled.append(error)
                check(rows,f'100digit anchor {label}:{component}:{row}:{index}:{join}',error,1e-10,'identity')
            exact=mp.fsum(mp.mpf(weight)*value for weight,value in zip(config['operator_weights'],exact_anchors))
            value=mp.mpf(float(predicted['high'][component,row,index,join]))+mp.mpf(float(predicted['low'][component,row,index,join]))
            error=float(abs(value-exact)/max(abs(exact),mp.mpf('1e-300')))
            sampled.append(error)
            check(rows,f'100digit interpolation {component}:{row}:{index}:{join}',error,1e-10,'identity')
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'no bytecode or partial writes',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial')))+len(list(ROOT.rglob('*.tmp'))),0,'integrity')
    for name,value in config['bookmarks'].items():
        assert digest(name)==value,name
    protected=BRANCH.parent.parent/'formalization-workbench'
    since=datetime.fromisoformat(config['turn_start']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
    check(rows,'protected workbench recent-mtime count',len(changed),0,'integrity')
    failed=[row for row in rows if not row['passed']]
    integrity_failures=[row for row in failed if row['category'] not in ('physical_prediction','operator_prediction')]
    assert not integrity_failures,integrity_failures
    report=dict(stage=215,checks=rows,failed_checks=failed,integrity_passed=True,
        qualified=not failed,physical_history_prediction_passed=assessment['physical_history_prediction_passed'],
        operator_block_prediction_passed=assessment['operator_block_prediction_passed'],
        inputs_rehashed=len(inputs),decimal_sample_max=max(sampled),
        assessment_sha256=digest(ROOT/'results/assessment.json'),
        protected_workbench_recent_modified_file_count=len(changed),workbench_guard_scope='recent mtime, not full-tree hash',
        uniform_temperature_qualified=False,permission_to_propagate=False)
    write(ROOT/'results/validation.json',report)
    print(json.dumps(dict(checks=len(rows),failed=len(failed),inputs=len(inputs),
        physical_history_prediction_passed=report['physical_history_prediction_passed'],
        operator_block_prediction_passed=report['operator_block_prediction_passed'],decimal_sample_max=max(sampled))),flush=True)


def seal():
    config=protocol()
    validation=read(ROOT/'results/validation.json')
    assert validation['integrity_passed']
    assert digest(ROOT/'results/assessment.json')==validation['assessment_sha256']
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):
        assert (ROOT/name).is_file()
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            path=Path(name);before=archive.read(path.name)
            assert hashlib.sha256(before).hexdigest()==value and path.read_bytes().endswith(before)
            bookmarks.append(dict(path=str(path),previous_sha256=value,current_sha256=digest(path),previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='complete',integrity_passed=True,
        physical_history_prediction_passed=validation['physical_history_prediction_passed'],
        operator_block_prediction_passed=validation['operator_block_prediction_passed'],
        active_numerical_workers=0,completed_at=now(),permission_to_propagate=False))
    destination=ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(stage=215,state='complete',sealed_at=now(),qualified=validation['qualified'],
        integrity_passed=True,physical_history_prediction_passed=validation['physical_history_prediction_passed'],
        operator_block_prediction_passed=validation['operator_block_prediction_passed'],
        parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        consumed_and_immediate_rehashed=inputs,file_hashes=hashes,
        anchor_events=108,target_events_reused=36,new_virtual_integrals=0,
        original_bank_changed=False,global_curve_changed=False,grids_changed=False,tolerances_changed=False,
        uniform_temperature_qualified=False,permission_to_propagate=False,
        maximum_concurrent_event_workers=2,numerical_threads_per_worker=1,active_workers_at_seal=0,
        protected_workbench_recent_modified_file_count=validation['protected_workbench_recent_modified_file_count'],
        retained_current_failures=len(validation['failed_checks']),github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md')))
    print(json.dumps(dict(seal=str(destination),sha256=digest(destination),payloads=len(hashes))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['validate','seal'])
    args=parser.parse_args()
    {'validate':validate,'seal':seal}[args.phase]()
