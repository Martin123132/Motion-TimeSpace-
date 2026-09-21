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
    from annular_clock_reservoir_coupling_20260913 import ClockReservoirPreparation, ProperClockDrive, clock_factor

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    destination = intake / 'annular-clock-reservoir-coupling-final-integrity.json'
    snapshot = intake / 'annular-clock-reservoir-coupling-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Existing evidence must not be overwritten.')
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'independent_cases': [], 'zero_budget_controls': [],
              'valid_for_physics_claim': False, 'full_GR_limit_proven': False, 'full_C2_evaluated': False,
              'full_first_jet_closed': False, 'boundary_histories_complete': False,
              'full_physical_radial_port_action_signed': False, 'unique_parent_regularizer_derived': False,
              'apparatus_microphysics_derived': False, 'full_geometric_evolution': False,
              'point_force_adopted': False, 'new_fundamental_MTS_field_claimed': False,
              'initial_positive_reservoir_energy_not_global_stability': True,
              'forced_acceleration_recovery_is_not_independent_prediction': True,
              'protected_scan_scope': 'mtime since 2026-09-13T10:28:20Z; not pre-turn content hashes'}

    def save():
        destination.write_text(json.dumps(report, indent=2) + '\n')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        directory = intake / 'annular-clock-reservoir-coupling-attempt01'
        batch = json.loads((directory / 'status.json').read_text())
        check('main_run_complete_eight_cases', batch['state'] == 'complete' and len(batch['cases']) == 8 and all(row['passed'] for row in batch['checks']))
        for key, value in report.items():
            if value is False:
                check(key + '_remains_false', batch[key] is False)
        for table in ['inputs', 'outputs']:
            for filename, expected in batch[table].items():
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Conflicting inherited hash: ' + filename)
                if filename not in report['inputs']:
                    if hashlib.sha256((root / filename).read_bytes()).hexdigest() != expected:
                        raise RuntimeError('Changed evidence: ' + filename)
                    report['inputs'][filename] = expected
        check('all_inherited_source_and_output_hashes_match', True, len(report['inputs']))
        for path in directory.iterdir():
            if path.is_file():
                own(path, 'outputs')
                if path.name.startswith('executed-'):
                    check(path.name + '_immutable_source_matches', path.read_bytes() == (root / 'scripts' / path.name.removeprefix('executed-')).read_bytes())
                if path.suffix == '.npz':
                    with np.load(path, allow_pickle=False) as archive:
                        check(path.name + '_all_arrays_finite', all(np.isfinite(archive[key]).all() for key in archive.files))

        points, weights = np.polynomial.legendre.leggauss(64)
        times, time_weights = (points + 1) / 2, weights / 2

        def history_action(times, jacobian):
            lapse = (.83 + .02 * times) * jacobian
            mass = 1 + .01 * times
            momentum = .12 + .02 * times
            energy = .02 + .003 * times
            theta = .04 + .8 * times + .01 * times**2
            theta_rate = (.8 + .02 * times) * jacobian
            scalar = .02 + .03 * times
            multiplier = .07 + .01 * times
            prescribed = .02 + .03 * theta + .015 * theta**2
            clock = clock_factor(6.1, lapse, mass, momentum)
            return time_weights @ (energy * theta_rate - clock * energy + clock * multiplier * (scalar - prescribed))

        original = history_action(times, np.ones_like(times))
        transformed = times + .06 * np.sin(2 * np.pi * times)
        jacobian = 1 + .12 * np.pi * np.cos(2 * np.pi * times)
        check('finite_worldline_time_reparametrization', jacobian.min() > 0 and abs(original - history_action(transformed, jacobian)) < 1e-12)
        check('dropping_clock_density_jacobian_fails_covariance', abs(original - history_action(transformed, np.ones_like(times))) > 1e-8)

        for row in batch['cases']:
            branch, case = row['branch'], row['case']
            source_path = root / 'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03' / (branch + '_source_snapshot.npz')
            prepared_path = intake / 'annular-finite-width-boundary-cut-attempt01' / (branch + '_' + str(case) + '_prepared_collar.npz')
            history_path = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / ('canonical_N16_' + branch + '_sample0.npz')
            with np.load(source_path, allow_pickle=False) as archive:
                source = {key: archive[key].copy() for key in archive.files}
            with np.load(prepared_path, allow_pickle=False) as archive:
                prepared = {key: archive[key].copy() for key in archive.files}
            with np.load(history_path, allow_pickle=False) as archive:
                clock = archive['affine_clock'].copy()
                acceleration = float(archive['endpoint_acceleration'][-1])
            preparation = ClockReservoirPreparation(source, branch != 'GR', prepared['kinetic_seed'], float(prepared['outer_clock']), prepared['drive'], row['width'], row['shape'], reservoir_energy=row['reservoir_energy'])
            model = preparation.build(np.asarray(row['coefficients']))
            beginning = model.metric(np.array([model.edges[0]]))['U'][0]
            state = [beginning]
            max_root_error = 0.
            for lower, upper in zip(model.edges[:-1], model.edges[1:]):
                span = upper - lower

                def root_equation(fraction, values):
                    radius = lower + span * fraction
                    root_f = values[0]
                    density = model.energy_density(np.array([radius]))[0]
                    reservoir = model.reservoir_density(np.array([radius]))[0]
                    return [span * ((1 - root_f**2) / (2 * radius * root_f) - model.coupling * root_f * density / radius - model.coupling * reservoir / radius)]

                solution = solve_ivp(root_equation, (0., 1.), state, method='DOP853', rtol=3e-13, atol=3e-15, max_step=.1, dense_output=True)
                if not solution.success:
                    raise RuntimeError(solution.message)
                sample = np.linspace(0., 1., 7)
                error = abs(solution.sol(sample)[0] - model.metric(lower + span * sample)['U']).max()
                max_root_error = max(max_root_error, float(error))
                state = solution.y[:, -1]
            check(row['label'] + '_independent_U_equation_with_source_energy', max_root_error < 1e-11, max_root_error)

            with np.load(directory / (row['label'] + '_source_coupled_initial.npz'), allow_pickle=False) as archive:
                data = {key: archive[key].copy() for key in archive.files}
            changed_momentum = 1e-24j * data['P1']
            direct_mu_rate = -data['N'] * model.coupling**2 * data['U']**4 * changed_momentum * data['sigma'] / np.sqrt(1 - model.coupling**2 * data['U']**4 * changed_momentum**2)
            curvature_error = float(abs(direct_mu_rate.imag / 1e-24 - data['source_direct_mu2_term']).max())
            check(row['label'] + '_nonzero_direct_source_metric_second_derivative', curvature_error < 1e-12 and abs(data['source_direct_mu2_term']).max() > 1e-9, curvature_error)
            source_constraint_rate = (np.sqrt(1 - model.coupling**2 * data['U']**4 * changed_momentum**2) * (data['sigma'] + 1e-24j * data['sigma1'])).imag / 1e-24
            check(row['label'] + '_source_lapse_constraint_time_derivative', abs(source_constraint_rate - data['sigma1']).max() < 1e-12)
            mechanical_power = data['layer_rho'] * data['layer_q']
            reservoir_hamiltonian_rate = data['layer_N'] * row['log_lapse_rate'] * row['reservoir_energy'] + data['layer_N'] * data['layer_reservoir_E1']
            metric_power = data['layer_N'] * row['log_lapse_rate'] * row['reservoir_energy']
            check(row['label'] + '_lapse_work_not_confused_with_source_transfer', abs(reservoir_hamiltonian_rate + mechanical_power - metric_power).max() < 1e-12)
            check(row['label'] + '_free_failure_and_energy_cost_not_laundered', row['free_acceleration'] < -1 and row['reservoir_energy_rate_center'] < 0 and row['omit_source_energy_rate_error'] > .001)
            report['independent_cases'].append({'label': row['label'], 'U_equation_error': max_root_error, 'source_direct_mu2_derivative_error': curvature_error})
            if case == 0 and row['reservoir_energy'] == .001:
                empty_preparation = ClockReservoirPreparation(source, branch != 'GR', prepared['kinetic_seed'], float(prepared['outer_clock']), prepared['drive'], row['width'], row['shape'], reservoir_energy=0.)
                empty_model = empty_preparation.build(prepared['coefficients'])
                empty_driver = ProperClockDrive(empty_model, float(clock[1]), acceleration)
                empty = empty_driver.layer([0.])
                check(branch + '_zero_initial_energy_source_immediately_depletes_negative', empty['reservoir_E1'][0] < -.001)
                report['zero_budget_controls'].append({'branch': branch, 'initial_energy': 0., 'initial_energy_rate': float(empty['reservoir_E1'][0]), 'negative_energy_for_small_positive_time_if_differentiable': True, 'adopted': False})

        note = root / 'DERIVATION-20260913-proper-clock-source-action-and-live-initial-backreaction.md'
        for citation in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')):
            if citation.endswith(('.py', '.md', '.json', '.npz')):
                check('cited_path_exists_' + citation, (root / citation).is_file())
        own(note, 'outputs')
        for stem in ['annular_clock_reservoir_coupling', 'derive_annular_clock_reservoir_coupling', 'verify_annular_clock_reservoir_coupling']:
            path = root / 'scripts' / (stem + '_20260913.py')
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('three_new_scripts_compile_without_bytecode', True)
        protected = root.parent / 'formalization-workbench'
        check('protected_workbench_exists', protected.is_dir())
        start = datetime.fromisoformat('2026-09-13T10:28:20+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
        check('protected_mtime_changed_count_zero', not changed, changed)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        snapshot.write_bytes((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot, 'outputs')
        report.update({'state': 'complete', 'main_run_checks': len(batch['checks']), 'prepared_cases': len(batch['cases']),
                       'protected_changed_count': len(changed),
                       'maximum_C0': max(row['maximum_C0'] for row in batch['cases']),
                       'maximum_C1': max(row['maximum_C1'] for row in batch['cases']),
                       'maximum_acceleration_error': max(row['acceleration_error'] for row in batch['cases'])})
        save()
        print(json.dumps({key: report[key] for key in ['state', 'main_run_checks', 'prepared_cases', 'maximum_C0', 'maximum_C1', 'maximum_acceleration_error', 'protected_changed_count']} | {'seal_checks': len(report['checks'])}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
