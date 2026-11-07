from common226 import *
import finish226
import feedback226

def validate():
    feedback226.verify()
    finish226.validate()
    original=read(ROOT/'results/validation.json')
    feedback=read(ROOT/'results/feedback-controls.json')
    rows=original['checks']+[dict(row,name='feedback:'+row['name']) for row in feedback['checks']]
    inputs=read(ROOT/'inputs-final.json')
    for name in ('feedback226.py','complete226.py','FINITE-TIME-FEEDBACK.md','feedback-configuration.json'):
        register(inputs,ROOT/name)
    for path,value in inputs.items():
        assert digest(path)==value,path
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'inputs-complete.json',inputs)
    write(ROOT/'results/completion.json',dict(stage=226,checks=rows,failed_checks=failed,qualified=not failed,
        inputs_rehashed=len(inputs),protected_recent_mtime_count=original['protected_recent_mtime_count'],
        finished_at=now(),scope=original['scope']+'; finite-time return theorem with independent controls',
        metric_return_coefficients_not_numerically_acquired=True))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),inputs=len(inputs))),flush=True)

def seal():
    feedback226.verify()
    report=read(ROOT/'results/completion.json')
    inputs=read(ROOT/'inputs-complete.json')
    for path,value in inputs.items():
        assert digest(path)==value,path
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):
        assert (ROOT/name).is_file()
    path=ROOT/'results/stage-integrity.json'
    assert not path.exists()
    write(path,dict(stage=226,state='complete',qualified=report['qualified'],sealed_at=now(),
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

