import re
from radial_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    folder.mkdir(parents=True, exist_ok=False)
    scripts = sorted(ROOT.glob('*.py'))
    script_hashes = {digest(script) for script in scripts}
    for script in scripts:
        compile(script.read_bytes(), str(script), 'exec')
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    expected_failures = {key: set(value) for key, value in review['retained_failed_checks'].items()}
    statuses = sorted(path for path in ROOT.rglob('status.json') if path.parent != folder)
    inputs, checks, failures, scientific, passed_count = [], [], [], 0, 0
    for path in statuses:
        packet = json.loads(path.read_text())
        assert packet['state'] == 'complete' and (path.parent / 'COMPLETE').exists(), path
        assert packet['count'] == len(packet['checks'])
        failed = {row['name'] for row in packet['checks'] if not row['passed']}
        name = path.parent.relative_to(ROOT).as_posix()
        assert failed == expected_failures.get(name, set()), (name, failed)
        assert packet['all_checks_passed'] == (not failed)
        assert packet['script_sha256'] in script_hashes
        for filename, expected in packet['input_hashes'].items():
            assert digest(filename) == expected, (path, filename)
        for array in path.parent.rglob('*.npz'):
            with np.load(array) as saved:
                for key in saved.files:
                    if np.issubdtype(saved[key].dtype, np.number):
                        assert np.isfinite(saved[key]).all(), (array, key)
            inputs.append(array)
        if 'nodes' in packet:
            assert len(list((path.parent / 'nodes').rglob('*.npz'))) == packet['nodes']
        scientific += packet['count']
        passed_count += sum(bool(row['passed']) for row in packet['checks'])
        failures += [dict(packet=name, test=test) for test in sorted(failed)]
        checks.append(dict(name='Completed packet integrity and truthful gate status: ' + name, passed=True))
        inputs.append(path)
    assert set(expected_failures).issubset({path.parent.relative_to(ROOT).as_posix() for path in statuses})
    for key in ['new_empirical_fit', 'full_parent_feedback_applied', 'new_parent_history',
                'control_coefficient_fitted', 'source_smallness_used_to_waive_gate', 'github_action']:
        assert review[key] is False
    assert review['new_virtual_loop_evaluations'] == len(list((ROOT / 'virtual-cache').rglob('*.json'))) and review['modes_removed'] == 0
    audit = json.loads((ROOT / 'results/node-audit/status.json').read_text())
    assert audit['all_checks_passed'] and audit['every_source_node_verified']
    checks.append(dict(name='No promoted history, fit, dropped mode or fitted control coefficient', passed=True))
    documents = [ROOT / name for name in ['RESULTS.md', 'DERIVATION.md', 'SOURCES.md', 'RESUME.md', 'DEVELOPMENT-NOTES.md']]
    citations = set()
    urls = set()
    for document in documents:
        contents = document.read_text(encoding='utf-8')
        urls.update(re.findall(r'https?://[^\s`<>]+', contents))
        for reference in re.findall(r'`([^`]+)`', contents):
            if reference.endswith(('.py', '.npz', '.md', '.json', '.pdf', '.html')):
                target = (ROOT / reference).resolve()
                if target in {folder / 'status.json', ROOT / 'results/stage-integrity.json'}:
                    continue
                assert target.is_file(), (document, reference)
                citations.add(target)
    checks.append(dict(name='All cited local sources exist', passed=True))
    parent = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert len(parent['file_hashes']) == 27666
    for name, expected in parent['file_hashes'].items():
        assert digest(PARENT / name) == expected, name
    checks.append(dict(name='All27666 Stage99 payloads remain unchanged', passed=True))
    maximum = max(len(files) for directory, directories, files in os.walk(ROOT))
    assert maximum < 1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Scripts compile, no bytecode or interrupted writes, folders below1000 files', value=maximum, passed=True))
    finish(folder, dict(checks=checks, accepted_current_scope_verified=True,
        checked_packets=len(statuses), scientific_checks=scientific, passing_scientific_checks=passed_count,
        retained_failed_scientific_checks=scientific - passed_count, retained_failure_records=failures,
        compiled_scripts=len(scripts), largest_direct_file_count=maximum,
        local_citations=[str(path) for path in sorted(citations)], recorded_web_urls=sorted(urls),
        web_sources_newly_consulted=[],
        counts_are_tests_not_independent_proofs=True), __file__,
        [*scripts, *documents, *inputs, *citations, ROOT / 'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(packets=len(statuses), scientific=scientific, passed=passed_count,
        retained_failed=scientific - passed_count, validation_checks=len(checks))), flush=True)


if __name__ == '__main__':
    main()
