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
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_canonical_nodal_data_20260911 import CanonicalInitialNodalData

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-canonical-mesh-continuation-final-integrity.json'
    if destination.exists():
        raise FileExistsError('Completed evidence is immutable.')
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'historical_sources': [], 'outcomes': [], 'valid_for_physics_claim': False, 'interval_certificate': False, 'new_evolution': False, 'inner_flux_parent_selected': False, 'protected_scan_scope': 'mtime since 2026-09-11T00:50:55Z, not a pre-turn content snapshot'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    prior_path = intake / 'annular-canonical-initial-data-final-integrity.json'
    own(prior_path)
    prior = json.loads(prior_path.read_text())
    check('prior_complete', prior['state'] == 'complete')
    for table in ['inputs', 'outputs']:
        for name, expected in prior[table].items():
            if digest(root / name) != expected:
                raise RuntimeError('Previously sealed evidence changed: ' + name)
            report['inputs'][name] = expected
    failed_directory = intake / 'annular-canonical-mesh-continuation-attempt01'
    failed = json.loads((failed_directory / 'status.json').read_text())
    check('failed_mesh_count_attempt_preserved', failed['state'] == 'failed' and 'size 16 is different from 17' in failed['error'])
    for name, expected in failed['inputs'].items():
        if digest(root / name) == expected:
            report['inputs'][name] = expected
        else:
            snapshot = failed_directory / ('executed-' + Path(name).name)
            check('failed_attempt_executed_snapshot_' + Path(name).name, snapshot.is_file() and digest(snapshot) == expected)
            report['historical_sources'].append({'current_path': name, 'executed_path': str(snapshot.relative_to(root)), 'sha256': expected})
    for path in failed_directory.iterdir():
        if path.is_file():
            own(path, 'outputs')
    for name in ['annular-canonical-mesh-continuation-attempt02', 'annular-canonical-continuation-control-attempt01', 'annular-canonical-fixed-derivative-attempt01']:
        directory = intake / name
        batch = json.loads((directory / 'status.json').read_text())
        check(name + '_completed_checks', batch['state'] == 'complete' and all(item['passed'] for item in batch['checks']))
        check(name + '_no_evolution_or_physics_claim', batch['new_evolution'] is False and batch['valid_for_physics_claim'] is False)
        for table in ['inputs', 'outputs']:
            for source, expected in batch[table].items():
                if digest(root / source) != expected:
                    raise RuntimeError('Completed new evidence changed: ' + source)
                report['inputs'][source] = expected
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
        for path in directory.glob('*.npz'):
            with numerical.load(path, allow_pickle=False) as archive:
                check(name + '_' + path.stem + '_finite_arrays', all(numerical.all(numerical.isfinite(archive[key])) for key in archive.files))
        for sample in batch['samples']:
            label = sample['label']
            if sample['status'] == 'converged':
                check(label + '_strict_root_tolerances', sample['all_residual_max'] < 1e-9 and sample['all_scaled_residual_max'] < 1e-10 and sample['failure'] is None)
            else:
                check(label + '_failed_iterate_explicit', sample['status'] == 'not_converged' and bool(sample['failure']))
            report['outcomes'].append({'batch': name, 'label': label, 'status': sample['status'], 'all_residual_max': sample['all_residual_max'], 'bulk_density_L2': sample.get('bulk_density_L2'), 'pi_difference_L2': sample.get('solved_vs_coarse_fields', {}).get('pi_difference_L2')})
            if name == 'annular-canonical-fixed-derivative-attempt01':
                parameter_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
                constants = {key: float(symbolic.sympify(value)) for key, value in json.loads(parameter_path.read_text())['parameters'].items()}
                source_path = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / ('canonical_N' + str(sample['mesh']) + '_' + sample['branch'] + '_sample0.npz')
                with numerical.load(source_path, allow_pickle=False) as archive:
                    source = {key: archive[key].copy() for key in archive.files}
                with numerical.load(directory / (label + '.npz'), allow_pickle=False) as archive:
                    saved = {key: archive[key].copy() for key in archive.files}
                basis = MixedActionBasis(source['basis_radii'])
                count = basis.radii.size
                configuration, momenta = source['original_configuration'], source['original_momenta']
                packed = (source['initial_root_box_lower'] + source['initial_root_box_upper']) / 2
                system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], source['affine_clock'][0], MetricLinkQuadrature(basis))
                model = CanonicalInitialNodalData(system, packed, configuration, sample['branch'] != 'GR', saved['boundary_velocity'])
                model.mass_coeff_seed[0] = saved['mass_coefficients'][0]

                def independently_parametrized_residual(candidate):
                    nodal = candidate[count:2 * count]
                    model.pi_coeff_seed = saved['pi_coefficients'].astype(numerical.result_type(candidate)).copy()
                    model.pi_coeff_seed[count:] = basis.spacing * (saved['fixed_auxiliary_derivative'] - basis.derivative @ nodal)
                    return model.data_residual(candidate)

                state = saved['state']
                replayed = independently_parametrized_residual(state)
                stored = numerical.concatenate([saved['constraint'], saved['residual']])
                check(label + '_independent_parameterization_roundtrip_including_failed_iterates', abs(replayed - stored).max() < 1e-12, float(abs(replayed - stored).max()))
                direction = numerical.cos(numerical.arange(state.size) + .7) * numerical.maximum(abs(state), .001)
                complex_direction = independently_parametrized_residual(state.astype(complex) + 1e-25j * direction).imag / 1e-25
                step = 1e-5
                finite_direction = (independently_parametrized_residual(state + step * direction) - independently_parametrized_residual(state - step * direction)) / (2 * step)
                error = float(abs(finite_direction - complex_direction).max() / max(1., float(abs(complex_direction).max())))
                check(label + '_derivative_control_including_failed_iterates', error < 1e-7, error)
    script_names = ['annular_canonical_mesh_transfer_20260911.py', 'derive_annular_canonical_mesh_continuation_20260911.py', 'verify_annular_canonical_continuation_20260911.py', 'derive_annular_canonical_fixed_derivative_20260911.py', Path(__file__).name]
    for name in script_names:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('five_new_scripts_compile_without_bytecode', True)
    note = root / 'DERIVATION-20260911-physical-momentum-transfer-and-mesh-continuation.md'
    for citation in re.findall(r'`([^`]+)`', note.read_text()):
        if citation.endswith(('.py', '.md', '.json', '.npz')):
            check('cited_path_exists_' + citation, (root / citation).is_file())
    own(note, 'outputs')
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    start = datetime.fromisoformat('2026-09-11T00:50:55+00:00').timestamp()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    check('protected_modified_file_count_zero_mtime', not changed, changed)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    snapshot = intake / 'annular-canonical-mesh-continuation-resume-snapshot.md'
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
