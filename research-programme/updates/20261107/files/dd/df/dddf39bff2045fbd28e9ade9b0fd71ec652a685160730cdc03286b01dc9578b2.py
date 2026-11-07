from common232 import *
import argparse


def validate():
    modest()
    protocol()
    for name, expected in read(ROOT / 'assessment-configuration.json')['hashes'].items():
        assert digest(ROOT / name) == expected
    assert digest(ROOT / 'real_rotation232.py') == read(ROOT / 'rotation-configuration.json')['script_sha256']
    reports = [read(ROOT / ('results/' + name)) for name in ('assessment.json', 'interface.json', 'real-rotation.json')]
    assert all(report['qualified'] for report in reports)
    checks = [row for report in reports for row in report['checks']]
    inputs = read(ROOT / 'results/assessment-inputs.json')
    for path, expected in read(ROOT / 'results/interface-inputs.json').items():
        assert path not in inputs or inputs[path] == expected
        inputs[path] = expected
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
    progress = read(ROOT / 'progress.json')
    assert progress['state'] == 'complete' and len(progress['completed']) == 28
    comparison = reports[0]['comparisons']
    elapsed = sum(read(path)['elapsed_seconds'] for path in (ROOT / 'runs').glob('*/status.json'))
    result = dict(stage=232, state='complete', finished_at=now(), qualified=True, checks=checks, failed=[],
        comparisons=comparison, maximum_refinement=max(row['quadrature_relative_error'] for row in comparison),
        maximum_scheme_change=max(max(row.get('profile', 0), row.get('separator', 0)) for row in comparison),
        maximum_interface_pairing=max(row['photon_gas_pairing'] for row in reports[1]['results']),
        packet_count=len(progress['completed']), numerical_worker_seconds=elapsed,
        inputs_rehashed=len(inputs), protected_recent_mtime_count=len(changed),
        new_virtual_amplitudes=0, old_sources_modified=0,
        scope='Finite matched unpolarized angular dipole/quadrupole weak projections and derived NR/EOS gas ports at two existing conditional probes; no full spatial wave or population claim')
    assert not (ROOT / 'results/completion.json').exists()
    write(ROOT / 'results/inputs-final.json', inputs)
    write(ROOT / 'results/completion.json', result)
    print(json.dumps({name: value for name, value in result.items() if name not in ('checks', 'comparisons')}), flush=True)


def seal():
    result = read(ROOT / 'results/completion.json')
    assert result['qualified']
    for path, expected in read(ROOT / 'results/inputs-final.json').items():
        assert digest(path) == expected, path
    target = ROOT / 'results/stage-integrity.json'
    assert not target.exists()
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    for bookmark in bookmarks:
        assert bookmark.read_text(encoding='utf-8').startswith('# Stage232 SAVED')
    files = {str(path.relative_to(ROOT)): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file()}
    write(target, dict(stage=232, state='complete', qualified=True, sealed_at=now(), file_hashes=files,
        bookmarks={str(path): digest(path) for path in bookmarks}, directly_consumed_inputs=read(ROOT / 'results/inputs-final.json'), scope=result['scope']))
    print(json.dumps(dict(seal_sha256=digest(target), files=len(files), checks=len(result['checks']))), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['validate', 'seal'])
    arguments = parser.parse_args()
    validate() if arguments.mode == 'validate' else seal()
