import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    target = intake / 'annular-constraint-routhian-final-integrity.json'
    if target.exists():
        raise FileExistsError(target)
    inputs, outputs, owners = {}, {}, []
    for name in ['annular-constraint-routhian-derived', 'annular-constraint-tangent-verified-full-fixture', 'annular-constraint-work-split-derived']:
        path = intake / name / 'status.json'
        owner = json.loads(path.read_text())
        if owner['state'] != 'complete' or owner['passed'] != owner['total'] or not (path.parent / 'COMPLETE').exists():
            raise RuntimeError('Owner not complete: ' + name)
        owners.append({key: owner[key] for key in ['state', 'passed', 'total', 'completed_utc']} | {'owner': name})
        for table, inherited in [(inputs, owner['inputs']), (outputs, owner['outputs'])]:
            for relative, expected in inherited.items():
                actual = hashlib.sha256((root / relative).read_bytes()).hexdigest()
                if actual != expected or relative in table and table[relative] != actual:
                    raise RuntimeError('Changed source/output: ' + relative)
                table[relative] = actual
        for extra in [path, path.parent / 'COMPLETE', path.parent / 'executed-script.py']:
            inputs[str(extra.relative_to(root))] = hashlib.sha256(extra.read_bytes()).hexdigest()
    scripts = ['annular_constraint_routhian_20260909.py', 'derive_annular_constraint_routhian_20260909.py', 'verify_annular_constraint_tangent_20260909.py', 'derive_annular_constraint_work_split_20260909.py', 'finalize_annular_constraint_routhian_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        inputs[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    note = root / 'DERIVATION-20260909-constrained-initial-slice-solve-and-mass-flux-tangent.md'
    cited_paths = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json'))]
    missing = [value for value in cited_paths if root / value != target and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    inputs[str(note.relative_to(root))] = hashlib.sha256(note.read_bytes()).hexdigest()
    snapshot = intake / 'annular-constraint-routhian-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    outputs[str(snapshot.relative_to(root))] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 12, 39, 38, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched:
        raise RuntimeError('Protected workbench has newer writes; investigate ownership: ' + repr(touched[:10]))
    if (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Unexpected bytecode cache')
    report = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'owners': owners, 'final_check_count': sum(owner['total'] for owner in owners), 'compiled_scripts': len(scripts), 'unique_input_hashes': len(inputs), 'output_hashes': len(outputs), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited_paths, 'mutable_resume_pinned_as_immutable_snapshot_only': True, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T12:39:38Z, not a pre-turn full hash comparison; all tool writes scoped to post-checkpoint-work', 'no_bytecode_cache': True, 'valid_for_physics_claim': False, 'initial_constraints_solved': True, 'all_shift_rows_closed': False, 'live_evolution_run': False, 'historical_failure_preserved': 'annular-constraint-tangent-verified:120/132; full fixture vs four-key metadata check, executed source snapshot retained and verified'}
    with target.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2)
        handle.write('\n')
    if not all((root / value).is_file() for value in cited_paths):
        raise RuntimeError('Final cited path check failed')
    print(json.dumps({key: report[key] for key in ['state', 'completed_utc', 'final_check_count', 'compiled_scripts', 'unique_input_hashes', 'output_hashes', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()
