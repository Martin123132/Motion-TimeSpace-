from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import re


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260914'
    statuses = ['annular-directional-coupled-Euler-attempt02',
                'annular-directional-coupled-Euler-validation-attempt01',
                'annular-support-Schur-conditioning-attempt01']
    hashes, check_counts = {}, {}

    def own(path, expected=None):
        if not path.is_file():
            raise RuntimeError('Missing file: ' + str(path))
        relative = str(path.relative_to(root))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and expected != digest:
            raise RuntimeError('Changed evidence: ' + relative)
        if relative in hashes and hashes[relative] != digest:
            raise RuntimeError('Conflicting digest: ' + relative)
        hashes[relative] = digest

    csv_count = 0
    for folder in statuses:
        path = intake / folder / 'status.json'
        report = json.loads(path.read_text())
        if report['state'] != 'complete' or not all(row['passed'] for row in report['checks']):
            raise RuntimeError('Incomplete authority: ' + folder)
        own(path)
        check_counts[folder] = len(report['checks'])
        for category in ['inputs', 'outputs']:
            for relative, digest in report[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                own(root / relative, digest)
                if category == 'outputs' and relative.endswith('.csv'):
                    with (root / relative).open(newline='', encoding='utf-8') as stream:
                        rows = list(csv.DictReader(stream))
                    if not rows or any(None in row or any(value is None for value in row.values()) for row in rows):
                        raise RuntimeError('Malformed CSV: ' + relative)
                    csv_count += len(rows)
    failed_path = intake / 'annular-directional-coupled-Euler-attempt01/status.json'
    failed = json.loads(failed_path.read_text())
    if failed['state'] != 'failed' or 'Unowned input' not in failed['error']:
        raise RuntimeError('Failed source-loading attempt must remain explicit')
    own(failed_path)
    for category in ['inputs', 'outputs']:
        for relative, digest in failed[category].items():
            if relative != 'CURRENT_LOCAL_RESUME.md':
                own(root / relative, digest)
    documents = ['RESULTS-20260928-directional-coupled-Euler-and-support-response.md',
                 'DERIVATION-20260928-directional-coupled-Euler-test.md',
                 'DERIVATION-20260928-support-Schur-conditioning.md', 'CURRENT_LOCAL_RESUME.md']
    cited = []
    for name in documents:
        path = root / name
        own(path)
        if name != 'CURRENT_LOCAL_RESUME.md':
            for value in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
                if value.endswith(('.md', '.py', '.json', '.csv', '.npz')):
                    target = root / value
                    if not target.is_file():
                        raise RuntimeError('Missing cited path: ' + value)
                    cited.append(value)
    scripts = ['annular_directional_coupled_Euler_20260928.py',
               'derive_annular_directional_coupled_Euler_20260928.py',
               'derive_annular_directional_coupled_Euler_v2_20260928.py',
               'validate_annular_directional_coupled_Euler_20260928.py',
               'derive_annular_support_Schur_conditioning_20260928.py',
               'seal_annular_directional_coupled_Euler_20260928.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    if (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode cache; inspect before cleanup')
    since = datetime.fromisoformat('2026-09-28T00:07:05+00:00').timestamp()
    changed = [str(path) for path in (root.parent / 'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench mtime audit found changes: ' + repr(changed))
    output = intake / 'annular-directional-coupled-Euler-final-integrity-20260928.json'
    report = dict(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=0, validation_checks=check_counts,
        new_csv_rows=csv_count, cited_paths=sorted(set(cited)), scripts_compiled=len(scripts),
        protected_workbench_changed_since_turn_start=len(changed),
        protected_audit_scope='mtime since turn start, together with all tool writes confined to post-checkpoint-work',
        bytecode_cache_present=False, github_action=False)
    with output.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ['hashes', 'cited_paths']}))


if __name__ == '__main__':
    main()
