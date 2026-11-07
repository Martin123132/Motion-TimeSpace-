from source203 import *


def main():
    config=protocol();manifest=runner.verify_frozen()
    assert not (ROOT/'results/restart-integrity.json').exists()
    files=dict(manifest['files'])
    files['frozen/prediction-manifest.json']=digest(ROOT/'frozen/prediction-manifest.json')
    counts={};checks=[]
    for kind in ('prediction','actual'):
        paths=sorted((ROOT/kind).glob('event-*.npz'))
        counts[kind]=len(paths)
        for index,path in enumerate(paths):
            assert path.name==f'event-{index:02d}.npz'
            record=read(path.with_suffix('.json'))
            assert digest(path)==record['sha256'] and not record['failed_checks']
            assert digest(record['loop_path'])==record['loop_sha256'] and record['new_virtual_integrals']==0
            for item in (path,path.with_suffix('.json')):files[str(item.relative_to(ROOT))]=digest(item)
            checks.extend(dict(row,name=f'{kind}:{index}:'+row['name']) for row in record['checks'])
    assert counts['prediction']==36 and counts['actual']<36
    assert not list(ROOT.rglob('*.partial')) and not list(ROOT.rglob('*.tmp'))
    for name,value in read(ROOT/'inputs.json').items():assert digest(name)==value,name
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            path=Path(name);before=archive.read(path.name)
            assert hashlib.sha256(before).hexdigest()==value
            current=path.read_bytes()
            assert current.startswith(b'# Stage203 SAFE RESTART')
            assert current[current.index(b'# Stage202 COMPLETE'):]==before
            bookmarks.append(dict(path=str(path),previous_sha256=value,current_sha256=digest(path),previous_body_preserved=True))
    protected=BRANCH.parent.parent/'formalization-workbench'
    started=datetime.fromisoformat(config['started_utc']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    assert not changed,changed
    write(ROOT/'results/restart-integrity.json',dict(stage=203,state='safe_restart',counts=counts,
        next_actual_event=counts['actual'],qualified=False,source_comparison_complete=False,
        saved_at_utc=datetime.now(timezone.utc).isoformat(),configuration_sha256=digest(ROOT/'configuration.json'),
        parent_seal_sha256=PARENT_SHA,immutable_file_hashes=files,bookmarks=bookmarks,
        event_checks=checks,failed_checks=[row for row in checks if not row['passed']],
        protected_workbench_recent_modified_file_count=0,active_numerical_workers=0,new_virtual_integrals=0,
        original_bank_changed=False,histories_changed=False,tolerances_changed=False,github_action=False))
    print(json.dumps(dict(state='safe_restart',counts=counts,next_actual_event=counts['actual'],checks=len(checks))),flush=True)


if __name__=='__main__':
    source.modest()
    main()
