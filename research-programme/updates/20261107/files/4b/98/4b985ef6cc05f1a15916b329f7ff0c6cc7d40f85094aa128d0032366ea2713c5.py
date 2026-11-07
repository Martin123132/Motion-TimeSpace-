import re
import psutil
from kernel_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    assert not folder.exists()
    checks, inputs = [], []
    def check(name, passed, **details):
        checks.append(dict(name=name, passed=bool(passed), **details))
    scripts = sorted(ROOT.glob('*.py'))
    hashes = {digest(path) for path in scripts}
    packets = sorted(ROOT.glob('results/*/status.json')) + sorted(ROOT.glob('runs/*/status.json'))
    assert len(packets) == 12, len(packets)
    for path in packets:
        packet = json.loads(path.read_text())
        check(path.parent.name + ': complete saved packet', packet['state'] == 'complete'
              and (path.parent / 'COMPLETE').is_file() and packet['all_checks_passed'])
        assert packet['script_sha256'] in hashes, path
        for source, expected in packet['input_hashes'].items():
            assert digest(source) == expected, (path, source)
        checks.extend(dict(row, name=path.parent.name + ': ' + row['name']) for row in packet['checks'])
        inputs.append(path)
    check('Saved packets match actual scripts and source hashes', True, packet_count=len(packets))
    for path in sorted(ROOT.rglob('*.npz')):
        with np.load(path, allow_pickle=False) as saved:
            check(path.parent.name + '/' + path.name + ': finite saved arrays',
                  all(np.isfinite(saved[key]).all() for key in saved.files))
        inputs.append(path)
    for label in ['base', 'refined']:
        packet = json.loads((ROOT / 'results' / ('polarized-' + label) / 'status.json').read_text())
        check(label + ': all81 distinct polarized tensor probes retained', len(packet['rows']) == 81
              and set(row['kind'] for row in packet['rows']) == {'intensity', 'linear', 'circular'}
              and max(row['relative_coefficient_error'] for row in packet['rows']) < 1e-4)
    parent_stability = PARENT / 'results/spectral-stability/status.json'
    previous_failure = json.loads(parent_stability.read_text())
    check('Prior positive384-grid result retained, not overwritten', previous_failure['excluded_grid_count'] == 1
          and any(row['frequency_points'] == 384 and max(row['largest_photon_eigenvalues']) > .05 for row in previous_failure['rows']))
    inputs.append(parent_stability)
    for points in [192, 384, 768]:
        with np.load(ROOT / 'runs' / ('dipole-' + str(points)) / 'operator.npz') as saved:
            check(str(points) + ': physical dipole and coupled spectra have no growing mode',
                  max(saved['eigenvalues']) < 0 and max(saved['coupled_eigenvalues']) < 1e-9
                  and abs(float(saved['theta']) - .00045962015785263325) < 1e-15)
    refinements = json.loads((ROOT / 'results/grid-refinements/status.json').read_text())
    rough = [row for row in refinements['rows'] if row['fixture'] == 'oscillatory' and 'frequency' in row['comparison']]
    check('Rough waveform inaccuracy explicitly retained outside smooth acceptance', len(rough) == 2
          and all(not row['meets_accuracy_gate'] and row['relative_defect_discrepancy'] > .3 for row in rough))
    check('Smooth physical defect refinement passes without hiding behind common bulk',
          all(row['meets_accuracy_gate'] for row in refinements['rows'] if row['fixture'] == 'smooth'))
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    check('All scripts compile without producing bytecode', True, script_count=len(scripts))
    citations, urls = set(), set()
    pending = {ROOT / 'results/stage-integrity.json', folder / 'status.json'}
    for path in ROOT.glob('*.md'):
        content = path.read_text(encoding='utf-8')
        for reference in re.findall(r'`([^`\n]+)`', content):
            if reference.endswith(('.md', '.py', '.npz', '.json', '.html', '.pdf', '.f90', '.dll', '.txt')):
                target = (path.parent / reference).resolve()
                assert target in pending or target.is_file(), (path, reference)
                if target not in pending:
                    citations.add(str(target))
        urls.update(url.rstrip('.,;)') for url in re.findall(r'https?://[^\s<>`]+', content))
        inputs.append(path)
    check('Every cited local source exists or is pending seal', True)
    source_packet = json.loads((ROOT / 'results/source-acquisition/status.json').read_text())
    check('Used external reference is archived and URL recorded', source_packet['source_url'] in urls)
    process = psutil.Process()
    check('One-core below-normal numerical resource limits', process.cpu_affinity() == [2]
          and process.nice() == psutil.BELOW_NORMAL_PRIORITY_CLASS
          and all(os.environ[key] == '1' for key in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']))
    others, inaccessible = [], []
    root = str(ROOT).replace('\\', '/').lower()
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['pid'] == os.getpid() or 'python' not in (process.info['name'] or '').lower():
            continue
        try:
            command = ' '.join(process.info['cmdline'] or []).replace('\\', '/').lower()
            directory = process.cwd().replace('\\', '/').lower()
            if root in command or directory == root:
                others.append(process.info['pid'])
        except psutil.NoSuchProcess:
            continue
        except psutil.AccessDenied:
            inaccessible.append(process.info['pid'])
    check('No other stage worker active and other chats untouched', not others and not inaccessible,
          other_stage_pids=others, inaccessible_python_pids=inaccessible)
    check('No bytecode cache introduced', not any(path.is_dir() for path in ROOT.rglob('__pycache__')))
    passed = all(row['passed'] for row in checks)
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=passed,
                        all_current_acceptance_checks_passed=passed, local_citations=sorted(citations),
                        recorded_web_urls=sorted(urls), new_primary_source_urls=[source_packet['source_url']],
                        raw_rough_waveform_accuracy_failures=rough,
                        acceptance_scope='Physical channels, smooth coefficient/refinement tests, and dipole grid stability; not rough waveform accuracy or full cosmology.',
                        no_new_observational_fit=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)
    assert passed


if __name__ == '__main__':
    main()
