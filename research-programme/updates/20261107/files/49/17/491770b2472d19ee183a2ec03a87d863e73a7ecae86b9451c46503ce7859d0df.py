from source207 import *


RESTART_SHA='acab1d3b714bbe9af299aabd75f32bc4d9cc6f33ecef51f6f8e125778f2ad360'


def authenticate():
    ledger_path=ROOT/'results/restart-integrity.json'
    assert digest(ledger_path)==RESTART_SHA
    ledger=read(ledger_path)
    config=protocol()
    manifest=runner.verify_frozen()
    assert ledger['counts']==dict(prediction=36,actual=25)
    assert ledger['next_actual_event']==25 and not ledger['failed_checks']
    assert ledger['configuration_sha256']==digest(ROOT/'configuration.json')
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SHA
    for name,value in ledger['immutable_file_hashes'].items():
        assert digest(ROOT/name)==value,name
    for bookmark in ledger['bookmarks']:
        assert digest(bookmark['path'])==bookmark['current_sha256']
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    assert not read(ROOT/'results/adapter-validation.json')['failed_checks']
    assert not read(ROOT/'results/preparation.json')['failed_checks']
    assert config['partial_panel']==config['original_panel']
    assert config['source_prediction_tolerance']==.01 and config['identity_tolerance']==1e-10
    assert not list(ROOT.rglob('__pycache__'))
    assert not list(ROOT.rglob('*.partial')) and not list(ROOT.rglob('*.tmp'))
    for script in ROOT.glob('*.py'):
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    counts={}
    for kind in ('prediction','actual'):
        paths=sorted((ROOT/kind).glob('event-*.npz'))
        counts[kind]=len(paths)
        for index,path in enumerate(paths):
            assert path.name==f'event-{index:02d}.npz'
            record=read(path.with_suffix('.json'))
            assert digest(path)==record['sha256'] and not record['failed_checks']
            assert digest(record['loop_path'])==record['loop_sha256']
            assert record['new_virtual_integrals']==0
            if kind=='actual':
                assert datetime.fromisoformat(record['started_utc'])>datetime.fromisoformat(manifest['frozen_utc'])
    assert counts['prediction']==36 and 25<=counts['actual']<=36
    return ledger,counts,len(inputs)


def main(seconds):
    destination=ROOT/'results/resume-verification.json'
    assert not destination.exists()
    ledger,counts,input_count=authenticate()
    assert counts['actual']==25
    write(destination,dict(verified=True,restart_sha256=RESTART_SHA,counts_before=counts,
        saved_payloads_verified=len(ledger['immutable_file_hashes']),inputs_rehashed=input_count,
        configuration_sha256=digest(ROOT/'configuration.json'),
        frozen_manifest_sha256=digest(ROOT/'frozen/prediction-manifest.json'),
        checked_at=datetime.now(timezone.utc).isoformat(),next_actual_event=25,
        new_virtual_integrals_this_resume=0,source_prediction_tolerance=.01,identity_tolerance=1e-10))
    print(json.dumps(dict(state='restart_authenticated',counts=counts,inputs_rehashed=input_count)),flush=True)
    runner.run('actual',seconds)
    for name,value in ledger['immutable_file_hashes'].items():
        assert digest(ROOT/name)==value,name
    progress=read(ROOT/'progress.json')
    finished=len(list((ROOT/'actual').glob('event-*.npz')))
    write(ROOT/'results/resume-outcome.json',dict(state=progress['state'],actual_events=finished,
        new_actual_events=finished-counts['actual'],original_saved_payloads_unchanged=True,
        predictions_recomputed=False,virtual_inputs_recomputed=False,
        source_comparison_complete=False,finished_at=datetime.now(timezone.utc).isoformat()))
    print(json.dumps(dict(state=progress['state'],actual_events=finished,new_actual_events=finished-counts['actual'])),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--seconds',type=float,default=10800)
    args=parser.parse_args()
    main(args.seconds)
