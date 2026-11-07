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
            raise RuntimeError('Conflicting evidence: ' + relative)
        hashes[relative] = digest

    folders = ['annular-live-compensation-time-attempt04', 'annular-live-compensation-time-validation-attempt02']
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
    failures = []
    for folder in ['annular-live-compensation-time-attempt0' + str(number) for number in [1, 2, 3]] + ['annular-live-compensation-time-validation-attempt01']:
        path = intake / folder / 'status.json'
        status = json.loads(path.read_text())
        if status['state'] != 'failed':
            raise RuntimeError('Failed attempt was changed: ' + folder)
        failures.append(dict(folder=folder, error=status['error']))
        own(path)
        for category in ['inputs', 'outputs']:
            for relative, expected in status[category].items():
                if relative != 'CURRENT_LOCAL_RESUME.md':
                    own(root / relative, expected)
    diagnostic = intake / 'annular-compensation-replay-diagnostic-attempt01/status.json'
    exploratory = json.loads(diagnostic.read_text())
    own(diagnostic)
    for category in ['inputs', 'outputs']:
        for relative, expected in exploratory[category].items():
            own(root / relative, expected)
    documents = ['DERIVATION-20260928-live-compensation-time-derivative.md',
        'DERIVATION-20260928-compensation-source-replay-correction.md',
        'DERIVATION-20260928-compensation-oracle-convention.md',
        'DERIVATION-20260928-compensation-end-to-end-precision.md',
        'DERIVATION-20260928-mixed-radial-precision-warning.md',
        'RESULTS-20260928-live-compensation-time-derivative.md', 'CURRENT_LOCAL_RESUME.md']
    cited = []
    for name in documents:
        path = root / name
        own(path)
        if name != 'CURRENT_LOCAL_RESUME.md':
            for value in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
                if value.endswith(('.md', '.py', '.json', '.npz', '.csv')):
                    if not (root / value).is_file():
                        raise RuntimeError('Missing cited file: ' + value)
                    cited.append(value)
    scripts = ['annular_live_compensation_derivative_20260928.py',
        'annular_compensation_complex_oracle_20260928.py', 'annular_compensation_complex_oracle_v2_20260928.py',
        'annular_compensation_cardinal_source_20260928.py', 'annular_compensation_oracle_transport_20260928.py',
        'derive_annular_live_compensation_time_20260928.py', 'derive_annular_live_compensation_time_v2_20260928.py',
        'derive_annular_live_compensation_time_v3_20260928.py', 'derive_annular_live_compensation_time_v4_20260928.py',
        'diagnose_annular_compensation_replay_20260928.py', 'validate_annular_live_compensation_time_20260928.py',
        'validate_annular_live_compensation_time_v2_20260928.py',
        'seal_annular_compensation_time_20260928.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    for pattern in ['annular-live-compensation-time-attempt*.log', 'annular-live-compensation-time-validation-attempt*.log']:
        for path in intake.glob(pattern):
            own(path)
    since = datetime.fromisoformat('2026-09-28T16:20:34+00:00').timestamp()
    changed = [str(path) for path in (root.parent / 'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench changes: ' + repr(changed))
    if (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode; inspect before deleting')
    main_status = json.loads((intake / folders[0] / 'status.json').read_text())
    validation_status = json.loads((intake / folders[1] / 'status.json').read_text())
    report = dict(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=0, authorities=authorities, csv_rows=csv_rows,
        total_new_csv_rows=sum(csv_rows.values()), scripts_compiled=len(scripts), cited_paths=sorted(set(cited)),
        preserved_failures=failures, original_density_relative_gate_results=[
            dict(branch=row['branch'], level=row['level'], passed=row['compensated_density_relative_gate_pass']) for row in main_status['summaries']],
        precision_acceptance='End-to-end wdot sensitivity <=2e-12; failed intermediate relative flags remain explicit',
        precision_warning_count=validation_status['precision_warning_count'],
        pointwise_mixed_radial_accuracy_pass=validation_status['pointwise_mixed_radial_accuracy_pass'],
        precision_diagnostics=validation_status['precision_diagnostics'],
        scope='Local differentiated live compensation; full C1/C0 columns and support trajectory not computed',
        protected_workbench_changed_since_turn_start=len(changed),
        protected_audit_scope='mtime since turn start, all task writes inside post-checkpoint-work',
        bytecode_cache_present=False, github_action=False, subagents_used=False, valid_for_physics_claim=False)
    with (intake / 'annular-compensation-time-final-integrity-20260928.json').open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ['hashes', 'cited_paths']}))


if __name__ == '__main__':
    main()
