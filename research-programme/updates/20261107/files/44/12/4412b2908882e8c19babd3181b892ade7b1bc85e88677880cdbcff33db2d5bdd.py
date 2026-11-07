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
    folders = ['annular-background-time-tangent-attempt02', 'annular-direct-background-coupled-current-attempt01',
        'annular-direct-background-current-validation-attempt01']
    hashes, authorities, csv_rows = {}, {}, {}

    def own(path, expected=None):
        if not path.is_file():
            raise RuntimeError('Missing evidence: ' + str(path))
        relative = str(path.relative_to(root))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and digest != expected:
            raise RuntimeError('Changed evidence: ' + relative)
        if relative in hashes and hashes[relative] != digest:
            raise RuntimeError('Conflicting evidence: ' + relative)
        hashes[relative] = digest

    for folder in folders:
        path = intake / folder / 'status.json'
        status = json.loads(path.read_text())
        if status['state'] != 'complete' or not all(row['passed'] for row in status['checks']):
            raise RuntimeError('Incomplete authority: ' + folder)
        own(path)
        authorities[folder] = dict(checks=len(status['checks']), seconds=status['seconds'])
        for category in ['inputs', 'outputs']:
            for relative, expected in status[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                own(root / relative, expected)
                if category == 'outputs' and relative.endswith('.csv'):
                    with (root / relative).open(newline='', encoding='utf-8') as stream:
                        rows = list(csv.DictReader(stream))
                    if not rows or any(None in row or any(value is None for value in row.values()) for row in rows):
                        raise RuntimeError('Malformed CSV: ' + relative)
                    csv_rows[relative] = len(rows)
    failed_path = intake / 'annular-background-time-tangent-attempt01/status.json'
    failed = json.loads(failed_path.read_text())
    if failed['state'] != 'failed' or 'incompatible velocities' not in failed['error']:
        raise RuntimeError('The original coincident-grid failure must remain explicit')
    own(failed_path)
    for category in ['inputs', 'outputs']:
        for relative, expected in failed[category].items():
            if relative != 'CURRENT_LOCAL_RESUME.md':
                own(root / relative, expected)
    documents = ['DERIVATION-20260928-direct-background-time-tangent.md',
        'DERIVATION-20260928-coincident-grid-correction.md', 'DERIVATION-20260928-one-sided-source-traces.md',
        'RESULTS-20260928-direct-background-and-coupled-current.md', 'CURRENT_LOCAL_RESUME.md']
    cited = []
    for name in documents:
        path = root / name
        own(path)
        if name != 'CURRENT_LOCAL_RESUME.md':
            for value in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
                if value.endswith(('.md', '.py', '.json', '.csv', '.npz')):
                    if not (root / value).is_file():
                        raise RuntimeError('Missing cited path: ' + value)
                    cited.append(value)
    scripts = ['annular_background_time_tangent_20260928.py', 'annular_background_complex_oracle_20260928.py',
        'derive_annular_background_time_tangent_20260928.py', 'annular_background_eulerian_20260928.py',
        'derive_annular_background_time_tangent_v2_20260928.py', 'annular_background_weak_checks_20260928.py',
        'annular_background_trace_20260928.py', 'derive_annular_direct_background_coupled_current_20260928.py',
        'validate_annular_direct_background_current_20260928.py', 'seal_annular_direct_background_20260928.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    since = datetime.fromisoformat('2026-09-28T15:08:14+00:00').timestamp()
    changed = [str(path) for path in (root.parent / 'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench mtime changes: ' + repr(changed))
    if (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode cache; inspect rather than delete blindly')
    report = dict(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=0, authorities=authorities, csv_rows=csv_rows,
        total_new_csv_rows=sum(csv_rows.values()), cited_paths=sorted(set(cited)), scripts_compiled=len(scripts),
        preserved_failed_attempt='annular-background-time-tangent-attempt01',
        raw_untraced_acquisition_is_not_final_response=True,
        accepted_response='One-sided-traced Eulerian derivative in coupled-current authority',
        protected_workbench_changed_since_turn_start=len(changed),
        protected_audit_scope='mtime since turn start and all task writes confined to post-checkpoint-work',
        bytecode_cache_present=False, github_action=False, subagents_used=False)
    with (intake / 'annular-direct-background-final-integrity-20260928.json').open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ['hashes', 'cited_paths']}))


if __name__ == '__main__':
    main()
