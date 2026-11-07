import re
from population_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    assert not (folder / 'status.json').exists() and not (folder / 'COMPLETE').exists()
    folder.mkdir(parents=True, exist_ok=True)
    scripts = sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    statuses = sorted([*(ROOT / 'runs').glob('*/status.json'), *(ROOT / 'results').glob('*/status.json')])
    required = ['midpoint-pilot', 'midpoint-population-v2', 'midpoint-population-v3',
                'quarter-population-v2', 'final-population-v2', 'input-and-born-control', 'population-comparison']
    assert set(required).issubset({path.parent.name for path in statuses})
    inputs, checks, scientific = [], [], 0
    for path in statuses:
        packet = json.loads(path.read_text())
        assert packet['state'] == 'complete' and (path.parent / 'COMPLETE').is_file(), path
        assert packet['all_checks_passed'] and all(item['passed'] for item in packet['checks']), path
        assert packet['count'] == len(packet['checks'])
        assert packet['script_sha256'] in {digest(script) for script in scripts}
        for name, expected in packet['input_hashes'].items():
            assert digest(name) == expected, (path, name)
        for array in path.parent.glob('*.npz'):
            with np.load(array) as saved:
                assert all(np.isfinite(saved[key]).all() for key in saved.files)
            inputs.append(array)
        if 'nodes' in packet:
            nodes = sorted((path.parent / 'nodes').glob('*.json'))
            assert len(nodes) == packet['nodes']
            for node in nodes:
                record = json.loads(node.read_text())
                assert record['complete'] and Path(record['cache_path']).is_file()
                assert record['weight'] > 0
                cache = json.loads(Path(record['cache_path']).read_text())
                assert cache['finite'] and cache['scalar'] == record['virtual_scalar']
            inputs.extend(nodes)
        checks.append(dict(name='Completed packet, arrays, node ownership and input integrity: ' + path.parent.name, passed=True))
        inputs.append(path)
        scientific += packet['count']
    documents = [ROOT / name for name in ['DERIVATION.md', 'RESULTS.md', 'SOURCES.md', 'RESUME.md']]
    citations = set()
    for document in documents:
        for reference in re.findall(r'`([^`]+)`', document.read_text(encoding='utf-8')):
            if reference.endswith(('.py', '.npz', '.md', '.json', '.pdf', '.html')):
                target = (ROOT / reference).resolve()
                if target in {ROOT / 'results/stage-integrity.json', folder / 'status.json'}:
                    continue
                assert target.is_file(), (document, reference)
                citations.add(target)
    urls = ['https://arxiv.org/html/2005.06941v1', 'https://doi.org/10.1103/PhysRev.85.231',
            'https://doi.org/10.1103/PhysRevD.46.3630']
    assert all(url in (ROOT / 'SOURCES.md').read_text() for url in urls)
    checks.append(dict(name='Local citations exist and primary source URLs recorded', passed=True))
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    for key in ['new_empirical_fit', 'full_parent_feedback_applied', 'unconditional_all_frequency_source_bound',
                'collective_plasma_completion', 'complete_polarized_source', 'new_parent_theory']:
        assert review[key] is False
    comparison = json.loads((ROOT / 'results/population-comparison/status.json').read_text())
    assert comparison['numerical_finite_domain_energy_projection_accepted']
    assert not comparison['relative_one_percent_precision_claimed'] and not comparison['omitted_seed_tail_bounded']
    assert all(row['continuous_domain_bound'] is False and row['full_spectrum_feedback_applied'] is False for row in comparison['rows'])
    checks.append(dict(name='Finite-domain numerical tolerance is not promoted to a universal physical bound', passed=True))
    controls = json.loads((ROOT / 'results/input-and-born-control/status.json').read_text())
    assert all(item['passed'] for item in controls['checks'])
    assert len(controls['expected_parent_born_energy']) == 2
    checks.append(dict(name='Independent standard Compton baseline retained beside NLO source', passed=True))
    parent = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert len(parent['file_hashes']) == 56
    for name, expected in parent['file_hashes'].items():
        assert digest(PARENT / name) == expected, name
    checks.append(dict(name='All56 Stage90 payloads unchanged', passed=True))
    maximum = max(sum(path.is_file() for path in Path(directory).iterdir()) for directory, unused, files in os.walk(ROOT))
    assert maximum < 1000, maximum
    checks.append(dict(name='Cache and node payloads stay below1000 direct files per folder', passed=True, value=maximum))
    assert not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Scripts compile; no bytecode or interrupted atomic payload remains', passed=True))
    finish(folder, dict(checks=checks, all_current_acceptance_checks_passed=True,
        accepted_scientific_checks=scientific, checked_packets=len(statuses), compiled_scripts=len(scripts),
        local_citations=[str(path) for path in sorted(citations)], recorded_web_urls=urls,
        largest_direct_file_count=maximum, physical_failed_checks=0, counts_are_tests_not_independent_proofs=True),
        __file__, [*scripts, *inputs, *documents, *citations, ROOT / 'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(packets=len(statuses), scientific_checks=scientific, validation_checks=len(checks), scripts=len(scripts))), flush=True)


if __name__ == '__main__':
    main()
