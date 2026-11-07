from history242 import *
import target242
from datetime import datetime, timezone


def finish():
    modest()
    config = protocol()
    target_config = target242.target_protocol()
    assert not (ROOT / 'results/stage-integrity.json').exists()
    inputs = dict(read(ROOT / 'inputs.json'))
    primary_checks = []
    reports = ('results/history.json', 'results/tail-rhs.json', 'results/source-history.json', 'target/results/assessment.json')
    for name in reports:
        result = read(ROOT / name)
        assert result['qualified'] and not result['failed'], name
        primary_checks.extend(dict(row, owner=name) for row in result['checks'])
        for path, expected in result.get('consumed_inputs', {}).items():
            register(inputs, path, expected)
    algebra = read(ROOT / 'results/algebra.json')
    assert all(algebra['checks'].values())
    for name, passed in algebra['checks'].items():
        primary_checks.append(dict(name=name, owner='results/algebra.json', passed=passed, value=0, limit=0))
    assert len(primary_checks) == 9891
    assert all(row['passed'] for row in primary_checks)
    for path, expected in target_config['input_manifest'].items():
        register(inputs, path, expected)
    forecast = read(ROOT / 'prediction/configuration.json')
    for path, expected in forecast['consumed_inputs'].items():
        register(inputs, path, expected)
    assert digest(ROOT / 'contract242.py') == forecast['script_sha256']
    assert digest(ROOT / 'prediction/target-prediction.npz') == forecast['output_sha256']
    assert digest(ROOT / 'results/history.json') == forecast['history_sha256']
    assert digest(ROOT / 'tail242.py') == read(ROOT / 'results/tail-rhs.json')['script_sha256']
    assert digest(PARENT / 'results/stage-integrity.json') == SEAL
    for worker in ('real0', 'real1'):
        status = read(ROOT / 'target/workers' / worker / 'status.json')
        assert status['state'] == 'complete'
        import psutil
        if psutil.pid_exists(status['pid']):
            try:
                command = ' '.join(psutil.Process(status['pid']).cmdline())
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                command = ''
            assert 'target242.py' not in command, (status['pid'], command)
    real_records = [path for path in (ROOT / 'target').rglob('ray-*.json') if 'interrupted-20261027' not in path.parts]
    assert len(real_records) == 528
    evaluated_events = 0
    for path in real_records:
        record = read(path)
        assert record['sha256'] == digest(path.with_suffix('.npz'))
        assert record['configuration_sha256'] == digest(ROOT / 'target/configuration.json')
        evaluated_events += record['evaluated_events']
    auxiliary_checks = 0
    for directory in ('virtual', 'state'):
        for path in (ROOT / 'target' / directory).rglob('*.npz'):
            record = read(path.with_suffix('.json'))
            assert record['qualified'] and not record['failed']
            assert record['sha256'] == digest(path)
            auxiliary_checks += len(record['checks'])
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__'))
    protected = BRANCH.parent.parent / 'formalization-workbench'
    start = datetime.fromisoformat('2026-10-27T09:39:36+00:00').timestamp()
    recent = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    assert not recent, recent[:10]
    transfer_path = Path('C:/MTS-Data/stage242-transfer-20261027.json')
    transfer = read(transfer_path)
    assert transfer['phase'] == 'complete'
    assert (ROOT / 'target').resolve() == Path(transfer['destination']).resolve()
    register(inputs, transfer_path)
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    completion = dict(stage=242, state='complete', qualified=True, finished_at=now(),
        primary_checks=len(primary_checks), auxiliary_report_checks=auxiliary_checks,
        real_packets=len(real_records), evaluated_signed_events=evaluated_events,
        directly_consumed_inputs=inputs, protected_recent_mtime_count=len(recent),
        original_bank_changed=False, original_histories_changed=False, original_tolerances_changed=False,
        target_temperature_history_term_calculated=True, tail_rhs_evaluated=True,
        complete_tail_history_repair_evolved=False, explicit_operator_temperature_derivative_complete=False,
        finite_interval_gravity_propagated=False, workers_live=False,
        source_scope=target_config['source_scope'], physical_target=str((ROOT / 'target').resolve()))
    write(ROOT / 'results/completion.json', completion)
    files = {}
    for directory, subdirectories, names in os.walk(ROOT, followlinks=False):
        subdirectories[:] = [name for name in subdirectories if Path(directory) / name != ROOT / 'target']
        for name in names:
            path = Path(directory) / name
            files[path.relative_to(ROOT).as_posix()] = digest(path)
    physical_target = (ROOT / 'target').resolve()
    for path in physical_target.rglob('*'):
        if path.is_file():
            files['target/' + path.relative_to(physical_target).as_posix()] = digest(path)
    bookmarks = {str(path): digest(path) for path in (BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md')}
    write(ROOT / 'results/stage-integrity.json', dict(stage=242, state='complete', qualified=True,
        primary_checks=len(primary_checks), file_hashes=files, directly_consumed_inputs=inputs,
        bookmarks=bookmarks, parent_seal_sha256=SEAL, finished_at=now(),
        source_scope=completion['source_scope'], physical_target=completion['physical_target'],
        full_time_derivative_claimed=False, original_bank_changed=False, original_tolerances_changed=False,
        protected_recent_mtime_count=0, workers_live=False))
    print(dict(stage=242, sealed=True, primary_checks=len(primary_checks), auxiliary_checks=auxiliary_checks,
        files=len(files), consumed_inputs=len(inputs), real_packets=len(real_records),
        seal=digest(ROOT / 'results/stage-integrity.json')), flush=True)


if __name__ == '__main__':
    finish()
