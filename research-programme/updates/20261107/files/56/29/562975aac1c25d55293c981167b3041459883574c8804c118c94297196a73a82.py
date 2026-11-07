from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
import csv
import ctypes
import hashlib
import json


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 4):
        raise OSError('Cannot set one-core affinity')
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-position-support-stage-integrity-20260930.json'
    if target.exists():
        raise FileExistsError(target)
    inherited_path = directory/'annular-refined-wave-stage-integrity-20260930.json'
    inherited = json.loads(inherited_path.read_text())
    if inherited['state'] != 'complete' or inherited['mismatches']:
        raise RuntimeError('Inherited seal not complete')
    hashes, mismatches = {}, []

    def verify(relative, expected=None):
        if relative == 'CURRENT_LOCAL_RESUME.md':
            return
        path = (root/relative).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Missing or out-of-scope scientific file: '+relative)
        key = str(path.relative_to(root))
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and actual != expected:
            mismatches.append(key)
        if key in hashes and hashes[key] != actual:
            raise RuntimeError('Conflicting current digest: '+key)
        hashes[key] = actual

    verify(str(inherited_path.relative_to(root)))
    for relative, expected in inherited['hashes'].items():
        verify(relative, expected)
    authorities, csv_tables, csv_rows = [], [], 0
    names = ['annular-flux-corrected-Euler-'+branch+suffix+'-attempt01'
        for branch in ['reference', 'MTS'] for suffix in ['', '-third']]
    names += ['annular-position-support-manufactured-attempt01',
        'annular-position-support-reference-attempt01', 'annular-position-support-MTS-attempt01']
    total_checks, probes = 0, 0
    for name in names:
        path = directory/name/'status.json'
        status = json.loads(path.read_text())
        verify(str(path.relative_to(root)))
        if status['state'] != 'complete' or not all(row['passed'] for row in status['checks']):
            raise RuntimeError('Incomplete or failed authority: '+name)
        if 'Euler' in name and not status['all_fresh_equation_checks_passed']:
            raise RuntimeError('Fresh Euler acceptance missing: '+name)
        if 'support' in name and status['actual_integrated_C0_complete']:
            raise RuntimeError('Pointwise procedure claimed a full integral: '+name)
        if 'support-reference' in name or 'support-MTS' in name:
            probes += len(status['cases'])
            if not status['all_four_fresh_Euler_checks_verified']:
                raise RuntimeError('Pointwise input gate missing')
        total_checks += len(status['checks'])
        authorities.append(dict(name=name, checks=len(status['checks']), state=status['state']))
        for category in ['inputs', 'outputs']:
            for relative, expected in status[category].items():
                verify(relative, expected)
                if category == 'outputs' and relative.endswith('.csv') and relative not in csv_tables:
                    with (root/relative).open(newline='', encoding='utf-8') as stream:
                        rows = list(csv.DictReader(stream, strict=True))
                    if not rows or any(None in row or any(value is None for value in row.values()) for row in rows):
                        raise RuntimeError('Malformed CSV: '+relative)
                    if any(row.get('valid_for_claim', '').lower() != 'false' for row in rows):
                        raise RuntimeError('Unexpected claim flag: '+relative)
                    csv_tables.append(relative)
                    csv_rows += len(rows)
    files = ['DERIVATION-20260930-position-support-C0.md',
        'RESULTS-20260930-fresh-third-Euler-and-position-column.md',
        'DERIVATION-20260929-position-old-Euler-reaction.md',
        'DERIVATION-20260929-reacted-force-current-columns.md',
        'scripts/annular_support_shift_jet_20260928.py',
        'scripts/annular_directional_coupled_Euler_20260928.py',
        'scripts/annular_native_tangent_precision_repair_20260929.py']
    scripts = ['annular_position_support_column_20260930.py',
        'validate_annular_position_support_manufactured_20260930.py',
        'probe_annular_position_support_column_20260930.py',
        'validate_annular_flux_corrected_Euler_20260930.py',
        'seal_annular_position_support_stage_20260930.py']
    for name in scripts:
        path = root/'scripts'/name
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        files.append(str(path.relative_to(root)))
    for relative in files:
        verify(relative)
    started = datetime(2026, 9, 30, 11, 39, 50, tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
        if path.is_file() and path.stat().st_mtime >= started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode or probes != 12:
        raise RuntimeError(dict(mismatches=mismatches, protected_changes=changed,
            bytecode=[str(path) for path in bytecode], probes=probes))
    seal = dict(state='complete', sealed_at=datetime.now(timezone.utc).isoformat(),
        hashes=hashes, unique_files_rehashed=len(hashes), mismatches=mismatches,
        authorities=authorities, authority_checks=total_checks,
        csv_tables=csv_tables, csv_rows=csv_rows, scripts_compiled=scripts,
        all_four_fresh_Euler_checks_complete_and_passed=True,
        C0_manufactured_checks_passed=True, C0_actual_pointwise_probes=probes,
        C0_complete_integral=False, ready_for_boundary_complete_C0_integration=True,
        accepted_for_finite_history=False, valid_for_physics_claim=False,
        inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4,
        inherited_raw_C2_warnings=2, old_weak_flux_flags_retained=True,
        protected_workbench_changed_since_turn_start=len(changed), bytecode_cache_present=False,
        github_action=False, subagents_used=False,
        historical_status_alias_inherited_from_previous_seal=True)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(seal, indent=2)+'\n')
    print(json.dumps({key:value for key, value in seal.items() if key != 'hashes'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
