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
    from scipy.integrate import solve_ivp
    from annular_finite_width_boundary_cut_20260913 import CutPreparation
    from annular_finite_width_full_scalar_20260913 import TranslatedScalarAction
    from annular_nonlinear_history_20260912 import ManufacturedHistory

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    destination = intake / 'annular-finite-width-boundary-cut-final-integrity.json'
    snapshot = intake / 'annular-finite-width-boundary-cut-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Existing evidence must not be overwritten.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'boundary_action_controls': [],
              'cross_action_controls': [], 'clock_composition_controls': [], 'valid_for_physics_claim': False,
              'full_first_jet_closed': False, 'full_GR_limit_proven': False, 'boundary_histories_complete': False,
              'full_physical_radial_port_action_signed': False, 'unique_parent_regularizer_derived': False,
              'new_spacetime_evolution': False, 'point_scalar_reaction_derived': False, 'old_forced_IBVP_solved': False,
              'protected_scan_scope': 'mtime since 2026-09-13T02:45:46Z, not pre-turn content hashes'}
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

    def propagate(action, initial_time, initial_jacobian, anchors, targets):
        shape = initial_time.shape
        distance = targets - anchors

        def equation(fraction, packed):
            time, jacobian = packed.reshape((2,) + shape)
            radius = anchors + fraction * distance
            fields, rates, unused_second, unused_delta, unused_rate, unused_accel = action.history.evaluate(time, radius, [0, 0, 0, 0])
            geometry = action.geometry.evaluate(radius, fields)
            connection_time = np.sum(geometry['c_y'] * rates[:3], axis=0)
            return (distance * np.stack([geometry['c'], connection_time * jacobian])).ravel()

        initial = np.stack([initial_time, initial_jacobian])
        result = solve_ivp(equation, (0., 1.), initial.ravel(), method='DOP853', rtol=1e-12, atol=1e-14, max_step=.1)
        if not result.success:
            raise RuntimeError(result.message)
        return result.y[:, -1].reshape((2,) + shape)

    save()
    try:
        directory = intake / 'annular-finite-width-boundary-cut-attempt01'
        batch = json.loads((directory / 'status.json').read_text())
        check('completed_six_matched_initial_preparations', batch['state'] == 'complete' and len(batch['cases']) == 6 and all(item['passed'] for item in batch['checks']))
        for flag in ['valid_for_physics_claim', 'full_first_jet_closed', 'full_GR_limit_proven', 'boundary_histories_complete', 'full_physical_radial_port_action_signed', 'unique_parent_regularizer_derived', 'new_spacetime_evolution', 'point_scalar_reaction_derived', 'old_forced_IBVP_solved']:
            check(flag + '_remains_false', batch[flag] is False)
        for table in ['inputs', 'outputs']:
            for filename, expected in batch[table].items():
                if digest(root / filename) != expected:
                    raise RuntimeError('Changed evidence: ' + filename)
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Conflicting inherited hash: ' + filename)
                report['inputs'][filename] = expected
        check('all_inherited_and_run_hashes_match', True, len(report['inputs']))
        for path in directory.iterdir():
            if not path.is_file():
                continue
            own(path, 'outputs')
            if path.name.startswith('executed-'):
                check(path.name + '_matches', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
            if path.suffix == '.npz':
                with np.load(path, allow_pickle=False) as arrays:
                    check(path.name + '_finite', all(np.isfinite(arrays[key]).all() for key in arrays.files))
        for row in batch['cases']:
            name = row['branch'] + '_' + str(row['case'])
            source_path = root / 'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03' / (row['branch'] + '_source_snapshot.npz')
            with np.load(source_path, allow_pickle=False) as archive:
                source = {key: archive[key].copy() for key in archive.files}
            with np.load(directory / (name + '_prepared_collar.npz'), allow_pickle=False) as archive:
                saved = {key: archive[key].copy() for key in archive.files}
            preparation = CutPreparation(source, row['branch'] != 'GR', saved['kinetic_seed'], float(saved['outer_clock']), saved['drive'], row['width'], row['shape'])
            model = preparation.build(saved['coefficients'])
            radius, weights = model.cut_quadrature(40)
            fields = model.metric(radius)
            endpoints = model.metric(model.radii[[0, -1]])
            mass_r = model.coupling * fields['U']**2 * fields['epsilon']
            inner_reaction = endpoints['N'][0] / (model.coupling * endpoints['U'][0])
            fraction = (radius - model.radii[0]) / (model.radii[-1] - model.radii[0])
            errors = []
            for power in range(6):
                test = fraction**power
                derivative = np.zeros_like(fraction) if power == 0 else power * fraction**(power - 1) / (model.radii[-1] - model.radii[0])
                endpoint_test = np.array([1. if power == 0 else 0., 1.])
                step = 1e-24j
                varied_mass = fields['mu'] + step * test
                varied_mass_r = mass_r + step * derivative
                varied_root = np.sqrt(1 - 2 * varied_mass / radius)
                action = weights @ (fields['N'] * varied_mass_r / (model.coupling * varied_root) - fields['N'] * varied_root * fields['epsilon'])
                action += -float(saved['outer_clock']) * (endpoints['mu'][1] + step * endpoint_test[1]) / model.coupling
                action += inner_reaction * (endpoints['mu'][0] + step * endpoint_test[0] - source['mu'][0])
                measured = action.imag / step.imag
                expected = weights @ (test * fields['P1'])
                errors.append(float(abs(measured - expected)))
            check(name + '_six_unrestricted_metric_boundary_action_variations', max(errors) < 1e-10, errors)
            check(name + '_outer_clock_and_inner_reaction_are_not_silent', min(inner_reaction, float(saved['outer_clock']) / model.coupling) > 1.)
            report['boundary_action_controls'].append({'case': name, 'maximum_action_error': max(errors), 'inner_reaction': float(inner_reaction)})
        history = ManufacturedHistory(soluble=False)
        for gram in [False, True]:
            branch = 'GR' if not gram else 'metric_Gram'
            for offset in [-.43, -.11, .19, .47]:
                action = TranslatedScalarAction(history, gram, offset / 128)
                times = np.array([-.3, .05, .4])
                measured = action.integrands(times, [0, 0, 0, 0])
                fields = history.evaluate(measured['T'], action.targets, [0, 0, 0, 0])[0]
                coefficient = action.geometry.evaluate(action.targets, fields)['C']
                amplitude = action.collect(action.factor_weight * fields[3])
                density = action.collect(action.sample_weight * measured['J'] * coefficient)
                factor_action = -amplitude**2 * density / (2 * action.spacing)
                masks = (action.factors != 0) | (action.sampling != 0)
                lower = np.array([action.radii[mask].min() for mask in masks])
                upper = np.array([action.radii[mask].max() for mask in masks])
                inside = (lower >= 5.875) & (upper <= 6.125)
                exterior = (upper < 5.875) | (lower > 6.125)
                crossing = ~(inside | exterior)
                partitions = np.stack([factor_action[:, selection].sum(axis=1) for selection in [inside, exterior, crossing]])
                error = float(abs(partitions.sum(axis=0) - measured['action']).max())
                cross_magnitude = float(abs(partitions[2]).max())
                check(branch + '_' + str(offset) + '_whole_factor_action_partition', error < 1e-11 and cross_magnitude > 1e-8 and crossing.any())
                report['cross_action_controls'].append({'branch': branch, 'offset': offset, 'partition_error': error, 'cross_action_magnitude': cross_magnitude, 'crossing_factors': int(crossing.sum()), 'finite_P_history_not_coupled_solution': True})
                cut = 5.875 if offset < 0 else 6.125
                selected = (np.minimum(action.anchors, action.targets) < cut) & (np.maximum(action.anchors, action.targets) > cut)
                anchors, targets = action.anchors[selected], action.targets[selected]
                initial = np.broadcast_to(times[:, None], (len(times), len(anchors)))
                first = propagate(action, initial, np.ones_like(initial), anchors, np.full_like(anchors, cut))
                second = propagate(action, first[0], first[1], np.full_like(anchors, cut), targets)
                error = float(max(abs(second[0] - measured['T'][:, selected]).max(), abs(second[1] - measured['J'][:, selected]).max()))
                check(branch + '_' + str(offset) + '_finite_clock_transport_composition', error < 1e-9, error)
                report['clock_composition_controls'].append({'branch': branch, 'offset': offset, 'composition_error': error, 'crossing_links': int(selected.sum())})
            print(json.dumps({'branch': branch, 'boundary_action_and_finite_clock_controls': 'complete'}), flush=True)
            save()
        check('collar_counterexamples_preserved', len(batch['collar_controls']) == 2 and all(row['interior_metric_max_change'] < 1e-11 and row['all_original_node_trace_max_change'] < 1e-11 and abs(row['inner_current_change']) > 1e-7 for row in batch['collar_controls']))
        report['collar_controls'] = batch['collar_controls']
        report['shape_dependence'] = []
        for branch in ['GR', 'metric_Gram']:
            first = next(row for row in batch['cases'] if row['branch'] == branch and row['case'] == 0)
            alternate = next(row for row in batch['cases'] if row['branch'] == branch and row['case'] == 2)
            report['shape_dependence'].append({'branch': branch, 'outer_mass_rate_relative_change': abs(alternate['outer_mass_rate_not_prescribed'] / first['outer_mass_rate_not_prescribed'] - 1), 'derived_inner_scalar_velocity_relative_change': abs(alternate['inner_scalar_velocity_derived_not_fixed'] / first['inner_scalar_velocity_derived_not_fixed'] - 1), 'not_a_unique_regulator_prediction': True})
        note = root / 'DERIVATION-20260913-cross-cut-source-action-and-driven-initial-boundaries.md'
        for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
            if citation.endswith(('.py', '.md', '.json', '.npz')):
                check('cited_path_exists_' + citation, (root / citation).is_file())
        own(note, 'outputs')
        for stem in ['annular_finite_width_boundary_cut', 'derive_annular_finite_width_boundary_cut', 'verify_annular_finite_width_boundary_cut']:
            path = root / 'scripts' / (stem + '_20260913.py')
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('three_new_scripts_compile_without_bytecode', True)
        protected = root.parent / 'formalization-workbench'
        check('protected_workbench_exists', protected.is_dir())
        start = datetime.fromisoformat('2026-09-13T02:45:46+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot, 'outputs')
        report.update({'state': 'complete', 'completed_run_checks': len(batch['checks']), 'maximum_C0': max(row['C0_max'] for row in batch['cases']),
                       'maximum_C1': max(row['C1_max'] for row in batch['cases']), 'maximum_initial_boundary_error': max(row['maximum_initial_boundary_error'] for row in batch['cases']), 'protected_changed_count': len(changed)})
        save()
        print(json.dumps({'state': 'complete', 'seal_checks': len(report['checks']), 'run_checks': report['completed_run_checks'], 'maximum_C0': report['maximum_C0'], 'maximum_C1': report['maximum_C1'], 'maximum_initial_boundary_error': report['maximum_initial_boundary_error'], 'maximum_boundary_action_error': max(row['maximum_action_error'] for row in report['boundary_action_controls']), 'full_first_jet_closed': False}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
