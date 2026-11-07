from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
import ctypes
import hashlib
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 4):
        raise OSError('Cannot pin one CPU')
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-integrated-baseline-progress-integrity-20261001.json'
    if target.exists():
        raise FileExistsError(target)
    hashes, mismatches, records, partials = {}, [], {}, {}

    def verify(relative, expected=None):
        path = (root/relative).resolve()
        if path==root/'CURRENT_LOCAL_RESUME.md':
            return
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Invalid progress source '+relative)
        key = str(path.relative_to(root))
        if key not in hashes:
            hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and hashes[key]!=expected:
            mismatches.append(key)

    prior_path = directory/'annular-repaired-compatibility-stage-integrity-20261001.json'
    prior = json.loads(prior_path.read_text())
    if prior['state']!='complete' or prior['mismatches']:
        raise RuntimeError('Last complete stage invalid')
    verify(str(prior_path.relative_to(root)))
    for relative, expected in prior['hashes'].items():
        verify(relative, expected)
    for short in ['reference', 'MTS']:
        previous_index = 0
        for attempt in ['01', '02']:
            name = 'annular-coefficient-baseline-'+short+'-third-attempt'+attempt
            path = directory/name/'status.json'
            report = json.loads(path.read_text())
            if report['state']!='failed' or report.get('error')!="RuntimeError('Safe coefficient-baseline boundary')" or any(not row['passed'] for row in report['checks']):
                raise RuntimeError('Run is not a safely stopped partial '+name)
            if len(report['rule_outputs'])!=1 or report['rule_outputs'][0]['summary']['order']!=24:
                raise RuntimeError('Expected complete lower rule only')
            verify(str(path.relative_to(root)))
            for category in ['inputs', 'outputs']:
                for relative, expected in report[category].items():
                    verify(relative, expected)
            for item in path.parent.iterdir():
                if item.is_file():
                    verify(str(item.relative_to(root)))
            log = directory/(name+'.log')
            if log.exists():
                verify(str(log.relative_to(root)))
            partial_path = path.parent/'partial-baseline-32.npz'
            with np.load(partial_path, allow_pickle=False) as saved:
                next_index, count = int(saved['next_index']), int(saved['total_nodes'])
                if bool(saved['complete']) or int(saved['order'])!=32 or next_index%16 or not previous_index<=next_index<count:
                    raise RuntimeError('Invalid saved integration boundary')
                for key in ['total', 'correction', 'absolute']:
                    values = saved[key]
                    if values.shape!=(3, 4) or not np.isfinite(values).all():
                        raise RuntimeError('Invalid saved compensated sum')
                if np.any(saved['absolute']<0) or saved['total'][2, 0]!=0 or saved['correction'][2, 0]!=0:
                    raise RuntimeError('Broken force-hold partial invariant')
                partials[short] = dict(authority=name, next_index=next_index, total_nodes=count,
                    remaining_nodes=count-next_index, node_hash=str(saved['node_hash']),
                    archive=str(partial_path.relative_to(root)), lower_rule=report['rule_outputs'][0])
            previous_index = next_index
            records[name] = dict(state='safely_stopped', checks=len(report['checks']), error=report['error'])
    if partials['reference']['node_hash']!=partials['MTS']['node_hash']:
        raise RuntimeError('Different remaining rule hashes')
    compiled = []
    for name in ['integrate_annular_coefficient_baseline_20261001.py', 'assemble_annular_integrated_baseline_20261001.py',
            'seal_annular_integrated_baseline_20261001.py', 'seal_annular_baseline_progress_20261001.py']:
        path = root/'scripts'/name
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        verify(str(path.relative_to(root)))
        compiled.append(name)
    for name in ['DERIVATION-20261001-integrated-baseline-current-contract.md', 'RESULTS-20261001-integrated-baseline-progress.md']:
        verify(name)
    started = datetime(2026, 10, 1, 13, 32, 29, tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches, protected_changes=changed, bytecode=[str(path) for path in bytecode]))
    seal = dict(state='saved_partial', integrity_verified=True, sealed_at=datetime.now(timezone.utc).isoformat(),
        hashes=hashes, mismatches=mismatches, unique_files_rehashed=len(hashes), authorities=records,
        pending=partials, scripts_compiled=compiled, lower_rules_complete=True, higher_rules_complete=False,
        coupled_equation_daughter_executed=False, complete_stage_sealer_executed=False,
        last_complete_scientific_authority=str(prior_path.relative_to(root)), original_failures_retained=True,
        numerical_checks_failed=False, stops_are_wall_time_guards=True, force_and_nonwave_inputs_held=True,
        protected_workbench_changed_since_turn_start=len(changed), bytecode_cache_present=False,
        current_resume_excluded=True, github_action=False, subagents_used=False, valid_for_physics_claim=False)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(seal, indent=2)+'\n')
    print(json.dumps({key:value for key, value in seal.items() if key!='hashes'}, indent=2), flush=True)


if __name__=='__main__':
    main()
