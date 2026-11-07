from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import psutil
from scipy.interpolate import PPoly

from orbit_system import ROOT, PARENT, ResponseProblem, static_master_basis, reference_wave, jumps, determinant, action_from_wave
from response_system_v2 import DynamicProblem


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def strict_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            assert key not in result, (path, key)
            result[key] = value
        return result

    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def decode(value):
    return complex(value['real'], value['imaginary'])


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation'
    output.mkdir(exist_ok=False)
    reports = {name: strict_json(ROOT/f'results/{name}/status.json') for name in ['derivation', 'far-action', 'fine', 'control', 'balance']}
    checks = []

    def check(name, passed):
        assert passed, name
        checks.append({'name': name, 'passed': True})

    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    for name, report in reports.items():
        check('script_owned_'+name, report['state'] == 'complete' and report['script_sha256'] in script_hashes)
    for name in ['derivation', 'far-action', 'balance']:
        check('all_symbolic_'+name, all(row['passed'] for row in reports[name]['checks']))
    symbolic_count = sum(len(reports[name]['checks']) for name in ['derivation', 'far-action', 'balance'])
    check('symbolic_count', symbolic_count == 28)
    profile = ResponseProblem().profile
    replay_errors, action_errors, boundary_errors, lambda_replays = [], [], [], []
    archived = 0
    for label in ['fine', 'control']:
        report = reports[label]
        check('current_system_'+label, report['system_sha256'] == digest(ROOT/'orbit_system.py'))
        for path, expected in report['parent_input_hashes'].items():
            check('unchanged_parent_'+label+'_'+Path(path).parent.name, digest(path) == expected)
        rows = report['derivative_rows']
        all_archives = [{'archive': 'static.npz', 'sigma': 0.}]+[{'archive': row['archive'], 'sigma': row['wave']['sigma'], 'row': row} for row in rows]
        settings = report['settings']
        for entry in all_archives:
            path = ROOT/f'results/{label}'/entry['archive']
            with np.load(path, allow_pickle=False) as arrays:
                check('finite_archive_'+label+'_'+entry['archive'], all(np.all(np.isfinite(arrays[key])) for key in arrays.files))
                spline = PPoly(arrays['spline_coefficients'], arrays['spline_knots'])
                solution = SimpleNamespace(sol=spline, p=arrays['parameters'].copy())
                check('archive_frequency_'+label+'_'+entry['archive'], complex(arrays['sigma']) == entry['sigma'])
            problem = DynamicProblem(profile, complex(entry['sigma']), settings['distance'], settings['interior_tolerance'])
            boundary_error = float(max(abs(problem.boundary(spline(spline.x[0]), spline(spline.x[-1]), solution.p))))
            boundary_errors.append(boundary_error)
            _, _, master, derivative = problem.surface(solution)
            inside = np.array([1., derivative/master])
            archived += 1
            if entry['sigma'] == 0:
                coefficients = np.linalg.solve(static_master_basis(report['radius'], report['mass'], report['radius']), inside)
                value = report['radius']**5*coefficients[1]/(3*coefficients[0])
                lambda_replays.append(abs(value/report['tidal_lambda']-1))
                continue
            row = entry['row']
            wave = row['wave']
            check('interior_ODE_residual_'+label+'_'+entry['archive'], wave['interior_maximum_residual'] <= 1.01*settings['interior_tolerance'])
            reference = reference_wave(wave['orbit'], wave['mass'], wave['radius'], settings['far_phase'], settings['outer_order'],
                                       settings['horizon_epsilon'], settings['horizon_order'], settings['tolerance'])
            outgoing = reference['outgoing']
            horizon = reference['horizon']
            jump_a, jump_b, _ = jumps(wave['orbit'], wave['mass'], 2)
            out_overlap = jump_b*outgoing[wave['orbit']][0]-jump_a*outgoing[wave['orbit']][1]
            in_overlap = jump_b*horizon[wave['orbit']][0]-jump_a*horizon[wave['orbit']][1]
            ratio = -determinant(inside, horizon[wave['radius']])/determinant(inside, outgoing[wave['radius']])*out_overlap/in_overlap
            replay_errors.append(abs(ratio/decode(wave['amplitude_ratio_minus_one'])-1))
            body_wronskian = determinant(inside, outgoing[wave['radius']])
            independent_pair_action = 3/(8*np.pi)*np.real(determinant(inside, horizon[wave['radius']])*out_overlap**2/(body_wronskian*reference['wronskian']))
            action_errors.append(abs(independent_pair_action/row['action_pair_per_particle_squared']-1))
            identical_reference_action = determinant(horizon[wave['radius']], horizon[wave['radius']])*out_overlap**2
            check('same_inner_boundary_zero_excess_'+label+'_'+entry['archive'], identical_reference_action == 0)
        check('new_interiors_count_'+label, len(all_archives) == report['new_interiors'] == 22)
        all_rows = report['rows']+rows
        check('metric_reconstruction_'+label, max(max(row['m0_metric_reciprocity_error'], row['pair_metric_reciprocity_error']) for row in all_rows) < 1e-12)
        check('positive_action_'+label, all(row['action_per_particle_squared'] > 0 for row in all_rows))
        wide = [row for row in report['rows'] if row['separation_over_radius'] >= 10]
        check('unfitted_first_PN_improves_'+label, all(row['first_PN_relative_error'] < row['leading_relative_error'] for row in wide))
        check('unfitted_first_PN_converges_'+label, all(first['first_PN_relative_error'] > second['first_PN_relative_error'] for first, second in zip(wide, wide[1:])))
        check('widest_action_coefficient_'+label, abs(wide[-1]['inferred_first_PN_action_coefficient']-4) < .01)
        check('widest_first_PN_accuracy_'+label, wide[-1]['first_PN_relative_error'] < 1e-6)
        check('static_mode_quarter_limit_'+label, abs(wide[-1]['static_mode_fraction']-.25) < 1e-4)
    check('all_saved_interiors_replayed', archived == 44)
    check('replayed_boundaries', max(boundary_errors) < 1e-7)
    check('replayed_static_lambda', max(lambda_replays) < 1e-10)
    check('replayed_physical_waves', max(replay_errors) < 1e-10)
    check('independent_source_action', max(action_errors) < 1e-10)
    precision, derivative_controls = [], []
    for first, second in zip(reports['fine']['rows'], reports['control']['rows']):
        check('matching_precision_positions_'+str(first['separation_over_radius']), abs(first['orbit']/second['orbit']-1) < 1e-14)
        precision.append(abs(first['action_per_particle_squared']/second['action_per_particle_squared']-1))
    for fine, control in zip(reports['fine']['derivatives'], reports['control']['derivatives']):
        for key in ['energy_per_particle_squared', 'angular_momentum_per_particle_squared', 'd_energy_d_log_omega_per_particle_squared']:
            step_error = abs(fine['estimates'][0][key]/fine['estimates'][1][key]-1)
            settings_error = abs(fine['estimates'][0][key]/control['estimates'][0][key]-1)
            check('derivative_step_'+str(fine['separation_over_radius'])+'_'+key, step_error < 1e-7)
            check('derivative_settings_'+str(fine['separation_over_radius'])+'_'+key, settings_error < 3e-7)
            derivative_controls.append({'separation_over_radius': fine['separation_over_radius'], 'quantity': key,
                                        'step_relative_difference': step_error, 'settings_relative_difference': settings_error})
    check('action_precision_controls', max(precision) < 3e-7)
    balance = reports['balance']
    for path, expected in balance['input_hashes'].items():
        check('balance_input_'+Path(path).parent.name, digest(path) == expected)
    algebra = balance['nonlinear_algebra_controls']
    check('independent_Newton_first_law', max(row['first_law_relative_residual'] for row in algebra) < 1e-12)
    for mass_ratio in [.001, .01]:
        rows = [row for row in algebra if row['mass_ratio'] == mass_ratio]
        for key in ['chirp_linear_remainder', 'energy_linear_remainder']:
            check('quadratic_remainder_'+str(mass_ratio)+'_'+key, all(abs(second[key]/first[key]-.25) < .002 for first, second in zip(rows, rows[1:])))
    check('analytic_numeric_phase', max(row['quadrature_relative_error'] for row in balance['phase_illustrations']) < 1e-10)
    check('phase_illustrations_small_tidal_chirp', max(row['endpoint_leading_chirp_fraction'] for row in balance['phase_illustrations']) < 5e-5)
    provenance = strict_json(ROOT/'sources/provenance.json')
    check('source_script', provenance['script_sha256'] == digest(ROOT/'acquire_sources.py'))
    for index, row in enumerate(provenance['sources']):
        check('source_pdf_'+str(index), digest(row['path']) == row['sha256'])
        check('source_renders_'+str(index), all(Path(path).is_file() for path in row['selected_page_renders']))
    table_rows = []
    for group in reports['fine']['derivatives']:
        table_rows.append({'separation_over_radius': group['separation_over_radius'], **group['estimates'][0]})
    csv_path = ROOT/'results/conservative-orbit.csv'
    with csv_path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(table_rows[0]))
        writer.writeheader()
        writer.writerows(table_rows)
    with csv_path.open(newline='', encoding='utf-8') as stream:
        replay = list(csv.DictReader(stream))
    check('CSV_roundtrip', len(replay) == len(table_rows) and all(None not in row and all(np.isfinite(float(value)) for value in row.values()) for row in replay))
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    check('no_python_cache', not list(ROOT.rglob('__pycache__')))
    inputs = {path.relative_to(ROOT).as_posix(): digest(path) for path in ROOT.rglob('*')
              if path.is_file() and path.suffix in ['.json', '.py', '.npz', '.pdf', '.csv'] and output not in path.parents}
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'checks': checks, 'input_hashes': inputs,
              'symbolic_checks': symbolic_count, 'new_saved_interiors_replayed': archived,
              'inherited_wave_rows_reconstructed': len(reports['fine']['rows'])+len(reports['control']['rows']),
              'maximum_wave_replay_error': float(max(replay_errors)), 'maximum_independent_action_replay_error': float(max(action_errors)),
              'maximum_boundary_replay_error': max(boundary_errors), 'maximum_action_precision_difference': max(precision),
              'derivative_controls': derivative_controls, 'widest_orbit_result': reports['fine']['rows'][-1],
              'compiled_scripts': compiled, 'phase_illustrations': balance['phase_illustrations'],
              'scope': 'Finite numerical controls and exact algebra within the documented polar-quadrupole/weak-field truncations, not total physical error bounds.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({key: report[key] for key in ['state', 'symbolic_checks', 'new_saved_interiors_replayed', 'maximum_wave_replay_error',
                       'maximum_independent_action_replay_error', 'maximum_action_precision_difference', 'widest_orbit_result']}))
    print(json.dumps({'validation_checks': len(checks), 'derivative_controls': derivative_controls}))


if __name__ == '__main__':
    main()
