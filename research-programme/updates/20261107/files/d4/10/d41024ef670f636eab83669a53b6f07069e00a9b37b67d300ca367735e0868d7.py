from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime,timezone
import csv
import ctypes
import hashlib
import json


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),4):
        raise OSError('Cannot pin one core')
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-compensated-polynomial-stage-integrity-20261001.json'
    if target.exists():
        raise FileExistsError(target)
    hashes,mismatches,records = {},[],{}

    def verify(relative,expected=None):
        source = (root/relative).resolve()
        if source==root/'CURRENT_LOCAL_RESUME.md':
            return
        if not source.is_relative_to(root) or not source.is_file():
            raise RuntimeError('Invalid stage source '+relative)
        key = str(source.relative_to(root))
        if key not in hashes:
            hashes[key] = hashlib.sha256(source.read_bytes()).hexdigest()
        if expected is not None and hashes[key]!=expected:
            mismatches.append(key)

    prior_path = directory/'annular-higher-C0-and-resolved-channel-stage-integrity-20261001.json'
    prior = json.loads(prior_path.read_text())
    if prior['state']!='complete' or prior['mismatches']:
        raise RuntimeError('Prior checkpoint incomplete')
    verify(str(prior_path.relative_to(root)))
    for relative,expected in prior['hashes'].items():
        verify(relative,expected)
    names = ['annular-compensated-polynomial-'+short+'-third-attempt'+attempt
        for short in ['reference','MTS'] for attempt in ['01','02']]
    names += ['annular-compensated-C2-'+short+'-third-attempt01' for short in ['reference','MTS']]
    names += ['annular-compensated-C2-attribution-attempt01']
    names += ['annular-compensated-material-'+short+'-third-attempt01' for short in ['reference','MTS']]
    names += ['annular-compensated-material-'+short+'-third-attempt02' for short in ['reference','MTS']]
    csv_counts = {}
    for name in names:
        path = directory/name/'status.json'
        status = json.loads(path.read_text())
        failed = [row['name'] for row in status['checks'] if not row['passed']]
        loader_failure = name.startswith('annular-compensated-polynomial-') and name.endswith('attempt01')
        replay_failure = name.startswith('annular-compensated-material-') and name.endswith('attempt01')
        if loader_failure:
            if status['state']!='failed' or 'has no attribute' not in status.get('error','') or failed:
                raise RuntimeError('Unexpected retained loader failure')
        elif replay_failure:
            if status['state']!='failed' or failed!=['original_material_replay-48']:
                raise RuntimeError('Unexpected retained material replay failure')
        elif status['state']!='complete' or failed:
            raise RuntimeError('New calculation incomplete '+name)
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
        records[name] = dict(state=status['state'],checks=len(status['checks']),failed_checks=failed,error=status.get('error'))
        for table in path.parent.glob('*.csv'):
            with table.open(newline='',encoding='utf-8') as stream:
                rows = list(csv.DictReader(stream,strict=True))
            if any(None in row or any(value is None for value in row.values()) for row in rows):
                raise RuntimeError('Malformed CSV '+str(table))
            if any(row.get('valid_for_claim','False').lower()!='false' for row in rows):
                raise RuntimeError('Unexpected claim row')
            csv_counts[str(table.relative_to(root))] = len(rows)
    compiled = []
    for name in ['annular_compensated_acceleration_polynomial_20261001.py','probe_annular_compensated_polynomial_20261001.py',
            'annular_compensated_acceleration_polynomial_v2_20261001.py','probe_annular_compensated_polynomial_v2_20261001.py',
            'integrate_annular_compensated_C2_20261001.py','attribute_annular_compensated_C2_20261001.py',
            'replay_annular_material_C2_20261001.py',
            'replay_annular_material_C2_v2_20261001.py',
            'seal_annular_compensated_polynomial_20261001.py']:
        path = root/'scripts'/name
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
        verify(str(path.relative_to(root)))
        compiled.append(name)
    for name in ['DERIVATION-20261001-compensated-acceleration-polynomial.md','DERIVATION-20261001-compensated-source-binding.md',
            'DERIVATION-20261001-material-rule-C2-replay.md',
            'DERIVATION-20261001-material-replay-arithmetic-binding.md',
            'RESULTS-20261001-compensated-acceleration-ablation.md']:
        verify(name)
    started = datetime(2026,10,1,10,24,51,tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches,protected_changes=changed,bytecode=[str(path) for path in bytecode]))
    seal = dict(state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),hashes=hashes,mismatches=mismatches,
        unique_files_rehashed=len(hashes),authorities=records,scripts_compiled=compiled,csv_rows=csv_counts,pending={},
        exact_compensated_polynomial_derived=True,both_actual_probe_sets_complete=True,both_same_node_ablation_pairs_complete=True,
        both_historical_material_replays_complete=True,
        gravity_attribution_complete=True,physical_uncertainty_shrunk=False,parent_coefficient_precision_proven=False,
        candidate_refit_performed=False,original_failures_retained=True,inherited_flags_retained=True,
        spatial_convergence_established=False,finite_history_established=False,valid_for_physics_claim=False,
        protected_workbench_changed_since_turn_start=len(changed),bytecode_cache_present=False,
        github_action=False,subagents_used=False,current_resume_excluded=True)
    with target.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(seal,indent=2)+'\n')
    print(json.dumps({key:value for key,value in seal.items() if key!='hashes'},indent=2),flush=True)


if __name__=='__main__':
    main()
