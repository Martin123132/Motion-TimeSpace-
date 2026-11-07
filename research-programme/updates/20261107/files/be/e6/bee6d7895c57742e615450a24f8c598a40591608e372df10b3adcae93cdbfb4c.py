import psutil
from thermal_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    assert not folder.exists()
    checks = []
    inputs = []

    def check(name, passed, **details):
        checks.append(dict(name=name, passed=bool(passed), **details))

    scripts = sorted(ROOT.glob('*.py'))
    script_hashes = {digest(path) for path in scripts}
    packets = sorted(ROOT.glob('runs/*/status.json')) + sorted(ROOT.glob('results/*/status.json'))
    assert len(packets) == 18, len(packets)
    retained_failures = []
    expected_failures = {
        'heavy: derived stress obeys homogeneous conservation',
        'cold: derived stress obeys homogeneous conservation',
    }
    for path in packets:
        packet = json.loads(path.read_text())
        check(path.parent.name + ': complete saved packet',
              packet['state'] == 'complete' and (path.parent / 'COMPLETE').is_file())
        assert packet['script_sha256'] in script_hashes, path
        for source, expected in packet['input_hashes'].items():
            assert digest(source) == expected, (path, source)
        if path.parent.name == 'flrw-response':
            retained_failures = [row for row in packet['checks'] if not row['passed']]
            check('Original coarse conservation probes remain recorded as failures',
                  len(retained_failures) == 2
                  and {row['name'] for row in retained_failures} == expected_failures
                  and all(row['gate'] == 1e-8 for row in retained_failures)
                  and packet['all_checks_passed'] is False)
            checks.extend(dict(row, name=path.parent.name + ': ' + row['name'])
                          for row in packet['checks'] if row['passed'])
        else:
            assert packet['all_checks_passed'] is True, path
            checks.extend(dict(row, name=path.parent.name + ': ' + row['name']) for row in packet['checks'])
        inputs.append(path)

    check('All saved packet source hashes match current inputs', True, packet_count=len(packets))
    for label in ['heavy', 'cold']:
        path = ROOT / 'runs' / (label + '-domain') / 'spectrum.npz'
        report = json.loads(path.with_name('status.json').read_text())
        with np.load(path, allow_pickle=False) as saved:
            check(label + ': all saved spectral arrays finite',
                  all(np.isfinite(saved[key]).all() for key in saved.files))
            frequency = saved['frequency']
            histories = saved['history_potentials']
            capacity = float(saved['chi'])
            physical_capacity = float(saved['physical_chi'])
            check(label + ': principal spectrum has physical heat capacity and expected grid',
                  saved['potential'].shape == (1600,) and histories.shape == (41, 1600)
                  and np.all(np.diff(frequency) > 0)
                  and float(saved['minimum']) == 1e-5 and float(saved['maximum']) == 60.
                  and int(saved['steps']) == 800 and capacity == physical_capacity > 0
                  and report['override_is_numerical_test_only'] is False)
            ratios = 1 + capacity * (1 + planck(frequency)) * histories
            check(label + ': every saved physical occupation is positive', np.min(ratios) > 0,
                  minimum_ratio=float(np.min(ratios)))
            energy_fraction = capacity * float(saved['energy'] @ saved['potential'])
            check(label + ': saved energy agrees with reported result',
                  math.isclose(energy_fraction, report['final_photon_energy_fraction'], rel_tol=1e-14))
        limit_path = ROOT / 'runs' / (label + '-fast-limit') / 'status.json'
        limit_report = json.loads(limit_path.read_text())
        check(label + ': zero-capacity probe is labelled numerical, not physical',
              limit_report['chi'] == 0 and limit_report['physical_chi'] > 0
              and limit_report['override_is_numerical_test_only'] is True)
        inputs.extend([path, limit_path])
        gravity_path = ROOT / 'results/flrw-response' / (label + '.npz')
        with np.load(gravity_path, allow_pickle=False) as saved:
            check(label + ': saved gravitational response arrays finite',
                  all(np.isfinite(saved[key]).all() for key in saved.files))
        inputs.append(gravity_path)

    refined = json.loads((ROOT / 'results/flrw-conservation-refined/status.json').read_text())
    check('Independent refined conservation packet clears its unchanged gates',
          refined['all_checks_passed'] is True and len(refined['checks']) == 7
          and all(row['passed'] for row in refined['checks']))
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    check('All scripts compile without bytecode', True, script_count=len(scripts))
    citations = set()
    pending = {ROOT / 'results/stage-integrity.json', folder / 'status.json'}
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
            if reference.endswith(('.md', '.py', '.npz', '.json', '.html', '.f90', '.dll', '.txt')):
                target = (path.parent / reference).resolve()
                assert target in pending or target.is_file(), (path, reference)
                if target not in pending:
                    citations.add(str(target))
        inputs.append(path)
    check('Every cited local source exists or is pending seal', True)
    scope = json.loads((ROOT / 'results/thermal-scope/status.json').read_text())
    check('Thermal-scope evidence survives recorded console-only formatting failure',
          scope['state'] == 'complete' and scope['all_checks_passed'] is True
          and len(scope['checks']) == 6
          and 'formatting exception AFTER' in (ROOT / 'RESULTS.md').read_text())
    process = psutil.Process()
    check('One-core below-normal resource settings',
          process.cpu_affinity() == [2] and process.nice() == psutil.BELOW_NORMAL_PRIORITY_CLASS
          and all(os.environ[key] == '1' for key in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']))
    other_workers = []
    unresolved_python_processes = []
    normalized_root = str(ROOT).replace('\\', '/').lower()
    for candidate in psutil.process_iter(['pid', 'name', 'cmdline']):
        if candidate.info['pid'] == os.getpid() or 'python' not in (candidate.info['name'] or '').lower():
            continue
        try:
            command = ' '.join(candidate.info['cmdline'] or []).replace('\\', '/').lower()
            directory = candidate.cwd().replace('\\', '/').lower()
            if normalized_root in command or directory == normalized_root:
                other_workers.append(candidate.info['pid'])
        except psutil.NoSuchProcess:
            continue
        except psutil.AccessDenied:
            unresolved_python_processes.append(candidate.info['pid'])
    check('No other stage worker remains active', not other_workers and not unresolved_python_processes,
          other_stage_pids=other_workers, inaccessible_python_pids=unresolved_python_processes)
    check('No bytecode cache introduced', not any(path.is_dir() for path in ROOT.rglob('__pycache__')))
    passed = all(row['passed'] for row in checks)
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=passed,
        all_current_acceptance_checks_passed=passed, retained_coarse_failures=retained_failures,
        local_citations=sorted(citations), new_primary_source_urls=[
            'https://arxiv.org/html/1110.0475v2', 'https://arxiv.org/abs/1109.6552',
            'https://arxiv.org/abs/2109.04895'],
        scope_console_trailer_failure_recorded=True, new_observational_fit=False), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                         retained_coarse_failures=len(retained_failures))), flush=True)
    assert passed


if __name__ == '__main__':
    main()
