import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_gram_joint_action_20260909 import gram_matrices
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_time_link_adjoint_20260911 import frozen_maps, slice_sources

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    final = intake / 'annular-initial-jet-adjoint-final-integrity.json'
    if final.exists():
        raise FileExistsError('Final evidence is immutable.')
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'valid_for_physics_claim': False, 'full_parent_evolution_proved': False, 'Gram_initial_jet_interval_certified': False, 'frozen_check_scope': 'mtime scan since 2026-09-10T23:49:15Z, not a full pre-turn content baseline'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        name, actual = str(path.relative_to(root)), digest(path)
        if name in report[table] and report[table][name] != actual:
            raise RuntimeError('Conflicting hash: ' + name)
        report[table][name] = actual

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    attempts = ['annular-initial-shift-jet-probe01', 'annular-initial-shift-jet-probe02', 'annular-time-link-adjoint-attempt01', 'annular-time-link-lapse-control-attempt01', 'annular-initial-mesh-control-attempt01']
    for attempt in attempts:
        directory = intake / attempt
        state = json.loads((directory / 'status.json').read_text())
        check(attempt + '_complete_and_checks_pass', state['state'] == 'complete' and all(item['passed'] for item in state.get('checks', [])))
        for table in ['inputs', 'outputs']:
            for name, expected in state.get(table, {}).items():
                check_value = digest(root / name)
                if check_value != expected:
                    raise RuntimeError('Changed inherited evidence: ' + name)
                report['inputs'][name] = expected
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
        for source in directory.glob('executed-*.py'):
            current = root / 'scripts' / source.name[len('executed-'):]
            check(attempt + '_' + current.name + '_executed_source_unchanged', digest(source) == digest(current))
        for path in directory.glob('*.npz'):
            with numerical.load(path) as archive:
                check(path.stem + '_' + attempt + '_finite_array_archive', bool(archive.files) and all(numerical.all(numerical.isfinite(archive[name])) for name in archive.files))
    script_names = ['annular_initial_shift_jet_20260911.py', 'derive_annular_initial_shift_jet_20260911.py', 'annular_initial_shift_schur_20260911.py', 'annular_time_link_adjoint_20260911.py', 'derive_annular_time_link_adjoint_20260911.py', 'verify_annular_time_link_lapse_20260911.py', 'verify_annular_initial_mesh_20260911.py', Path(__file__).name]
    for name in script_names:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    check('eight_new_scripts_compile_without_bytecode', True)
    note = root / 'DERIVATION-20260911-coupled-initial-jet-and-exact-time-link-adjoint.md'
    citations = []
    for reference in re.findall(r'`([^`]+)`', note.read_text()):
        if reference.endswith(('.md', '.py', '.json', '.npz')):
            check('cited_path_exists_' + reference, (root / reference).is_file())
            citations.append(reference)
    own(note, 'outputs')
    report['cited_paths'] = citations
    roots = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'
    case_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
    constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(case_path.read_text())['parameters'].items()}
    for branch in ['GR', 'metric_Gram']:
        label = 'canonical_N16_' + branch + '_sample0'
        with numerical.load(roots / (label + '.npz')) as archive:
            saved = {name: archive[name].copy() for name in archive.files}
        basis = MixedActionBasis(saved['basis_radii'])
        count = basis.radii.size
        knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces]))
        samples = numerical.concatenate([basis.radii, basis.faces])
        segment = numerical.clip(numerical.searchsorted(knots, samples, side='right') - 1, 0, knots.size - 2)
        fraction = (samples - knots[segment]) / (knots[segment + 1] - knots[segment])
        even = 4 * fraction * (1 - fraction)
        odd = even * (2 * fraction - 1)
        check(branch + '_actual_bubble_polynomials_vanish_at_nodes_faces_endpoints', numerical.all(even == 0) and numerical.all(odd == 0))
        configuration, momenta = saved['original_configuration'], saved['original_momenta']
        packed = (saved['initial_root_box_lower'] + saved['initial_root_box_upper']) / 2
        links = MetricLinkQuadrature(basis)
        system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], saved['affine_clock'][0], links)
        maps = frozen_maps(system, packed, configuration)
        zero = slice_sources(system, packed, configuration, maps, numerical.zeros(maps['shift_map'].shape[1]))
        factors, sampling = gram_matrices(count)
        mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
        q_node = packed[system.slices[2]]
        coefficient = basis.radii**2 * lapse * numerical.sqrt(1 - 2 * (basis.face_to_node @ mass) / basis.radii)
        amplitude = factors @ configuration[:count]
        expected_scalar = -(factors.T @ ((sampling @ coefficient) * amplitude / basis.spacing))
        expected_density_time = sampling.T @ (amplitude * (factors @ q_node)) / basis.spacing
        expected_shift = links.matrix(mass, lapse, constants).T @ zero['current']
        check(branch + '_old_unit_J_scalar_force_recovered', float(abs(zero['scalar_force'][:count] - expected_scalar).max()) < 1e-12)
        check(branch + '_old_unit_J_density_time_recovered', float(abs(zero['density_time'] - expected_density_time).max()) < 1e-12)
        check(branch + '_old_unit_J_shift_covector_recovered', float(abs(zero['shift_force'][:system.face_count] - expected_shift).max()) < 1e-12)
    mesh = json.loads((intake / 'annular-initial-mesh-control-attempt01/status.json').read_text())
    check('both_branches_evaluated_at_two_finer_meshes', len(mesh['samples']) == 4 and all(sample['state'] == 'evaluated' and sample['finite_values'] for sample in mesh['samples']))
    report['near_null_mode_diagnostics'] = []
    for branch in ['GR', 'metric_Gram']:
        path = intake / 'annular-initial-mesh-control-attempt01' / ('canonical_N64_' + branch + '_sample0.npz')
        with numerical.load(path) as archive:
            eigenvalues, eigenvectors = numerical.linalg.eigh(archive['schur'])
            rate = archive['lapse_rate']
            component = float(eigenvectors[:, 0] @ rate)
            remainder = rate - eigenvectors[:, 0] * component
        report['near_null_mode_diagnostics'].append({'branch': branch, 'smallest_eigenvalues': eigenvalues[:4].tolist(), 'largest_eigenvalue': float(eigenvalues[-1]), 'leading_rate_component': component, 'remaining_rate_coefficient_max': float(abs(remainder).max()), 'diagnostic_only_no_mode_removed': True})
    for module in tuple(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.parent == root / 'scripts' and path.suffix == '.py':
                own(path)
    protected = root.parent / 'formalization-workbench'
    check('protected_workbench_exists', protected.is_dir())
    start = datetime.fromisoformat('2026-09-10T23:49:15+00:00').timestamp()
    touched = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
    check('frozen_workbench_changed_file_count_zero_mtime', not touched, touched)
    check('no_python_cache_created', not (root / 'scripts/__pycache__').exists())
    snapshot = intake / 'annular-initial-jet-adjoint-resume-snapshot.md'
    if snapshot.exists():
        raise FileExistsError(snapshot)
    snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    own(snapshot, 'outputs')
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    final.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'input_hashes': len(report['inputs']), 'output_hashes': len(report['outputs']), 'frozen_changed_count': len(touched), 'final_seal': str(final)}), flush=True)


if __name__ == '__main__':
    run()
