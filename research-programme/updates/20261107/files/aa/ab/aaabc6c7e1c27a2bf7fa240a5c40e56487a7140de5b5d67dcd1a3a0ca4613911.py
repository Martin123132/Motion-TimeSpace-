from __future__ import annotations

import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re

import numpy as np
import psutil
from scipy.integrate import quad

from wave_network import ROOT, digest, forcing
from spectral_work import source_transform


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    checks, inputs, reports = [], {}, {}

    def check(name, passed, **details):
        checks.append({'name': name, 'passed': bool(passed), **details})
        assert passed, (name, details)

    def remember(path):
        inputs[str(Path(path).resolve())] = digest(path)

    for label, script in [('coarse', 'run_network.py'), ('fine', 'run_network.py'), ('far', 'run_network.py'),
                          ('time-control', 'run_network.py'), ('derivation', 'derive_balance.py'),
                          ('spectral-work', 'spectral_work.py'), ('analysis', 'analyze_network.py')]:
        path = ROOT/f'results/{label}/status.json'
        report = read_json(path)
        reports[label] = report
        check(f'{label}_complete', report['state'] == 'complete')
        check(f'{label}_script_hash', report['script_sha256'] == digest(ROOT/script))
        for source, expected in report.get('input_hashes', {}).items():
            check(f'{label}_input_{source}', Path(source).is_file() and digest(source) == expected)
            remember(source)
        remember(path)
    derivation = reports['derivation']
    check('thirteen_exact_identities', derivation['exact_checks'] == 13 and len(derivation['checks']) == 13
          and all(row['passed'] for row in derivation['checks']))
    peak_balance, peak_optical = [], []
    for label in ['coarse', 'fine', 'far', 'time-control']:
        report = reports[label]
        check(f'{label}_two_fair_branches', [row['kind'] for row in report['rows']] == ['body', 'BH']
              and report['rows'][0]['source_tortoise'] == report['rows'][1]['source_tortoise']
              and report['rows'][0]['compactness'] == report['rows'][1]['compactness'])
        check(f'{label}_no_new_fits_or_background', report['new_background_solves'] == report['new_fitted_parameters'] == 0)
        for row in report['rows']:
            kind = row['kind']
            path = ROOT/f'results/{label}/{kind}.npz'
            check(f'{label}_{kind}_hash', digest(path) == row['archive_sha256'])
            remember(path)
            with np.load(path, allow_pickle=False) as archive:
                data = {key: archive[key] for key in archive.files}
            check(f'{label}_{kind}_finite_time_series', all(np.isfinite(value).all() for value in data.values())
                  and np.all(np.diff(data['time']) > 0))
            check(f'{label}_{kind}_zero_pre_forcing_field', np.max(np.abs(data['source_field'][data['time'] <= 2.])) == 0
                  and np.max(np.abs(data['interface_field'][data['time'] <= 2.])) == 0)
            check(f'{label}_{kind}_positive_storage', np.min(data['interior_energy']) >= 0 and np.min(data['exterior_energy']) >= 0)
            check(f'{label}_{kind}_passive_boundaries', np.all(np.diff(data['outer_loss']) >= 0)
                  and np.all(np.diff(data['horizon_loss']) >= 0))
            peak = np.max(np.abs(data['work']))
            residual = data['work']-data['interior_energy']-data['exterior_energy']-data['outer_loss']-data['horizon_loss']
            replay = float(np.max(np.abs(residual))/peak)
            peak_balance.append(replay)
            check(f'{label}_{kind}_total_work_replay', replay < 2e-10
                  and abs(replay-row['total_balance_error_over_peak_work']) < 1e-20)
            check(f'{label}_{kind}_regional_work', row['interior_balance_error_over_peak_work'] < 2e-10
                  and row['exterior_balance_error_over_peak_work'] < 2e-10)
            check(f'{label}_{kind}_correct_horizon_branch', row['final_horizon_loss'] == 0 if kind == 'body' else row['final_horizon_loss'] > 0)
            for harmonic in row['harmonic_rows']:
                peak_optical.append(harmonic['optical_identity_relative_error'])
                check(f'{label}_{kind}_harmonic_passivity_{harmonic["frequency_R"]}',
                      harmonic['source_work'] > 0 and harmonic['outer_loss'] > 0 and harmonic['horizon_loss'] >= 0
                      and harmonic['optical_identity_relative_error'] < 2e-9)
            if kind == 'body':
                wrong = row['wrong_surface_contact_control']
                reference = row['continuum_rows'][1]
                error = abs(complex(wrong['G_real'], wrong['G_imag'])-
                            complex(reference['finite_G_real'], reference['finite_G_imag']))/abs(
                            complex(reference['finite_G_real'], reference['finite_G_imag']))
                check(f'{label}_wrong_surface_contact_rejected_independently', error > .01
                      and wrong['optical_identity_relative_error'] < 2e-9, relative_response_error=error)
    analysis = reports['analysis']
    for row in analysis['difference_budgets']:
        label = row['label']
        check(f'{label}_difference_budget', row['difference_budget_error_over_peak_difference_work'] < 2e-8)
        check(f'{label}_horizon_omission_fails', row['final_error_if_horizon_omitted'] >
              50*max(row['final_budget_error'], 1e-18))
        check(f'{label}_instantaneous_optical_shortcut_fails', row['maximum_storage_omission_error_over_peak_difference_work'] > 1)
    for row in analysis['harmonic_controls']:
        label, frequency = row['label'], row['frequency_R']
        check(f'{label}_{frequency}_independent_continuum_response', row['maximum_FE_to_finite_ODE_relative_error'] < 5e-7
              and row['difference_FE_to_finite_ODE_relative_error'] < 5e-4)
        check(f'{label}_{frequency}_finite_boundary_not_claimed_infinity', row['maximum_finite_to_infinite_relative_difference'] > 0
              and row['maximum_finite_to_infinite_dissipative_relative_difference'] > 0)
    infinity_dissipative_error = max(row['maximum_finite_to_infinite_dissipative_relative_difference'] for row in analysis['harmonic_controls'])
    check('finite_boundary_dissipative_error_exposed', infinity_dissipative_error > .01)
    for row in analysis['refinements']:
        label = f'{row["first"]}_{row["second"]}'
        check(f'{label}_waveform_and_work_refinement',
              max(row['body_work_relative_difference'], row['BH_work_relative_difference'],
                  row['body_source_waveform_difference_over_peak_before_echo'],
                  row['BH_source_waveform_difference_over_peak_before_echo'], row['difference_work_relative_difference']) < 1e-3)
    far = analysis['refinements'][-1]
    check('pre_echo_work_insensitive_to_extraction_radius', far['body_work_relative_difference'] < 1e-9
          and far['BH_work_relative_difference'] < 1e-9 and far['difference_work_relative_difference'] < 1e-7)
    spectral = reports['spectral-work']
    first, second = spectral['settings']
    check('spectral_order_and_cutoff_varied', first['order_per_band'] == 24 and second['order_per_band'] == 36
          and first['cutoff_frequency_R'] == 9 and second['cutoff_frequency_R'] == 12)
    check('spectral_quadrature_agreement', max(abs(first[key]/second[key]-1)
          for key in ['body_work', 'BH_work', 'difference_work']) < 1e-7)
    check('spectral_tail_extension_small_not_a_bound', abs(second['bands'][-1]['body_work']/second['body_work']) < 1e-10
          and abs(second['bands'][-1]['difference_work']/second['difference_work']) < 1e-8)
    transform_errors = []
    for frequency in [.3, .6, 1.2, 5.]:
        real = quad(lambda time: forcing(time)*np.cos(frequency*(time-2)), 2., 14., epsabs=1e-13, epsrel=1e-12)[0]
        imaginary = quad(lambda time: forcing(time)*np.sin(frequency*(time-2)), 2., 14., epsabs=1e-13, epsrel=1e-12)[0]
        error = abs(source_transform(frequency)-complex(real, imaginary))
        transform_errors.append(error)
        check(f'independent_source_transform_{frequency}', error < 1e-11)
    parseval = analysis['continuum_Parseval_controls']
    check('independent_true_infinity_work_agreement', max(parseval[-1][key] for key in
          ['body_work_relative_error', 'BH_work_relative_error', 'difference_work_relative_error']) < 1e-5)
    for key in ['body_work_relative_error', 'BH_work_relative_error', 'difference_work_relative_error']:
        check(f'time_refinement_improves_{key}', parseval[1][key] < parseval[0][key]/2
              and parseval[2][key] < parseval[1][key]/2)
    pairs = [('difference-budgets', 'difference_budgets'), ('harmonic-controls', 'harmonic_controls'),
             ('refinements', 'refinements'), ('continuum-Parseval', 'continuum_Parseval_controls')]
    for filename, key in pairs:
        path = ROOT/f'results/analysis/{filename}.csv'
        with path.open(encoding='utf-8', newline='') as handle:
            reader = csv.DictReader(handle)
            fields, rows = reader.fieldnames, list(reader)
        check(f'{filename}_CSV_schema', len(rows) == len(analysis[key]) and len(fields) == len(set(fields))
              and all(None not in row and all(value is not None and value != '' for value in row.values()) for row in rows))
        for actual, expected in zip(rows, analysis[key]):
            for name, value in expected.items():
                assert actual[name] == value if isinstance(value, str) else float(actual[name]) == value
        check(f'{filename}_CSV_values', True)
        remember(path)
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    for relative in sorted(set(re.findall(r'`([^`\n]+\.(?:py|json|npz|csv|md))`', prose))):
        if relative in {'results/validation/status.json', 'results/stage-integrity.json'}:
            continue
        path = (ROOT/relative).resolve()
        check(f'cited_local_path_{relative}', path.is_file())
        remember(path)
    check('scope_and_method_limitations_disclosed', all(phrase in prose for phrase in
          ['externally powered', 'NOT the exact', 'structural property', 'about2%', 'not a rigorous bound',
           'conserved', 'Einstein-Hilbert']))
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    check('no_python_cache', not list(ROOT.rglob('__pycache__')))
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'checks': checks, 'exact_checks': 13, 'input_hashes': inputs,
              'compiled_scripts': compiled, 'maximum_total_discrete_balance_error': max(peak_balance),
              'maximum_harmonic_optical_error': max(peak_optical),
              'maximum_finite_boundary_dissipative_relative_difference': infinity_dissipative_error,
              'finest_true_infinity_work_errors': parseval[-1],
              'maximum_source_Fourier_quadrature_error': max(transform_errors),
              'new_background_solves': 0, 'new_fitted_parameters': 0,
              'orbital_stress_source_or_chirp_derived': False,
              'finite_boundary_is_exact_transparent_boundary': False}
    destination = ROOT/'results/validation/status.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'exact_checks': 13,
                      'maximum_balance_error': max(peak_balance), 'finite_boundary_flux_error': infinity_dissipative_error,
                      'finest_Parseval_errors': parseval[-1]}))


if __name__ == '__main__':
    main()
