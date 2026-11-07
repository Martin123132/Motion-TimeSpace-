from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_label_rule_20260929 import decimal_label_rule, exact_weighted_moment
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from pathlib import Path
import csv
import hashlib
import json
import re


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260914'
    hashes, attempts, tables, reports = {}, {}, {}, {}

    def own(path, expected=None):
        path = path.resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Missing or out-of-scope evidence: ' + str(path))
        relative = str(path.relative_to(root))
        if relative not in hashes:
            hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and hashes[relative] != expected:
            raise RuntimeError('Changed evidence: ' + relative)

    prior_path = intake / 'annular-mts-position-reaction-final-integrity-20260929.json'
    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete' or prior['completed_matched_diagnostic_cases'] != 4:
        raise RuntimeError('Prior four-case seal incomplete')
    own(prior_path)
    for relative, expected in prior['hashes'].items():
        if relative != 'CURRENT_LOCAL_RESUME.md':
            own(root / relative, expected)
    names = ['annular-native-position-arithmetic-probe-attempt01',
        'annular-native-position-arithmetic-integral-attempt01',
        'annular-native-rounding-channels-attempt01',
        'annular-native-tangent-precision-repair-attempt01',
        'annular-native-precision-live-response-attempt01',
        'annular-position-force-commuted-diagnostic-attempt01']
    for name in names:
        path = intake / name / 'status.json'
        status = json.loads(path.read_text())
        own(path)
        if status['state'] not in ['complete', 'failed']:
            raise RuntimeError('Unsettled calculation: ' + name)
        if status['state'] == 'complete' and not all(row['passed'] for row in status['checks']):
            raise RuntimeError('Unacknowledged hard check failure: ' + name)
        if any(status.get(key, False) for key in ['accepted_for_C0', 'valid_for_physics_claim', 'full_GR_limit_proven']):
            raise RuntimeError('Unexpected claim promotion: ' + name)
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
        log = intake / (name + '.log')
        if log.is_file():
            own(log)
        attempts[name] = dict(state=status['state'], checks=len(status['checks']), cases=len(status['cases']),
            error=status.get('error'), summaries=[row.get('summary', row) for row in status['cases']])
        reports[name] = status
    repair = reports['annular-native-tangent-precision-repair-attempt01']
    if repair['state'] != 'complete' or not repair['all_native_pairs_passed'] or len(repair['native_quadrature_checks']) != 4:
        raise RuntimeError('Minimal native repair acceptance inconsistent with reader')
    documents = ['DERIVATION-20260929-native-force-directional-arithmetic.md',
        'DERIVATION-20260929-native-force-precision-integration.md',
        'DERIVATION-20260929-native-tangent-rounding-repair.md',
        'DERIVATION-20260929-native-precision-live-response.md',
        'DERIVATION-20260929-wave-force-commuted-edge-gradient.md',
        'RESULTS-20260929-native-force-precision-repair.md', 'CURRENT_LOCAL_RESUME.md']
    for name in documents:
        path = root / name
        own(path)
        if name != 'CURRENT_LOCAL_RESUME.md':
            for citation in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
                if citation.endswith(('.py', '.md', '.json', '.npz', '.csv')) and not (root / citation).is_file():
                    raise RuntimeError('Missing citation: ' + citation)
    names = ['annular_native_position_precision_20260929.py', 'annular_native_precision_context_20260929.py',
        'diagnose_annular_native_precision_probe_20260929.py', 'annular_decimal_label_rule_20260929.py',
        'diagnose_annular_native_precision_integral_20260929.py', 'diagnose_annular_native_precision_integral_v2_20260929.py',
        'diagnose_annular_native_rounding_channels_20260929.py',
        'annular_native_tangent_precision_repair_20260929.py', 'validate_annular_native_tangent_precision_20260929.py',
        'derive_annular_native_precision_response_20260929.py', 'annular_position_force_compensated_v3_20260929.py',
        'diagnose_annular_position_force_commuted_20260929.py', 'seal_annular_native_precision_repair_20260929.py']
    for name in names:
        path = root / 'scripts' / name
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        own(path)
    rule_checks = []
    with localcontext() as context:
        context.prec = 70
        for order in [3, 4, 8]:
            labels, weights = decimal_label_rule(order)
            if min(weights) <= 0 or not all(labels[index] < labels[index + 1] for index in range(order - 1)):
                raise RuntimeError('Optional Decimal Gauss rule ordering or positivity')
            for power in range(2 * order - 2):
                observed = sum(weight * (label ** power if power else Decimal(1)) for label, weight in zip(labels, weights))
                error = abs(observed - exact_weighted_moment(power))
                if error >= Decimal('1e-55'):
                    raise RuntimeError('Optional Decimal Gauss moment check')
                rule_checks.append(dict(order=order, power=power, error=str(error)))
    if (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode cache')
    since = datetime.fromisoformat('2026-09-29T19:14:11+00:00').timestamp()
    changed = [str(path) for path in (root.parent / 'formalization-workbench').rglob('*')
        if path.is_file() and path.stat().st_mtime >= since]
    if changed:
        raise RuntimeError('Protected workbench modified: ' + repr(changed))
    response = reports['annular-native-precision-live-response-attempt01']
    wave = reports['annular-position-force-commuted-diagnostic-attempt01']
    wave_pairs = [row['summary'] for row in wave['cases'] if row['summary'].get('compensated_successive_inverse') is not None]
    report = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=0, attempts=attempts, csv_tables=tables,
        csv_rows=sum(tables.values()), scripts_compiled=len(names),
        native_pair_checks=repair['native_quadrature_checks'], native_pairs_passed=True,
        native_live_response_complete=response['state'] == 'complete' and len(response['cases']) == 2,
        reference_wave_pair_passed=bool(wave_pairs) and all(row['successive_within_2e11'] for row in wave_pairs),
        reference_wave_pair_results=wave_pairs, optional_decimal_rule_unit_checks=rule_checks,
        decimal_Gauss_rule_used_in_repair=False, accepted_for_C0=False,
        full_material_reintegration=False, actual_flux_by_parts_implemented=False,
        protected_workbench_changed_since_turn_start=0, bytecode_cache_present=False,
        github_action=False, subagents_used=False)
    path = intake / 'annular-native-precision-repair-integrity-20260929.json'
    with path.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in report.items()
        if key not in ['hashes', 'attempts', 'csv_tables', 'optional_decimal_rule_unit_checks']}))


if __name__ == '__main__':
    main()
