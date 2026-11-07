from common227 import *

def validate():
    config=protocol()
    inputs=read(ROOT/'inputs.json');rows=[]
    for model in parent.MODELS:
        report=read(ROOT/f'envelopes/{model}/complete.json')
        rows.extend(dict(row,name=model+':'+row['name']) for row in report['checks'])
        for path,value in read(ROOT/f'inputs-{model}.json').items():
            assert path not in inputs or inputs[path]==value,path
            inputs[path]=value
    report=read(ROOT/'results/probes.json')
    rows.extend(dict(row,name='probes:'+row['name']) for row in report['checks'])
    for path,value in read(ROOT/'inputs-probes.json').items():
        assert path not in inputs or inputs[path]==value,path
        inputs[path]=value
    for path,value in inputs.items():
        assert digest(path)==value,path
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'no bytecode or partial files',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial'))),0,'integrity')
    since=datetime.fromisoformat(config['turn_start']).timestamp()
    protected=BRANCH.parent.parent/'formalization-workbench'
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
    check(rows,'protected recent-mtime guard',len(changed),0,'integrity')
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'inputs-final.json',inputs)
    write(ROOT/'results/validation.json',dict(stage=227,checks=rows,failed_checks=failed,qualified=not failed,
        inputs_rehashed=len(inputs),protected_recent_mtime_count=len(changed),finished_at=now(),
        scope='Sourced continuous reference return-force envelope and closed metric-rate channel within retained weak model',
        all_higher_order_thermal_terms_claimed=False))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),inputs=len(inputs),failures=failed[:10])),flush=True)

def seal():
    protocol()
    report=read(ROOT/'results/validation.json')
    inputs=read(ROOT/'inputs-final.json')
    for path,value in inputs.items():
        assert digest(path)==value,path
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):
        assert (ROOT/name).is_file()
    path=ROOT/'results/stage-integrity.json'
    assert not path.exists()
    write(path,dict(stage=227,state='complete',qualified=report['qualified'],sealed_at=now(),
        consumed_and_immediate_rehashed=inputs,
        file_hashes={file.relative_to(ROOT).as_posix():digest(file) for file in ROOT.rglob('*') if file.is_file() and file!=path},
        bookmarks={str(file):digest(file) for file in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')},
        scope=report['scope']))
    print(json.dumps(dict(seal=str(path),sha256=digest(path),qualified=report['qualified'])),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['validate','seal'])
    globals()[parser.parse_args().phase]()

