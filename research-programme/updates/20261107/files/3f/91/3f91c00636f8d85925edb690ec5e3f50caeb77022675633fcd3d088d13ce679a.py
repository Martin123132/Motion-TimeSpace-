from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
import csv
import ctypes
import hashlib
import json


def main():
    kernel=ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype=ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),4):
        raise OSError('Cannot set one core')
    root=Path(__file__).resolve().parents[1]
    directory=root/'source-intake/navier-stokes/20260914'
    target=directory/'annular-C0-stable-current-stage-integrity-20260930.json'
    table=directory/'annular-C0-stable-current-summary-20260930.csv'
    if target.exists() or table.exists():
        raise FileExistsError('Outputs already exist')
    hashes,mismatches={},[]

    def verify(relative,expected=None):
        if relative=='CURRENT_LOCAL_RESUME.md':
            return
        path=(root/relative).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Invalid source '+relative)
        key=str(path.relative_to(root))
        if key not in hashes:
            hashes[key]=hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and hashes[key]!=expected:
            mismatches.append(key)

    prior_path=directory/'annular-C0-integral-stage-integrity-20260930.json'
    prior=json.loads(prior_path.read_text())
    if prior['state']!='complete' or prior['mismatches']:
        raise RuntimeError('Prior seal failed')
    verify(str(prior_path.relative_to(root)))
    for relative,expected in prior['hashes'].items():
        verify(relative,expected)
    patterns=['annular-C0-transport-probe-*','annular-C0-precise-transport-probe-*',
        'annular-C0-transport-*-fine-*','annular-C0-stable-current-validation-*','annular-C0-stable-*-fine-*',
        'annular-C0-force-product-*-fine-*']
    statuses,ledger,rows={},{},[]
    for pattern in patterns:
        for path in sorted(directory.glob(pattern+'/status.json')):
            name=path.parent.name
            status=json.loads(path.read_text())
            if status['state'] not in ['complete','failed']:
                raise RuntimeError('Unsettled run '+name)
            if status['state']=='complete' and not all(row['passed'] for row in status['checks']):
                raise RuntimeError('Invalid complete run '+name)
            statuses[name]=status
            verify(str(path.relative_to(root)))
            for category in ['inputs','outputs']:
                for relative,expected in status[category].items():
                    verify(relative,expected)
            for item in path.parent.iterdir():
                if item.is_file():
                    verify(str(item.relative_to(root)))
            log=directory/(name+'.log')
            if log.exists():
                verify(str(log.relative_to(root)))
            ledger[name]=dict(state=status['state'],checks=len(status['checks']),error=status.get('error'),
                failed_checks=[row['name'] for row in status['checks'] if not row['passed']])
            for item in status.get('rule_outputs',[]):
                summary=item['summary']
                rows.append(dict(source=str(path.relative_to(root)),branch=status['branch'],order=summary['order'],
                    method='force-product' if status.get('independent_force_complete') else ('stable' if status.get('stable_integration_complete') else 'transport-decomposition'),
                    values=json.dumps(summary,sort_keys=True),valid_for_claim='false'))
    for name in ['annular-C0-precise-transport-probe-attempt01','annular-C0-stable-current-validation-attempt01']:
        if name not in statuses or statuses[name]['state']!='complete':
            raise RuntimeError('Required validation incomplete '+name)
    required=['annular-C0-stable-'+branch+'-fine-attempt01' for branch in ['reference','MTS']]
    if not all(name in statuses for name in required):
        raise RuntimeError('Missing matched stable attempts')
    compiled=[]
    for path in sorted((root/'scripts').glob('*C0*20260930*.py')):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
        verify(str(path.relative_to(root)))
        compiled.append(path.name)
    for name in ['DERIVATION-20260930-C0-transport-identity.md','DERIVATION-20260930-C0-stable-current.md',
        'DERIVATION-20260930-C0-independent-force-check.md','RESULTS-20260930-C0-transport-and-stable-current.md']:
        verify(name)
    started=datetime(2026,9,30,17,28,36,tzinfo=timezone.utc).timestamp()
    protected=root.parent/'formalization-workbench'
    changed=[str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    bytecode=list((root/'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches,protected_changes=changed,bytecode=[str(path) for path in bytecode]))
    with table.open('x',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=['source','branch','order','method','values','valid_for_claim'])
        writer.writeheader()
        writer.writerows(rows)
    with table.open(newline='',encoding='utf-8') as stream:
        replay=list(csv.DictReader(stream,strict=True))
    if len(replay)!=len(rows) or any(None in row or any(value is None for value in row.values()) for row in replay):
        raise RuntimeError('Malformed CSV')
    if any(row['valid_for_claim']!='false' for row in replay):
        raise RuntimeError('Unexpected claim flag')
    verify(str(table.relative_to(root)))
    seal=dict(state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),hashes=hashes,mismatches=mismatches,
        unique_files_rehashed=len(hashes),authorities=ledger,scripts_compiled=compiled,csv_rows=len(rows),
        stable_material_both_pass=all(statuses[name].get('material_pair_passed',False) for name in required),
        stable_eulerian_both_pass=all(statuses[name].get('euler_pair_passed',False) for name in required),
        stable_cross_method_both_pass=all(statuses[name].get('both_cross_comparisons_passed',False) for name in required),
        stable_current_cross_checks_pass=all(max(abs(value) for value in row['summary']['cross_difference'][1:])<=2e-17
            for name in required for row in statuses[name].get('rule_outputs',[])),
        stable_current_pairs_pass=all(max(abs(value) for value in statuses[name]['rule_outputs'][-1]['summary'][method][1:])<=2e-17
            for name in required for method in ['material_pair','euler_pair']),
        independent_force_both_pass=all(statuses.get('annular-C0-force-product-'+branch+'-fine-attempt01',{}).get('independent_force_complete',False)
            for branch in ['reference','MTS']),
        third_grid_completed=False,coupled_amplitudes_solved=False,valid_for_physics_claim=False,
        protected_workbench_changed_since_turn_start=len(changed),bytecode_cache_present=False,
        inherited_position_density_precision_warnings=4,inherited_mixed_time_precision_warnings=4,
        inherited_raw_C2_warnings=2,old_weak_flux_flags_retained=True,original_failing_diagnostics_retained=True,
        github_action=False,subagents_used=False,current_resume_excluded=True)
    with target.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(seal,indent=2)+'\n')
    print(json.dumps({key:value for key,value in seal.items() if key!='hashes'},indent=2),flush=True)


if __name__=='__main__':
    main()
