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
    parser.add_argument('--main', default='annular-compensated-position-attempt03')
    parser.add_argument('--validator', default='annular-position-metric-jet-validation-attempt01')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260914'
    hashes, authorities, csv_rows = {}, {}, {}

    def own(path, expected=None):
        path = path.resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Missing or outside-project evidence: ' + str(path))
        relative = str(path.relative_to(root))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and expected != digest:
            raise RuntimeError('Changed evidence: ' + relative)
        if relative in hashes and hashes[relative] != digest:
            raise RuntimeError('Conflicting digest: ' + relative)
        hashes[relative] = digest

    for folder in [args.main, args.validator]:
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
                    csv_rows[relative] = len(rows)
    preserved = []
    for pattern in ['annular-compensated-position-attempt*', 'annular-position-oracle-diagnostic-attempt*', 'annular-position-metric-jet-validation-attempt*']:
        for folder in intake.glob(pattern):
            path = folder / 'status.json'
            if not folder.is_dir() or not path.is_file() or folder.name in [args.main, args.validator]:
                continue
            status = json.loads(path.read_text())
            if status['state'] not in ['complete', 'failed']:
                raise RuntimeError('Unfinished related attempt: ' + folder.name)
            own(path)
            for category in ['inputs', 'outputs']:
                for relative, expected in status[category].items():
                    if relative != 'CURRENT_LOCAL_RESUME.md':
                        own(root / relative, expected)
            preserved.append(dict(folder=folder.name, state=status['state'], error=status.get('error')))
    documents = ['DERIVATION-20260928-compensated-position-response.md', 'DERIVATION-20260928-position-reference-zero-sampling.md',
        'DERIVATION-20260928-position-precision-protocol.md', 'DERIVATION-20260928-position-metric-jet-and-old-reaction.md',
        'DERIVATION-20260928-position-safe-resume.md', 'DERIVATION-20260928-position-refined-sampling-embedding.md',
        'RESULTS-20260928-compensated-position-and-metric-jet.md', 'CURRENT_LOCAL_RESUME.md']
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
    for pattern in ['annular_compensated_position*_20260928.py', 'annular_position_*_20260928.py',
        'derive_annular_compensated_position*_20260928.py', 'resume_annular_compensated_position*_20260928.py', 'diagnose_annular_position*_20260928.py',
        'validate_annular_position*_20260928.py', 'seal_annular_position*_20260928.py']:
        scripts.update((root / 'scripts').glob(pattern))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    for pattern in ['annular-compensated-position-attempt*.log', 'annular-position-metric-jet-validation-attempt*.log']:
        for path in intake.glob(pattern):
            own(path)
    since = datetime.fromisoformat('2026-09-28T19:30:29+00:00').timestamp()
    changed = [str(path) for path in (root.parent / 'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench changes: ' + repr(changed))
    if (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode; inspect before deleting')
    position = json.loads((intake / args.main / 'status.json').read_text())
    validator = json.loads((intake / args.validator / 'status.json').read_text())
    report = dict(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=0, authorities=authorities, csv_rows=csv_rows,
        total_new_csv_rows=sum(csv_rows.values()), scripts_compiled=len(scripts), cited_paths=sorted(set(cited)),
        preserved_attempts=preserved, inherited_mixed_time_precision_warning_count=4,
        inherited_pointwise_mixed_time_accuracy_pass=False,
        position_density_precision_diagnostics=position['position_density_precision_diagnostics'],
        new_position_density_precision_warning_count=position['new_position_density_precision_warning_count'],
        sensitivity_is_rigorous_bound=False, full_force_current_column_computed=False,
        old_Euler_velocity_reaction_solved=False, protected_workbench_changed_since_turn_start=len(changed),
        protected_audit_scope='mtime since turn start, all task writes confined to post-checkpoint-work',
        bytecode_cache_present=False, github_action=False, subagents_used=False, valid_for_physics_claim=False,
        completed_jet_summaries=validator['summaries'])
    with (intake / 'annular-position-metric-jet-final-integrity-20260928.json').open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ['hashes', 'cited_paths']}))


if __name__ == '__main__':
    main()
