from __future__ import annotations

import csv
import sys

import numpy as np

from susceptibility import ROOT, BRANCH, PARENT, read_json, digest, save, dependencies, modest_process
from budget import frozen_boundary, carrier_flux, sideband_response, sideband_flux, project_rates, orbit_series
from integrate_budget import integrate


def main():
    modest_process()
    inputs, predicted_nodes, predictions, slopes, controls = {}, [], [], [], []

    def load(path):
        inputs[str(path)] = digest(path)
        report = read_json(path)
        assert report['state'] == 'complete'
        return report

    tangent = load(ROOT/'results/tangent/status.json')
    baseline = load(PARENT/'results/nodes/status.json')
    original_integrals = load(PARENT/'results/integrals/status.json')
    for settings in ['fine', 'coarse']:
        body = next(row for row in baseline['static_boundaries'] if row['settings'] == settings)
        solved = next(row for row in tangent['rows'] if row['label'] == ('refined' if settings == 'fine' else 'coarse'))
        static_slope, coefficient = body['slope'], solved['coefficient_s2']
        mass, radius = body['mass'], body['radius']
        carriers, bands = [], []
        for plan in ['pilot', 'nodes', 'extension']:
            directory = BRANCH/'postcircular-clock-20261005/results'/(plan+'-'+settings)
            carriers.extend((row, directory/row['archive']) for row in load(directory/'status.json')['rows'] if row['sector']=='polar')
        for directory in [BRANCH/'near-circular-quadrupole-20261005/results'/('analytic-'+settings),
                          BRANCH/'near-circular-inspiral-20261005/results'/('nodes-'+settings)]:
            bands.extend((row, directory/row['archive']) for row in load(directory/'status.json')['rows']
                if row['sector']=='polar' and row['harmonic'] != 0 and 5.-1e-10 <= row['separation_over_radius'] <= 10.+1e-10)
        for separation in sorted({row['separation'] for row, path in carriers}):
            predicted_carriers = []
            for row, path in carriers:
                if abs(row['separation']-separation) > 1e-10:
                    continue
                inputs[str(path)] = digest(path)
                model_slope = static_slope+coefficient*row['frequency']**2
                with np.load(path, allow_pickle=False) as archive:
                    modified, diagnostic = frozen_boundary(row, archive, model_slope)
                    actual_slope = float(archive['direct_body'][0, 1])
                predicted_carriers.append(modified)
                controls.append(diagnostic)
                slopes.append(dict(settings=settings, separation=separation, role='carrier', frequency=row['frequency'],
                    actual_slope=actual_slope, static_slope=static_slope, predicted_slope=model_slope,
                    actual_change=actual_slope-static_slope, predicted_change=coefficient*row['frequency']**2,
                    fractional_dynamic_error=(model_slope-actual_slope)/(actual_slope-static_slope),
                    remainder_over_omega4=(actual_slope-model_slope)/row['frequency']**4))
            center = next(row for row in predicted_carriers if row['fractional_frequency_shift'] == 0.)
            flux = carrier_flux(predicted_carriers)
            alternative = carrier_flux(predicted_carriers, .001)
            circular = [dict(azimuth=2, frequency=center['frequency'], alpha=orbit_series(center['semilatus'])['angular_frequency_fraction'],
                            power0=flux['difference'][0], power2=flux['difference'][1])]
            side = []
            action_values = list(flux['action'])
            for row, path in bands:
                if abs(row['separation_over_radius']-separation) > 1e-10:
                    continue
                response = sideband_response(row)
                inputs[str(path)] = digest(path)
                model_slope = static_slope+coefficient*row['frequency']**2
                with np.load(path, allow_pickle=False) as archive:
                    modified, diagnostic = frozen_boundary(response, archive, model_slope)
                    actual_slope = float(archive['direct_body'][0, 1])
                value = sideband_flux(modified)
                side.append(dict(azimuth=row['azimuth'], harmonic=row['harmonic'], frequency=row['frequency'], power=value['difference']))
                action_values[1] += complex(*modified['responses'][0]['action']).real
                controls.append(diagnostic)
                slopes.append(dict(settings=settings, separation=separation, role='sideband', frequency=row['frequency'],
                    actual_slope=actual_slope, static_slope=static_slope, predicted_slope=model_slope,
                    actual_change=actual_slope-static_slope, predicted_change=coefficient*row['frequency']**2,
                    fractional_dynamic_error=(model_slope-actual_slope)/(actual_slope-static_slope),
                    remainder_over_omega4=(actual_slope-model_slope)/row['frequency']**4))
            rates = project_rates(mass, separation*radius/mass, circular, side)
            frozen = next(row for row in baseline['nodes'] if row['settings'] == settings and
                row['component'] == 'frozen_polar' and abs(row['separation']-separation) < 1e-10)
            truth = next(row for row in baseline['nodes'] if row['settings'] == settings and
                row['component'] == 'dynamic_polar' and abs(row['separation']-separation) < 1e-10)
            dynamic = {key:rates[key]-frozen[key] for key in ['P0','P2','G0']}
            predicted_nodes.append(dict(settings=settings, component='dynamic_polar', separation=separation,
                semilatus=separation*radius/mass, **dynamic))
            prediction = dict(settings=settings, separation=separation,
                frequency_stencil_error=abs(flux['difference'][1]-alternative['difference'][1])/abs(flux['difference'][1]),
                balance_error=rates['balance_error'],
                rate_errors={key:dynamic[key]/truth[key]-1 for key in dynamic})
            prediction['action_errors'] = {}
            for index, order in enumerate([0, 2]):
                old = next(row for row in baseline['conservative_actions'] if row['settings']==settings and
                           row['order']==order and abs(row['separation']-separation)<1e-10)
                static00 = next(row for row in read_json(BRANCH/'conservative-eccentric-action-20261005/results/action/status.json')['raw_nodes'][settings]
                                if abs(row['separation']-separation)<1e-10)['static'+str(order)]
                projected_dynamic = action_values[index]+static00-old['frozen_polar']
                prediction['action_errors'][str(order)] = projected_dynamic/old['dynamic_polar']-1
            predictions.append(prediction)
    action_source = BRANCH/'conservative-eccentric-action-20261005/results/action/status.json'
    inputs[str(action_source)] = digest(action_source)
    integrated, integral_errors = {}, {}
    for settings in ['fine', 'coarse']:
        body = next(row for row in baseline['static_boundaries'] if row['settings']==settings)
        replacement = [row for row in baseline['nodes'] if row['settings']==settings and row['component']!='dynamic_polar']
        replacement += [row for row in predicted_nodes if row['settings']==settings]
        integrated[settings], unused_samples = integrate(replacement, body)
        predicted = np.array(integrated[settings]['endpoint']['dynamic_polar'])
        actual = np.array(original_integrals['runs'][settings]['endpoint']['dynamic_polar'])
        integral_errors[settings] = (predicted/actual-1).tolist()
    fine = [row for row in slopes if row['settings']=='fine']
    report = save('prediction', __file__, dict(input_hashes={**inputs, **dependencies()}, slope_predictions=slopes,
        node_predictions=predictions, replacement_nodes=predicted_nodes, controls=controls,
        integrated=integrated, fractional_dynamic_integral_errors=integral_errors,
        maximum_fractional_slope_change_error=max(abs(row['fractional_dynamic_error']) for row in fine),
        static_anchor='Inherited static slope at each resolution, independently reproduced by the tangent static block; no finite-frequency calibration.',
        approximation='s0+s2 omega^2 surface surrogate with unchanged exact archived exterior transfer; not a full fourth-order frequency derivation.',
        comparison_order=['log action-z transport', 'circular time', 'circular phase', 'eccentric time coefficient', 'eccentric phase coefficient']))
    with (ROOT/'results/prediction/slope-predictions.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(slopes[0]))
        writer.writeheader()
        writer.writerows(slopes)
    print(dict(state='complete', largest_slope_change_error=report['maximum_fractional_slope_change_error'],
        dynamic_integral_errors=integral_errors,
        endpoint_predictions=[row for row in predictions if row['settings']=='fine' and row['separation'] in [5.,10.]]), flush=True)


if __name__ == '__main__':
    main()
