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
    destination = intake / 'annular-canonical-mass-reduction-final-integrity.json'
    if destination.exists():
        raise FileExistsError('Completed evidence is immutable.')
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'outcomes': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'boundary_replacement_implemented': False, 'protected_scan_scope': 'mtime since 2026-09-11T01:23:15Z, not a pre-turn content snapshot'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    prior_path = intake / 'annular-canonical-mesh-continuation-final-integrity.json'
    own(prior_path)
    prior = json.loads(prior_path.read_text())
    check('prior_seal_complete', prior['state'] == 'complete')
    for table in ['inputs', 'outputs']:
        for name, expected in prior[table].items():
            if digest(root / name) != expected:
                raise RuntimeError('Previously sealed evidence changed: ' + name)
            report['inputs'][name] = expected
    for name in ['annular-canonical-mass-reduction-attempt01', 'annular-canonical-mass-reduction-control-attempt01', 'annular-canonical-boundary-compatibility-attempt01']:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        check(name + '_complete_all_checks_pass', batch['state'] == 'complete' and all(item['passed'] for item in batch['checks']))
        check(name + '_no_physics_or_evolution_claim', batch['valid_for_physics_claim'] is False and batch['new_evolution'] is False)
        for table in ['inputs', 'outputs']:
            for source, expected in batch[table].items():
                if digest(root / source) != expected:
                    raise RuntimeError('New completed evidence changed: ' + source)
                report['inputs'][source] = expected
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
        for path in directory.glob('*.npz'):
            with numerical.load(path, allow_pickle=False) as archive:
                check(name + '_' + path.stem + '_finite_arrays', all(numerical.all(numerical.isfinite(archive[key])) for key in archive.files))
        for path in directory.glob('executed-*.py'):
            check(name + '_' + path.name + '_matches_executed_source', digest(path) == digest(root / 'scripts' / path.name[len('executed-'):]))
        if name == 'annular-canonical-mass-reduction-attempt01':
            check('five_known_root_neighborhoods_recovered', len(batch['replays']) == 5 and all(sample['converged'] and sample['distance_from_original'] < 1e-5 for sample in batch['replays']))
            for sample in batch['samples']:
                label = sample['label']
                check(label + '_all_accepted_mass_projections_satisfy_tolerance', bool(sample['history']) and all(item['mass_residual'] <= batch['mass_tolerance'] for item in sample['history']))
                with numerical.load(directory / (label + '.npz'), allow_pickle=False) as saved:
                    absolute = float(abs(saved['full_residual']).max())
                    scaled = float(abs(saved['full_residual'] / saved['row_scales']).max())
                    check(label + '_residual_metrics_replayed', absolute == sample['all_residual_max'] and scaled == sample['all_scaled_residual_max'])
                    if sample['status'] == 'converged':
                        check(label + '_all_root_gates_not_only_mass', absolute < 1e-9 and scaled < 1e-10 and sample['failure'] is None)
                    else:
                        check(label + '_failure_not_promoted', sample['status'] == 'not_converged' and bool(sample['failure']))
                report['outcomes'].append({'label': label, 'status': sample['status'], 'mass_residual': sample['constraint_max'], 'full_residual': absolute})
        if name == 'annular-canonical-mass-reduction-control-attempt01':
            check('symbolic_boundary_flux_law_was_verified', any(item['name'] == 'exact_canonical_bulk_boundary_flux_law' and item['passed'] for item in batch['checks']))
            for sample in batch['samples']:
                boundary = sample['boundary_prediction']
                difference = Fraction(int(boundary['exact_mismatch_numerator']), int(boundary['exact_mismatch_denominator']))
                check(sample['label'] + '_stored_rational_mismatch_nonzero', difference != 0 and float(difference) == boundary['prescribed_minus_bulk_flux'])
        if name == 'annular-canonical-boundary-compatibility-attempt01':
            check('Gram_endpoint_sign_not_assumed_from_positive_energy', len(batch['factor_signs']) == 3 and all(item['negative_products'] > 0 and item['positive_products'] > 0 and item['unconditional_force_sign_from_these_products'] == 'not_sign_definite' for item in batch['factor_signs']))
    names = ['annular_canonical_mass_reduction_20260911.py', 'derive_annular_canonical_mass_reduction_20260911.py', 'verify_annular_canonical_mass_reduction_20260911.py', 'derive_annular_canonical_boundary_compatibility_20260911.py', Path(__file__).name]
    for name in names:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('five_scripts_compile_without_bytecode', True)
    note = root / 'DERIVATION-20260911-nonlinear-mass-elimination-and-boundary-flux-compatibility.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text()):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('cited_path_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    start = datetime.fromisoformat('2026-09-11T01:23:15+00:00').timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    check('protected_modified_count_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot = intake / 'annular-canonical-mass-reduction-resume-snapshot.md'
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
