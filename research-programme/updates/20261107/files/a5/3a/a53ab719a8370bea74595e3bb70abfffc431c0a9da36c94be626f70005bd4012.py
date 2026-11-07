from common234 import *
import radial234
import assemble234
import argparse


def validate():
    modest()
    config = protocol()
    radial234.radial_protocol()
    assemble234.protocol_assembly()
    checks = []
    report_paths = []
    for folder in ('tensors', 'radial', 'response'):
        for path in sorted((ROOT / folder).glob('*.json')):
            report = read(path)
            assert report['state'] == 'complete' and report['qualified'] and not report['failed'], path
            assert digest(path.with_suffix('.npz')) == report['sha256'], path
            checks.extend(report['checks'])
            report_paths.append(path)
    for filename in ('radial-assessment.json', 'virtual-mixed-assessment.json', 'product-controls.json'):
        path = ROOT / 'results' / filename
        report = read(path)
        assert report['state'] == 'complete' and report['qualified'] and not report['failed'], path
        checks.extend(report['checks'])
        report_paths.append(path)
    blocks = read(ROOT / 'results/virtual-mixed-assessment.json')
    controls = read(ROOT / 'results/product-controls.json')
    frozen_controls = read(ROOT / 'controls-configuration.json')
    assert digest(ROOT / 'controls234.py') == frozen_controls['script_sha256']
    assert digest(ROOT / 'results/virtual-mixed-blocks.npz') == blocks['block_sha256'] == frozen_controls['block_sha256']
    assert len(blocks['records']) == 3 * 2 * 6 * 3
    assert {entry['model'] for entry in blocks['records']} == {'heavy', 'cold'}
    inputs = read(ROOT / 'inputs.json')
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    for path, expected in config['bookmarks'].items():
        assert digest(path) == expected, path
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__'))
    assert not list(ROOT.rglob('*.partial'))
    protected = BRANCH.parent.parent / 'formalization-workbench'
    since = datetime.fromisoformat(START).timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    assert not changed, changed
    check(checks, 'consumed source hashes unchanged', 0, 0)
    check(checks, 'protected workbench recent-mtime count', len(changed), 0)
    responses = [read(path) for path in sorted((ROOT / 'response').glob('*.json'))]
    radials = [read(path) for path in sorted((ROOT / 'radial').glob('*.json'))]
    tensors = [read(path) for path in sorted((ROOT / 'tensors').glob('*.json'))]
    summary = dict(stage=234, state='complete', qualified=True, finished_at=now(), checks=checks, failed=[],
        total_checks=len(checks), anchors=3, hard_event='x=14 event0', original_thermal_rays=8,
        photon_coordinates=98, angular_components=13, history_states=6, infrared_joins=2,
        radial_cells=config['spline_grid_cells'], radial_orders=config['radial_orders'],
        maximum_scalar_cache_replay=max(entry['checks'][-1]['value'] for entry in tensors),
        maximum_thermal_tensor_identity=max(entry['checks'][0]['value'] for entry in responses),
        maximum_radial_identity=max(check['value'] for entry in radials for check in entry['checks']),
        maximum_virtual_block_refinement=max(entry['total_refinement'] for entry in blocks['records']),
        medium_over_statistical_range=[min(entry['medium_over_statistical'] for entry in blocks['records']),
            max(entry['medium_over_statistical'] for entry in blocks['records'])],
        minimum_wave_medium_fraction=min(entry['wave_term_over_medium'] for entry in blocks['records']),
        derivative_controls=controls['maximum'],
        tensor_worker_seconds=sum(entry['seconds'] for entry in tensors),
        radial_worker_seconds=sum(entry['seconds'] for entry in radials),
        response_worker_seconds=sum(entry['seconds'] for entry in responses),
        directly_consumed_inputs_rehashed=len(inputs), protected_recent_mtime_count=0,
        report_hashes={str(path.relative_to(ROOT)): digest(path) for path in report_paths},
        original_bank_changed=False, original_tolerances_changed=False, new_virtual_cache_entries=0,
        full_history_exterior_supplied=False, inclusive_mixed_source_qualified=False,
        polarized_soft_bath_variation_implemented=False, new_empirical_fit=False,
        scope='Finite-domain full98-coordinate unpolarized photon-cut medium map retaining hard-photon polarization, and both mixed scalar-intensity virtual product terms on saved histories; not full inclusive/spatial source')
    assert not (ROOT / 'results/completion.json').exists()
    write(ROOT / 'results/inputs-final.json', inputs)
    write(ROOT / 'results/completion.json', summary)
    print(json.dumps({name: value for name, value in summary.items() if name not in ('checks', 'report_hashes')}), flush=True)


def seal():
    completion = read(ROOT / 'results/completion.json')
    assert completion['qualified']
    for path, expected in read(ROOT / 'results/inputs-final.json').items():
        assert digest(path) == expected, path
    for path, expected in completion['report_hashes'].items():
        assert digest(ROOT / path) == expected, path
    for filename in ('RESULTS.md', 'NEXT.md', 'RUN-NOTES.md'):
        assert (ROOT / filename).exists()
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    assert all(path.read_text(encoding='utf-8').startswith('# Stage234 SAVED') for path in bookmarks)
    target = ROOT / 'results/stage-integrity.json'
    assert not target.exists()
    paths = {str(path.relative_to(ROOT)): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file()}
    write(target, dict(stage=234, state='complete', qualified=True, sealed_at=now(), file_hashes=paths,
        directly_consumed_inputs=read(ROOT / 'results/inputs-final.json'), bookmarks={str(path): digest(path) for path in bookmarks},
        scope=completion['scope'], inclusive_mixed_source_qualified=False))
    print(json.dumps(dict(seal_sha256=digest(target), files=len(paths), checks=completion['total_checks'])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['validate', 'seal'])
    args = parser.parse_args()
    validate() if args.mode == 'validate' else seal()
