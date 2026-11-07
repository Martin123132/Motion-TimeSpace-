from __future__ import annotations

import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re

import numpy as np
import psutil
from scipy.special import spherical_jn

from causal_system import ROOT, BRANCH, digest


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    checks, inputs = [], {}

    def check(name, passed, **details):
        checks.append({'name': name, 'passed': bool(passed), **details})
        assert passed, (name, details)

    def remember(path):
        inputs[str(Path(path).resolve())] = digest(path)

    reports = {}
    for label, script in [('spectrum', 'run_spectrum.py'), ('derivation', 'derive_causal.py'),
                          ('pulses', 'run_pulses.py'), ('time-domain-control', 'check_time_domain.py'),
                          ('fast-pulse-refinement', 'refine_fast_pulse.py')]:
        path = ROOT/f'results/{label}/status.json'
        report = read_json(path)
        reports[label] = report
        check(f'{label}_complete', report['state'] == 'complete')
        check(f'{label}_script_hash', report['script_sha256'] == digest(ROOT/script))
        for source, expected in report.get('input_hashes', {}).items():
            check(f'{label}_source_{source}', Path(source).is_file() and digest(source) == expected)
            remember(source)
        remember(path)
    check('twenty_four_exact_identities', reports['derivation']['exact_checks'] == 24
          and len(reports['derivation']['checks']) == 24 and all(row['passed'] for row in reports['derivation']['checks']))
    spectrum = reports['spectrum']
    check('three_body_meshes_and_flat_control', [row['name'] for row in spectrum['rows']] == ['flat-64', 'body-64', 'body-128', 'body-256'])
    check('no_background_solve_or_mode_fit', spectrum['new_background_solves'] == spectrum['fitted_spectral_parameters'] == 0)
    ode = spectrum['independent_ODE_reference']
    error_rows = []
    for row in spectrum['rows']:
        name = row['name']
        path = ROOT/f'results/spectrum/{name}.npz'
        check(f'{name}_archive_hash', digest(path) == row['archive_sha256'])
        remember(path)
        with np.load(path, allow_pickle=False) as archive:
            model = {key: archive[key] for key in archive.files}
        check(f'{name}_finite_arrays', all(np.isfinite(value).all() for value in model.values()))
        eigenvalues, weights = model['eigenvalues'], model['coupling']**2
        check(f'{name}_positive_spectrum_gap', np.all(eigenvalues > row['gap_lower']) and row['positive_eigenvalues'])
        check(f'{name}_positive_kinetic_remainder', row['unresolved_kinetic_norm'] >= 0 and model['norm'] > np.sum(weights))
        check(f'{name}_orthonormal_modes', row['gram_error'] < 1e-10)
        check(f'{name}_eigen_residual', row['eigen_error'] < 1e-9)
        check(f'{name}_symmetric_forms', np.allclose(model['inertia'], model['inertia'].T, rtol=0, atol=1e-15)
              and np.allclose(model['stiffness'], model['stiffness'].T, rtol=0, atol=1e-12))
        for wave in row['responses']:
            frequency = wave['frequency_R']
            check(f'{name}_Schur_spectral_{frequency}', abs(wave['spectral_Y']-wave['direct_Y']) < 2e-9)
            check(f'{name}_Wronskian_norm_{frequency}', abs(wave['dY_ds']/(-wave['direct_norm'])-1) < 2e-8)
            check(f'{name}_periodic_energy_{frequency}', abs(wave['direct_energy_without_kappa_over_R']/
                  wave['Legendre_energy_without_kappa_over_R']-1) < 2e-9)
            squared = frequency**2
            quartic_remainder = squared**3*np.sum(weights/(eigenvalues*(eigenvalues-squared)))
            bound = squared**3*float(model['moment'])/(row['gap_lower']-squared)
            check(f'{name}_quartic_spectral_bound_{frequency}', 0 < quartic_remainder <= bound)
        if row['nominal'] == 0:
            check('flat_exact_static_and_inertia', abs(row['static_impedance']/3-1) < 1e-10 and abs(row['norm']*7-1) < 1e-10)
            check('flat_exact_quartic_moment', abs(row['moment']*441-1) < 1e-8)
            check('flat_Bessel_first_eigenvalue', abs(eigenvalues[0]/row['flat_exact_first_eigenvalue']-1) < 1e-7)
            for wave in row['responses']:
                frequency = wave['frequency_R']
                exact = 1+frequency*spherical_jn(2, frequency, derivative=True)/spherical_jn(2, frequency)
                check(f'flat_Bessel_Y_{frequency}', abs(wave['spectral_Y']-exact) < 2e-9)
        else:
            static = ode['static']
            errors = {'name': name, 'Y0': abs(row['static_impedance']/static['Y']-1),
                      'I': abs(row['norm']/static['I_over_R']-1),
                      'J1': abs(row['moment']/(-static['Y_frequency_fourth_coefficient'])-1),
                      'Y_frequency_maximum': max(abs(wave['spectral_Y']/reference['Y']-1)
                                                 for wave, reference in zip(row['responses'], ode['waves']))}
            error_rows.append(errors)
            check(f'{name}_independent_ODE', max(value for key, value in errors.items() if key != 'name') < 2e-8,
                  errors={key: value for key, value in errors.items() if key != 'name'})
    first_values = [row['first_five_eigenvalues'][0] for row in spectrum['rows'][1:]]
    check('first_eigenvalue_mesh_convergence', first_values[0] > first_values[1] > first_values[2]
          and (first_values[1]-first_values[2]) < (first_values[0]-first_values[1])/8)
    pulses = reports['pulses']['rows']
    check('eight_pulse_controls', len(pulses) == 8)
    all_samples = {}
    bound_floors = []
    for row in pulses:
        label = row['label']
        path = ROOT/f'results/pulses/{label}.npz'
        check(f'{label}_hash', digest(path) == row['archive_sha256'])
        remember(path)
        with np.load(path, allow_pickle=False) as archive:
            data = {key: archive[key] for key in archive.files}
        all_samples[label] = data
        check(f'{label}_finite_and_increasing', all(np.isfinite(value).all() for value in data.values()) and np.all(np.diff(data['time']) > 0))
        check(f'{label}_positive_storage', row['kinetic_remainder'] > 0 and row['energy_minimum'] >= -1e-15*row['energy_maximum'])
        check(f'{label}_work_identity', row['instantaneous_work_identity_error'] < 1e-12)
        check(f'{label}_integrated_work', row['work_integral_error_over_peak_energy'] < 2e-8)
        check(f'{label}_free_storage_constant', row['post_pulse_energy_relative_drift'] < 1e-12)
        check(f'{label}_initial_modes_zero', row['initial_mode_amplitude'] == row['initial_mode_velocity'] == 0)
        check(f'{label}_derived_term_improves', row['quartic_traction_error_over_peak'] < row['quadratic_traction_error_over_peak'])
        check(f'{label}_global_causal_remainder_bound', row['projected_quartic_error_maximum'] <= row['causal_quartic_remainder_bound_maximum'])
        if row['duration'] == 64:
            check(f'{label}_tiny_final_energy_not_resolved_by_work', row['energy_after_pulse'] <
                  row['energy_maximum']*row['work_integral_error_over_peak_energy'])
            bound_floors.append(label)
    mode_differences = []
    for duration in [4, 16, 64]:
        short = all_samples[f'cells256-T{duration}-n4097-m64']
        long = all_samples[f'cells256-T{duration}-n8193-m128']
        check(f'pulse_nested_times_{duration}', np.array_equal(short['time'], long['time'][::2]))
        difference = np.abs(short['p']-long['p'][::2])
        bound = short['modal_tail_bound']+long['modal_tail_bound'][::2]
        floor = 2e-12*np.max(np.abs(long['p']))
        check(f'modal_tail_history_bound_{duration}', np.all(difference <= bound+floor))
        relative = float(np.max(difference)/np.max(np.abs(long['p'])))
        if duration == 4:
            coarse_fast_difference = relative
            check('fast_coarse_cut_requires_refinement', relative > 2e-7, relative=relative)
        else:
            mode_differences.append(relative)
            check(f'modal_cut_convergence_{duration}', relative < 2e-7, relative=relative)
    refined = reports['fast-pulse-refinement']
    refined_path = ROOT/'results/fast-pulse-refinement/pulse.npz'
    check('refined_fast_archive_hash', digest(refined_path) == refined['archive_sha256'])
    remember(refined_path)
    with np.load(refined_path, allow_pickle=False) as archive:
        refined_samples = {key: archive[key] for key in archive.files}
    previous_samples = all_samples['cells256-T4-n16385-m128']
    refined_difference = float(np.max(np.abs(refined_samples['p']-previous_samples['p']))/np.max(np.abs(refined_samples['p'])))
    check('refined_fast_modal_gate', refined_difference < 2e-7
          and refined_difference < coarse_fast_difference/4, relative=refined_difference)
    mode_differences.append(refined_difference)
    check('refined_fast_work_and_storage', refined['row']['work_integral_error_over_peak_energy'] < 2e-8
          and refined['row']['instantaneous_work_identity_error'] < 1e-12 and refined['row']['energy_minimum'] >= 0)
    coarse_time = next(row for row in pulses if row['label'] == 'cells256-T4-n8193-m128')
    fine_time = next(row for row in pulses if row['label'] == 'cells256-T4-n16385-m128')
    check('independent_time_quadrature_refinement', fine_time['work_integral_error_over_peak_energy'] <
          coarse_time['work_integral_error_over_peak_energy']/8)
    mesh_coarse = all_samples['cells128-T16-n8193-m128']
    mesh_fine = all_samples['cells256-T16-n8193-m128']
    mesh_error = float(np.max(np.abs(mesh_coarse['p']-mesh_fine['p']))/np.max(np.abs(mesh_fine['p'])))
    check('pulse_spatial_refinement', mesh_error < 2e-7, relative=mesh_error)
    control = reports['time-domain-control']
    check('direct_ODE_archive_hash', digest(ROOT/'results/time-domain-control/direct-ODE.npz') == control['archive_sha256'])
    integration = control['integration_control']
    check('no_response_before_switch_on_computed', integration['initial_time'] < integration['source_switch_on_time']
          and integration['pre_forcing_maximum_state'] == 0)
    check('independent_time_integration', max(integration[key] for key in ['energy_solution_difference_over_peak',
          'traction_solution_difference_over_peak', 'ODE_work_energy_error_over_peak']) < 2e-8)
    check('three_high_precision_end_controls', len(control['high_precision_controls']) == 3
          and all(row['binary64_relative_error'] < 2e-8 for row in control['high_precision_controls']))
    csv_path = ROOT/'results/pulses/pulse-summary.csv'
    with csv_path.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        fields, csv_rows = reader.fieldnames, list(reader)
    check('CSV_schema', len(csv_rows) == len(pulses) and len(fields) == len(set(fields))
          and all(None not in row and all(value is not None and value != '' for value in row.values()) for row in csv_rows))
    for actual, expected in zip(csv_rows, pulses):
        for key, value in expected.items():
            assert actual[key] == value if isinstance(value, str) else float(actual[key]) == value, key
    check('CSV_values_match', True)
    remember(csv_path)
    references = read_json(ROOT/'references.json')
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    check('primary_source_urls_recorded', all(row['url'] in prose for row in references['sources']))
    remember(ROOT/'references.json')
    for relative in sorted(set(re.findall(r'`([^`\n]+\.(?:py|json|npz|csv|md))`', prose))):
        if relative in {'results/validation/status.json', 'results/stage-integrity.json'}:
            continue
        path = (ROOT/relative).resolve()
        check(f'cited_local_path_{relative}', path.is_file())
        remember(path)
    check('scope_and_resolution_disclosed', all(phrase in prose for phrase in ['NOT a radiating', 'NOT band-limited',
          'below the final-work', 'not a material Love', 'computed inspiral trajectory', 'Einstein-Hilbert']))
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    check('no_python_cache', not list(ROOT.rglob('__pycache__')))
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'checks': checks, 'exact_checks': 24, 'input_hashes': inputs,
              'compiled_scripts': compiled, 'source_urls': [row['url'] for row in references['sources']],
              'independent_ODE_errors': error_rows, 'maximum_modal_cut_traction_difference': max(mode_differences),
              'fast_coarse_cut_failed_gate_difference': coarse_fast_difference,
              'pulse_spatial_traction_difference': mesh_error,
              'small_final_energy_unresolved_by_work_quadrature': bound_floors,
              'periodic_boundary_energy_identity_recovered': True,
              'full_evolving_binary_or_exterior_pulse_solved': False,
              'new_background_solves': 0, 'fitted_spectral_parameters': 0}
    destination = ROOT/'results/validation/status.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'exact_checks': 24,
                      'maximum_modal_cut_difference': max(mode_differences), 'pulse_spatial_difference': mesh_error,
                      'ODE_errors': error_rows}))


if __name__ == '__main__':
    main()
