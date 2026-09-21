import hashlib
import json
import re
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-canonical-inverse-boundary-final-integrity.json'
    if destination.exists():
        raise FileExistsError('Completed evidence is immutable.')
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'outcomes': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'classical_MTS_boundary_certified': False, 'finite_GR_root_claimed': False, 'formula_GR_reference_positive_chart': True, 'protected_scan_scope': 'mtime since 2026-09-11T19:57:26Z, not a pre-turn content snapshot'}

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
                    raise RuntimeError('Previously saved evidence changed: ' + name)
                report['inputs'][name] = expected

    prior_path = intake / 'annular-canonical-mass-reduction-final-integrity.json'
    own(prior_path)
    prior = json.loads(prior_path.read_text())
    check('prior_seal_complete', prior['state'] == 'complete')
    inherit(prior)
    names = ['annular-canonical-inverse-boundary-attempt01', 'annular-canonical-gr-boundary-reference-attempt01', 'annular-canonical-inverse-boundary-control-attempt01']
    for name in names:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        check(name + '_complete_all_checks_pass', batch['state'] == 'complete' and all(row['passed'] for row in batch['checks']))
        check(name + '_no_physics_or_evolution_claim', batch['valid_for_physics_claim'] is False and batch['new_evolution'] is False)
        inherit(batch)
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
        for path in directory.glob('*.npz'):
            with numerical.load(path, allow_pickle=False) as saved:
                check(path.stem + '_finite_arrays', all(numerical.all(numerical.isfinite(saved[key])) for key in saved.files))
        for path in directory.glob('executed-*.py'):
            check(path.stem + '_executed_source_unchanged', digest(path) == digest(root / 'scripts' / path.name[len('executed-'):]))
        if name == 'annular-canonical-inverse-boundary-attempt01':
            check('fair_four_case_coarse_matrix', len(batch['samples']) == 4 and {(row['branch'], row['normalize_clock']) for row in batch['samples']} == {(branch, normalized) for branch in ['GR', 'metric_Gram'] for normalized in [False, True]})
            check('no_failed_coarse_refinement', all(row['mesh'] == 16 for row in batch['samples']) and 'Not run' in batch['N32_policy'])
            for sample in batch['samples']:
                with numerical.load(directory / (sample['label'] + '.npz'), allow_pickle=False) as saved:
                    absolute = float(abs(saved['full_residual']).max())
                    scaled = float(abs(saved['full_residual'] / saved['row_scales']).max())
                check(sample['label'] + '_residual_metrics_replayed', absolute == sample['absolute_residual'] and scaled == sample['scaled_residual'])
                if sample['status'] == 'converged':
                    check(sample['label'] + '_full_root_not_just_trace', absolute < 1e-9 and scaled < 1e-10 and sample['failure'] is None)
                else:
                    check(sample['label'] + '_failure_retained', bool(sample['failure']) and sample['status'] == 'not_converged')
                check(sample['label'] + '_reaction_gap_not_hidden', sample['classical_boundary_certified'] is False and max(abs(value) for value in sample['diagnostics']['spatial_boundary_reaction_gaps']) > 1e-6)
                report['outcomes'].append({'label': sample['label'], 'status': sample['status'], 'absolute_residual': absolute, 'local_EP_gap': sample['diagnostics']['local_EP_trace_gap']})
        if name == 'annular-canonical-gr-boundary-reference-attempt01':
            result = batch['result']
            check('GR_reference_distinct_from_finite_solver', batch['finite_initial_system_solved'] is False and result['constraint_max'] < 1e-12 and result['constraint_rate_max'] < 1e-12)
            check('GR_reference_boundary_and_independent_integration', abs(result['outer_clock_gap']) < 1e-13 and abs(result['inner_flux_gap']) < 1e-15 and result['independent_integrator_error'] < 1e-11)
            report['GR_reference'] = result
        if name == 'annular-canonical-inverse-boundary-control-attempt01':
            check('two_Gram_roots_independently_replayed', len([row for row in batch['samples'] if row['replay_distance'] is not None]) == 2)
    global_path = intake / 'annular-canonical-gr-reference-global-chart.json'
    global_report = json.loads(global_path.read_text())
    check('global_chart_complete_all_checks_pass', global_report['state'] == 'complete' and all(row['passed'] for row in global_report['checks']))
    inherit(global_report)
    own(global_path, 'outputs')
    bounds = {name: Fraction(int(value['numerator']), int(value['denominator'])) for name, value in global_report['bounds'].items()}
    check('exact_rational_global_F_chart', bounds['F_global_lower'] > Fraction(1, 10))
    check('exact_rational_global_lapse_chart', bounds['N_squared_global_lower'] > Fraction(1, 100))
    check('exact_rational_clock_discriminant', bounds['clock_discriminant_lower'] > 0)
    report['GR_reference_global_bounds'] = {name: float(value) for name, value in bounds.items()}
    scripts = ['annular_canonical_inverse_boundary_20260911.py', 'derive_annular_canonical_inverse_boundary_20260911.py', 'derive_annular_canonical_gr_boundary_reference_20260911.py', 'verify_annular_canonical_inverse_boundary_20260911.py', 'verify_annular_gr_reference_global_chart_20260911.py', Path(__file__).name]
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('six_scripts_compile_without_bytecode', True)
    note = root / 'DERIVATION-20260911-inverse-boundary-preparation-and-constructive-GR-reference.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text()):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('cited_path_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    start = datetime.fromisoformat('2026-09-11T19:57:26+00:00').timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    check('protected_workbench_modified_count_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot = intake / 'annular-canonical-inverse-boundary-resume-snapshot.md'
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
