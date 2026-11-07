from response217 import *


def validate():
    config=protocol()
    original=read(ROOT/'results/validation.json')
    repair=read(ROOT/'results/reference-repair.json')
    diagnosis=read(ROOT/'results/energy-readout-diagnosis.json')
    assert digest(ROOT/'reference-repair-contract.json')==repair['contract_sha256']
    contract=read(ROOT/'reference-repair-contract.json')
    for name,value in contract['files'].items():
        assert digest(ROOT/name)==value,name
    for name,value in repair['files'].items():
        assert digest(ROOT/name)==value,name
    for name,value in diagnosis['input_hashes'].items():
        assert digest(name)==value,name
    replaced=[row for row in original['checks'] if ':independent physical solve:' in row['name']]
    assert len(replaced)==864
    original_failed=original['failed_checks']
    assert len(original_failed)==48
    assert all(':independent physical solve:energy:' in row['name'] for row in original_failed)
    rows=[row for row in original['checks'] if ':independent physical solve:' not in row['name']]
    rows.extend(dict(row,name='readout diagnosis:'+row['name']) for row in diagnosis['checks'])
    rows.extend(dict(row,name='repaired reference:'+row['name']) for row in repair['checks'])
    for model in config['models']:
        for count in config['counts']:
            folder=ROOT/f'cases/{model}-{count}'
            result=read(folder/'result.json')
            for name,value in result['file_hashes'].items():
                assert digest(folder/name)==value,name
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    for name,value in config['bookmarks'].items():
        assert digest(name)==value,name
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.partial'))
    protected=BRANCH.parent.parent/'formalization-workbench'
    since=datetime.fromisoformat(config['turn_start']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
    assert not changed,changed
    failed=[row for row in rows if not row['passed']]
    witnesses=[ROOT/'results/validation.json',ROOT/'results/reference-repair.json',ROOT/'results/energy-readout-diagnosis.json',ROOT/'inputs.json']
    report=dict(stage=217,checks=rows,failed_checks=failed,qualified=not failed,
        retained_initial_failures=original_failed,superseded_reference_checks=replaced,
        replacement_reason='reference protected energy assembled from the mass matrix used in the same independent solve; measured row-rounding defect verified',
        original_reference_failure_count=48,current_failure_count=len(failed),
        inputs_rehashed=len(inputs),protected_recent_mtime_count=0,guard_scope='mtime, not full-tree content hash',
        evidence_hashes={str(path.relative_to(ROOT)):digest(path) for path in witnesses},
        original_bank_changed=False,source_changed=False,grids_changed=False,tolerances_changed=False,
        reference_energy_readout_changed=True,physical_trajectory=False,complete_frequency_operator=False)
    write(ROOT/'results/current-validation.json',report)
    print(json.dumps(dict(checks=len(rows),failed=len(failed),original_failures_retained=48,qualified=not failed,inputs=len(inputs))),flush=True)


def seal():
    config=protocol();validation=read(ROOT/'results/current-validation.json')
    for name,value in validation['evidence_hashes'].items():
        assert digest(ROOT/name)==value,name
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):
        assert (ROOT/name).is_file()
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            before=archive.read(Path(name).name)
            assert hashlib.sha256(before).hexdigest()==value and Path(name).read_bytes().endswith(before)
            bookmarks.append(dict(path=name,current_sha256=digest(name),previous_sha256=value,previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='complete',qualified=validation['qualified'],cases_complete=4,active_workers=0,completed_at=now(),
        original_reference_failures_retained=48,authoritative_validation='results/current-validation.json'))
    destination=ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(stage=217,state='complete',qualified=validation['qualified'],sealed_at=now(),
        parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        consumed_and_immediate_rehashed=read(ROOT/'inputs.json'),file_hashes=hashes,
        retained_initial_failures=48,retained_current_failures=validation['current_failure_count'],
        authoritative_validation='results/current-validation.json',original_bank_changed=False,source_changed=False,
        grids_changed=False,tolerances_changed=False,reference_energy_readout_changed=True,
        physical_trajectory=False,complete_frequency_operator=False,permission_to_propagate=False,
        active_workers_at_seal=0,github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md')))
    print(json.dumps(dict(sha256=digest(destination),payloads=len(hashes),qualified=validation['qualified'])),flush=True)


if __name__=='__main__':
    inherited.source.modest()
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['validate','seal'])
    args=parser.parse_args();{'validate':validate,'seal':seal}[args.phase]()
