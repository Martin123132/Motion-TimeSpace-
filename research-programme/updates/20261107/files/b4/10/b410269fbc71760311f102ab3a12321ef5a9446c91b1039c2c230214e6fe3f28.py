from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime,timezone
import csv
import ctypes
import hashlib
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),4):
        raise OSError('Cannot pin one CPU')
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-C0-higher-grid-and-position-stage-integrity-20260930.json'
    table = directory/'annular-C0-higher-grid-and-position-summary-20260930.csv'
    if target.exists() or table.exists():
        raise FileExistsError('Checkpoint outputs already exist')
    hashes,mismatches,records,rows = {},[],{},[]

    def verify(relative,expected=None):
        path = (root/relative).resolve()
        if path==root/'CURRENT_LOCAL_RESUME.md':
            return
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Invalid source '+relative)
        key = str(path.relative_to(root))
        if key not in hashes:
            hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and hashes[key]!=expected:
            mismatches.append(key)

    prior_path = directory/'annular-C0-stable-current-stage-integrity-20260930.json'
    prior = json.loads(prior_path.read_text())
    if prior['state']!='complete' or prior['mismatches']:
        raise RuntimeError('Prior integrity incomplete')
    verify(str(prior_path.relative_to(root)))
    for relative,expected in prior['hashes'].items():
        verify(relative,expected)
    names = ['annular-C0-higher-reference-third-attempt01','annular-C0-higher-MTS-third-attempt01',
        'annular-C0-wave-resume-validation-attempt01','annular-position-enabled-algebra-attempt01',
        'annular-position-enabled-fine-attempt01','annular-position-enabled-fine-attempt02']
    pending = {}
    for name in names:
        path = directory/name/'status.json'
        status = json.loads(path.read_text())
        if status['state'] not in ['complete','failed']:
            raise RuntimeError('Unsettled run '+name)
        if status['state']=='complete' and not all(row['passed'] for row in status['checks']):
            raise RuntimeError('Invalid complete run '+name)
        verify(str(path.relative_to(root)))
        for category in ['inputs','outputs']:
            for relative,expected in status[category].items():
                verify(relative,expected)
        for item in path.parent.iterdir():
            if item.is_file():
                verify(str(item.relative_to(root)))
        log = directory/(name+'.log')
        if log.exists():
            verify(str(log.relative_to(root)))
        records[name] = dict(state=status['state'],checks=len(status['checks']),error=status.get('error'),
            failed_checks=[row['name'] for row in status['checks'] if not row['passed']])
        if name.startswith('annular-C0-higher-'):
            if status['state']!='failed' or status.get('error')!="RuntimeError('Safe higher-grid boundary')" or records[name]['failed_checks']:
                raise RuntimeError('Unexpected higher-grid stop '+name)
            if len(status['rule_outputs'])!=1 or status['rule_outputs'][0]['summary']['order']!=24:
                raise RuntimeError('Unexpected completed rules '+name)
            if not status['rule_outputs'][0]['summary']['independent_passed']:
                raise RuntimeError('Low-rule independent force failed '+name)
            partial = path.parent/'partial-wave-32.npz'
            with np.load(partial,allow_pickle=False) as saved:
                if bool(saved['complete']) or int(saved['order'])!=32 or str(saved['phase'])!='volume':
                    raise RuntimeError('Invalid saved volume '+name)
                pending[name] = dict(path=str(partial.relative_to(root)),next_index=int(saved['next_index']),
                    phase=str(saved['phase']),complete=False,total_radial_nodes_regenerated_on_resume=True)
            rows.append(dict(source=str(path.relative_to(root)),kind='third_order24_only',branch=status['branch'],
                result=json.dumps(status['rule_outputs'][0]['summary'],sort_keys=True),valid_for_claim='false'))
        elif name=='annular-position-enabled-fine-attempt02':
            if status['state']!='complete' or len(status['cases'])!=2:
                raise RuntimeError('Fine diagnostic incomplete')
            for case in status['cases']:
                for variant in case['variants']:
                    rows.append(dict(source=variant['path'],kind='fine_position_diagnostic',branch=case['branch'],
                        result=json.dumps(variant['summary'],sort_keys=True),valid_for_claim='false'))
    for name in ['annular-C0-wave-resume-validation-attempt01','annular-position-enabled-algebra-attempt01']:
        if records[name]['state']!='complete':
            raise RuntimeError('New method validation incomplete')
    compiled = []
    for name in ['integrate_annular_C0_higher_grid_20260930.py','annular_C0_wave_resume_20260930.py',
            'validate_annular_C0_wave_resume_20260930.py','continue_annular_C0_higher_grid_20260930.py',
            'annular_position_enabled_compatibility_20260930.py','validate_annular_position_enabled_compatibility_20260930.py',
            'assemble_annular_position_enabled_fine_20260930.py','assemble_annular_position_enabled_fine_v2_20260930.py',
            'seal_annular_C0_higher_position_20260930.py']:
        path = root/'scripts'/name
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
        verify(str(path.relative_to(root)))
        compiled.append(name)
    for name in ['DERIVATION-20260930-C0-higher-grid-completion.md','DERIVATION-20260930-C0-force-eliminated-compatibility.md',
            'RESULTS-20260930-higher-grid-C0-and-position-reduction.md']:
        verify(name)
    started = datetime(2026,9,30,20,13,36,tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches,protected_changes=changed,bytecode=[str(path) for path in bytecode]))
    with table.open('x',newline='',encoding='utf-8') as stream:
        writer = csv.DictWriter(stream,fieldnames=['source','kind','branch','result','valid_for_claim'])
        writer.writeheader()
        writer.writerows(rows)
    with table.open(newline='',encoding='utf-8') as stream:
        parsed = list(csv.DictReader(stream,strict=True))
    if len(parsed)!=len(rows) or any(None in row or any(value is None for value in row.values()) for row in parsed):
        raise RuntimeError('Malformed summary CSV')
    for row in parsed:
        json.loads(row['result'])
        if row['valid_for_claim']!='false':
            raise RuntimeError('Unexpected claim flag')
    verify(str(table.relative_to(root)))
    seal = dict(state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),hashes=hashes,mismatches=mismatches,
        unique_files_rehashed=len(hashes),authorities=records,scripts_compiled=compiled,csv_rows=len(rows),
        both_third_low_rule_integrals_complete=True,both_third_low_independent_force_checks_pass=True,
        both_third_rule_pairs_complete=False,pending=pending,compensated_resume_manufactured_checks=10,
        position_elimination_manufactured_checks=12,fine_actual_position_diagnostics_complete=True,
        higher_grid_actual_amplitudes_evaluated=False,finite_history_established=False,valid_for_physics_claim=False,
        original_failures_retained=True,inherited_position_density_warnings=4,inherited_mixed_time_warnings=4,
        inherited_raw_C2_warnings=2,old_weak_flux_flags_retained=True,protected_workbench_changed_since_turn_start=len(changed),
        bytecode_cache_present=False,github_action=False,subagents_used=False,current_resume_excluded=True)
    with target.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(seal,indent=2)+'\n')
    print(json.dumps({key:value for key,value in seal.items() if key!='hashes'},indent=2),flush=True)


if __name__=='__main__':
    main()
