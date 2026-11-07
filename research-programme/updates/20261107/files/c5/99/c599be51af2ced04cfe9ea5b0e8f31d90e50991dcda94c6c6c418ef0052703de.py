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
    folders = ['annular-live-support-acceleration-attempt01',
        'annular-live-support-acceleration-validation-attempt02',
        'annular-support-metric-feedback-bound-attempt01',
        'annular-probe-gravity-precision-validation-attempt01',
        'annular-archived-probe-baseline-comparison-attempt01',
        'annular-radial-time-forcing-derivation-attempt01']
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
    failed_attempts = {}
    for folder, expected_error in [
            ('annular-live-support-acceleration-validation-attempt01', 'raw_endpoint_derivative'),
            ('annular-instantaneous-support-trial-attempt01', 'baseline_gravity_quadrature'),
            ('annular-instantaneous-support-trial-attempt02', 'baseline_gravity_quadrature'),
            ('annular-instantaneous-support-trial-attempt03', 'MTS-primary-third:independent_shift_amplitude:48:0')]:
        failed_path = intake / folder / 'status.json'
        failed = json.loads(failed_path.read_text())
        if failed['state'] != 'failed' or expected_error not in failed['error']:
            raise RuntimeError('Original failed numerical check must remain explicit: ' + folder)
        failed_attempts[folder] = failed['error']
        own(failed_path)
        for category in ['inputs', 'outputs']:
            for relative, expected in failed[category].items():
                if relative != 'CURRENT_LOCAL_RESUME.md':
                    own(root / relative, expected)
    documents = ['RESULTS-20260928-live-metric-and-instantaneous-support-trial.md',
        'DERIVATION-20260928-live-metric-support-acceleration.md',
        'DERIVATION-20260928-instantaneous-support-constraint-trial.md',
        'DERIVATION-20260928-live-current-validator-precision-correction.md',
        'DERIVATION-20260928-union-grid-gravity-correction.md',
        'DERIVATION-20260928-probe-gravity-precision-correction.md',
        'DERIVATION-20260928-archived-probe-baseline-control.md',
        'DERIVATION-20260928-exact-background-radial-time-forcing.md', 'CURRENT_LOCAL_RESUME.md']
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
    scripts = ['annular_support_radial_response_20260928.py',
        'derive_annular_live_support_acceleration_20260928.py',
        'validate_annular_live_support_acceleration_20260928.py',
        'validate_annular_live_support_acceleration_v2_20260928.py',
        'annular_high_precision_current_20260928.py',
        'derive_annular_instantaneous_support_trial_20260928.py',
        'derive_annular_instantaneous_support_trial_v2_20260928.py',
        'derive_annular_instantaneous_support_trial_v3_20260928.py',
        'annular_union_grid_gravity_20260928.py',
        'annular_precise_union_gravity_20260928.py',
        'validate_annular_probe_gravity_precision_20260928.py',
        'compare_annular_archived_probe_baselines_20260928.py',
        'annular_radial_time_forcing_20260928.py',
        'derive_annular_radial_time_forcing_20260928.py',
        'annular_stable_acceleration_current_20260928.py',
        'bound_annular_support_metric_feedback_20260928.py',
        'seal_annular_live_support_acceleration_20260928.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    if (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode cache; inspect before cleanup')
    since = datetime.fromisoformat('2026-09-28T12:10:23+00:00').timestamp()
    changed = [str(path) for path in (root.parent / 'formalization-workbench').rglob('*')
        if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench mtime audit found changes: ' + repr(changed))
    report = dict(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=0, authorities=authorities, csv_rows=csv_rows,
        preserved_failed_attempts=failed_attempts,
        large_amplitude_current_trial_complete=False,
        scope='Integrity of completed acceleration/forcing blocks and baseline controls, with the precision-limited large-amplitude trial explicitly retained as failed',
        total_new_csv_rows=sum(csv_rows.values()), cited_paths=sorted(set(cited)), scripts_compiled=len(scripts),
        protected_workbench_changed_since_turn_start=len(changed),
        protected_audit_scope='mtime since turn start plus all writes confined to post-checkpoint-work',
        bytecode_cache_present=False, github_action=False)
    with (intake / 'annular-live-support-acceleration-final-integrity-20260928.json').open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ['hashes', 'cited_paths']}))


if __name__ == '__main__':
    main()
