from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from scipy.integrate import simpson

from transient import ROOT, PARENT, body, dependencies, digest, read_json, save, modest_process


def main():
    modest_process()
    checks, inputs = [], dependencies()

    def check(name, passed, detail=None):
        checks.append(dict(name=name, passed=bool(passed), detail=detail))
        assert passed, (name, detail)

    reports = {}
    for label in ['checked-coarse', 'checked-fine', 'packet', 'derivation']:
        path = ROOT/'results'/label/'status.json'
        report = read_json(path)
        reports[label] = report
        check(label+' completed', report['state'] == 'complete')
        script = ROOT/('solve_packet.py' if label.startswith('checked') else
                      'analyze_packet.py' if label == 'packet' else 'derive_energy.py')
        check(label+' script hash', digest(script) == report['script_sha256'])
        check(label+' input hashes', all(digest(source) == expected for source, expected in report['input_hashes'].items()))
        check(label+' output hashes', all(digest(path.parent/source) == expected for source, expected in report.get('output_hashes', {}).items()))
        inputs[str(path)] = digest(path)
    exact = reports['derivation']
    check('28 exact identities', len(exact['checks']) == exact['exact_checks'] == 28
          and all(row['passed'] and row['residual'] == '0' for row in exact['checks']))
    parent_validation = read_json(PARENT/'results/validation/status.json')
    model = body()
    check('parent-owned positive inertia and stiffness', model['inertia'] > 0 and model['stiffness'] > 0)
    check('whole pulse spectral support inside verified parent band',
          parent_validation['omega_R_range'][0] < .006 < .03 < parent_validation['omega_R_range'][1])
    for label in ['checked-coarse', 'checked-fine']:
        archive_path = ROOT/'results'/label/'transfer.npz'
        archive = np.load(archive_path)
        inputs[str(archive_path)] = digest(archive_path)
        controls = reports[label]['maximum_controls']
        for key in ['derivative_jump_error', 'surface_boundary_error', 'outgoing_series_current_error',
                    'raw_detector_current_error', 'outgoing_reconstruction_error', 'optical_error',
                    'detector_optical_error']:
            check(label+' '+key, controls[key] < 1e-8, controls[key])
        check(label+' unit pulse normalization', abs(np.sum(archive['frequency_weights']*archive['amplitudes'])-1) < 1e-12)
        check(label+' finite transfer fields', np.isfinite(archive['green']).all() and np.isfinite(archive['infinity']).all())
    packet = reports['packet']
    for label in ['checked-coarse', 'checked-fine']:
        metrics = packet['metrics'][label]
        check(label+' differential sourced balance', metrics['differential_balance_relative'] < 1e-9, metrics['differential_balance_relative'])
        check(label+' finite-window net balance', metrics['net_balance_over_emitted_energy'] < 1e-7, metrics['net_balance_over_emitted_energy'])
        check(label+' independent infinity current normalization', metrics['spectral_balance_relative'] < 1e-10)
        check(label+' detector spectral balance', metrics['detector_spectral_balance_relative'] < 1e-8)
        check(label+' windowed source work recovers spectral work', metrics['work_window_error'] < 1e-7)
        check(label+' windowed detector radiation recovers spectrum', metrics['detector_window_error'] < 1e-7)
        check(label+' windowed infinity radiation recovers spectrum', metrics['infinity_window_error'] < 1e-7)
        check(label+' negligible endpoint stored energy', metrics['endpoint_energy_fraction'] < 1e-14)
        check(label+' small pulse endpoint amplitude', metrics['endpoint_source_amplitude'] < 1e-8)
        check(label+' boundary power exchange', metrics['surface_exchange_relative'] < 1e-12)
        check(label+' omitting boundary energy fails', metrics['missing_surface_relative'] > 1e4*metrics['differential_balance_relative']
              and metrics['missing_surface_relative'] > 1e-5, metrics['missing_surface_relative'])
        check(label+' reversing flux fails', metrics['reversed_flux_relative'] > 1e4*metrics['differential_balance_relative'],
              metrics['reversed_flux_relative'])
        check(label+' reversing source fails', metrics['reversed_source_relative'] > 1.)
        archive_path = ROOT/'results/packet'/(label+'-time.npz')
        archive = np.load(archive_path)
        inputs[str(archive_path)] = digest(archive_path)
        check(label+' nonnegative stored energy and infinity flux',
              all(np.min(archive[key]) >= 0 for key in ['bulk', 'surface', 'surface_kinetic', 'surface_potential', 'radiation']))
        check(label+' energy-window balance independently recomputed',
              abs((archive['bulk'][-1]+archive['surface'][-1]-archive['bulk'][0]-archive['surface'][0])
                  -simpson(archive['work']-archive['flux'], x=archive['time']))/metrics['infinity_spectral'] < 1e-7)
    ratio = packet['metrics']['checked-coarse']['cumulative_balance_over_peak_energy']/packet['metrics']['checked-fine']['cumulative_balance_over_peak_energy']
    check('cumulative Simpson error refines at fourth order', 14. < ratio < 18., ratio)
    check('fine cumulative balance resolved', packet['metrics']['checked-fine']['cumulative_balance_over_peak_energy'] < 5e-8)
    check('transfer and spatial refinement', max(packet['waveform_refinement'].values()) < 1e-8, packet['waveform_refinement'])
    check('net work refinement', max(packet['metric_refinement'].values()) < 1e-7, packet['metric_refinement'])
    archived_source = ROOT/'attempts/transient-v1.py'
    for old_label, corrected in [('coarse', 'checked-coarse'), ('fine', 'checked-fine')]:
        attempt_path = ROOT/'results'/old_label/'status.json'
        attempt = read_json(attempt_path)
        check(old_label+' superseded diagnostic source archived',
              attempt['input_hashes'][str(ROOT/'transient.py')] == digest(archived_source))
        old_archive = np.load(attempt_path.parent/'transfer.npz')
        corrected_archive = np.load(ROOT/'results'/corrected/'transfer.npz')
        check(old_label+' diagnostic repair leaves all numerical arrays identical',
              old_archive.files == corrected_archive.files and
              all(np.array_equal(old_archive[key], corrected_archive[key]) for key in old_archive.files))
        expected_factor_error = max(abs(row['frequency']-1) for row in attempt['diagnostics'])
        check(old_label+' original optical diagnostic error accounted for',
              abs(attempt['maximum_controls']['optical_error']-expected_factor_error) < 1e-12)
        inputs[str(attempt_path)] = digest(attempt_path)
        inputs[str(attempt_path.parent/'transfer.npz')] = digest(attempt_path.parent/'transfer.npz')
    csv_path = ROOT/'results/packet/energy-ledger.csv'
    with csv_path.open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        check('CSV schema and row count', len(rows) == packet['csv_rows'] == 12001
              and len(reader.fieldnames) == len(set(reader.fieldnames))
              and all(None not in row and None not in row.values() for row in rows))
        check('CSV finite values', all(np.isfinite(float(value)) for row in rows for value in row.values()))
    inputs[str(csv_path)] = digest(csv_path)
    check('no bytecode cache', not list(ROOT.rglob('__pycache__')))
    parent_seal = read_json(PARENT/'results/stage-integrity.json')
    check('all stage42 payload hashes unchanged',
          all(digest(PARENT/source) == expected for source, expected in parent_seal['file_hashes'].items()))
    directory = ROOT/'results/validation'
    directory.mkdir(parents=True, exist_ok=False)
    result = save(directory, Path(__file__), dict(checks=checks, input_hashes=inputs, exact_checks=28,
        validation_checks=len(checks), csv_rows=len(rows), coefficient_source=parent_validation['coefficient_s2'],
        model=model, fine_metrics=packet['metrics']['checked-fine'], cumulative_refinement_ratio=ratio,
        spectral_window=[.006, .030], observation_window=[-6000., 6000.],
        source='Prescribed canonical master-shell probe; not a derived companion stress history.',
        exploratory_runs='coarse and fine are superseded: extra frequency factor in optical DIAGNOSTIC only; arrays unchanged.',
        historical_source_hash_substitution={str(ROOT/'transient.py'):str(archived_source)},
        primary_pdfs=parent_seal['primary_pdfs'], source_urls=parent_seal['source_urls'],
        scope='Energy balance of the inherited polar exterior with the stage42 low-frequency boundary action and prescribed probe.'))
    print(dict(state=result['state'], exact_checks=28, validation_checks=len(checks)), flush=True)


if __name__ == '__main__':
    main()

