from __future__ import annotations

import csv
import math

import numpy as np

from conservative import ROOT, BRANCH, PARENT, PRIOR, AnalyticWave, carrier_action, static_law, finite_static, ActionCurve
from conservative import read_json, digest, dependencies, save, modest_process


def main():
    modest_process()
    inputs = {}

    def load(path):
        report = read_json(path)
        assert report['state'] == 'complete'
        inputs[str(path)] = digest(path)
        return report

    archive_directory = ROOT/'results/archives'
    archive_directory.mkdir(parents=True, exist_ok=False)
    results, static_controls, finite_comparisons, source_controls = {}, {}, [], []
    for label in ['fine', 'coarse']:
        engine = AnalyticWave('polar', label)
        slope, diagnostic, archive = engine.interior(0.)
        basis = engine.vacuum.static_master_basis(engine.radius, engine.mass, 1.)
        amplitudes = np.linalg.solve(basis, [1., slope])
        tidal_lambda = float((amplitudes[1]/(3*amplitudes[0])).real)
        np.savez_compressed(archive_directory/('static-interior-'+label+'.npz'), **archive)
        static_controls[label] = dict(tidal_lambda=tidal_lambda, **diagnostic)
        modes = [row for plan in ['pilot', 'nodes', 'extension']
                 for row in load(PARENT/'results'/(plan+'-'+label)/'status.json')['rows']]
        analytic = load(PRIOR/'results'/('analytic-'+label)/'status.json')['rows']
        analytic += load(BRANCH/'near-circular-inspiral-20261005/results'/('nodes-'+label)/'status.json')['rows']
        collected = []
        for separation in sorted({row['separation'] for row in modes}):
            selected = [row for row in modes if abs(row['separation']-separation) < 1e-10]
            sidebands = [row for row in analytic if abs(row['separation_over_radius']-separation) < 1e-10]
            assert len(sidebands) == 7
            semilatus = selected[0]['semilatus']
            static = static_law(engine.mass, semilatus, tidal_lambda)
            result = dict(separation=separation, semilatus=semilatus, mass=engine.mass, radius=engine.radius,
                          tidal_lambda=tidal_lambda, static0=static['action0'], static2=static['action2'], static_law=static)
            for sector in ['polar', 'odd']:
                wave_rows = [row for row in selected if row['sector'] == sector]
                carrier = carrier_action(wave_rows)
                alternate = carrier_action(wave_rows, .001)
                sideband_action = math.fsum(row['retarded_action_real'] for row in sidebands if row['sector'] == sector and row['harmonic'] != 0)
                result[sector+'0'] = carrier['action0']+(static['action0'] if sector == 'polar' else 0.)
                result[sector+'2'] = carrier['action2']+sideband_action+(static['action2'] if sector == 'polar' else 0.)
                result[sector+'_carrier'] = carrier
                result[sector+'_sideband2'] = sideband_action
                result[sector+'_frequency_step_error'] = abs(alternate['action2']-carrier['action2'])/abs(result[sector+'2'])
                inherited = next(row for row in sidebands if row['sector'] == sector and row['harmonic'] == 0)
                result[sector+'_carrier_regression_error'] = abs(inherited['retarded_action_real']/carrier['action0']-1)
            result['total0'] = result['polar0']+result['odd0']
            result['total2'] = result['polar2']+result['odd2']
            collected.append(result)
        results[label] = collected
        finite = load(PRIOR/'results'/('finite-'+label)/'status.json')['rows']
        odd = load(BRANCH/'secular-actions-20261005/results'/('small-e-'+label)/'status.json')['rows']
        finite += [{**row, 'sector':'odd'} for row in odd]
        central = next(row for row in collected if row['separation'] == 5.)
        statics = []
        for eccentricity in [.005, .01]:
            value, archive = finite_static(engine.mass, central['semilatus'], eccentricity, tidal_lambda)
            np.savez_compressed(archive_directory/f'static-source-{label}-e{eccentricity:g}.npz', **archive)
            alternative, _ = finite_static(engine.mass, central['semilatus'], eccentricity, tidal_lambda, order=40, panels=32)
            value['quadrature_error'] = abs(alternative['action']/value['action']-1)
            statics.append(value)
        source_controls.extend([{**value, 'settings':label} for value in statics])
        for component in ['static', 'polar', 'odd', 'total']:
            estimates = []
            for static in statics:
                eccentricity = static['eccentricity']
                selected = [row for row in finite if row['eccentricity'] == eccentricity and
                            (component == 'total' or row['sector'] == component)]
                value = math.fsum(row['retarded_action_real'] for row in selected)
                if component in ['static', 'polar', 'total']:
                    value += static['action']
                estimates.append((value-central[component+'0'])/eccentricity**2)
            extrapolated = (4*estimates[0]-estimates[1])/3
            finite_comparisons.append(dict(settings=label, component=component, predicted=central[component+'2'],
                     estimates=estimates, extrapolated=extrapolated, relative_error=abs(extrapolated/central[component+'2']-1)))
        print(label, 'action assembled; lambda', tidal_lambda, 'held-out errors', finite_comparisons[-4:], flush=True)
    frequencies, curves = {}, {}
    for label, rows in results.items():
        frequencies[label] = []
        for component in ['polar', 'odd', 'total']:
            curve = ActionCurve(rows, component)
            frequencies[label].extend(curve.frequency_law(row) for row in rows)
            curves[label+'-'+component] = curve
            if label == 'fine':
                for stride in [2, 4]:
                    nested = ActionCurve(rows[::stride], component)
                    key = 'nested'+str(len(rows[::stride]))
                    frequencies.setdefault(key, []).extend(nested.frequency_law(row) for row in rows)
    circular = load(BRANCH/'orbital-backreaction-20261004/results/fine/status.json')
    regressions = []
    for row in frequencies['fine']:
        if row['component'] != 'polar' or row['separation'] not in [5., 10.]:
            continue
        prior = next(value for value in circular['rows'] if abs(value['separation_over_radius']-row['separation']) < 1e-10)
        derived = next(value for value in circular['derivatives'] if value['separation_over_radius'] == row['separation'])
        regressions.append(dict(separation=row['separation'], action_error=abs(row['action0']/prior['action_per_particle_squared']-1),
                                stage20_derivatives=derived, stage38=row))
    report = save('action', __file__, dict(input_hashes={**inputs, **dependencies()}, static_interiors=static_controls,
        raw_nodes=results, finite_comparisons=finite_comparisons, static_source_controls=source_controls,
        frequency_laws=frequencies, circular_regressions=regressions,
        new_static_interior_solves=2, new_frequency_wave_solves=0,
        normalization='action per mu squared; eccentricity coefficient at fixed p',
        scope='First-order conservative body-minus-BH ell2 response; circular-limit frequencies from the O(e²) action.'))
    with (ROOT/'results/action/frequency-shifts.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(frequencies['fine'][0]))
        writer.writeheader()
        writer.writerows(frequencies['fine'])
    print('finished', len(frequencies['fine']), 'frequency-law rows', flush=True)


if __name__ == '__main__':
    main()
