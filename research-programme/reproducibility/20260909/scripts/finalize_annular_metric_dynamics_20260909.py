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
    target = intake / 'annular-metric-dynamics-final-integrity.json'
    snapshot = intake / 'annular-metric-dynamics-resume-snapshot.md'
    if target.exists() or snapshot.exists():
        raise FileExistsError('Final evidence already exists.')
    inputs, outputs, owners = {}, {}, []
    for name in ['annular-metric-quadratic-derived', 'annular-metric-evolution-smoke', 'annular-metric-evolution-independent-controls']:
        path = intake / name / 'status.json'
        owner = json.loads(path.read_text())
        if owner['state'] != 'complete' or owner['passed'] != owner['total'] or not (path.parent / 'COMPLETE').exists():
            raise RuntimeError('Incomplete owner: ' + name)
        owners.append({'owner': name, **{key: owner[key] for key in ['state', 'passed', 'total', 'completed_utc']}})
        for table, inherited in [(inputs, owner['inputs']), (outputs, owner['outputs'])]:
            for relative, expected in inherited.items():
                actual = hashlib.sha256((root / relative).read_bytes()).hexdigest()
                if actual != expected or relative in table and table[relative] != actual:
                    raise RuntimeError('Changed source/output: ' + relative)
                table[relative] = actual
        for extra in [path, path.parent / 'COMPLETE', path.parent / 'executed-script.py']:
            inputs[str(extra.relative_to(root))] = hashlib.sha256(extra.read_bytes()).hexdigest()
    script_names = ['annular_metric_link_quadratic_20260909.py', 'derive_annular_metric_dynamics_20260909.py', 'verify_annular_metric_evolution_20260909.py', 'finalize_annular_metric_dynamics_20260909.py']
    for name in script_names:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        inputs[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    note = root / 'DERIVATION-20260909-metric-link-quadratic-action-and-short-evolution.md'
    cited_paths = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json'))]
    missing = [value for value in cited_paths if root / value != target and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    inputs[str(note.relative_to(root))] = hashlib.sha256(note.read_bytes()).hexdigest()
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    outputs[str(snapshot.relative_to(root))] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 14, 1, 36, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected-file or bytecode-cache check needs attention: ' + repr(touched))
    quadratic = json.loads((intake / 'annular-metric-quadratic-derived/status.json').read_text())
    evolution = json.loads((intake / 'annular-metric-evolution-smoke/status.json').read_text())
    verification = json.loads((intake / 'annular-metric-evolution-independent-controls/status.json').read_text())
    report = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'owners': owners, 'owner_check_count': sum(owner['total'] for owner in owners), 'compiled_scripts': len(script_names), 'unique_input_hashes': len(inputs), 'output_hashes': len(outputs), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited_paths, 'mutable_resume_pinned_as_snapshot_only': True, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T14:01:36Z, not a pre-turn full hash comparison; all tool writes scoped to post-checkpoint-work', 'no_bytecode_cache': True, 'valid_for_physics_claim': False, 'metric_link_second_variation_validated': True, 'secondary_Dirac_closure_proven': False, 'all_shift_rows_closed': False, 'short_constraint_tangent_evolution_run': True, 'full_coupled_DAE_solved': False, 'long_time_stability_claim': False, 'quadratic_patches': len(quadratic['samples']), 'short_trajectories': len(evolution['samples']), 'evolving_full_Ward_controls': len(verification['samples']), 'maximum_evolving_Ward_error': max(row['Ward_error'] for row in verification['samples']), 'maximum_all_face_reconstruction_error': max(row['full_residual_reconstruction_error'] for row in verification['samples']), 'comparisons': evolution['comparisons']}
    with target.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2)
        handle.write('\n')
    if not all((root / value).is_file() for value in cited_paths):
        raise RuntimeError('Final cited path check failed.')
    print(json.dumps({key: report[key] for key in ['state', 'completed_utc', 'owner_check_count', 'compiled_scripts', 'unique_input_hashes', 'output_hashes', 'protected_workbench_files_written_since_turn_start', 'short_trajectories', 'maximum_evolving_Ward_error', 'maximum_all_face_reconstruction_error']}), flush=True)


if __name__ == '__main__':
    run()
