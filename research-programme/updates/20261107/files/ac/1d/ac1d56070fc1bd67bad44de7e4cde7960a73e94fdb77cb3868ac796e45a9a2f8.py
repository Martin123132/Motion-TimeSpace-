from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
import csv
import ctypes
import hashlib
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 4):
        raise OSError('Cannot set one core')
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-C0-integral-stage-integrity-20260930.json'
    table = directory/'annular-C0-integral-stage-summary-20260930.csv'
    if target.exists() or table.exists():
        raise FileExistsError('Stage outputs already exist')
    hashes, mismatches = {}, []

    def verify(relative, expected=None):
        if relative == 'CURRENT_LOCAL_RESUME.md':
            return
        path = (root/relative).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Missing or out-of-scope source: '+relative)
        key = str(path.relative_to(root))
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and actual != expected:
            mismatches.append(key)
        if key in hashes and hashes[key] != actual:
            raise RuntimeError('Conflicting current hash: '+key)
        hashes[key] = actual

    inherited_path = directory/'annular-position-support-stage-integrity-20260930.json'
    inherited = json.loads(inherited_path.read_text())
    if inherited['state'] != 'complete' or inherited['mismatches']:
        raise RuntimeError('Inherited seal failed')
    verify(str(inherited_path.relative_to(root)))
    for relative, expected in inherited['hashes'].items():
        verify(relative, expected)
    statuses, ledger, rows = {}, [], []
    for path in sorted(directory.glob('annular-C0-*/status.json')):
        name = path.parent.name
        status = json.loads(path.read_text())
        if status['state'] not in ['complete', 'failed']:
            raise RuntimeError('Unsettled worker: '+name)
        if status['state'] == 'complete' and not all(check['passed'] for check in status['checks']):
            raise RuntimeError('Invalid complete status: '+name)
        statuses[name] = status
        verify(str(path.relative_to(root)))
        for category in ['inputs', 'outputs']:
            for relative, expected in status[category].items():
                verify(relative, expected)
        for extra in path.parent.iterdir():
            if extra.is_file():
                verify(str(extra.relative_to(root)))
        log = directory/(name+'.log')
        if log.exists():
            verify(str(log.relative_to(root)))
        ledger.append(dict(name=name, state=status['state'], checks=len(status['checks']),
            failed_checks=[check['name'] for check in status['checks'] if not check['passed']],
            external_safe_stop=status.get('external_safe_boundary_stop', False), error=status.get('error')))
        for case in status.get('cases', []):
            summary = case.get('summary', {})
            if summary.get('complete_integral_constructed'):
                values = np.asarray(summary['C0'])
                if values.shape != (4,) or not np.isfinite(values).all():
                    raise RuntimeError('Malformed integral: '+name)
                rows.append(dict(source=str(path.relative_to(root)), branch=summary['branch'], level=summary['level'],
                    method='Eulerian', C0=json.dumps(summary['C0']), diagnostic=json.dumps(summary['paired_difference']),
                    passed=str(summary['paired_passed']).lower(), valid_for_claim='false'))
        if status.get('complete_C0_constructed'):
            outputs = status['rule_outputs']
            if status['requested_orders'] != [24, 32]:
                raise RuntimeError('Unexpected material order scope')
            rows.append(dict(source=str(path.relative_to(root)), branch=status['branch'], level=status['level'],
                method='material', C0=json.dumps(outputs[-1]['summary']['C0']), diagnostic=str(outputs[-1]['summary']['pair']),
                passed=str(status['all_requested_pairs_passed']).lower(), valid_for_claim='false'))
            cross_difference = outputs[-1]['summary']['old_Eulerian_difference']
            rows.append(dict(source=str(path.relative_to(root)), branch=status['branch'], level=status['level'],
                method='material-versus-Eulerian', C0=json.dumps(outputs[-1]['summary']['C0']), diagnostic=json.dumps(cross_difference),
                passed=str(np.max(np.abs(cross_difference)) <= 2e-17).lower(), valid_for_claim='false'))
        if status.get('reaction_sensitivity_integrated'):
            rows.append(dict(source=str(path.relative_to(root)), branch=status['branch'], level=status['level'],
                method='reaction-sensitivity-budget', C0=json.dumps(status['rule_outputs'][-1]['summary']['reaction_C0']),
                diagnostic=json.dumps(status['diagnostic_budget']), passed=str(status['diagnostic_budget_passed']).lower(), valid_for_claim='false'))
    required = ['annular-C0-material-'+branch+'-fine-attempt01' for branch in ['reference', 'MTS']]
    if not all(name in statuses for name in required):
        raise RuntimeError('Matched material attempts missing')
    new_scripts = sorted(path for path in (root/'scripts').glob('*C0*20260930*') if path.suffix in ['.py', '.ps1'])
    compiled = []
    for path in new_scripts:
        verify(str(path.relative_to(root)))
        if path.suffix == '.py':
            compile(path.read_text(encoding='utf-8'), str(path), 'exec')
            compiled.append(path.name)
    for pattern in ['DERIVATION-20260930-C0-*.md', 'DERIVATION-20260930-native-coefficient-event-interpolation.md',
        'RESULTS-20260930-boundary-complete-C0-and-sensitivity.md']:
        paths = list(root.glob(pattern))
        if not paths:
            raise RuntimeError('Missing stage document: '+pattern)
        for path in paths:
            verify(str(path.relative_to(root)))
    for path in directory.glob('annular-C0-*.log'):
        verify(str(path.relative_to(root)))
    started = datetime(2026, 9, 30, 14, 2, tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
        if path.is_file() and path.stat().st_mtime >= started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches, protected_changes=changed, bytecode=[str(path) for path in bytecode]))
    with table.open('x', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=['source', 'branch', 'level', 'method', 'C0', 'diagnostic', 'passed', 'valid_for_claim'])
        writer.writeheader()
        writer.writerows(rows)
    with table.open(newline='', encoding='utf-8') as stream:
        replay = list(csv.DictReader(stream, strict=True))
    if len(replay) != len(rows) or any(None in row or any(value is None for value in row.values()) for row in replay):
        raise RuntimeError('CSV replay failed')
    if any(row['valid_for_claim'] != 'false' for row in replay):
        raise RuntimeError('Unexpected physical claim')
    verify(str(table.relative_to(root)))
    seal = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(), hashes=hashes,
        unique_files_rehashed=len(hashes), mismatches=mismatches, authorities=ledger, scripts_compiled=compiled,
        csv_rows=len(rows), csv_path=str(table.relative_to(root)),
        material_fine_both_pass=all(statuses[name].get('all_requested_pairs_passed', False) for name in required),
        actual_cross_representation_agreement_passed=all(row['passed'] == 'true' for row in rows if row['method'] == 'material-versus-Eulerian'),
        reaction_sensitivity_both_pass=all(statuses.get(name, {}).get('diagnostic_budget_passed', False)
            for name in ['annular-C0-sensitivity-reference-fine-attempt01', 'annular-C0-sensitivity-MTS-fine-attempt02']),
        full_third_integral_complete=False, accepted_for_finite_history=False, valid_for_physics_claim=False,
        inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4,
        inherited_raw_C2_warnings=2, old_weak_flux_flags_retained=True,
        protected_workbench_changed_since_turn_start=len(changed), bytecode_cache_present=False,
        github_action=False, subagents_used=False, current_resume_excluded=True)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(seal, indent=2)+'\n')
    print(json.dumps({key:value for key,value in seal.items() if key != 'hashes'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
