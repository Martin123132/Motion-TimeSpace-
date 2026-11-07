from common223 import *
import tail223

def validate():
    config=protocol()
    tail223.tail_protocol()
    continuation=read(ROOT/'continuation-configuration.json')
    for name,value in continuation['hashes'].items():
        assert digest(ROOT/name)==value,name
    rows=[]
    spectrum=read(ROOT/'results/final-spectrum-reference.json')
    assert digest(ROOT/'spectrum223.py')==spectrum['configuration']['script_sha256']
    rows.extend(spectrum['checks'])
    for scope in ('window','tail'):
        assessment=read(ROOT/f'results/{scope}-assessment.json')
        rows.extend(dict(row,name=scope+':'+row['name']) for row in assessment['checks'])
    inputs=read(ROOT/'inputs.json')
    for path in ROOT.glob('inputs-*.json'):
        if path.name=='inputs-final.json':
            continue
        for name,value in read(path).items():
            assert name not in inputs or inputs[name]==value,name
            inputs[name]=value
    for model in MODELS:
        for count in COUNTS:
            folder=ROOT/f'restart-check/{model}-{count}'
            report=read(folder/'complete.json')
            assert report['script_sha256']==digest(ROOT/'replay223.py')
            for name,value in report['file_hashes'].items():
                assert digest(folder/name)==value,name
            rows.extend(dict(row,name=f'{model}:{count}:restart:'+row['name']) for row in report['checks'])
    for name,value in inputs.items():
        assert digest(name)==value,name
    check(rows,'all consumed/immediate inputs unchanged',0,0,'integrity')
    for name,value in config['frozen_hashes'].items():
        assert digest(ROOT/'frozen'/name)==value,name
    protected=BRANCH.parent.parent/'formalization-workbench'
    since=datetime.fromisoformat(config['turn_start']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
    check(rows,'protected-workbench recent mtime count',len(changed),0,'integrity')
    check(rows,'no bytecode or partial outputs',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial'))),0,'integrity')
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'inputs-final.json',inputs)
    write(ROOT/'results/current-validation.json',dict(stage=223,finished_at=now(),previous_goal_turn='progress',
        checks=rows,failed_checks=failed,qualified=not failed,inputs_rehashed=len(inputs),
        protected_recent_mtime_count=len(changed),guard_scope='recent mtime, not full-tree snapshot',
        source_window=[FIRST_FRACTION,LAST_FRACTION],short_window_target=TARGET_FRACTION,final_fraction=1.,
        bank_unchanged=True,global_curve_unchanged=True,response_grids_unchanged=True,tolerances_unchanged=True,
        unknown_incoming_terms_remain_explicit=True,physical_eighth_incoming_not_assumed=True,
        scope='numerical physical source-window matching and interval-contribution transport; not full cosmological history'))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),inputs=len(inputs),protected_recent_mtime_count=len(changed))),flush=True)

def seal():
    report=read(ROOT/'results/current-validation.json')
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):
        assert (ROOT/name).is_file()
    for name,value in read(ROOT/'inputs-final.json').items():
        assert digest(name)==value,name
    path=ROOT/'results/stage-integrity.json'
    assert not path.exists()
    files={file.relative_to(ROOT).as_posix():digest(file) for file in ROOT.rglob('*') if file.is_file() and file!=path}
    bookmarks={str(file):digest(file) for file in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}
    write(path,dict(stage=223,state='complete',qualified=report['qualified'],sealed_at=now(),
        consumed_and_immediate_rehashed=read(ROOT/'inputs-final.json'),file_hashes=files,bookmarks=bookmarks,
        scope=report['scope']))
    print(json.dumps(dict(seal=str(path),sha256=digest(path),payloads=len(files),qualified=report['qualified'])),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['validate','seal'])
    args=parser.parse_args()
    globals()[args.phase]()

