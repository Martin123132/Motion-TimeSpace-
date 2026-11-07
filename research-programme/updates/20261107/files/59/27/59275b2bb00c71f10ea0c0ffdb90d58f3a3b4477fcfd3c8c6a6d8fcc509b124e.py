from matching198 import *
import hashlib,zipfile

def snapshot():
    config=protocol();destination=ROOT/'results/resume-before.zip'
    assert not destination.exists()
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,value in config['bookmarks'].items():
            path=Path(name);assert digest(path)==value
            archive.writestr(path.name,path.read_bytes())
    print('Original resume bytes backed up.',flush=True)

def seal():
    config=protocol();status=read(ROOT/'results/status.json')
    assert status['all_selected_checks_passed']
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    for model in ('heavy','cold'):
        for count in (2048,4096):
            folder=ROOT/'runs-matched'/f'{model}-{count}';report=read(folder/'status.json')
            assert not report['failed_checks']
            for name,value in report['output_hashes'].items():
                assert digest(folder/name)==value,name
    implementations=[]
    for script,folder in [('attempt1-matching198.py','runs'),('attempt2-matching198.py','runs-stable'),
                          ('attempt3-matching198.py','runs-connected'),('matching198.py','runs-matched')]:
        report=read(ROOT/folder/'heavy-2048/status.json')
        implementations.append(dict(script=script,script_sha256=digest(ROOT/script),output_folder=folder,
                                    retained_failed_checks=len(report['failed_checks']),
                                    scope='heavy2048 initial diagnostic' if folder!='runs-matched' else 'selected implementation, both backgrounds/resolutions checked'))
    write(ROOT/'results/implementation-history.json',implementations)
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            path=Path(name);before=archive.read(path.name)
            assert hashlib.sha256(before).hexdigest()==value
            current=path.read_bytes();suffix=current[current.index(b'# Stage197 COMPLETE'):]
            assert suffix==before,path
            bookmarks.append(dict(path=str(path),previous_sha256=value,current_sha256=digest(path),previous_body_bytes_identical=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.partial'))
    workbench=BRANCH.parent.parent/'formalization-workbench';assert workbench.is_dir()
    began=datetime.fromisoformat(config['started_utc']).timestamp()
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>=began]
    assert not changed,changed
    write(ROOT/'results/final-validation.json',dict(inputs_rehashed=len(inputs),selected_failures=0,
          retained_diagnostic_failures=sum(row['retained_failed_checks'] for row in implementations),
          previous_resume_bodies_preserved=True,protected_workbench_recent_modified_file_count=0,
          scripts_compiled=len(list(ROOT.glob('*.py'))),compiled_without_bytecode=True))
    write(ROOT/'progress.json',dict(state='complete',active_numerical_workers=0,completed_utc=datetime.now(timezone.utc).isoformat()))
    destination=ROOT/'results/stage-integrity.json';assert not destination.exists()
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    parent=read(PARENT/'results/stage-integrity.json');assert digest(PARENT/'results/stage-integrity.json')==SEAL
    inherited=parent['inherited_sealed_payload_count']+len(parent['file_hashes'])
    record=dict(state='complete',stage=198,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
                parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=SEAL,
                inherited_sealed_payload_count=inherited,file_hashes=hashes,consumed_and_immediate_rehashed=inputs,
                inherited_context='Follow authenticated parent seals for historical provenance; older archive not rehashed in full',
                latest_matching_contract=str(ROOT/'MATCHING-CONTRACT.json'),latest_response_matching=str(ROOT/'results/status.json'),
                selected_failures=0,retained_diagnostic_failures=64,source_scope=status['scope'],
                original_bank_changed=False,source_curve_changed=False,tolerances_changed=False,grids_changed=False,
                protected_workbench_recent_modified_file_count=0,active_workers_at_seal=0,maximum_active_workers=1,
                library_threads_per_worker=1,github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md'))
    write(destination,record)
    for name,value in hashes.items():
        assert digest(ROOT/name)==value,name
    print(json.dumps(dict(state='complete',payloads=len(hashes),cumulative=inherited+len(hashes),
          seal_sha256=digest(destination),inputs=len(inputs),selected_failures=0,retained_diagnostic_failures=64)),flush=True)

if __name__=='__main__':
    if '--snapshot' in sys.argv:
        snapshot()
    else:
        seal()
