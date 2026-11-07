import re
from nonlocal_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    folder.mkdir(parents=True, exist_ok=False)
    scripts = sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    script_hashes = {digest(path) for path in scripts}
    statuses = sorted([*(ROOT / 'results').glob('*/status.json'),
                       *(ROOT / 'banks').glob('*/status.json'),
                       *(ROOT / 'backgrounds').glob('*/status.json')])
    checks, inputs, count = [], [], 0
    for path in statuses:
        packet = json.loads(path.read_text())
        assert packet['state'] == 'complete' and (path.parent / 'COMPLETE').is_file(), path
        assert packet['script_sha256'] in script_hashes and packet['count'] == len(packet['checks']), path
        assert packet['all_checks_passed'] and all(row['passed'] for row in packet['checks']), path
        for input_path, expected in packet['input_hashes'].items():
            assert Path(input_path).is_file() and digest(input_path) == expected, (path, input_path)
        for array_path in path.parent.glob('*.npz'):
            with np.load(array_path) as saved:
                assert all(np.isfinite(saved[key]).all() for key in saved.files), array_path
            inputs.append(array_path)
        checks.append(dict(name='Completed packet and input integrity: ' + path.parent.name, passed=True))
        inputs.append(path)
        count += packet['count']
    assert len(statuses) == 22 and count == 159, (len(statuses), count)
    documents = [ROOT / name for name in ['DERIVATION.md', 'RESULTS.md', 'SOURCES.md', 'RESUME.md']]
    citations = set()
    for document in documents:
        for reference in re.findall(r'`([^`]+)`', document.read_text(encoding='utf-8')):
            if reference.endswith(('.json', '.npz', '.py', '.md', '.html', '.pdf', '.dat')):
                target = (ROOT / reference).resolve()
                if target == ROOT / 'results/stage-integrity.json':
                    continue
                assert target.is_file(), (document, reference)
                citations.add(target)
    urls = ['https://arxiv.org/html/2005.06941v1', 'https://arxiv.org/abs/1109.6552',
            'https://academic.oup.com/mnras/article/454/4/4182/999273']
    assert all(url in (ROOT / 'SOURCES.md').read_text(encoding='utf-8') for url in urls)
    checks.append(dict(name='Cited paths exist and source URLs are recorded', passed=True))
    assert not list(ROOT.rglob('__pycache__'))
    checks.append(dict(name='All current scripts compile without bytecode', passed=True))
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    assert review['both_leading_backgrounds_updated'] and review['hard_spectrum_infrared_slope_derived']
    for key in ['full_thermal_gas_collision_source', 'complete_finite_temperature_polarized_operator',
                'actual_nonthermal_infrared_tail_solved', 'collective_plasma_completion',
                'full_finite_recoil_virtual_remainder_bounded', 'new_empirical_fit', 'new_parent_theory']:
        assert not review[key], key
    comparison = json.loads((ROOT / 'results/history-comparison/status.json').read_text())
    assert all(row['value'] == 0 for row in comparison['checks'] if row['name'].startswith('Unchanged retained control'))
    assert all(row['structural_change_time_refinement'] < .002 for row in comparison['rows'])
    checks.append(dict(name='Old controls exact and structural effect distinguished from higher-order sensitivity', passed=True))
    correction = json.loads((ROOT / 'results/infrared-domain-corrected/status.json').read_text())
    raw = json.loads((ROOT / 'results/infrared-domain/status.json').read_text())
    assert correction['authoritative_for_plasma_scale'] and not correction['historical_evolutions_affected']
    for before, after in zip(raw['rows'], correction['rows']):
        assert abs(after['plasma_frequency_over_temperature'] / before['plasma_frequency_over_temperature'] / math.sqrt(np.pi) - 1) < 1e-13
        assert after['dc_hard_slope'] == before['dc_hard_slope']
    assert len(review['raw_superseded_diagnostics']) == 1
    checks.append(dict(name='Incorrect raw plasma diagnostic explicitly superseded by independent normalization', passed=True))
    previous = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert len(previous['file_hashes']) == 84
    for relative_path, expected in previous['file_hashes'].items():
        assert digest(PARENT / relative_path) == expected, relative_path
    checks.append(dict(name='All84 Stage88 payloads unchanged', passed=True))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=True,
           all_current_acceptance_checks_passed=True, accepted_scientific_checks=count,
           checked_packets=len(statuses), compiled_scripts=len(scripts),
           local_citations=[str(path) for path in sorted(citations)], recorded_web_urls=urls,
           raw_plasma_diagnostic_superseded=True, counts_are_tests_not_independent_discoveries=True),
           __file__, [*scripts, *inputs, *documents, *citations, ROOT / 'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(packets=len(statuses), scientific_checks=count,
                         validation_checks=len(checks), scripts=len(scripts))), flush=True)


if __name__ == '__main__':
    main()
