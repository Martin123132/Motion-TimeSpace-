from common225 import *
import finalize225
import sharpen225

def validate():
    sharpen225.sharp_protocol()
    finalize225.validate()
    original=read(ROOT/'results/validation.json')
    sharp=read(ROOT/'results/sharp-bound.json')
    rows=original['checks']+[dict(row,name='sharp:'+row['name']) for row in sharp['checks']]
    inputs=read(ROOT/'inputs-final.json')
    for name,value in read(ROOT/'inputs-sharp.json').items():
        assert name not in inputs or inputs[name]==value,name
        inputs[name]=value
    for path in (ROOT/'completion225.py',ROOT/'results/sharp-bound.json'):
        register(inputs,path)
    for name,value in inputs.items():
        assert digest(name)==value,name
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'inputs-complete.json',inputs)
    write(ROOT/'results/completion.json',dict(stage=225,checks=rows,failed_checks=failed,qualified=not failed,
        inputs_rehashed=len(inputs),protected_recent_mtime_count=original['protected_recent_mtime_count'],
        finished_at=now(),scope=original['scope']+' plus energy/work sharpening',
        retained_original_solver_failure=True,unknown_incoming_and_other_sources_kept=True))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),inputs=len(inputs))),flush=True)

def seal():
    sharpen225.sharp_protocol()
    report=read(ROOT/'results/completion.json')
    inputs=read(ROOT/'inputs-complete.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):
        assert (ROOT/name).is_file()
    path=ROOT/'results/stage-integrity.json'
    assert not path.exists()
    write(path,dict(stage=225,state='complete',qualified=report['qualified'],sealed_at=now(),
        consumed_and_immediate_rehashed=inputs,
        file_hashes={file.relative_to(ROOT).as_posix():digest(file) for file in ROOT.rglob('*') if file.is_file() and file!=path},
        bookmarks={str(file):digest(file) for file in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')},scope=report['scope']))
    print(json.dumps(dict(seal=str(path),sha256=digest(path),qualified=report['qualified'])),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['validate','seal'])
    globals()[parser.parse_args().phase]()
