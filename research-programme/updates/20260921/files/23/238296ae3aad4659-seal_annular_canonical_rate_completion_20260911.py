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
    destination = intake / 'annular-canonical-rate-completion-final-integrity.json'
    if destination.exists():
        raise FileExistsError('Completed evidence is immutable.')
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'outcomes': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'full_MTS_initial_data_solved': False, 'interval_certificate': False, 'protected_scan_scope': 'mtime since 2026-09-11T21:01:06Z, not a pre-turn content snapshot'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def inherit(batch):
        for table in ['inputs', 'outputs']:
            for name, expected in batch[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Saved evidence changed: ' + name)
                report['inputs'][name] = expected

    prior_path = intake / 'annular-canonical-inverse-boundary-final-integrity.json'
    own(prior_path)
    prior = json.loads(prior_path.read_text())
    check('predecessor_complete', prior['state'] == 'complete')
    inherit(prior)
    for name in ['annular-canonical-rate-completion-attempt01', 'annular-canonical-rate-completion-control-attempt01']:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        check(name + '_complete_and_checks_pass', batch['state'] == 'complete' and all(row['passed'] for row in batch['checks']))
        check(name + '_no_physics_or_evolution_claim', batch['valid_for_physics_claim'] is False and batch['new_evolution'] is False)
        inherit(batch)
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
        for path in directory.glob('*.npz'):
            with numerical.load(path, allow_pickle=False) as saved:
                check(path.stem + '_all_arrays_finite', all(numerical.all(numerical.isfinite(saved[key])) for key in saved.files))
        for path in directory.glob('executed-*.py'):
            check(path.stem + '_executed_source_retained', digest(path) == digest(root / 'scripts' / path.name[len('executed-'):]))
        if name == 'annular-canonical-rate-completion-attempt01':
            check('both_branches_present', {sample['label'] for sample in batch['samples']} == {'N16_GR', 'N16_metric_Gram'})
            for sample in batch['samples']:
                label = sample['label']
                for phase, diagnostic in sample['phase_completion'].items():
                    check(label + '_' + phase + '_all_original_modes_retained', diagnostic['original_modes_removed'] == 0 and diagnostic['completed_phase_dimension'] == diagnostic['original_phase_dimension'] + diagnostic['position_rate_additions'] + diagnostic['momentum_rate_additions'])
                    check(label + '_' + phase + '_triangular_pairing_checked', diagnostic['pairing_block_identity_error'] < 1e-8 and diagnostic['pairing_condition'] < 10)
                result_arrays = {}
                for variant in ['original', 'completed', 'overintegrated']:
                    with numerical.load(directory / (label + '_' + variant + '.npz'), allow_pickle=False) as saved:
                        actual = float(abs(saved['constraint_rate']).max())
                        interior = float(abs(saved['constraint_rate'][1:-1]).max())
                        result_arrays[variant] = saved['constraint_rate'].copy()
                    check(label + '_' + variant + '_full_residual_replayed', actual == sample['outcomes'][variant]['constraint_rate_max'])
                    if variant != 'original':
                        check(label + '_' + variant + '_interior_initial_identity', interior < 1e-11)
                    if label == 'N16_GR' and variant != 'original':
                        check(label + '_' + variant + '_all_rows_close', actual < 1e-12)
                    if label != 'N16_GR' and variant != 'original':
                        check(label + '_' + variant + '_remaining_boundary_not_promoted', actual > 1e-8 and sample['enlarged_initial_data_solved'] is False)
                check(label + '_independent_overintegration_same_frame', abs(result_arrays['completed'] - result_arrays['overintegrated']).max() < 1e-10)
                report['outcomes'].append({'label': label, 'old_Cdot_max_natural_reactions': sample['outcomes']['original']['constraint_rate_max'], 'new_Cdot_max': sample['outcomes']['completed']['constraint_rate_max'], 'new_interior_Cdot_max': float(abs(result_arrays['completed'][1:-1]).max())})
        else:
            for sample in batch['samples']:
                branch = sample['branch']
                check(branch + '_three_unfitted_lapse_variations', len(sample['unfitted_lapse_checks']) == 3 and all(row['interior_max'] < 1e-11 for row in sample['unfitted_lapse_checks']))
                completed = sample['results']['completed']
                with numerical.load(directory / (branch + '_completed.npz'), allow_pickle=False) as saved:
                    boundary_error = float(abs(saved['constraint_rate'] - saved['boundary_prediction']).max())
                check(branch + '_independent_boundary_trace_identity', boundary_error == completed['full_boundary_identity_error'] and boundary_error < 1e-11)
                if branch == 'GR':
                    check('simpler_coordinate_only_GR_repair', sample['coordinate_only_dimensions'] == {'mass': 50, 'scalar': 50} and sample['results']['coordinate_only']['constraint_rate_max'] < 1e-12)
                    check('four_phase_action_variations', len(sample['results']['bulk_action_directional_errors']) == 4 and max(sample['results']['bulk_action_directional_errors']) < 1e-10)
                else:
                    check('two_MTS_trace_gaps_still_nonzero', all(abs(value) > 1e-8 for value in completed['mass_flux_trace_gaps']))
                report[branch + '_boundary_result'] = completed
    scripts = ['annular_canonical_reference_fields_20260911.py', 'annular_canonical_rate_completion_20260911.py', 'derive_annular_canonical_rate_completion_20260911.py', 'verify_annular_canonical_rate_completion_20260911.py', Path(__file__).name]
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('five_scripts_compile_without_bytecode', True)
    note = root / 'DERIVATION-20260911-canonical-rate-completion-and-two-boundary-flux-defects.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text()):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('citation_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    start = datetime.fromisoformat('2026-09-11T21:01:06+00:00').timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    check('protected_modified_count_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot = intake / 'annular-canonical-rate-completion-resume-snapshot.md'
    if snapshot.exists():
        raise FileExistsError(snapshot)
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'inputs': len(report['inputs']), 'outputs': len(report['outputs']), 'outcomes': report['outcomes'], 'protected_changed_count': len(changed)}), flush=True)


if __name__ == '__main__':
    run()
