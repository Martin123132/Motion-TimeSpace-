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
    folders = ['annular-support-shift-jet-attempt01',
               'annular-support-shift-jet-validation-attempt01',
               'annular-geometric-support-jet-attempt01']
    hashes, authorities, csv_rows = {}, {}, {}

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

    for folder in folders:
        path = intake / folder / 'status.json'
        status = json.loads(path.read_text())
        if status['state'] != 'complete' or not all(row['passed'] for row in status['checks']):
            raise RuntimeError('Incomplete authority: ' + folder)
        own(path)
        authorities[folder] = dict(checks=len(status['checks']), seconds=status['seconds'])
        for category in ['inputs', 'outputs']:
            for relative, digest in status[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                own(root / relative, digest)
                if category == 'outputs' and relative.endswith('.csv'):
                    with (root / relative).open(newline='', encoding='utf-8') as stream:
                        rows = list(csv.DictReader(stream))
                    if not rows or any(None in row or any(value is None for value in row.values()) for row in rows):
                        raise RuntimeError('Malformed CSV: ' + relative)
                    csv_rows[relative] = len(rows)
    documents = ['RESULTS-20260928-support-shift-and-geometric-time-jet.md',
                 'DERIVATION-20260928-support-shift-current-jet.md',
                 'DERIVATION-20260928-geometric-support-jet-completion.md',
                 'CURRENT_LOCAL_RESUME.md']
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
    scripts = ['annular_support_shift_jet_20260928.py',
               'derive_annular_support_shift_jet_20260928.py',
               'validate_annular_support_shift_jet_20260928.py',
               'derive_annular_geometric_support_jet_20260928.py',
               'seal_annular_support_shift_jet_20260928.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    if (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode cache; inspect before cleanup')
    since = datetime.fromisoformat('2026-09-28T10:14:00+00:00').timestamp()
    changed = [str(path) for path in (root.parent / 'formalization-workbench').rglob('*')
               if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench mtime audit found changes: ' + repr(changed))
    report = dict(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=0, authorities=authorities,
        csv_rows=csv_rows, total_new_csv_rows=sum(csv_rows.values()), cited_paths=sorted(set(cited)),
        scripts_compiled=len(scripts), protected_workbench_changed_since_turn_start=len(changed),
        protected_audit_scope='mtime since turn start, together with all tool writes confined to post-checkpoint-work',
        bytecode_cache_present=False, github_action=False)
    output = intake / 'annular-support-shift-jet-final-integrity-20260928.json'
    with output.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ['hashes', 'cited_paths']}))


if __name__ == '__main__':
    main()
