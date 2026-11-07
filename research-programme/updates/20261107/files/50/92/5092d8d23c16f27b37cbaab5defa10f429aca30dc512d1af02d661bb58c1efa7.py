from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--radial', default='annular-position-time-radial-attempt03')
    parser.add_argument('--validator', default='annular-position-time-radial-validation-attempt01')
    parser.add_argument('--reader', default='RESULTS-20260929-position-time-loading-and-metric-response.md')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260914'
    hashes, authorities, tables, preserved = {}, {}, {}, []

    def own(path, expected=None):
        path = path.resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Missing or outside-workspace evidence: ' + str(path))
        relative = str(path.relative_to(root))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and expected != digest:
            raise RuntimeError('Changed evidence: ' + relative)
        if relative in hashes and hashes[relative] != digest:
            raise RuntimeError('Conflicting evidence: ' + relative)
        hashes[relative] = digest

    accepted = ['annular-position-time-loads-attempt01', 'annular-position-time-load-validation-attempt01',
        'annular-position-time-probe-attempt02', args.radial, args.validator]
    for folder in intake.glob('annular-position-time-*-attempt*'):
        if not folder.is_dir() or not (folder / 'status.json').is_file():
            continue
        status = json.loads((folder / 'status.json').read_text())
        own(folder / 'status.json')
        if status['state'] not in ['complete', 'failed']:
            raise RuntimeError('Unfinished attempt: ' + folder.name)
        if folder.name in accepted:
            if status['state'] != 'complete' or len(status['cases']) != 4 or not all(row['passed'] for row in status['checks']):
                raise RuntimeError('Incomplete authority: ' + folder.name)
            authorities[folder.name] = dict(checks=len(status['checks']), seconds=status['seconds'])
        else:
            preserved.append(dict(folder=folder.name, state=status['state'], error=status.get('error'),
                numerical_failure=status.get('numerical_failure', status['state'] == 'failed'),
                external_safe_boundary_stop=status.get('external_safe_boundary_stop', False)))
        for category in ['inputs', 'outputs']:
            for relative, expected in status[category].items():
                if relative != 'CURRENT_LOCAL_RESUME.md':
                    own(root / relative, expected)
                if category == 'outputs' and relative.endswith('.csv'):
                    with (root / relative).open(encoding='utf-8', newline='') as stream:
                        rows = list(csv.DictReader(stream))
                    if not rows or any(None in row or any(value is None for value in row.values()) for row in rows):
                        raise RuntimeError('Malformed CSV: ' + relative)
                    if any(row.get('valid_for_claim', 'False') != 'False' for row in rows):
                        raise RuntimeError('Unexpected claim row: ' + relative)
                    tables[relative] = len(rows)
    if set(authorities) != set(accepted):
        raise RuntimeError('An accepted authority is missing')
    documents = ['DERIVATION-20260929-position-time-loads-and-interface-jumps.md',
        'DERIVATION-20260929-position-time-radial-response.md',
        'DERIVATION-20260929-position-old-Euler-reaction.md', args.reader, 'CURRENT_LOCAL_RESUME.md']
    for name in documents:
        own(root / name)
        if name != 'CURRENT_LOCAL_RESUME.md':
            for value in re.findall(r'`([^`\n]+)`', (root / name).read_text(encoding='utf-8')):
                if value.endswith(('.py', '.md', '.npz', '.json', '.csv')) and not (root / value).is_file():
                    raise RuntimeError('Missing document citation: ' + value)
    scripts = list((root / 'scripts').glob('*position_time*20260929.py'))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    for path in intake.glob('annular-position-time-*.log'):
        own(path)
    since = datetime.fromisoformat('2026-09-29T00:59:30+00:00').timestamp()
    changed = [str(path) for path in (root.parent / 'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench changed: ' + repr(changed))
    if (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode; inspect before deletion')
    report = dict(state='complete', hashes=hashes, unique_files_rehashed=len(hashes), mismatches=0,
        authorities=authorities, total_computational_checks=sum(value['checks'] for value in authorities.values()),
        tables=tables, csv_rows=sum(tables.values()), scripts_compiled=len(scripts), preserved_attempts=preserved,
        protected_workbench_changed_since_turn_start=0, bytecode_cache_present=False,
        github_action=False, subagents_used=False, inherited_position_density_precision_warnings=4,
        inherited_mixed_time_precision_warnings=4, inherited_raw_C2_precision_warnings=2,
        mixed_weak_loading_constructed=True, B0_metric_response_computed=True,
        C0_old_reaction_solved=False, C0_force_current_column_computed=False, uncertainty_is_rigorous_bound=False)
    path = intake / 'annular-position-time-final-integrity-20260929.json'
    with path.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'hashes'}))


if __name__ == '__main__':
    main()
