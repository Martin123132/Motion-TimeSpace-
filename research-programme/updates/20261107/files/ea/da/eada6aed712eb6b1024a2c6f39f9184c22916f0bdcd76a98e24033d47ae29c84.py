import re
from rectangular_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    assert not (folder / 'status.json').exists() and not (folder / 'COMPLETE').exists()
    folder.mkdir(parents=True, exist_ok=True)
    scripts = sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    statuses = sorted(path for group in ['runs', 'results', 'comparisons', 'overlaps', 'controls']
                      for path in (ROOT / group).glob('*/status.json') if path.parent != folder)
    expected_failures = {
        'results/input-controls': {'Energy test reproduced analytically'},
        'comparisons/linear-outer': {'Actual96-source-vector refinement within1percent in mass-dual norm'},
        'comparisons/linear-real': {'Actual96-source-vector refinement within1percent in mass-dual norm'},
        'comparisons/log-outer': {'Actual96-source-vector refinement within1percent in mass-dual norm'},
        'comparisons/log-real': {'Actual96-source-vector refinement within1percent in mass-dual norm'},
        'results/source-resolution': {'raw outer full96 source converges within1percent', 'raw real full96 source converges within1percent'},
    }
    inputs, checks, failed_records = [], [], []
    scientific, passed_count = 0, 0
    for path in statuses:
        packet = json.loads(path.read_text())
        assert packet['state'] == 'complete' and (path.parent / 'COMPLETE').is_file(), path
        assert packet['count'] == len(packet['checks'])
        failed = {row['name'] for row in packet['checks'] if not row['passed']}
        name = path.parent.relative_to(ROOT).as_posix()
        assert failed == expected_failures.get(name, set()), (name, failed)
        assert packet['all_checks_passed'] == (not failed)
        assert packet['script_sha256'] in {digest(script) for script in scripts}
        for filename, expected in packet['input_hashes'].items():
            assert digest(filename) == expected, (path, filename)
        for array in path.parent.glob('*.npz'):
            with np.load(array) as saved:
                assert all(np.isfinite(saved[key]).all() for key in saved.files)
            inputs.append(array)
        for node in (path.parent / 'nodes').glob('*.json'):
            row = json.loads(node.read_text())
            assert row['complete'] and row['weight'] > 0
            assert all(np.isfinite(value).all() for value in map(np.asarray, row['parts'].values()))
            inputs.append(node)
        if 'nodes' in packet:
            assert len(list((path.parent / 'nodes').glob('*.json'))) == packet['nodes']
        scientific += len(packet['checks'])
        passed_count += sum(bool(row['passed']) for row in packet['checks'])
        failed_records += [dict(packet=name, test=test) for test in sorted(failed)]
        checks.append(dict(name='Completed packet integrity and truthful acceptance status: ' + name, passed=True))
        inputs.append(path)
    assert set(expected_failures).issubset({path.parent.relative_to(ROOT).as_posix() for path in statuses})
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    resolution = json.loads((ROOT / 'results/source-resolution/status.json').read_text())
    assert resolution['control_variate_source_accepted'] and not resolution['raw_source_accepted']
    assert review['full_source_precision_gate_closed'] and not review['finite_remainder_response_precision_closed']
    for key in ['new_empirical_fit', 'full_parent_feedback_applied', 'new_parent_history',
                'unconditional_all_frequency_source_bound', 'collective_plasma_completion',
                'complete_polarized_source', 'new_parent_theory', 'control_coefficient_fitted',
                'source_smallness_used_to_waive_gate', 'github_action']:
        assert review[key] is False
    assert review['new_virtual_loop_evaluations'] == 0 and review['modes_removed'] == 0
    checks.append(dict(name='Only corrected full source is accepted; finite-remainder response and raw failures stay explicit', passed=True))
    addback = json.loads((ROOT / 'results/leading-addback-control/status.json').read_text())
    assert addback['all_checks_passed'] and not addback['coefficient_fitted']
    checks.append(dict(name='Independent leading addback succeeds without fitting or mode removal', passed=True))
    documents = [ROOT / name for name in ['RESULTS.md', 'DERIVATION.md', 'SOURCES.md', 'RESUME.md']]
    citations = set()
    for document in documents:
        for reference in re.findall(r'`([^`]+)`', document.read_text(encoding='utf-8')):
            if reference.endswith(('.py', '.npz', '.md', '.json', '.pdf', '.html')):
                target = (ROOT / reference).resolve()
                if target in {folder / 'status.json', ROOT / 'results/stage-integrity.json'}:
                    continue
                assert target.is_file(), (document, reference)
                citations.add(target)
    urls = ['https://arxiv.org/html/2005.06941v1']
    assert all(url in (ROOT / 'SOURCES.md').read_text() for url in urls)
    checks.append(dict(name='All cited local artifacts exist and consulted primary URL is recorded', passed=True))
    parent = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert len(parent['file_hashes']) == 6888
    for name, expected in parent['file_hashes'].items():
        assert digest(PARENT / name) == expected, name
    checks.append(dict(name='All6888 Stage91 payloads unchanged', passed=True))
    maximum = max(sum(path.is_file() for path in Path(directory).iterdir()) for directory, unused, files in os.walk(ROOT))
    assert maximum < 1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Scripts compile; no bytecode/interrupted write; each direct folder below1000 files', passed=True, value=maximum))
    finish(folder, dict(checks=checks, accepted_current_scope_verified=True,
        checked_packets=len(statuses), scientific_checks=scientific, passing_scientific_checks=passed_count,
        retained_failed_scientific_checks=scientific - passed_count, retained_failure_records=failed_records,
        compiled_scripts=len(scripts), largest_direct_file_count=maximum,
        local_citations=[str(path) for path in sorted(citations)], recorded_web_urls=urls,
        counts_are_tests_not_independent_proofs=True), __file__,
        [*scripts, *inputs, *documents, *citations, ROOT / 'ACCURACY-REVIEW.json', ROOT / 'operational-print-diagnostic.json'])
    print(json.dumps(dict(packets=len(statuses), scientific=scientific, passed=passed_count,
        retained_failed=scientific - passed_count, validation_checks=len(checks), scripts=len(scripts))), flush=True)


if __name__ == '__main__':
    main()
