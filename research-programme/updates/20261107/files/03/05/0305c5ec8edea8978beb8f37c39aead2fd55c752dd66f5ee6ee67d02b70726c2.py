import re
import psutil
from angular_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    assert not folder.exists()
    checks, inputs = [], []
    def check(name, passed, **details):
        checks.append(dict(name=name, passed=bool(passed), **details))
    scripts = sorted(ROOT.glob('*.py'))
    hashes = {digest(path) for path in scripts}
    packets = sorted(ROOT.glob('results/*/status.json'))
    assert len(packets) == 7, len(packets)
    for path in packets:
        packet = json.loads(path.read_text())
        check(path.parent.name + ': complete saved packet', packet['state'] == 'complete'
              and (path.parent / 'COMPLETE').is_file() and packet['all_checks_passed'])
        assert packet['script_sha256'] in hashes, path
        for source, expected in packet['input_hashes'].items():
            assert digest(source) == expected, (path, source)
        checks.extend(dict(row, name=path.parent.name + ': ' + row['name']) for row in packet['checks'])
        inputs.append(path)
    check('All saved input/source hashes match', True, packet_count=len(packets))
    for path in sorted(ROOT.glob('results/*/*.npz')):
        with np.load(path, allow_pickle=False) as saved:
            check(path.parent.name + '/' + path.name + ': finite saved arrays',
                  all(np.isfinite(saved[key]).all() for key in saved.files))
        inputs.append(path)
    for label in ['heavy', 'cold']:
        with np.load(ROOT / 'results/saved-modes' / (label + '-sixteenth.npz')) as saved:
            check(label + ': principal source matches retained two-mode angular shape',
                  saved['rest_first_order'].shape == (2, 200, 3, 3)
                  and saved['induced_angular_tensor'].shape == (200, 3, 3)
                  and saved['force_per_kappa_theta'].shape == (4,))
    pdf = ROOT / 'sources/pitrou-1902.09456v2.pdf'
    html = ROOT / 'sources/pitrou-1902.09456v2.html'
    check('Primary PDF has PDF magic and HTML archive contains paper identity',
          pdf.read_bytes().startswith(b'%PDF-') and b'1902.09456' in html.read_bytes()
          and b'<html' in html.read_bytes().lower())
    check('Inspected equation source pages are present',
          all((ROOT / 'sources' / name).is_file() for name in ['page-30.png', 'page-31.png']))
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    check('All stage scripts compile without bytecode', True, script_count=len(scripts))
    citations = set()
    pending = {ROOT / 'results/stage-integrity.json', folder / 'status.json'}
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
            if reference.endswith(('.md', '.py', '.npz', '.json', '.html', '.pdf', '.f90', '.dll', '.txt')):
                target = (path.parent / reference).resolve()
                assert target in pending or target.is_file(), (path, reference)
                if target not in pending:
                    citations.add(str(target))
        inputs.append(path)
    check('Every cited local source exists or is pending seal', True)
    process = psutil.Process()
    check('Single-core below-normal resources and single-thread libraries',
          process.cpu_affinity() == [2] and process.nice() == psutil.BELOW_NORMAL_PRIORITY_CLASS
          and all(os.environ[key] == '1' for key in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']))
    others, inaccessible = [], []
    root = str(ROOT).replace('\\', '/').lower()
    for candidate in psutil.process_iter(['pid', 'name', 'cmdline']):
        if candidate.info['pid'] == os.getpid() or 'python' not in (candidate.info['name'] or '').lower():
            continue
        try:
            command = ' '.join(candidate.info['cmdline'] or []).replace('\\', '/').lower()
            directory = candidate.cwd().replace('\\', '/').lower()
            if root in command or directory == root:
                others.append(candidate.info['pid'])
        except psutil.NoSuchProcess:
            continue
        except psutil.AccessDenied:
            inaccessible.append(candidate.info['pid'])
    check('No other stage worker active', not others and not inaccessible,
          other_stage_pids=others, inaccessible_python_pids=inaccessible)
    check('No bytecode cache introduced', not any(path.is_dir() for path in ROOT.rglob('__pycache__')))
    passed = all(row['passed'] for row in checks)
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=passed,
                        all_current_acceptance_checks_passed=passed, local_citations=sorted(citations),
                        new_primary_source_urls=['https://arxiv.org/html/1902.09456v2',
                            'https://arxiv.org/pdf/1902.09456v2', 'https://doi.org/10.1016/j.astropartphys.2020.102494'],
                        source_pdf_pages_visually_inspected=[30, 31],
                        known_displayed_equation_typo_not_propagated=True,
                        subleading_angular_terms_have_separate_refinement_checks=True,
                        no_new_observational_fit=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)
    assert passed


if __name__ == '__main__':
    main()
