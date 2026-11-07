from common231 import *
import argparse


def validate():
    modest()
    protocol()
    for configuration in ('supplement-configuration.json', 'port-configuration.json'):
        for name, expected in read(ROOT / configuration)['hashes'].items():
            assert digest(ROOT / name) == expected, name
    reports = [read(ROOT / ('results/' + name)) for name in ('exact-recheck.json', 'background-defects.json', 'collision-ports.json')]
    assert all(report['qualified'] for report in reports)
    original = read(ROOT / 'results/local-source.json')
    assert digest(ROOT / 'results/local-source.json') == reports[0]['preserved_failed_report_sha256']
    checks = [row for report in reports for row in report['checks']]
    assert all(row['passed'] for row in checks)
    inputs = read(ROOT / 'results/port-inputs.json')
    sources = [
        'emitting-thermal-background-20261008/infrared_ladder.py',
        'infrared-source-domain-20261008/nonlocal_dc.py',
        'angular-emission-kernel-20261008/RESULTS.md',
        'emitting-wave-response-20261008/RESULTS.md',
        'mixed-bath-transport-20261007/RESULTS.md',
        'matched-weak-redistribution-20261008/RESULTS.md',
        'rectangular-matched-source-20261008/RESULTS.md',
        'complete-panel-operator-final-20261026/NEXT.md',
        'full-panel-short-history-response-20261026/NEXT.md']
    for source in sources:
        register(inputs, BRANCH / source)
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    protected = BRANCH.parent.parent / 'formalization-workbench'
    since = datetime.fromisoformat(START).timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    assert not changed
    assert not list(ROOT.rglob('__pycache__'))
    diagnostics = [row for row in original['records'] if 'represented_vs_discrete_transfer_relative' in row]
    sound = []
    for model in ('heavy', 'cold'):
        for index in (0, 6400):
            values = {row['kind']: row for row in original['records'] if row['model'] == model and row['count'] == 6400 and row['index'] == index}
            sound.append(dict(model=model, index=index, NR=values['NR']['sound_squared'], EOS=values['EOS']['sound_squared'],
                relative_change=values['EOS']['sound_squared'] / values['NR']['sound_squared'] - 1))
    report = dict(stage=231, state='complete', qualified=True, finished_at=now(), checks=checks, failed=[],
        exact=reports[0]['exact'], original_failed_report_retained=True,
        represented_bank_step_energy_discrepancy=max(abs(row['represented_vs_discrete_transfer_relative']) for row in diagnostics),
        sampled_gas_background_defect_over_H=max(abs(row['gas_background_defect_over_H']) for row in diagnostics),
        gas_sound_speed_squared=sound, background_defect_refinement=reports[1]['results'],
        maximum_source_boost_boundary_fraction=max(abs(row['boundary_over_bulk']) for row in reports[2]['records']),
        maximum_EOS_increment_coefficient_refinement=max(row['relative_change'] for row in original['refinements']),
        inputs_rehashed=len(inputs), protected_recent_mtime_count=len(changed),
        scope='Local EOS/source interface and exact forced constraint law on retained MTS parents; numerical coefficient and source tests, not a new fit or completed angular transport wave')
    assert not (ROOT / 'results/completion.json').exists()
    write(ROOT / 'results/inputs-final.json', inputs)
    write(ROOT / 'results/completion.json', report)
    print(json.dumps({name: value for name, value in report.items() if name not in ('checks',)}), flush=True)


def seal():
    report = read(ROOT / 'results/completion.json')
    assert report['qualified']
    for path, expected in read(ROOT / 'results/inputs-final.json').items():
        assert digest(path) == expected, path
    target = ROOT / 'results/stage-integrity.json'
    assert not target.exists()
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    for path in bookmarks:
        assert path.read_text(encoding='utf-8').startswith('# Stage231 SAVED')
    files = {str(path.relative_to(ROOT)): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file()}
    write(target, dict(stage=231, state='complete', qualified=True, sealed_at=now(), file_hashes=files,
        bookmarks={str(path): digest(path) for path in bookmarks}, directly_consumed_inputs=read(ROOT / 'results/inputs-final.json'),
        scope=report['scope']))
    print(json.dumps(dict(seal_sha256=digest(target), files=len(files), checks=len(report['checks']))), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['validate', 'seal'])
    arguments = parser.parse_args()
    validate() if arguments.mode == 'validate' else seal()
