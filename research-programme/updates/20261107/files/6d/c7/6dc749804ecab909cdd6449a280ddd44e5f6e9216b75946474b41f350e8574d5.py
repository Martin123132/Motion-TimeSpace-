from __future__ import annotations

import csv
from datetime import datetime, timezone
import json

import numpy as np
import psutil

from wave_network import ROOT, digest


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    inputs, comparisons, frequency_rows, archives = {}, [], [], {}
    reports = {}
    for label in ['coarse', 'fine', 'far', 'time-control']:
        path = ROOT/f'results/{label}/status.json'
        report = json.loads(path.read_text(encoding='utf-8'))
        reports[label] = report
        inputs[str(path)] = digest(path)
        for kind in ['body', 'BH']:
            archive_path = ROOT/f'results/{label}/{kind}.npz'
            with np.load(archive_path, allow_pickle=False) as archive:
                archives[label, kind] = {key: archive[key] for key in archive.files}
            inputs[str(archive_path)] = digest(archive_path)
        body, horizon = archives[label, 'body'], archives[label, 'BH']
        difference_work = body['work']-horizon['work']
        difference_stored = body['interior_energy']+body['exterior_energy']-horizon['interior_energy']-horizon['exterior_energy']
        difference_escaped = body['outer_loss']-horizon['outer_loss']
        residual = difference_work-difference_stored-difference_escaped+horizon['horizon_loss']
        scale = np.max(np.abs(difference_work))
        comparisons.append({'label': label, 'difference_work': float(difference_work[-1]),
                            'difference_stored': float(difference_stored[-1]), 'difference_escaped': float(difference_escaped[-1]),
                            'BH_horizon_absorption': float(horizon['horizon_loss'][-1]),
                            'difference_budget_error_over_peak_difference_work': float(np.max(np.abs(residual))/scale),
                            'maximum_storage_omission_error_over_peak_difference_work': float(np.max(np.abs(difference_work-difference_escaped+horizon['horizon_loss']))/scale),
                            'final_budget_error': float(abs(residual[-1])),
                            'final_error_if_horizon_omitted': float(abs((difference_work-difference_stored-difference_escaped)[-1]))})
        for index in range(3):
            fields = [row['harmonic_rows'][index] for row in report['rows']]
            references = [row['continuum_rows'][index] for row in report['rows']]
            values = [complex(row['G_real'], row['G_imag']) for row in fields]
            exact_finite = [complex(row['finite_G_real'], row['finite_G_imag']) for row in references]
            exact_infinite = [complex(row['infinite_G_real'], row['infinite_G_imag']) for row in references]
            difference = values[0]-values[1]
            difference_finite = exact_finite[0]-exact_finite[1]
            difference_infinite = exact_infinite[0]-exact_infinite[1]
            frequency_rows.append({'label': label, 'frequency_R': fields[0]['frequency_R'],
                                   'maximum_FE_to_finite_ODE_relative_error': float(max(abs(value-reference)/abs(reference) for value, reference in zip(values, exact_finite))),
                                   'difference_FE_to_finite_ODE_relative_error': float(abs(difference-difference_finite)/abs(difference_finite)),
                                   'maximum_finite_to_infinite_relative_difference': float(max(abs(value-reference)/abs(reference) for value, reference in zip(exact_finite, exact_infinite))),
                                   'difference_finite_to_infinite_relative_difference': float(abs(difference_finite-difference_infinite)/abs(difference_infinite)),
                                   'maximum_finite_to_infinite_dissipative_relative_difference': float(max(abs(value.imag/reference.imag-1) for value, reference in zip(exact_finite, exact_infinite))),
                                   'difference_finite_to_infinite_dissipative_relative_difference': float(abs(difference_finite.imag/difference_infinite.imag-1))})
    refinement = []
    for first_label, second_label, stride in [('coarse', 'fine', 2), ('fine', 'time-control', 2), ('fine', 'far', 1)]:
        row = {'first': first_label, 'second': second_label}
        for kind in ['body', 'BH']:
            first, second = archives[first_label, kind], archives[second_label, kind]
            assert np.allclose(first['time'], second['time'][::stride], rtol=0, atol=1e-12)
            row[f'{kind}_work_relative_difference'] = float(abs(first['work'][-1]/second['work'][-1]-1))
            before_echo = first['time'] < 70.
            row[f'{kind}_source_waveform_difference_over_peak_before_echo'] = float(np.max(np.abs(
                first['source_field'][before_echo]-second['source_field'][::stride][before_echo]))/np.max(np.abs(second['source_field'])))
        first = next(value for value in comparisons if value['label'] == first_label)
        second = next(value for value in comparisons if value['label'] == second_label)
        row['difference_work_relative_difference'] = abs(first['difference_work']/second['difference_work']-1)
        refinement.append(row)
    spectral_path = ROOT/'results/spectral-work/status.json'
    spectral = json.loads(spectral_path.read_text(encoding='utf-8'))
    inputs[str(spectral_path)] = digest(spectral_path)
    spectral_fine = spectral['settings'][-1]
    parseval_rows = []
    for label in ['coarse', 'fine', 'time-control']:
        report = reports[label]
        difference_work = next(row['difference_work'] for row in comparisons if row['label'] == label)
        parseval_rows.append({'label': label,
                             'body_work_relative_error': abs(report['rows'][0]['final_work']/spectral_fine['body_work']-1),
                             'BH_work_relative_error': abs(report['rows'][1]['final_work']/spectral_fine['BH_work']-1),
                             'difference_work_relative_error': abs(difference_work/spectral_fine['difference_work']-1)})
    output = ROOT/'results/analysis'
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'input_hashes': inputs, 'difference_budgets': comparisons,
              'harmonic_controls': frequency_rows, 'refinements': refinement, 'continuum_Parseval_controls': parseval_rows}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    for name, rows in [('difference-budgets', comparisons), ('harmonic-controls', frequency_rows),
                       ('refinements', refinement), ('continuum-Parseval', parseval_rows)]:
        with (output/f'{name}.csv').open('x', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    print(json.dumps({'difference_budgets': comparisons, 'refinements': refinement, 'Parseval': parseval_rows}))


if __name__ == '__main__':
    main()
