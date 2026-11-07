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
    target = directory/'annular-higher-C0-and-resolved-channel-stage-integrity-20261001.json'
    table = directory/'annular-higher-C0-and-resolved-channel-summary-20261001.csv'
    if target.exists() or table.exists():
        raise FileExistsError('Stage already written')
    hashes,mismatches,records,rows,pending = {},[],{},{},{}

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

    prior_path = directory/'annular-C0-higher-grid-and-position-stage-integrity-20260930.json'
    prior = json.loads(prior_path.read_text())
    if prior['state']!='complete' or prior['mismatches']:
        raise RuntimeError('Prior stage incomplete')
    verify(str(prior_path.relative_to(root)))
    for relative,expected in prior['hashes'].items():
        verify(relative,expected)
    names = ['annular-C0-higher-reference-third-attempt02','annular-C0-higher-MTS-third-attempt02',
        'annular-resolved-channels-reference-third-attempt01','annular-resolved-channels-MTS-third-attempt01']
    latest_channels = {}
    for short in ['reference','MTS']:
        latest = 'annular-resolved-channels-'+short+'-third-attempt01'
        daughter = 'annular-resolved-channels-'+short+'-third-attempt02'
        if (directory/daughter/'status.json').exists():
            names.append(daughter)
            latest = daughter
        latest_channels[short] = latest
    assembly_name = 'annular-position-enabled-third-attempt01'
    if (directory/assembly_name/'status.json').exists():
        names.append(assembly_name)
    for name in names:
        path = directory/name/'status.json'
        status = json.loads(path.read_text())
        if status['state'] not in ['complete','failed']:
            raise RuntimeError('Unsettled run '+name)
        failed = [row['name'] for row in status['checks'] if not row['passed']]
        if status['state']=='complete' and failed:
            raise RuntimeError('Invalid completed run '+name)
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
        records[name] = dict(state=status['state'],checks=len(status['checks']),error=status.get('error'),failed_checks=failed)
        rows[name] = []
        for record in status.get('rule_outputs',[]):
            rows[name].append(dict(source=str(path.relative_to(root)),kind='rule',branch=status['branch'],
                result=json.dumps(record['summary'],sort_keys=True),valid_for_claim='false'))
        if name.startswith('annular-C0-higher-'):
            if status['state']!='complete' or not status['complete_integral_constructed']:
                raise RuntimeError('Higher C0 not complete '+name)
            records[name].update(pair_passed=status['all_requested_pairs_passed'],
                independent_both_passed=status['independent_force_both_orders_passed'],
                independent_pair_passed=status['independent_force_pair_passed'])
        if name.startswith('annular-resolved-channels-'):
            records[name].update(resolved_C2_complete=status.get('resolved_C2_complete',False),
                reaction_sensitivity_integrated=status.get('reaction_sensitivity_integrated',False))
            if status['state']=='failed' and status.get('error')=="RuntimeError('Safe resolved-channel boundary')":
                pending[name] = []
                if failed:
                    raise RuntimeError('Failed scientific check at safe stop')
                completed_orders = [row['summary']['order'] for row in status['rule_outputs']]
                for partial in path.parent.glob('partial-channels-*.npz'):
                    with np.load(partial,allow_pickle=False) as saved:
                        order = int(saved['order'])
                        if order in completed_orders:
                            continue
                        if bool(saved['complete']) or any(saved[key].shape!=(2,2,4) or not np.isfinite(saved[key]).all()
                                for key in ['total','correction','absolute']):
                            raise RuntimeError('Invalid saved channel partial')
                        index,count = int(saved['next_index']),int(saved['total_nodes'])
                        if not 0<=index<=count or index%16:
                            raise RuntimeError('Invalid saved channel index')
                        pending[name].append(dict(path=str(partial.relative_to(root)),order=order,next_index=index,total_nodes=count,complete=False))
        for case in status.get('cases',[]):
            for variant in case.get('variants',[]):
                rows[name].append(dict(source=variant['path'],kind='third_position_diagnostic',branch=case['branch'],
                    result=json.dumps(variant['summary'],sort_keys=True),valid_for_claim='false'))
        for source in path.parent.glob('*.csv'):
            with source.open(newline='',encoding='utf-8') as stream:
                parsed = list(csv.DictReader(stream,strict=True))
            if any(None in row or any(value is None for value in row.values()) for row in parsed):
                raise RuntimeError('Malformed CSV '+str(source))
    compiled = []
    for name in ['annular_resolved_acceleration_channels_20261001.py','integrate_annular_resolved_channels_20261001.py',
            'assemble_annular_position_enabled_third_20261001.py','seal_annular_resolved_channels_20261001.py']:
        path = root/'scripts'/name
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
        verify(str(path.relative_to(root)))
        compiled.append(name)
    for name in ['DERIVATION-20261001-resolved-acceleration-current.md','RESULTS-20261001-higher-C0-and-resolved-channels.md']:
        verify(name)
    started = datetime(2026,10,1,0,14,18,tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches,protected_changes=changed,bytecode=[str(path) for path in bytecode]))
    flat = [row for case in rows.values() for row in case]
    with table.open('x',newline='',encoding='utf-8') as stream:
        writer = csv.DictWriter(stream,fieldnames=['source','kind','branch','result','valid_for_claim'])
        writer.writeheader()
        writer.writerows(flat)
    with table.open(newline='',encoding='utf-8') as stream:
        parsed = list(csv.DictReader(stream,strict=True))
    if len(parsed)!=len(flat) or any(None in row or any(value is None for value in row.values()) for row in parsed):
        raise RuntimeError('Malformed summary CSV')
    for row in parsed:
        json.loads(row['result'])
        if row['valid_for_claim']!='false':
            raise RuntimeError('Unexpected claim flag')
    verify(str(table.relative_to(root)))
    seal = dict(state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),hashes=hashes,mismatches=mismatches,
        unique_files_rehashed=len(hashes),authorities=records,scripts_compiled=compiled,csv_rows=len(flat),
        historical_safe_partials=pending,pending={name:values for name,values in pending.items() if name in latest_channels.values()},
        resolved_channel_latest_authorities=latest_channels,
        both_third_C0_pairs_complete=True,both_resolved_channel_pairs_complete=all(records[name]['state']=='complete'
            for name in latest_channels.values()),
        third_position_diagnostics_executed=assembly_name in records,
        third_position_diagnostics_complete=records.get(assembly_name,{}).get('state')=='complete',
        original_failures_retained=True,inherited_flags_retained=True,finite_history_established=False,
        spatial_convergence_established=False,valid_for_physics_claim=False,
        protected_workbench_changed_since_turn_start=len(changed),bytecode_cache_present=False,
        github_action=False,subagents_used=False,current_resume_excluded=True)
    with target.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(seal,indent=2)+'\n')
    print(json.dumps({key:value for key,value in seal.items() if key!='hashes'},indent=2),flush=True)


if __name__=='__main__':
    main()
