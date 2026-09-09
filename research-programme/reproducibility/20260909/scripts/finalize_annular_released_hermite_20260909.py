import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['analyze', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    analysis_path = intake / 'annular-released-Hermite-all-face-analysis.json'
    target = intake / 'annular-released-Hermite-final-integrity.json'
    inputs, outputs, owners = {}, {}, []
    for name in ['annular-released-Hermite-initial-derived', 'annular-released-Hermite-evolution-smoke']:
        path = intake / name / 'status.json'
        owner = json.loads(path.read_text())
        if owner['state'] != 'complete' or owner['passed'] != owner['total'] or not (path.parent / 'COMPLETE').exists():
            raise RuntimeError('Incomplete owner: ' + name)
        owners.append({'owner': name, **{key: owner[key] for key in ['state', 'passed', 'total', 'completed_utc']}})
        for table, inherited in [(inputs, owner['inputs']), (outputs, owner['outputs'])]:
            for relative, expected in inherited.items():
                actual = hashlib.sha256((root / relative).read_bytes()).hexdigest()
                if actual != expected or relative in table and table[relative] != actual:
                    raise RuntimeError('Changed source or output: ' + relative)
                table[relative] = actual
        for extra in [path, path.parent / 'COMPLETE', path.parent / 'executed-script.py']:
            inputs[str(extra.relative_to(root))] = hashlib.sha256(extra.read_bytes()).hexdigest()
    scripts = ['annular_released_hermite_action_20260909.py', 'derive_annular_released_hermite_20260909.py', 'evolve_annular_released_hermite_20260909.py', 'finalize_annular_released_hermite_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        inputs[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    if arguments.phase == 'analyze':
        destination = intake / 'annular-released-Hermite-all-face-controls'
        if analysis_path.exists() or destination.exists():
            raise FileExistsError('Analysis evidence already exists.')
        destination.mkdir()
        records = []
        for case_name in ['canonical', 'nonlinear_modulated']:
            case = json.loads((intake / 'annular-constraint-correction-initial' / (case_name + '.json')).read_text())
            cosmological = float(symbolic.sympify(case['parameters']['Lambda']))
            for intervals in [16, 32]:
                for branch in ['GR', 'metric_Gram']:
                    tag = case_name + '_N' + str(intervals) + '_' + branch
                    with numerical.load(intake / 'annular-released-Hermite-evolution-smoke' / (tag + '_steps32.npz')) as loaded:
                        trajectory = {name: loaded[name].copy() for name in loaded.files}
                    basis = MixedActionBasis(trajectory['radius'])
                    node_count, face_count = basis.radii.size, basis.faces.size
                    for index in [0, 16, 32]:
                        with numerical.load(intake / 'annular-released-Hermite-evolution-smoke' / (tag + '_Ward' + str(index) + '.npz')) as loaded:
                            ward = {name: loaded[name].copy() for name in loaded.files}
                        packed = trajectory['state'][index, 4 * node_count:]
                        mass, lapse = packed[:face_count], packed[face_count:face_count + node_count]
                        gamma = (basis.node_to_face @ lapse)**2 * (1 - 2 * mass / basis.faces - cosmological * basis.faces**2 / 3)
                        desired = -numerical.eye(face_count) / gamma[:, None]
                        values, slopes = numerical.zeros((node_count, face_count)), numerical.zeros((node_count, face_count))
                        slopes[0], slopes[-1] = desired[0], desired[-1]
                        fractions = (basis.faces[1:-1] - basis.radii[:-1]) / basis.spacing
                        if not (numerical.all(gamma > 0) and numerical.all(fractions > 0) and numerical.all(fractions < 1)):
                            raise RuntimeError('Right inverse assumptions fail.')
                        for cell, fraction in enumerate(fractions):
                            left = 3 * fraction**2 - 4 * fraction + 1
                            right = 3 * fraction**2 - 2 * fraction
                            values[cell + 1] = values[cell] + basis.spacing * (desired[cell + 1] - left * slopes[cell] - right * slopes[cell + 1]) / (6 * fraction * (1 - fraction))
                        inverse = numerical.concatenate([values, basis.spacing * slopes], axis=0)
                        parts = {name: sign * inverse.T @ ward[name] for name, sign in [('bulk_remainder', 1), ('Gram_coefficient_remainder', -1), ('Gram_link_remainder', -1), ('lifting_work', -1), ('scalar_endpoint_and_bulk_work', -1), ('mass_boundary_and_bulk_work', -1), ('lapse_constraint_derivative_work', -1)]}
                        residual = trajectory['shifts'][index]
                        reconstructed = sum(parts.values())
                        matrix_error = float(numerical.max(numerical.abs(ward['shift_generator'] @ inverse - numerical.eye(face_count))))
                        error = float(numerical.max(numerical.abs(reconstructed - residual)))
                        if matrix_error > 1e-12 or error > 2e-11:
                            raise RuntimeError('Full face reconstruction failed: ' + tag)
                        boundary_pair = parts['scalar_endpoint_and_bulk_work'] + parts['mass_boundary_and_bulk_work']
                        artifact = destination / (tag + '_sample' + str(index) + '.npz')
                        numerical.savez_compressed(artifact, right_inverse=inverse, full_shift_residual=residual, reconstructed_shift_residual=reconstructed, combined_scalar_mass_boundary_work=boundary_pair, **parts)
                        outputs[str(artifact.relative_to(root))] = hashlib.sha256(artifact.read_bytes()).hexdigest()
                        records.append({'case': case_name, 'intervals': intervals, 'branch': branch, 'time': float(trajectory['time'][index]), 'right_inverse_error': matrix_error, 'reconstruction_error': error, 'shift_residual_max': float(numerical.max(numerical.abs(residual))), 'contribution_max_norms': {name: float(numerical.max(numerical.abs(value))) for name, value in parts.items()}, 'combined_scalar_mass_boundary_work_max': float(numerical.max(numerical.abs(boundary_pair))), 'basis_dependent_split_not_a_unique_physical_attribution': True, 'all_faces_retained': True})
        analysis = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'controls': records, 'valid_for_physics_claim': False}
        with analysis_path.open('x') as handle:
            json.dump(analysis, handle, indent=2)
            handle.write('\n')
        print(json.dumps({'state': 'complete', 'all_face_controls': len(records), 'maximum_reconstruction_error': max(row['reconstruction_error'] for row in records)}))
        print(json.dumps([row for row in records if row['intervals'] == 32 and row['time'] == 0.01], indent=2))
        return
    if target.exists():
        raise FileExistsError('Final evidence already exists.')
    analysis = json.loads(analysis_path.read_text())
    for table, inherited in [(inputs, analysis['inputs']), (outputs, analysis['outputs'])]:
        for relative, expected in inherited.items():
            actual = hashlib.sha256((root / relative).read_bytes()).hexdigest()
            if actual != expected:
                raise RuntimeError('Changed analysis source or result: ' + relative)
            table[relative] = actual
    inputs[str(analysis_path.relative_to(root))] = hashlib.sha256(analysis_path.read_bytes()).hexdigest()
    note = root / 'DERIVATION-20260909-released-Hermite-slope-dynamics.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json'))]
    missing = [value for value in cited if root / value != target and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    inputs[str(note.relative_to(root))] = hashlib.sha256(note.read_bytes()).hexdigest()
    snapshot = intake / 'annular-released-Hermite-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    outputs[str(snapshot.relative_to(root))] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 15, 5, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected-file or cache check failed: ' + repr(touched))
    report = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'owners': owners, 'owner_check_count': sum(row['total'] for row in owners), 'compiled_scripts': len(scripts), 'unique_input_hashes': len(inputs), 'output_hashes': len(outputs), 'inputs': inputs, 'outputs': outputs, 'all_face_controls': len(analysis['controls']), 'maximum_full_residual_reconstruction_error': max(row['reconstruction_error'] for row in analysis['controls']), 'cited_local_paths_checked': cited, 'mutable_resume_pinned_as_snapshot_only': True, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T15:05:00Z, not a pre-turn full hash comparison; all tool writes scoped to post-checkpoint-work', 'no_bytecode_cache': True, 'slope_equation_derived_and_evolved': True, 'full_coupled_DAE_solved': False, 'all_shift_rows_closed': False, 'long_time_stability_claim': False, 'valid_for_physics_claim': False}
    with target.open('x') as handle:
        json.dump(report, handle, indent=2)
        handle.write('\n')
    print(json.dumps({key: report[key] for key in ['state', 'completed_utc', 'owner_check_count', 'all_face_controls', 'compiled_scripts', 'unique_input_hashes', 'output_hashes', 'protected_workbench_files_written_since_turn_start']}))


if __name__ == '__main__':
    run()
