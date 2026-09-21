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
    import sympy as sp
    from annular_finite_width_boundary_cut_20260913 import CutPreparation

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    destination = intake / 'annular-collar-response-final-integrity.json'
    snapshot = intake / 'annular-collar-response-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Existing evidence must not be overwritten.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'action_controls': [], 'boundary_controls': [],
              'valid_for_physics_claim': False, 'full_first_jet_closed': False, 'full_GR_limit_proven': False,
              'boundary_histories_complete': False, 'full_physical_radial_port_action_signed': False,
              'full_C2_evaluated': False, 'new_spacetime_evolution': False, 'unique_parent_regularizer_derived': False,
              'point_force_adopted': False, 'retarded_kernel_is_standalone_single_history_action': False,
              'frozen_scalar_reservoir_response_derived': True,
              'protected_scan_scope': 'mtime since 2026-09-13T03:03:48Z, not pre-turn content hashes'}
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

    save()
    try:
        directory = intake / 'annular-collar-response-attempt01'
        batch = json.loads((directory / 'status.json').read_text())
        check('completed_response_matrix', batch['state'] == 'complete' and len(batch['responses']) == 24 and len(batch['physical_boundaries']) == 6 and all(item['passed'] for item in batch['checks']))
        for flag in ['valid_for_physics_claim', 'full_first_jet_closed', 'full_GR_limit_proven', 'boundary_histories_complete', 'full_physical_radial_port_action_signed', 'full_C2_evaluated', 'new_spacetime_evolution', 'unique_parent_regularizer_derived', 'point_force_adopted', 'retarded_kernel_is_standalone_single_history_action']:
            check(flag + '_remains_false', batch[flag] is False)
        for table in ['inputs', 'outputs']:
            for filename, expected in batch[table].items():
                if digest(root / filename) != expected:
                    raise RuntimeError('Changed evidence: ' + filename)
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Conflicting evidence hash: ' + filename)
                report['inputs'][filename] = expected
        check('all_inherited_hashes_match', True, len(report['inputs']))
        for path in directory.iterdir():
            if not path.is_file():
                continue
            own(path, 'outputs')
            if path.name.startswith('executed-'):
                check(path.name + '_source_matches', digest(path) == digest(root / 'scripts' / path.name.removeprefix('executed-')))
            if path.suffix != '.npz':
                continue
            with np.load(path, allow_pickle=False) as archive:
                data = {key: archive[key].copy() for key in archive.files}
            check(path.name + '_finite', all(np.isfinite(value).all() for value in data.values()))
            mass, stiffness, position, speed = [data[key] for key in ['M', 'K', 'chi0', 'v0']]
            exterior, interior = int(data['exterior']), data['interior']
            action = .5 * np.sum(mass * speed**2) - .5 * position @ stiffness @ position
            separated = .5 * np.sum(mass[interior] * speed[interior]**2) - .5 * position[interior] @ stiffness[np.ix_(interior, interior)] @ position[interior]
            separated += .5 * mass[exterior] * speed[exterior]**2 - .5 * stiffness[exterior, exterior] * position[exterior]**2 - position[interior] @ stiffness[interior, exterior] * position[exterior]
            check(path.name + '_symmetric_block_action_decomposition', abs(action - separated) < 1e-12)
            factor = 1.7
            rescaled_mass, rescaled_stiffness = mass / factor, stiffness * factor
            physical_force = -np.exp(-data['g']) * (stiffness @ position)
            rescaled_force = -np.exp(-data['g'] - np.log(factor)) * (rescaled_stiffness @ position)
            check(path.name + '_auxiliary_clock_scale_not_new_physical_coupling', abs(physical_force - rescaled_force).max() < 1e-11 and abs(rescaled_mass * factor - mass).max() < 1e-12)
            horizon = .025
            points, weights = np.polynomial.legendre.leggauss(28)
            times, time_weights = horizon * (points + 1) / 2, horizon * weights / 2
            exterior_acceleration = .05
            inside_acceleration = .01 * np.cos(np.arange(len(interior)) + 1)
            inside = position[interior, None] + speed[interior, None] * times + .5 * inside_acceleration[:, None] * times**2
            outside = position[exterior] + speed[exterior] * times + .5 * exterior_acceleration * times**2
            outside_speed = speed[exterior] + exterior_acceleration * times
            coupling = stiffness[exterior, interior]
            reaction = mass[exterior] * exterior_acceleration + stiffness[exterior, exterior] * outside + coupling @ inside
            test = (times / horizon)**2 * (1 - times / horizon)**2
            test_rate = (2 * times / horizon * (1 - times / horizon)**2 - 2 * (times / horizon)**2 * (1 - times / horizon)) / horizon
            step = 1e-24j
            varied = outside + step * test
            varied_speed = outside_speed + step * test_rate
            lagrangian = .5 * mass[exterior] * varied_speed**2 - .5 * stiffness[exterior, exterior] * varied**2 - varied * (coupling @ inside) + reaction * varied
            raw_variation = float(time_weights @ (lagrangian.imag / step.imag))
            check(path.name + '_driven_reservoir_force_from_action_variation', abs(raw_variation) < 1e-11, raw_variation)
            report['action_controls'].append({'path': str(path.relative_to(root)), 'driven_action_variation_error': abs(raw_variation)})
        earlier = intake / 'annular-finite-width-boundary-cut-attempt01'
        for row in batch['physical_boundaries']:
            branch, index = row['branch'], row['case']
            name = branch + '_' + str(index)
            source_path = root / 'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03' / (branch + '_source_snapshot.npz')
            with np.load(source_path, allow_pickle=False) as archive:
                source = {key: archive[key].copy() for key in archive.files}
            with np.load(earlier / (name + '_prepared_collar.npz'), allow_pickle=False) as archive:
                prepared = {key: archive[key].copy() for key in archive.files}
            preparation = CutPreparation(source, branch != 'GR', prepared['kinetic_seed'], float(prepared['outer_clock']), prepared['drive'], row['width'], row['shape'])
            model = preparation.build(prepared['coefficients'])
            locations, weights = model.quadrature(40)
            values = model.metric(locations)
            ends = model.metric(model.edges[[0, -1]])
            geometric_ends = ends['N'] * ends['U'] * np.exp(ends['g'])
            geometric_error = float(abs(np.log(geometric_ends[1] / geometric_ends[0]) - 2 * weights @ (values['mu'] / (locations**2 * values['U']**2))))
            check(name + '_independent_geometric_weight_integral', geometric_error < 1e-11, geometric_error)
            radius = model.radii[-1]
            boundary = model.metric(np.array([radius]))
            scalar = model.stencil([0.])
            lapse, root_f, mass = boundary['N'][0], boundary['U'][0], boundary['mu'][0]
            step = 1e-24j
            changed_mass = mass + step * row['outer_mass_rate']
            changed_lapse = lapse * (1 + step * row['logarithmic_outer_lapse_rate'])
            changed_momentum = scalar['p'][0, -1] + step * scalar['p1'][0, -1]
            changed_root = np.sqrt(1 - 2 * changed_mass / radius)
            differentiated_velocity = (changed_lapse * changed_root * changed_momentum / radius**2).imag / step.imag
            differentiated_clock = (changed_lapse / changed_root).imag / step.imag
            error = float(max(abs(differentiated_velocity - row['free_outer_acceleration']), abs(differentiated_clock - row['clock_rate'])))
            check(name + '_independent_clock_and_kinetic_time_derivative', error < 1e-11, error)
            if branch == 'GR':
                gradient_sign = scalar['chi'][0, -1] - scalar['chi'][0, -2]
                upper_bound = row['clock_rate'] / row['clock_value'] * row['outer_scalar_velocity']
                check(name + '_positive_geometry_free_endpoint_sign_obstruction', gradient_sign > 0 and row['outer_mass_rate'] >= 0 and row['outer_scalar_velocity'] > 0 and row['free_outer_momentum_rate'] < 0 and row['free_outer_acceleration'] < upper_bound < row['prescribed_outer_acceleration'])
            report['boundary_controls'].append({'case': name, 'geometric_weight_error': geometric_error, 'kinetic_clock_derivative_error': error})
        first, second, coefficient = sp.symbols('x1 x2 a', real=True)
        state = sp.Matrix([first, second])
        causal = sp.Matrix([[0, 0], [coefficient, 0]])
        naive_action = (state.T * causal * state)[0] / 2
        gradient = sp.Matrix([sp.diff(naive_action, variable) for variable in state])
        check('retarded_kernel_naive_action_symmetrizes_and_is_not_causal_force', gradient == (causal + causal.T) * state / 2 and gradient != causal * state)
        check('failed_free_acceleration_gates_retained', batch['free_outer_second_order_all_pass'] is False and all(not row['free_boundary_second_order_pass'] and abs(row['acceleration_defect']) > 1 for row in batch['physical_boundaries']))
        note = root / 'DERIVATION-20260913-geometric-collar-memory-and-driven-acceleration-law.md'
        for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
            if citation.endswith(('.py', '.md', '.json', '.npz')):
                check('cited_path_exists_' + citation, (root / citation).is_file())
        own(note, 'outputs')
        for stem in ['annular_collar_response', 'derive_annular_collar_response', 'verify_annular_collar_response']:
            path = root / 'scripts' / (stem + '_20260913.py')
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('three_new_scripts_compile_without_bytecode', True)
        protected = root.parent / 'formalization-workbench'
        check('protected_workbench_exists', protected.is_dir())
        start = datetime.fromisoformat('2026-09-13T03:03:48+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot, 'outputs')
        report.update({'state': 'complete', 'completed_run_checks': len(batch['checks']), 'protected_changed_count': len(changed),
                       'free_outer_second_order_all_pass': False, 'frozen_response_cases': len(batch['responses']),
                       'maximum_retarded_traction_error': max(row['free']['retarded_traction_error'] for row in batch['responses']),
                       'maximum_forced_replay_error': max(row['driven']['full_forced_replay_error'] for row in batch['responses'])})
        save()
        print(json.dumps({'state': 'complete', 'seal_checks': len(report['checks']), 'run_checks': report['completed_run_checks'], 'frozen_response_cases': report['frozen_response_cases'], 'maximum_retarded_traction_error': report['maximum_retarded_traction_error'], 'maximum_forced_replay_error': report['maximum_forced_replay_error'], 'free_outer_second_order_all_pass': False, 'full_C2_evaluated': False, 'protected_changed_count': len(changed)}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
