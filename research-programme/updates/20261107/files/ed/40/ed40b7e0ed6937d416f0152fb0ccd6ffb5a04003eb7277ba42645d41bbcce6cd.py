import re
import psutil
from grid_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    assert not folder.exists()
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    checks, inputs, failed_trials = [], [ROOT / 'ACCURACY-REVIEW.json'], []
    def check(name, passed, **details):
        checks.append(dict(name=name, passed=bool(passed), **details))
    scripts = sorted(ROOT.glob('*.py'))
    script_hashes = {digest(path) for path in scripts}
    packets = sorted(ROOT.glob('results/*/status.json')) + sorted(ROOT.glob('banks/*/status.json')) + sorted(ROOT.glob('runs/*/status.json'))
    excluded = review['retained_unaccepted_accuracy_trials']
    known = {path.relative_to(ROOT).as_posix(): path for path in packets}
    assert all(name in known for name in excluded)
    for name in review['required_accepted_packets']:
        assert name in known and name not in excluded, name
        check(name + ': accepted current accuracy target', json.loads(known[name].read_text())['all_checks_passed'])
    for path in packets:
        packet = json.loads(path.read_text())
        relative = path.relative_to(ROOT).as_posix()
        check(relative + ': complete saved packet', packet['state'] == 'complete' and (path.parent / 'COMPLETE').is_file())
        assert packet['script_sha256'] in script_hashes, path
        for source, expected in packet['input_hashes'].items():
            assert digest(source) == expected, (path, source)
        if relative in excluded:
            assert relative.startswith('results/'), relative
            failures = [row for row in packet['checks'] if not row['passed']]
            assert failures and not packet['all_checks_passed'] and excluded[relative]['reason']
            for replacement in excluded[relative]['superseded_by']:
                assert replacement in review['required_accepted_packets']
            failed_trials.append(dict(path=relative, reason=excluded[relative]['reason'], failed_checks=failures))
            check(relative + ': raw unsuccessful trial retained with explicit accepted successor', True)
        else:
            check(relative + ': all packet checks pass', packet['all_checks_passed'])
            checks.extend(dict(row, name=relative + ': ' + row['name']) for row in packet['checks'])
        inputs.append(path)
    for path in sorted(ROOT.rglob('*.npz')):
        with np.load(path, allow_pickle=False) as saved:
            check(path.relative_to(ROOT).as_posix() + ': finite retained arrays',
                  all(np.isfinite(saved[key]).all() for key in saved.files))
        inputs.append(path)
    for suffix in review['accepted_split_suffixes']:
        for model in ['heavy', 'cold', 'synthetic']:
            packet = json.loads((ROOT / 'runs' / (model + '-' + suffix) / 'status.json').read_text())
            check(model + '-' + suffix + ': full retained angular/polarization coverage',
                  len(packet['rows']) == 9 and packet['rows'][0]['names'] == ['I', 'V']
                  and all(row['names'] == ['I', 'E', 'B', 'V'] for row in packet['rows'][2:]))
            if model == 'synthetic':
                check(suffix + ': heat and momentum checked against actual transfer',
                      all(0 < row['exchanged_matter_energy_or_momentum_scale']
                          and row['transfer_relative_error'] < .002 for row in packet['rows'][:2]))
    check('Unsuccessful original small-response trials are not erased',
          'results/response-refinements/status.json' in excluded)
    check('Independent physical-channel algebra and leading-coefficient targets retained',
          json.loads((ROOT / 'results/angular-blocks/status.json').read_text())['all_checks_passed']
          and json.loads((ROOT / 'results/continuum-limits/status.json').read_text())['all_checks_passed'])
    band = json.loads((ROOT / 'results/split-band/status.json').read_text())
    tails = json.loads((ROOT / 'results/final-source-interface/status.json').read_text())
    for tail in tails['added_band_tail_diagnostics']:
        reference = next(row for row in band['rows'] if row['fixture'] == tail['fixture'])
        for name, magnitude in tail['peak_tail_norm'].items():
            sector = next(row for row in reference['sectors'] if row['sector'] == name)
            allowed = .002 * sector['peak_reference_norm'] if sector['numerically_resolved'] else sector['absolute_roundoff_floor']
            check(tail['fixture'] + ':' + name + ': explicitly measured added-band tail within response budget',
                  magnitude < allowed, peak_added_tail_norm=magnitude, allowed=allowed)
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    check('All scripts compile without creating bytecode', True, script_count=len(scripts))
    citations, urls = set(), set()
    pending = {ROOT / 'results/stage-integrity.json', folder / 'status.json'}
    for path in ROOT.glob('*.md'):
        content = path.read_text(encoding='utf-8')
        for reference in re.findall(r'`([^`\n]+)`', content):
            if reference.endswith(('.md', '.py', '.npz', '.json', '.html', '.pdf', '.f90', '.dll', '.txt', '.ps1')):
                target = (path.parent / reference).resolve()
                assert target in pending or target.is_file(), (path, reference)
                if target not in pending:
                    citations.add(str(target))
        urls.update(url.rstrip('.,;)') for url in re.findall(r'https?://[^\s<>`]+', content))
        inputs.append(path)
    check('All cited local files exist or are the pending seal', True)
    process = psutil.Process()
    check('One-core below-normal numerical resource policy',
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
    check('No other numerical stage worker active', not others and not inaccessible,
          other_stage_pids=others, inaccessible_python_pids=inaccessible)
    check('No bytecode cache introduced', not any(path.is_dir() for path in ROOT.rglob('__pycache__')))
    passed = all(row['passed'] for row in checks)
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=passed,
                        all_current_acceptance_checks_passed=passed, checked_packets=len(packets),
                        local_citations=sorted(citations), recorded_web_urls=sorted(urls),
                        new_primary_source_urls=[], raw_unaccepted_accuracy_trials=failed_trials,
                        acceptance_scope=review['accepted_scope'], no_new_observational_fit=True),
           __file__, sorted(set(inputs)))
    print(json.dumps(dict(checks=len(checks), packets=len(packets),
                          retained_unaccepted_accuracy_trials=len(failed_trials),
                          failed=[row for row in checks if not row['passed']])), flush=True)
    assert passed


if __name__ == '__main__':
    main()
