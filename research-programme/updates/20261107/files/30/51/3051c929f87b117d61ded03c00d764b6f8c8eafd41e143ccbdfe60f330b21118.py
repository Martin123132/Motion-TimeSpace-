import re
from tail_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    folder.mkdir(parents=True, exist_ok=False)
    scripts = sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    checks, inputs, total = [], [], 0
    packets = sorted([*(ROOT / 'runs').glob('*/status.json'), *(ROOT / 'results').glob('*/status.json')])
    for path in packets:
        packet = json.loads(path.read_text())
        assert packet['state'] == 'complete' and (path.parent / 'COMPLETE').is_file(), path
        assert packet['count'] == len(packet['checks']) and packet['all_checks_passed'], path
        assert all(item['passed'] for item in packet['checks']), path
        assert packet['script_sha256'] in {digest(script) for script in scripts}, path
        for name, expected in packet['input_hashes'].items():
            assert Path(name).is_file() and digest(name) == expected, (path, name)
        for array in path.parent.glob('*.npz'):
            with np.load(array) as data:
                assert all(np.isfinite(data[key]).all() for key in data.files), array
            inputs.append(array)
        inputs.append(path)
        total += packet['count']
        checks.append(dict(name='Completed packet and unchanged inputs: ' + path.parent.name, passed=True))
    assert len(packets) == 14 and total == 132, (len(packets), total)
    documents = [ROOT / name for name in ['DERIVATION.md', 'RESULTS.md', 'SOURCES.md', 'RESUME.md']]
    citations = set()
    for document in documents:
        for reference in re.findall(r'`([^`]+)`', document.read_text(encoding='utf-8')):
            if reference.endswith(('.md', '.json', '.npz', '.py', '.dat', '.html')):
                target = (ROOT / reference).resolve()
                assert target.is_file(), (document, reference)
                citations.add(target)
    urls = ['https://arxiv.org/html/2005.06941v1', 'https://arxiv.org/abs/1109.6552']
    assert all(url in (ROOT / 'SOURCES.md').read_text() for url in urls)
    checks.append(dict(name='Local citations exist and consulted primary URLs recorded', passed=True))
    pilot = (ROOT / 'solve_tail.py').read_text()
    production = (ROOT / 'evolve_tail.py').read_text()
    old_line = "print(json.dumps({key: value for key, value in report.items() if key not in ['input_hashes', 'beta_driver']}), flush=True)"
    new_line = "print(json.dumps(dict(name=arguments.name, passed=report['all_checks_passed'], elapsed=report['elapsed'], core_error=report['max_core_departure_from_source_target'], boundary_power=power), default=lambda value: value.item()), flush=True)"
    assert pilot.replace(old_line, new_line) == production
    assert (ROOT / 'runs/heavy-pilot/CONSOLE-FAILURE.md').is_file()
    checks.append(dict(name='Pilot operational failure preserved; production only repairs console output', passed=True))
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    assert review['driven_nonthermal_infrared_tail_solved'] and review['positive_kernel_residual_certificate_executed']
    for key in ['full_parent_history_feedback_applied', 'new_background_evolution', 'full_thermal_gas_collision_source',
                'full_finite_recoil_virtual_remainder_bounded', 'collective_plasma_completion',
                'unconditional_zero_frequency_solution', 'new_empirical_fit', 'new_parent_theory']:
        assert review[key] is False, key
    comparison = json.loads((ROOT / 'results/comparison/status.json').read_text())
    assert all(row['correction_error_ratio'] < .001 for row in comparison['rows'])
    assert comparison['full_parent_history_feedback_applied'] is False
    regularity = json.loads((ROOT / 'results/regularity-certificate/status.json').read_text())
    assert regularity['zero_source_imposed'] is False
    assert all(row['upper_boundary_barrier_power'] == 8 for row in regularity['rows'])
    assert all(row['upper_barrier_gaps']['10'] < 0 for row in regularity['rows'])
    checks.append(dict(name='Driven scope, nonzero source and rejected stronger barrier remain explicit', passed=True))
    parent = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert len(parent['file_hashes']) == 80
    for name, expected in parent['file_hashes'].items():
        assert digest(PARENT / name) == expected, name
    checks.append(dict(name='All80 Stage89 payloads unchanged', passed=True))
    assert not list(ROOT.rglob('__pycache__'))
    checks.append(dict(name='All scripts compile without bytecode', passed=True))
    finish(folder, dict(checks=checks, accepted_scientific_checks=total, checked_packets=len(packets),
        compiled_scripts=len(scripts), all_current_acceptance_checks_passed=True,
        local_citations=[str(path) for path in sorted(citations)], recorded_web_urls=urls,
        retained_operational_failure_count=1, physical_failed_checks=0,
        counts_are_tests_not_independent_discoveries=True), __file__,
        [*scripts, *inputs, *documents, *citations, ROOT / 'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(packets=len(packets), scientific_checks=total, validation_checks=len(checks), scripts=len(scripts))), flush=True)


if __name__ == '__main__':
    main()
