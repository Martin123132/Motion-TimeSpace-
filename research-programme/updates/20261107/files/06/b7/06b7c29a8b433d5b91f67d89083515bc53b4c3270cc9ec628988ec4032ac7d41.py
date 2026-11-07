from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import hashlib
import json
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--main', default='annular-old-field-reaction-attempt01')
    parser.add_argument('--columns', default='annular-reacted-support-columns-attempt02')
    parser.add_argument('--validator', default='annular-old-reaction-validation-attempt01')
    parser.add_argument('--sensitivity', default='annular-reacted-column-sensitivity-attempt01')
    parser.add_argument('--reader', default='RESULTS-20260929-old-field-reaction-and-coupled-columns.md')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260914'
    hashes, authorities, tables = {}, {}, {}

    def own(path, expected=None):
        path = path.resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Missing or outside-project evidence: ' + str(path))
        relative = str(path.relative_to(root))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and digest != expected:
            raise RuntimeError('Changed evidence: ' + relative)
        if relative in hashes and hashes[relative] != digest:
            raise RuntimeError('Conflicting evidence: ' + relative)
        hashes[relative] = digest

    for folder in [args.main, args.columns, args.validator, args.sensitivity]:
        path = intake / folder / 'status.json'
        status = json.loads(path.read_text())
        if status['state'] != 'complete' or len(status['cases']) != 4 or not all(row['passed'] for row in status['checks']):
            raise RuntimeError('Incomplete authority: ' + folder)
        own(path)
        authorities[folder] = dict(checks=len(status['checks']), seconds=status['seconds'])
        for category in ['inputs', 'outputs']:
            for relative, expected in status[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                own(root / relative, expected)
                if category == 'outputs' and relative.endswith('.csv'):
                    with (root / relative).open(encoding='utf-8', newline='') as stream:
                        rows = list(csv.DictReader(stream))
                    if not rows or any(None in row or any(value is None for value in row.values()) for row in rows):
                        raise RuntimeError('Malformed CSV: ' + relative)
                    tables[relative] = len(rows)
    preserved = []
    patterns = ['annular-old-field-reaction-attempt*', 'annular-reacted-support-columns-attempt*', 'annular-old-reaction-validation-attempt*', 'annular-reacted-column-sensitivity-attempt*', 'annular-C2-cancellation-diagnostic-attempt*']
    for pattern in patterns:
        for folder in intake.glob(pattern):
            path = folder / 'status.json'
            if not folder.is_dir() or not path.is_file() or folder.name in authorities:
                continue
            status = json.loads(path.read_text())
            if status['state'] not in ['failed', 'complete']:
                raise RuntimeError('Unfinished attempt: ' + folder.name)
            own(path)
            for category in ['inputs', 'outputs']:
                for relative, expected in status[category].items():
                    if relative != 'CURRENT_LOCAL_RESUME.md':
                        own(root / relative, expected)
            preserved.append(dict(folder=folder.name, state=status['state'], error=status.get('error')))
    documents = ['DERIVATION-20260929-old-field-reaction.md', 'DERIVATION-20260929-reacted-force-current-columns.md',
        'DERIVATION-20260929-reacted-column-sensitivity.md',
        'DERIVATION-20260929-C2-cancellation-correction.md',
        args.reader, 'CURRENT_LOCAL_RESUME.md']
    cited = []
    for name in documents:
        path = root / name
        own(path)
        if name != 'CURRENT_LOCAL_RESUME.md':
            for value in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
                if value.endswith(('.md', '.py', '.json', '.npz', '.csv')):
                    if not (root / value).is_file():
                        raise RuntimeError('Missing cited path: ' + value)
                    cited.append(value)
    scripts = set()
    for pattern in ['*old*reaction*20260929.py', '*reacted*20260929.py', '*aligned_acceleration*20260929.py', 'diagnose_annular_C2*20260929.py']:
        scripts.update((root / 'scripts').glob(pattern))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    for pattern in patterns:
        for path in intake.glob(pattern + '.log'):
            own(path)
    since = datetime.fromisoformat('2026-09-28T23:04:37+00:00').timestamp()
    changed = [str(path) for path in (root.parent / 'formalization-workbench').rglob('*')
        if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench changed: ' + repr(changed))
    if (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode; inspect before deleting')
    columns = json.loads((intake / args.columns / 'status.json').read_text())
    report = dict(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=0, authorities=authorities, csv_rows=tables,
        total_new_csv_rows=sum(tables.values()), scripts_compiled=len(scripts), cited_paths=sorted(set(cited)),
        preserved_attempts=preserved, inherited_mixed_time_precision_warnings=4,
        inherited_position_density_precision_warnings=4, uncertainty_is_rigorous_bound=False,
        raw_C2_precision_diagnostics=[dict(branch=row['branch'], level=row['level'],
            raw_replay_pass=row['raw_C2_evaluator_replay_pass'], raw_difference=row['raw_C2_difference']) for row in columns['cases']],
        old_field_reaction_solved=True, zero_position_force_and_three_current_columns_computed=True,
        finite_amplitude_solution_established=False, protected_workbench_changed_since_turn_start=len(changed),
        protected_audit_scope='mtime since turn start; this task writes only inside post-checkpoint-work',
        bytecode_cache_present=False, github_action=False, subagents_used=False)
    with (intake / 'annular-old-reaction-final-integrity-20260929.json').open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ['hashes', 'cited_paths']}))


if __name__ == '__main__':
    main()
