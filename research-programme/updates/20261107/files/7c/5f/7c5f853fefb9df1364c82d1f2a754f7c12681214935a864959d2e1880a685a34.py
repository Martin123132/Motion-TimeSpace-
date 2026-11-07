from run228 import *


def validate():
    protocol()
    thermo = read(ROOT / 'results/thermodynamics-reviewed.json')
    gravity = read(ROOT / 'results/gravity.json')
    derivative = read(ROOT / 'results/derivative-check.json')
    precision = read(ROOT / 'results/precision-check.json')
    assert thermo['qualified'] and precision['qualified']
    excluded = ('all normalized source stress continuity', 'all normalized Raychaudhuri identities')
    assert all(any(text in row['name'] for text in excluded) for row in gravity['failed'])
    assert len(derivative['failed']) == 1 and derivative['failed'][0]['name'] == 'heavy: finest derivative maximum_raychaudhuri'
    accepted_gravity = [row for row in gravity['checks'] if not any(text in row['name'] for text in excluded)]
    analytic = [row for row in derivative['checks'] if 'actual-equation' in row['name']]
    checks = thermo['checks'] + accepted_gravity + analytic + precision['checks']
    assert len(checks) == 104 and all(row['passed'] for row in checks)
    inputs = read(ROOT / 'results/gravity-inputs.json')
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    for manifest in ('derivative-configuration.json', 'precision-configuration.json'):
        for name, expected in read(ROOT / manifest)['input_hashes'].items():
            assert digest(ROOT / name) == expected, name
    repair = read(ROOT / 'protocol-repair.json')
    assert digest(ROOT / 'validate228.py') == repair['verifier_sha256']
    assert digest(ROOT / 'CHECK-REPAIR.md') == repair['notes_sha256']
    assert digest(ROOT / 'results/thermodynamics.json') == repair['original_report_sha256']
    runtime = read(ROOT / 'runtime-repair.json')
    assert digest(ROOT / 'launch228.py') == runtime['launcher_sha256']
    assert digest(ROOT / 'RUNTIME-REPAIR.md') == runtime['notes_sha256']
    assert digest(ROOT / 'configuration.json') == runtime['configuration_sha256']
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    protected = BRANCH.parent.parent / 'formalization-workbench'
    since = datetime.fromisoformat(START).timestamp()
    recent = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    check(checks, 'Protected workbench recent-mtime guard', len(recent), 0)
    check(checks, 'No local bytecode directories', len(list(ROOT.rglob('__pycache__'))), 0)
    assert not (ROOT / 'results/completion.json').exists()
    report = dict(stage=228, state='complete', finished_at=now(), checks=checks,
        qualified=all(row['passed'] for row in checks), failed=[row for row in checks if not row['passed']],
        inputs_rehashed=len(inputs), protected_recent_mtime_count=len(recent),
        retained_failed_reports=['results/thermodynamics.json', 'results/gravity.json', 'results/derivative-check.json'],
        replacements=dict(thermodynamic_normalization='results/thermodynamics-reviewed.json',
            finite_difference_identities='analytic equation checks plus independent high-precision directional probes'),
        scope='Electron-owned EOS, conserved leading-chi full-history heat source, and its retained-parent linear response',
        new_kinetic_evolution_performed=False, no_git_action=True)
    write(ROOT / 'results/completion.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'], inputs=len(inputs), workbench_guard=len(recent))), flush=True)


def seal():
    completion = read(ROOT / 'results/completion.json')
    assert completion['qualified']
    path = ROOT / 'results/stage-integrity.json'
    assert not path.exists()
    files = {str(item.relative_to(ROOT)): digest(item) for item in sorted(ROOT.rglob('*')) if item.is_file()}
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    for bookmark in bookmarks:
        assert bookmark.read_text(encoding='utf-8').startswith('# Stage228 SAVED')
    write(path, dict(stage=228, state='complete', qualified=True, sealed_at=now(),
        file_hashes=files, bookmarks={str(item): digest(item) for item in bookmarks},
        directly_consumed_inputs=read(ROOT / 'results/gravity-inputs.json'), scope=completion['scope']))
    print(json.dumps(dict(seal_sha256=digest(path), payloads=len(files), bookmarks=len(bookmarks))), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'validate':
        validate()
    elif sys.argv[1] == 'seal':
        seal()
    else:
        raise ValueError(sys.argv[1])
