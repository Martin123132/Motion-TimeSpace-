import hashlib
import json
import re
import traceback
from datetime import datetime
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_finite_width_bulk_current_20260913 import FiniteWidthBulk

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    destination = intake / 'annular-finite-width-bulk-current-final-integrity.json'
    snapshot = intake / 'annular-finite-width-bulk-current-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Existing evidence must not be overwritten.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'independent_cases': [],
              'valid_for_physics_claim': False, 'full_first_jet_closed': False,
              'full_GR_limit_proven': False, 'new_spacetime_evolution': False,
              'full_physical_radial_port_action_signed': False, 'unique_parent_regularizer_derived': False,
              'old_boundary_drives_transferred': False, 'source_extension_parent_selected': False,
              'protected_scan_scope': 'mtime since 2026-09-13T00:06:03Z, not pre-turn content hashes'}
    hashes = {}

    def save():
        destination.write_text(json.dumps(report, indent=2) + '\n')

    def digest(path):
        if path not in hashes:
            hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
        return hashes[path]

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def integrating_factor_control(model):
        points, weights = np.polynomial.legendre.leggauss(48)
        inside, inside_weights = np.polynomial.legendre.leggauss(32)
        mass = model.metric(np.array([model.edges[0]]))['mu'][0]
        error = 0.
        for lower, upper in zip(model.edges[:-1], model.edges[1:]):
            locations = (lower + upper) / 2 + (upper - lower) * points / 2
            radial_weights = (upper - lower) * weights / 2
            density = model.energy_density(locations)
            inner_locations = (lower + locations[:, None]) / 2 + (locations[:, None] - lower) * inside / 2
            inner_density = model.energy_density(inner_locations.ravel()).reshape(inner_locations.shape)
            exponents = (locations - lower) / 2 * np.sum(inside_weights * 2 * model.coupling * inner_density / inner_locations, axis=1)
            endpoint_exponent = radial_weights @ (2 * model.coupling * density / locations)
            mass = np.exp(-endpoint_exponent) * (mass + radial_weights @ (model.coupling * density * np.exp(exponents)))
            error = max(error, abs(mass - model.metric(np.array([upper]))['mu'][0]))
        return float(error)

    def action_trace_control(model, offset, direction, epsilon):
        initial = model.stencil([offset])
        total = 0.
        points, weights = np.polynomial.legendre.leggauss(20)
        step = 1e-24j
        for factor in range(len(model.factors)):
            mask = model.factor == factor
            nodes, factor_weights, sample_weights = model.node[mask], model.bpair[mask], model.spair[mask]
            jacobian = initial['J'][0, mask]
            cuts = np.unique(np.concatenate([-epsilon / jacobian, epsilon / jacobian]))
            for lower, upper in zip(cuts[:-1], cuts[1:]):
                times = (lower + upper) / 2 + (upper - lower) * points / 2
                moved_times = times[:, None] * jacobian
                scaled_time = moved_times / epsilon
                bump = np.where(abs(scaled_time) < 1, 315 / 256 * (1 - scaled_time**2)**4 / epsilon, 0.)
                scalar = initial['chi'][0, nodes] + initial['q'][0, nodes] * moved_times + step * direction[nodes] * bump
                fields = initial['fields']
                scaled_connection = fields['N'][0, nodes] * fields['U'][0, nodes] * fields['g_r'][0, nodes] * moved_times
                shift_variable = 2 * scaled_connection / (1 + np.sqrt(1 + 4 * scaled_connection**2))
                coefficient = initial['C'][0, nodes] * (1 - shift_variable**2)
                amplitude = scalar @ factor_weights
                density = (coefficient * jacobian) @ sample_weights
                action = -amplitude**2 * density / (2 * model.spacing)
                total += (upper - lower) / 2 * weights @ (action.imag / step.imag)
        return float(total)

    save()
    try:
        directory = intake / 'annular-finite-width-bulk-current-attempt01'
        batch = json.loads((directory / 'status.json').read_text())
        check('completed_run_checks_pass', batch['state'] == 'complete' and all(item['passed'] for item in batch['checks']))
        check('ten_matched_cases_pass_compact_only', len(batch['cases']) == 10 and batch['all_compact_bulk_tests_pass'] is True)
        for flag in ['valid_for_physics_claim', 'full_first_jet_closed', 'full_GR_limit_proven', 'new_spacetime_evolution', 'full_physical_radial_port_action_signed', 'unique_parent_regularizer_derived', 'old_boundary_drives_transferred', 'source_extension_parent_selected']:
            check(flag + '_remains_false', batch[flag] is False)
        for table in ['inputs', 'outputs']:
            for filename, expected in batch[table].items():
                if digest(root / filename) != expected:
                    raise RuntimeError('Changed evidence: ' + filename)
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Conflicting evidence hash: ' + filename)
                report['inputs'][filename] = expected
        check('all_inherited_and_run_hashes_match', True, len(report['inputs']))
        for path in directory.iterdir():
            if not path.is_file():
                continue
            own(path, 'outputs')
            if path.name.startswith('executed-'):
                check(path.name + '_matches_source', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
            if path.suffix == '.npz':
                with np.load(path, allow_pickle=False) as arrays:
                    check(path.name + '_all_finite', all(np.isfinite(arrays[key]).all() for key in arrays.files))
        for branch in ['GR', 'metric_Gram']:
            source_path = root / 'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03' / (branch + '_source_snapshot.npz')
            with np.load(source_path, allow_pickle=False) as archive:
                source = {key: archive[key].copy() for key in archive.files}
            model = FiniteWidthBulk(source, branch != 'GR', 1 / 128)
            factor_error = integrating_factor_control(model)
            check(branch + '_independent_linear_integrating_factor_mass_solution', factor_error < 1e-11, factor_error)
            arrays, fit = model.compact_checks(degree=44, order=40)
            radius, weights = arrays['R'], arrays['weights']
            tests, derivatives = model.tests(radius)
            reference = np.sqrt(2 / 3)

            def hamiltonian(mass, lapse, lapse_r):
                root_value = np.sqrt(1 - 2 * mass / radius)
                return weights @ (-lapse * (root_value + 1 / root_value - 2 * reference) / (2 * model.coupling) - radius * lapse_r * (root_value - reference) / model.coupling + lapse * root_value * arrays['epsilon'])

            action_errors = []
            step = 1e-24j
            for index in range(tests.shape[1]):
                mass_force = -hamiltonian(arrays['mu'] + step * tests[:, index], arrays['N'], model.slope * arrays['N']).imag / step.imag
                lapse_constraint = -hamiltonian(arrays['mu'], arrays['N'] + step * tests[:, index], model.slope * arrays['N'] + step * derivatives[:, index]).imag / step.imag
                action_errors.append(float(max(abs(mass_force - weights @ (tests[:, index] * arrays['P1'])), abs(lapse_constraint - arrays['C0'][index]))))
            check(branch + '_fourteen_direct_metric_action_variations', max(action_errors) < 1e-11, action_errors)
            left = model.metric(np.array([model.edges[0]]))
            right = model.metric(np.array([model.edges[-1]]))
            predicted_g = -np.log(right['N'][0] / left['N'][0]) - np.log(right['U'][0] / left['U'][0]) + 2 * weights @ (arrays['mu'] / (radius**2 * arrays['U']**2))
            clock_error = float(abs(predicted_g - right['g'][0]))
            check(branch + '_independent_shared_metric_clock_identity', clock_error < 1e-11, clock_error)
            controls = []
            for offset in [0., .173]:
                initial = model.stencil([offset])
                for direction in [np.eye(17)[8], np.sin(np.arange(17) + 1)]:
                    response = [action_trace_control(model, offset, direction, epsilon) for epsilon in [.004, .002]]
                    extrapolated = (4 * response[1] - response[0]) / 3
                    expected = initial['Gchi'][0] @ direction
                    error = float(abs(extrapolated - expected))
                    check(branch + '_' + str(offset) + '_localized_physical_time_action_force_' + str(len(controls)), error < 1e-10, {'error': error, 'expected': float(expected), 'extrapolated_action_variation': float(extrapolated)})
                    controls.append(error)
                trial_time = 1e-24j
                physical_d = np.zeros(len(model.radii), dtype=complex)
                for pair in range(len(model.node)):
                    factor, node = model.factor[pair], model.node[pair]
                    mask = model.factor == factor
                    factor_nodes = model.node[mask]
                    moved_time = trial_time * initial['J'][0, mask] / initial['J'][0, pair]
                    amplitude = np.sum(model.bpair[mask] * (initial['chi'][0, factor_nodes] + moved_time * initial['q'][0, factor_nodes]))
                    physical_d[node] += model.spair[pair] * amplitude**2 / (2 * model.spacing)
                trial_momentum = initial['p'][0] + trial_time * initial['p1'][0]
                live_energy = model.node_weights * trial_momentum**2 / (2 * initial['R'][0]**2) + initial['R'][0]**2 * physical_d
                live_error = float(abs(live_energy.imag / trial_time.imag - initial['energy1'][0]).max())
                check(branch + '_' + str(offset) + '_independent_resynchronized_energy_rate', live_error < 1e-11, live_error)
            report['independent_cases'].append({'branch': branch, 'integrating_factor_mass_error': factor_error, 'metric_action_max_error': max(action_errors), 'clock_identity_error': clock_error, 'physical_time_force_max_error': max(controls)})
            print(json.dumps(report['independent_cases'][-1]), flush=True)
            save()
        note = root / 'DERIVATION-20260913-shared-metric-bulk-current-and-compact-constraint-propagation.md'
        for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
            if citation.endswith(('.py', '.md', '.json', '.npz')):
                check('cited_path_exists_' + citation, (root / citation).is_file())
        own(note, 'outputs')
        for stem in ['annular_finite_width_bulk_current', 'derive_annular_finite_width_bulk_current', 'verify_annular_finite_width_bulk_current']:
            path = root / 'scripts' / (stem + '_20260913.py')
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('three_new_scripts_compile_without_bytecode', True)
        protected = root.parent / 'formalization-workbench'
        check('protected_workbench_exists', protected.is_dir())
        start = datetime.fromisoformat('2026-09-13T00:06:03+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
        check('protected_mtime_changed_file_count_zero', not changed, changed)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot, 'outputs')
        report.update({'state': 'complete', 'completed_run_checks': len(batch['checks']), 'all_compact_bulk_tests_pass': True,
                       'compact_C0_C1_residual_rows': 280, 'maximum_C0': max(max(row['C0_primary_max'], row['C0_higher_max']) for row in batch['cases']),
                       'maximum_C1': max(max(row['C1_primary_max'], row['C1_higher_max']) for row in batch['cases']),
                       'protected_changed_file_count': len(changed)})
        save()
        print(json.dumps({'state': 'complete', 'seal_checks': len(report['checks']), 'run_checks': report['completed_run_checks'], 'maximum_C0': report['maximum_C0'], 'maximum_C1': report['maximum_C1'], 'full_first_jet_closed': False, 'protected_changed_file_count': len(changed)}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
