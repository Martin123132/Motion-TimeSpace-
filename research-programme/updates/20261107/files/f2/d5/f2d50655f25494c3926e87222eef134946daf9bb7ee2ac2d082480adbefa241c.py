from refine222 import *
import response222
import matching222

def validate():
    config=protocol()
    response222.response_protocol()
    matching222.matching_protocol()
    rows=list(read(ROOT/'results/seed-identity.json')['checks'])
    inputs=read(ROOT/'inputs.json')
    for pattern in ('inputs-source-*.json','inputs-response-*.json','inputs-matching-*.json'):
        for path in ROOT.glob(pattern):
            for name,value in read(path).items():
                assert name not in inputs or inputs[name]==value,name
                inputs[name]=value
    for model in MODELS:
        folder=ROOT/f'histories/{model}/eighth'
        complete=read(folder/'complete.json')
        verify_restart(folder,complete,config['seed_hashes'][model])
        check(rows,model+':all history updates complete',complete['done']-config['schedules'][model]['updates'],0,'integrity')
        for path in sorted((folder/'blocks').glob('*.json')):
            rows.extend(dict(row,name=model+':history:'+row['name']) for row in read(path)['checks'])
    response=read(ROOT/'results/response-assessment.json')
    rows.extend(response['checks'])
    boundary=read(ROOT/'boundary-contract.json')
    assert digest(ROOT/'boundary222.py')==boundary['script_sha256']
    assert digest(ROOT/'BOUNDARY-MATCHING-DERIVATION.md')==boundary['derivation_sha256']
    rows.extend(read(ROOT/'results/boundary-algebra.json')['checks'])
    matching_records=[]
    for model in MODELS:
        for count in (2048,4096):
            folder=ROOT/f'precise-matching/{model}-{count}'
            report=read(folder/'complete.json')
            for name,value in report['file_hashes'].items():
                assert digest(folder/name)==value,name
            rows.extend(dict(row,name=f'{model}:{count}:matching:'+row['name']) for row in report['checks'])
            matching_records.extend(report['records'])
    old_diagnosis=read(PARENT/'results/matching-roundoff-diagnosis.json')
    check(rows,'all prior failing individual columns retested',len(matching_records)-len(old_diagnosis['records']),0,'integrity')
    for name,value in inputs.items():
        assert digest(name)==value,name
    check(rows,'consumed/immediate inputs unchanged',0,0,'integrity')
    protected=BRANCH.parent.parent/'formalization-workbench'
    since=datetime.fromisoformat('2026-10-26T08:17:37+00:00').timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
    check(rows,'protected recent mtime count',len(changed),0,'integrity')
    check(rows,'no temporary or bytecode files',len(list(ROOT.rglob('*.partial')))+len(list(ROOT.rglob('__pycache__'))),0,'integrity')
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'inputs-final.json',inputs)
    write(ROOT/'results/current-validation.json',dict(stage=222,finished_at=now(),checks=rows,failed_checks=failed,qualified=not failed,
        original_stage221_failed_checks_retained=len(read(PARENT/'results/current-validation.json')['failed_checks']),
        history_updates={model:config['schedules'][model]['updates'] for model in MODELS},
        source_points=130,history_shared_seed_error_certified=False,
        matching_old_failed_columns_retested=len(matching_records),
        matching_max_relative=max(record['precise_matching_relative'] for record in matching_records),
        source_response_qualified=response['qualified'],inputs_rehashed=len(inputs),protected_recent_mtime_count=len(changed),
        protected_guard_scope='recent mtime, not full-tree content snapshot',
        bank_unchanged=True,response_grids_unchanged=True,global_curve_unchanged=True,tolerances_unchanged=True,
        matching_scope='original arithmetic recurrence, eight total columns plus four baseline/MTS controls; causal matching separate',
        response_records=response['records']))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),inputs=len(inputs),old_failed_columns_retested=len(matching_records),
        matching_max_relative=max(record['precise_matching_relative'] for record in matching_records),
        protected_recent_mtime_count=len(changed))),flush=True)

def seal():
    validation=read(ROOT/'results/current-validation.json')
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):
        assert (ROOT/name).is_file(),name
    for name,value in read(ROOT/'inputs-final.json').items():
        assert digest(name)==value,name
    path=ROOT/'results/stage-integrity.json'
    assert not path.exists()
    payload={file.relative_to(ROOT).as_posix():digest(file) for file in ROOT.rglob('*') if file.is_file() and file!=path}
    bookmarks={str(file):digest(file) for file in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}
    write(path,dict(stage=222,state='complete',sealed_at=now(),qualified=validation['qualified'],
        scope='post-common-seed numerical refinement and promoted original-matching arithmetic',
        consumed_and_immediate_rehashed=read(ROOT/'inputs-final.json'),file_hashes=payload,bookmarks=bookmarks))
    print(json.dumps(dict(seal=str(path),sha256=digest(path),payloads=len(payload),qualified=validation['qualified'])),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['validate','seal'])
    args=parser.parse_args()
    globals()[args.phase]()

