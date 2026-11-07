import re
import psutil
from step_common import *


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
    assert len(packets) == 32, len(packets)
    for path in packets:
        packet = json.loads(path.read_text())
        check(path.parent.name + ': complete saved packet', packet['state'] == 'complete'
              and (path.parent / 'COMPLETE').is_file() and packet['all_checks_passed'])
        assert packet['script_sha256'] in hashes, path
        for source, expected in packet['input_hashes'].items():
            assert digest(source) == expected, (path, source)
        checks.extend(dict(row, name=path.parent.name + ': ' + row['name']) for row in packet['checks'])
        inputs.append(path)
    check('Every complete packet still matches original script and input hashes', True, packet_count=len(packets))
    for path in sorted(ROOT.rglob('*.npz')):
        with np.load(path, allow_pickle=False) as saved:
            check(path.parent.name + '/' + path.name + ': finite saved arrays',
                  all(np.isfinite(saved[key]).all() for key in saved.files))
        inputs.append(path)
    stability = json.loads((ROOT / 'results/spectral-stability/status.json').read_text())
    excluded = [row for row in stability['rows'] if not row['accepted_for_time_evolution']]
    check('Real fine-grid failure is retained and not recast as a physical pass', len(excluded) == 1
          and excluded[0]['frequency_points'] == 384 and excluded[0]['scale'] == 1e-6
          and max(excluded[0]['largest_photon_eigenvalues']) > .05)
    for path in ROOT.glob('runs/*/status.json'):
        packet = json.loads(path.read_text())
        check(path.parent.name + ': excluded frequency grid was not evolved', packet['points'] < 384)
    candidate = json.loads((ROOT / 'results/finite-shift/status.json').read_text())
    check('Rejected simple rate remains explicitly rejected despite dissipative structure',
          candidate['simple_phase_space_candidate_matches_parent'] is False
          and candidate['full_polarized_Compton_kernel_completed'] is False
          and all(abs(row['mismatch']) > 3 for row in candidate['scalar_candidate_matching']))
    physical = json.loads((ROOT / 'results/moving-kernel-independent-check/status.json').read_text())
    check('Physical replacement coefficients independently match without fitting',
          len(physical['rows']) == 36 and max(row['relative_error'] for row in physical['rows']) < 1e-5
          and physical['scalar_first_order_matching_only'])
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    check('All stage scripts compile without bytecode', True, script_count=len(scripts))
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
    check('Every cited local path exists or is pending seal', True)
    check('Read primary web sources and DOI are recorded',
          all(url in urls for url in ['https://arxiv.org/html/astro-ph/9910280v3', 'https://doi.org/10.1086/317078']))
    process = psutil.Process()
    check('Single-core below-normal resource limits and single-thread libraries',
          process.cpu_affinity() == [2] and process.nice() == psutil.BELOW_NORMAL_PRIORITY_CLASS
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
    check('No other stage worker active; other chats untouched', not others and not inaccessible,
          other_stage_pids=others, inaccessible_python_pids=inaccessible)
    check('No bytecode cache introduced', not any(path.is_dir() for path in ROOT.rglob('__pycache__')))
    passed = all(row['passed'] for row in checks)
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=passed,
                        all_current_acceptance_checks_passed=passed, local_citations=sorted(citations),
                        recorded_web_urls=sorted(urls),
                        new_primary_source_urls=['https://arxiv.org/abs/astro-ph/9910280v3',
                            'https://arxiv.org/html/astro-ph/9910280v3', 'https://doi.org/10.1086/317078'],
                        excluded_unstable_grids=excluded, complete_kernel_candidate_rejected=True,
                        acceptance_applies_to_documented_scope_not_uniform_FP_stability=True,
                        no_new_observational_fit=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)
    assert passed


if __name__ == '__main__':
    main()
