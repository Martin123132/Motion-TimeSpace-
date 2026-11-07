import re
import psutil
from emission_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    assert not folder.exists()
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    checks, inputs = [], [ROOT / 'ACCURACY-REVIEW.json']
    def check(name, passed, **details):
        checks.append(dict(name=name, passed=bool(passed), **details))
    scripts = sorted(ROOT.glob('*.py'))
    script_hashes = {digest(path) for path in scripts}
    packets = sorted(path for category in ['results', 'banks', 'backgrounds'] for path in (ROOT / category).glob('*/status.json'))
    known = {path.relative_to(ROOT).as_posix(): path for path in packets}
    excluded = review['retained_unaccepted_accuracy_trials']
    assert all(name in known for name in excluded)
    for name in review['required_accepted_packets']:
        assert name in known and name not in excluded, name
        check(name + ': required scoped result accepted', json.loads(known[name].read_text())['all_checks_passed'])
    for path in packets:
        packet = json.loads(path.read_text())
        relative = path.relative_to(ROOT).as_posix()
        check(relative + ': complete packet', packet['state'] == 'complete' and (path.parent / 'COMPLETE').is_file())
        assert packet['script_sha256'] in script_hashes, path
        for source, expected in packet['input_hashes'].items():
            assert digest(source) == expected, (path, source)
        if relative in excluded:
            failures = [row for row in packet['checks'] if not row['passed']]
            assert failures and not packet['all_checks_passed'] and excluded[relative]['reason']
            for successor in excluded[relative]['superseded_by']:
                assert successor in known and successor not in excluded, successor
                assert json.loads(known[successor].read_text())['all_checks_passed'], successor
            assert excluded[relative]['superseded_by'] or excluded[relative].get('unresolved_scope'), relative
            check(relative + ': failed accuracy trial preserved and excluded', True)
        else:
            check(relative + ': packet acceptance passes', packet['all_checks_passed'])
            checks.extend(dict(row, name=relative + ': ' + row['name']) for row in packet['checks'])
        inputs.append(path)
    for path in sorted(ROOT.rglob('*.npz')):
        with np.load(path, allow_pickle=False) as saved:
            check(path.relative_to(ROOT).as_posix() + ': finite retained arrays', all(np.isfinite(saved[key]).all() for key in saved.files))
        inputs.append(path)
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    check('All local Python scripts compile without bytecode', True, script_count=len(scripts))
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
    check('All cited local files exist or identify pending validation/seal', True)
    sources = json.loads((ROOT / 'results/sourced-emission/status.json').read_text())
    for source in sources['sources']:
        check('Primary source archived and cited: ' + source['url'], source['url'] in urls and digest(source['path']) == source['sha256'])
    process = psutil.Process()
    check('One-core below-normal numerical resource policy', process.cpu_affinity() == [2]
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
    check('No other stage numerical worker active', not others, other_stage_pids=others, inaccessible_other_python_pids=inaccessible)
    check('No bytecode cache introduced', not any(path.is_dir() for path in ROOT.rglob('__pycache__')))
    incomplete = [str(path) for category in ['results', 'banks', 'backgrounds'] for path in (ROOT / category).iterdir()
                  if path.is_dir() and not (path / 'COMPLETE').is_file()]
    check('No abandoned or incomplete local result directory', not incomplete, incomplete=incomplete)
    passed = all(row['passed'] for row in checks)
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=passed,
        all_current_acceptance_checks_passed=passed, checked_packets=len(packets),
        local_citations=sorted(citations), recorded_web_urls=sorted(urls),
        raw_unaccepted_accuracy_trials=excluded, acceptance_scope=review['accepted_scope'],
        all_requested_numerical_gates_closed=review['all_requested_numerical_gates_closed'],
        open_numerical_gate=review['open_numerical_gate'], no_new_observational_fit=True), __file__, sorted(set(inputs)))
    print(json.dumps(dict(checks=len(checks), packets=len(packets), failed=[row for row in checks if not row['passed']])), flush=True)
    assert passed


if __name__ == '__main__':
    main()
