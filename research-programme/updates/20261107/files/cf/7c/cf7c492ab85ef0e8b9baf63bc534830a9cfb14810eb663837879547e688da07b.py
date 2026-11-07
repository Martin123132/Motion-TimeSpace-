from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import re


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260914'
    hashes, records, tables = {}, {}, {}

    def own(path, expected=None):
        path = path.resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Missing or outside-scope evidence: ' + str(path))
        relative = str(path.relative_to(root))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and digest != expected:
            raise RuntimeError('Changed evidence: ' + relative)
        if relative in hashes and hashes[relative] != digest:
            raise RuntimeError('Conflicting evidence: ' + relative)
        hashes[relative] = digest

    prior_path = intake / 'annular-position-time-final-integrity-20260929.json'
    prior = json.loads(prior_path.read_text())
    own(prior_path)
    if prior['state'] != 'complete':
        raise RuntimeError('B0 seal is incomplete')
    for relative, expected in prior['hashes'].items():
        if relative != 'CURRENT_LOCAL_RESUME.md':
            own(root / relative, expected)
    expected_states = {
        'annular-position-reaction-attempt01': 'failed',
        'annular-position-reaction-attempt02': 'failed',
        'annular-position-reaction-attempt03': 'failed',
        'annular-position-force-diagnostic-attempt01': 'complete',
        'annular-position-metric-force-diagnostic-attempt01': 'complete',
        'annular-position-native-force-validation-attempt01': 'complete',
        'annular-centered-integrals-diagnostic-attempt01': 'complete',
        'annular-original-spatial-rule-diagnostic-attempt01': 'complete',
        'annular-position-force-flux-identity-attempt01': 'complete',
        'annular-position-reaction-diagnostic-attempt01': 'complete',
        'annular-position-reaction-diagnostic-attempt02': 'settled',
        'annular-position-reaction-recovery-dry-run-attempt01': 'complete'}
    matched = None
    for name, expected_state in expected_states.items():
        path = intake / name / 'status.json'
        status = json.loads(path.read_text())
        own(path)
        if (expected_state == 'settled' and status['state'] not in ['complete', 'failed']) or (expected_state != 'settled' and status['state'] != expected_state):
            raise RuntimeError('Unexpected or unfinished state: ' + name)
        if expected_state == 'complete' and not all(row['passed'] for row in status['checks']):
            raise RuntimeError('Unacknowledged failed check: ' + name)
        if status.get('valid_for_physics_claim', False) or status.get('full_GR_limit_proven', False):
            raise RuntimeError('Unexpected promotion: ' + name)
        for category in ['inputs', 'outputs']:
            for relative, expected in status[category].items():
                if relative != 'CURRENT_LOCAL_RESUME.md':
                    own(root / relative, expected)
                if category == 'outputs' and relative.endswith('.csv'):
                    with (root / relative).open(newline='', encoding='utf-8') as stream:
                        rows = list(csv.DictReader(stream))
                    if not rows or any(None in row or any(value is None for value in row.values()) for row in rows):
                        raise RuntimeError('Malformed CSV: ' + relative)
                    if any(row.get('valid_for_claim', 'false').lower() != 'false' for row in rows):
                        raise RuntimeError('Unexpected claim row: ' + relative)
                    tables[relative] = len(rows)
        records[name] = dict(state=status['state'], checks=len(status['checks']), cases=len(status['cases']),
            error=status.get('error'), failed_checks=[row for row in status['checks'] if not row['passed']])
        if name == 'annular-position-reaction-recovery-dry-run-attempt01':
            if status.get('run_kind') != 'dry_run' or status.get('numerical_worker_launched') is not False:
                raise RuntimeError('Recovery dry run was not dry')
            records[name]['recovery_plan'] = status['recovery_plan']
        if name in ['annular-position-reaction-diagnostic-attempt01', 'annular-position-reaction-diagnostic-attempt02']:
            case_count = 1 if name.endswith('01') else (4 if status['state'] == 'complete' else len(status['cases']))
            if not status['diagnostic_only'] or status['accepted_for_C0'] or status['numerical_acceptance_passed'] or len(status['cases']) != case_count:
                raise RuntimeError('Diagnostic reaction scope changed')
            records[name]['accuracy_diagnostics'] = status['accuracy_gate_failures']
            records[name]['summaries'] = [row['summary'] for row in status['cases']]
            if name.endswith('02'):
                matched = status
                records[name]['external_safe_boundary_stop'] = status.get('external_safe_boundary_stop', False)
                records[name]['operational_runtime_stop'] = status.get('error') == "RuntimeError('Safe Eulerian position reaction boundary')"
        if name == 'annular-position-native-force-validation-attempt01' and (len(status['cases']) != 2 or len(status['checks']) != 6):
            raise RuntimeError('Incomplete native-energy validation')
        if name == 'annular-position-force-flux-identity-attempt01' and (len(status['cases']) != 5 or len(status['checks']) != 8):
            raise RuntimeError('Incomplete flux identity validation')
        log = intake / (name + '.log')
        if log.is_file():
            own(log)
    control_path = intake / 'annular-position-reaction-boundary-workflow/status.json'
    control = json.loads(control_path.read_text())
    if control['state'] != 'complete':
        raise RuntimeError('Boundary controller is unsettled')
    own(control_path)
    own(root / 'scripts/save_annular_position_reaction_boundary_20260929.ps1')
    snapshot = intake / 'annular-position-reaction-diagnostic-attempt02/running-status-at-safe-boundary.json'
    if snapshot.is_file():
        own(snapshot)
    completed_rows = [row['summary'] for row in matched['cases']]
    table_path = intake / 'position-reaction-completed-controls-20260929.csv'
    with table_path.open('x', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(completed_rows[0]))
        writer.writeheader()
        writer.writerows(completed_rows)
    own(table_path)
    with table_path.open(newline='', encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != len(completed_rows) or any(None in row or any(value is None for value in row.values()) or row['valid_for_claim'].lower() != 'false' for row in rows):
        raise RuntimeError('Malformed completed-controls table')
    tables[str(table_path.relative_to(root))] = len(rows)
    document_names = [
        'DERIVATION-20260929-position-reaction-construction.md',
        'DERIVATION-20260929-position-reaction-sensitivity.md',
        'DERIVATION-20260929-position-force-quadrature-repair.md',
        'DERIVATION-20260929-source-centered-quadrature.md',
        'DERIVATION-20260929-position-reaction-diagnostic-solve.md',
        'DERIVATION-20260929-matched-position-reaction-diagnostics.md',
        'DERIVATION-20260929-position-force-flux-form.md',
        'DERIVATION-20260929-position-reaction-safe-recovery.md',
        'RESULTS-20260929-position-reaction-and-precision-gate.md', 'CURRENT_LOCAL_RESUME.md']
    for name in document_names:
        path = root / name
        own(path)
        if name != 'CURRENT_LOCAL_RESUME.md':
            for citation in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
                if citation.endswith(('.py', '.md', '.json', '.npz', '.csv')) and not (root / citation).is_file():
                    raise RuntimeError('Missing citation: ' + citation)
    patterns = ['*position_reaction*20260929.py', '*position_force*20260929.py',
        '*position_metric_force*20260929.py', '*position_native_force*20260929.py',
        '*source_centered_quadrature*20260929.py', '*centered_integrals*20260929.py', '*original_spatial_rule*20260929.py']
    scripts = sorted(set(path for pattern in patterns for path in (root / 'scripts').glob(pattern)))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    if (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode cache; inspect before deleting')
    since = datetime.fromisoformat('2026-09-29T11:13:05+00:00').timestamp()
    changed = [str(path) for path in (root.parent / 'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench modified: ' + repr(changed))
    report = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=0, attempts=records, csv_tables=tables,
        csv_rows=sum(tables.values()), scripts_compiled=len(scripts), protected_workbench_changed_since_turn_start=0,
        bytecode_cache_present=False, github_action=False, subagents_used=False,
        B0_four_case_stage_complete=True, independent_native_energy_checks_passed=6,
        manufactured_flux_identity_checks_passed=8,
        k0_reference_diagnostic_executed=True, k0_four_case_diagnostics_complete=matched['state'] == 'complete' and len(matched['cases']) == 4,
        k0_diagnostic_completed_case_count=len(matched['cases']), k0_four_case_acceptance_complete=False,
        C0_force_current_column_computed=False, accepted_for_C0=False,
        inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4,
        inherited_raw_C2_warnings=2, B0_to_k0_full_validator_executed=False,
        flux_form_identity_derived=True, flux_form_numerically_implemented=False)
    path = intake / 'annular-position-reaction-stage-integrity-20260929.json'
    with path.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ['hashes', 'attempts']}))


if __name__ == '__main__':
    main()
