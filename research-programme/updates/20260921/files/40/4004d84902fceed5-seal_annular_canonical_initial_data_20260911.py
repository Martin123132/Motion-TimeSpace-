import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    final = intake / 'annular-canonical-initial-data-final-integrity.json'
    if final.exists():
        raise FileExistsError('Completed evidence is immutable.')
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'preserved_failed_attempts': [], 'historical_sources': [], 'valid_for_physics_claim': False, 'interval_certificate': False, 'inner_flux_parent_selected': False, 'full_parent_evolution_proved': False, 'frozen_scan_scope': 'mtime since 2026-09-11T00:17:49Z, not a pre-turn content baseline'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    previous = intake / 'annular-initial-jet-adjoint-final-integrity.json'
    own(previous)
    prior = json.loads(previous.read_text())
    for table in ['inputs', 'outputs']:
        for name, expected in prior[table].items():
            if digest(root / name) != expected:
                raise RuntimeError('Previously sealed evidence changed: ' + name)
            report['inputs'][name] = expected
    check('prior_seal_complete_and_unchanged', prior['state'] == 'complete')
    failures = ['probe01', 'probe02', 'probe03', 'common01', 'GRmatrix01']
    for attempt in failures:
        directory = intake / ('annular-canonical-boundary-' + attempt)
        state = json.loads((directory / 'status.json').read_text())
        check(attempt + '_failed_attempt_explicitly_preserved', state['state'] == 'failed' and bool(state.get('error')))
        report['preserved_failed_attempts'].append({'attempt': attempt, 'error': state['error'], 'completed_partial_samples': len(state['samples'])})
        for name, expected in state['inputs'].items():
            if digest(root / name) == expected:
                report['inputs'][name] = expected
                continue
            snapshot = directory / ('executed-' + Path(name).name)
            if not snapshot.is_file() or digest(snapshot) != expected:
                raise RuntimeError('Unexplained failed-attempt input change: ' + name)
            report['historical_sources'].append({'original_path': name, 'executed_snapshot': str(snapshot.relative_to(root)), 'sha256': expected})
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
        if attempt == 'probe01':
            symbolic_checks = ['exact_bulk_auxiliary_elimination_recovers_parent', 'exact_canonical_bulk_linear_in_N_and_Nr', 'exact_physical_boundary_flux_pullback', 'canonical_connection_lapse_derivative']
            for name in symbolic_checks:
                check(name + '_executed_symbolic_result_preserved', any(item['name'] == name and item['passed'] for item in state['checks']))
    for attempt in ['annular-canonical-initial-data-nodal01', 'annular-canonical-independent-control-attempt01']:
        directory = intake / attempt
        state = json.loads((directory / 'status.json').read_text())
        check(attempt + '_completed_validation_checks', state['state'] == 'complete' and all(item['passed'] for item in state['checks']))
        for table in ['inputs', 'outputs']:
            for name, expected in state.get(table, {}).items():
                if digest(root / name) != expected:
                    raise RuntimeError('New completed evidence changed: ' + name)
                report['inputs'][name] = expected
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
        for path in directory.glob('executed-*.py'):
            check(attempt + '_' + path.name + '_matches_current_source', digest(path) == digest(root / 'scripts' / path.name[len('executed-'):]))
        for path in directory.glob('*.npz'):
            with numerical.load(path) as archive:
                check(attempt + '_' + path.stem + '_finite_arrays', all(numerical.all(numerical.isfinite(archive[name])) for name in archive.files))
        if attempt.endswith('nodal01'):
            successful = [sample for sample in state['samples'] if sample['status'] == 'converged']
            failed = [sample for sample in state['samples'] if sample['status'] == 'not_converged']
            check('exactly_two_coarse_roots_and_four_failed_fine_attempts_reported', len(successful) == 2 and len(failed) == 4 and all('_N16_' in sample['label'] for sample in successful))
            check('failed_fine_iterates_not_promoted', all(sample['failure'] and not sample['parent_evolution_proved'] for sample in failed))
            report['case_outcomes'] = [{'label': sample['label'], 'status': sample['status'], 'constraint_max': sample['constraint_max'], 'scalar_velocity_change_max': sample['scalar_velocity_field_change_max']} for sample in state['samples']]
    names = ['annular_canonical_boundary_20260911.py', 'derive_annular_canonical_boundary_20260911.py', 'annular_canonical_initial_data_20260911.py', 'annular_canonical_nodal_data_20260911.py', 'derive_annular_canonical_initial_data_20260911.py', 'verify_annular_canonical_control_20260911.py', Path(__file__).name]
    for name in names:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('seven_new_scripts_compile_without_bytecode', True)
    note = root / 'DERIVATION-20260911-canonical-action-and-boundary-consistent-initial-data.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text()):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('cited_path_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    start = datetime.fromisoformat('2026-09-11T00:17:49+00:00').timestamp()
    touched = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    check('frozen_workbench_changed_count_zero_mtime', not touched, touched)
    check('no_python_cache_created', not (root / 'scripts/__pycache__').exists())
    snapshot = intake / 'annular-canonical-initial-data-resume-snapshot.md'
    if snapshot.exists():
        raise FileExistsError(snapshot)
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    final.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'input_hashes': len(report['inputs']), 'output_hashes': len(report['outputs']), 'frozen_changed_count': len(touched), 'successful_initializations': 2, 'failed_fine_initializations': 4}), flush=True)


if __name__ == '__main__':
    run()
