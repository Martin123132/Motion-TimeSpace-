from common197 import *
import zipfile

def snapshot():
    config=frozen()
    destination=ROOT/'results/resume-before.zip'
    assert not destination.exists()
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,value in config['bookmark_hashes'].items():
            path=Path(name);assert digest(path)==value
            archive.writestr(path.name,path.read_bytes())
    print('Original resume bytes snapshotted.',flush=True)

def finish():
    config=frozen();status=read(ROOT/'results/status.json');independent=read(ROOT/'results/independent-validation.json')
    assert status['all_checks_passed'] and not independent['failed_checks']
    checks=[];stable=[]
    for path in sorted((ROOT/'comparisons').glob('*.npz')):
        data=packet(path);heat=float(data['heat']);measure=data['measure']
        before=heat*data['saved_residual'];delta=heat*data['delta_residual']
        before_norm=response.norm(before,measure);after_norm=response.norm(before+delta,measure)
        numerator=np.array([math.fsum(float(value) for value in measure*(2*before[:,column]*delta[:,column]+delta[:,column]**2)) for column in range(6)])
        change=numerator/(after_norm+before_norm)
        rounded=data['conditional_metrics'][3]-data['saved_metrics'][3]
        allowance=128*np.finfo(float).eps*(after_norm+before_norm)
        check(checks,path.stem+':stable norm-change versus rounded readout',np.max(abs(change-rounded)/np.maximum(allowance,1e-300)),1.,'identity')
        stable.append(dict(case=path.stem,stable_residual_norm_change=change.tolist(),rounded_subtraction=rounded.tolist(),
                           significance='direct vector increment is primary; stable norm difference avoids subtracting two large norms'))
    write(ROOT/'results/stable-norm-change.json',dict(rows=stable,checks=checks))
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        bookmarks=[]
        for name,value in config['bookmark_hashes'].items():
            path=Path(name);original=archive.read(path.name)
            assert hashlib.sha256(original).hexdigest()==value
            current=path.read_bytes();marker=b'# Stage196 COMPLETE'
            offset=current.index(marker)
            suffix=current[offset:]
            exact=suffix==original
            normalized=suffix.replace(b'\r\n',b'\n')==original.replace(b'\r\n',b'\n')
            check(checks,path.name+':original resume body preserved',int(not normalized),0,'integrity')
            bookmarks.append(dict(path=str(path),old_sha256=value,new_sha256=digest(path),
                                  old_body_bytes_identical=exact,old_body_text_identical=normalized))
    write(ROOT/'results/bookmarks.json',bookmarks)
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    for model in ('heavy','cold'):
        for count in (2048,4096):
            folder=ROOT/'responses'/f'{model}-{count}'
            assert digest(folder/'terminal.npz')==read(folder/'status.json')['terminal_sha256']
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.partial'))
    protected=BRANCH.parent.parent/'formalization-workbench'
    start=datetime.fromisoformat(config['started_utc']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=start]
    check(checks,'formalization-workbench recent changes',len(changed),0,'integrity')
    assert all(row['passed'] for row in checks)
    write(ROOT/'results/final-validation.json',dict(checks=checks,failed_checks=[],consumed_inputs_rehashed=len(inputs),
          scripts_compiled=len(list(ROOT.glob('*.py'))),protected_workbench_recent_modified_file_count=len(changed)))
    write(ROOT/'progress.json',dict(state='complete',active_numerical_workers=0,final_epoch_reached=True,
          scope='local interval contribution only',completed_utc=datetime.now(timezone.utc).isoformat()))
    destination=ROOT/'results/stage-integrity.json';assert not destination.exists()
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    parent=read(PARENT/'results/stage-integrity.json')
    inherited=parent['inherited_sealed_payload_count']+len(parent['file_hashes'])
    seal=dict(state='complete',stage=197,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
              parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=SEAL,
              inherited_context='Parent seal retains earlier provenance fields and failures; follow its authenticated path, not a fresh whole-archive rehash',
              inherited_sealed_payload_count=inherited,file_hashes=hashes,consumed_and_immediate_rehashed=inputs,
              latest_supported_panel_response=str(ROOT/'results/status.json'),source_scope=status['scope'],
              original_bank_changed=False,source_curve_changed=False,tolerances_changed=False,grids_changed=False,
              full_history_prediction_updated=False,new_observational_test=False,
              stage_retained_failures=0,protected_workbench_recent_modified_file_count=len(changed),
              maximum_active_workers=1,active_workers_at_seal=0,library_threads_per_worker=1,
              github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md'))
    write(destination,seal)
    for name,value in hashes.items():
        assert digest(ROOT/name)==value,name
    print(json.dumps(dict(state='complete',payloads=len(hashes),cumulative=inherited+len(hashes),
                          seal_sha256=digest(destination),inputs=len(inputs),bookmarks=bookmarks,
                          stable_norm_changes=[row for row in stable if 'cubic-m20' in row['case']])),flush=True)

if __name__=='__main__':
    if '--snapshot' in sys.argv:
        snapshot()
    else:
        finish()
