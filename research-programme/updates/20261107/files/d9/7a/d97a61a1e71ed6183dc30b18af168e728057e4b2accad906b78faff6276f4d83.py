from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import re


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    hashes, records, tables = {}, {}, {}

    def own(path, expected=None):
        path = path.resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Missing or out-of-scope evidence: '+str(path))
        relative = str(path.relative_to(root))
        if relative in hashes:
            if expected is not None and hashes[relative] != expected:
                raise RuntimeError('Conflicting evidence digest: '+relative)
            return
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and actual != expected:
            raise RuntimeError('Changed evidence: '+relative)
        hashes[relative] = actual

    prior_path = intake/'annular-position-reaction-stage-integrity-20260929.json'
    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete':
        raise RuntimeError('Prior stage seal incomplete')
    own(prior_path)
    for relative, expected in prior['hashes'].items():
        if relative != 'CURRENT_LOCAL_RESUME.md':
            own(root/relative, expected)
    names = [
        'annular-position-reaction-diagnostic-attempt03',
        'annular-position-reaction-diagnostic-attempt04',
        'annular-original-label-rule-diagnostic-attempt01',
        'annular-original-label-rule-diagnostic-attempt02',
        'annular-original-label-rule-diagnostic-attempt03',
        'annular-force-moving-cut-identity-attempt01',
        'annular-position-force-compensated-diagnostic-attempt01',
        'annular-registered-metric-center-diagnostic-attempt01',
        'annular-position-force-registered-diagnostic-attempt01',
        'annular-native-position-label-diagnostic-attempt01',
        'annular-position-quadrature-components-attempt01',
        'annular-position-quadrature-components-attempt02']
    matched = None
    for name in names:
        path = intake/name/'status.json'
        status = json.loads(path.read_text())
        own(path)
        if status['state'] not in ['complete', 'failed']:
            raise RuntimeError('Unsettled calculation: '+name)
        failed_checks = [row for row in status['checks'] if not row['passed']]
        if status['state'] == 'complete' and failed_checks:
            raise RuntimeError('Unacknowledged failed hard check: '+name)
        if any(status.get(key, False) for key in ['valid_for_physics_claim', 'full_GR_limit_proven', 'accepted_for_C0']):
            raise RuntimeError('Unexpected physics promotion: '+name)
        for category in ['inputs', 'outputs']:
            for relative, expected in status[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                own(root/relative, expected)
                if category == 'outputs' and relative.endswith('.csv'):
                    with (root/relative).open(newline='', encoding='utf-8') as stream:
                        rows = list(csv.DictReader(stream))
                    if not rows or any(None in row or any(value is None for value in row.values()) for row in rows):
                        raise RuntimeError('Malformed CSV: '+relative)
                    if any(row.get('valid_for_claim', 'false').lower() != 'false' for row in rows):
                        raise RuntimeError('Unexpected claim row: '+relative)
                    tables[relative] = len(rows)
        log = intake/(name+'.log')
        if log.is_file():
            own(log)
        records[name] = dict(state=status['state'], checks=len(status['checks']), cases=len(status['cases']),
            error=status.get('error'), failed_checks=failed_checks,
            summaries=[row.get('summary', row) for row in status['cases']],
            accuracy_diagnostics=status.get('accuracy_gate_failures', []),
            external_safe_boundary_stop=status.get('external_safe_boundary_stop', False))
        if name == 'annular-position-reaction-diagnostic-attempt04':
            matched = status
            if not status['diagnostic_only'] or status['numerical_acceptance_passed']:
                raise RuntimeError('Changed matched diagnostic scope')
        if name == 'annular-force-moving-cut-identity-attempt01' and (status['state'] != 'complete' or len(status['checks']) != 20):
            raise RuntimeError('Moving-cut proof incomplete')
        if name == 'annular-registered-metric-center-diagnostic-attempt01' and (
                status['state'] != 'complete' or len(status['cases']) != 4
                or not all(row['registered_exact_replay'] for row in status['cases'])):
            raise RuntimeError('Registered-coordinate probe incomplete')
    snapshot = intake/'annular-position-force-compensated-diagnostic-attempt01/pre-safe-stop-status.json'
    own(snapshot)
    document_names = [
        'DERIVATION-20260929-original-force-label-resolution.md',
        'DERIVATION-20260929-high-label-baseline-continuation.md',
        'DERIVATION-20260929-compensated-field-force-integration.md',
        'DERIVATION-20260929-force-moving-cut-terms.md',
        'DERIVATION-20260929-registered-metric-centers.md',
        'DERIVATION-20260929-native-position-force-label-resolution.md',
        'RESULTS-20260929-MTS-position-reaction-and-integration-repair.md',
        'CURRENT_LOCAL_RESUME.md']
    for name in document_names:
        path = root/name
        own(path)
        if name != 'CURRENT_LOCAL_RESUME.md':
            for citation in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
                if citation.endswith(('.py', '.md', '.json', '.npz', '.csv')) and not (root/citation).is_file():
                    raise RuntimeError('Missing citation: '+citation)
    patterns = ['*original_label_rule*20260929.py', '*position_force_compensated*20260929.py',
        '*force_moving_cuts*20260929.py', '*registered_metric*20260929.py',
        '*position_force_registered*20260929.py', '*position_quadrature_components*20260929.py',
        '*native_position_label_rule*20260929.py',
        'seal_annular_mts_position_reaction_20260929.py']
    scripts = sorted(set(path for pattern in patterns for path in (root/'scripts').glob(pattern)))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    if (root/'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode cache')
    since = datetime.fromisoformat('2026-09-29T15:17:27+00:00').timestamp()
    changed = [str(path) for path in (root.parent/'formalization-workbench').rglob('*')
        if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench modified: '+repr(changed))
    completed_rows = [row['summary'] for row in matched['cases']]
    table_path = intake/'mts-position-reaction-completed-controls-20260929.csv'
    with table_path.open('x', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(completed_rows[0]))
        writer.writeheader()
        writer.writerows(completed_rows)
    own(table_path)
    with table_path.open(newline='', encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != len(completed_rows) or any(None in row or row['valid_for_claim'].lower() != 'false' for row in rows):
        raise RuntimeError('Malformed matched-controls table')
    tables[str(table_path.relative_to(root))] = len(rows)
    report = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=0, attempts=records, csv_tables=tables,
        csv_rows=sum(tables.values()), scripts_compiled=len(scripts),
        protected_workbench_changed_since_turn_start=0, bytecode_cache_present=False,
        github_action=False, subagents_used=False, completed_matched_diagnostic_cases=len(completed_rows),
        all_four_diagnostics_complete=matched['state'] == 'complete' and len(completed_rows) == 4,
        accepted_for_C0=False, C0_force_current_column_computed=False,
        registered_coordinate_exact_replay_cases=4, registered_coordinate_probe_points=39270,
        moving_cut_manufactured_checks=20, actual_flux_by_parts_implemented=False,
        inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4,
        inherited_raw_C2_warnings=2)
    with (intake/'annular-mts-position-reaction-final-integrity-20260929.json').open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ['hashes', 'attempts', 'csv_tables']}))


if __name__ == '__main__':
    main()
