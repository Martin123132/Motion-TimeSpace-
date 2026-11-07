from __future__ import annotations

import csv
from datetime import datetime, timezone

import numpy as np
from scipy.integrate import quad

from inspiral import (ROOT, BRANCH, digest, read_json, write_json, modest_process,
                      dependencies, coefficients, analytic_coefficients,
                      variational_solution, resummed_control, normalized_endpoint, physical_row)


def main():
    modest_process()
    directory = ROOT/'results/trajectories'
    directory.mkdir(parents=True, exist_ok=False)
    source = BRANCH/'conservative-eccentric-action-20261005/results/action/status.json'
    body = read_json(source)['raw_nodes']['fine'][0]
    mass, radius, deformability = [body[key] for key in ['mass', 'radius', 'tidal_lambda']]
    ratios = np.linspace(1., .5, 33)
    rows, endpoints, solutions, quadratures, controls = [], [], [], [], []
    arrays = {'ratios':ratios}
    for mass_ratio in [0., .001, .01, 1.]:
        constants = coefficients(mass_ratio)
        exact = np.array([analytic_coefficients(mass_ratio, ratio) for ratio in ratios]).T
        fine = variational_solution(mass_ratio, .5)
        coarse = variational_solution(mass_ratio, .5, tolerance=3e-10)
        scale = np.maximum(np.max(abs(exact), axis=1), 1e-12)
        error = np.max(abs(fine.sol(ratios)-exact)/scale[:, None])
        resolution = np.max(abs(fine.sol(ratios)-coarse.sol(ratios))/scale[:, None])
        tag = str(mass_ratio).replace('.', '_')
        arrays['exact_'+tag] = exact
        arrays['fine_'+tag] = fine.sol(ratios)
        arrays['coarse_'+tag] = coarse.sol(ratios)
        solutions.append(dict(mass_ratio=mass_ratio, fine_evaluations=fine.nfev,
            coarse_evaluations=coarse.nfev, maximum_scaled_error=float(error),
            maximum_scaled_resolution=float(resolution), coefficient_scales=scale.tolist()))
        for exponent, offset in [(3., 2), (1.5, 6)]:
            eccentric, tide, transport, mixed, power = [constants[key] for key in
                ['eccentric', 'circular_tide', 'transport', 'mixed', 'power']]
            functions = [lambda ratio:-ratio**exponent,
                lambda ratio:eccentric*ratio**(exponent+power),
                lambda ratio:tide*ratio**(exponent-5),
                lambda ratio:-mixed*ratio**(exponent+power-5)+eccentric*transport*ratio**(exponent+power)]
            for index, function in enumerate(functions):
                value, estimate = quad(function, 1., .5, epsabs=1e-11, epsrel=1e-12)
                target = float(exact[offset+index, -1])
                quadratures.append(dict(mass_ratio=mass_ratio, exponent=exponent, component=index,
                    numerical=value, analytic=target, relative_error=abs(value/target-1),
                    quadrature_estimated_absolute_error=estimate))
    for mass_ratio in [.001, .01]:
        for initial_z in [0., .0001]:
            trajectory = [physical_row(mass, radius, deformability, mass_ratio, initial_z, 10., float(ratio))
                          for ratio in ratios]
            rows.extend(trajectory)
            endpoints.append(trajectory[-1])
    for family in ['tide_only', 'eccentricity_only', 'both']:
        for strength in [1., .5, .25]:
            initial_z = .001*strength if family != 'tide_only' else 0.
            initial_tide = 1e-5*strength if family != 'eccentricity_only' else 0.
            numerical = resummed_control(.01, .5, initial_z, initial_tide)
            strict = normalized_endpoint(.01, .5, initial_z, initial_tide)
            residual = numerical.y[:, -1]-strict
            controls.append(dict(family=family, strength=strength, initial_z=initial_z,
                initial_tide=initial_tide, resummed=numerical.y[:, -1].tolist(),
                strict=strict.tolist(), residual=residual.tolist(), evaluations=numerical.nfev,
                role='Order control of truncated equations only, not a higher-order physical prediction.'))
    with (directory/'trajectories.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with (directory/'coefficient-integrations.npz').open('xb') as handle:
        np.savez_compressed(handle, **arrays)
    inputs = dependencies()
    inputs.update({str(source):digest(source), str(ROOT/'results/derivation/status.json'):digest(ROOT/'results/derivation/status.json')})
    report = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(__file__), input_hashes=inputs,
        body=dict(mass=mass, radius=radius, tidal_lambda=deformability), endpoints=endpoints,
        solutions=solutions, quadratures=quadratures, order_controls=controls,
        trajectory_rows=len(rows), physical_trajectories=len(endpoints), coefficient_integrations=8,
        resummed_control_integrations=len(controls), new_background_or_wave_solves=0,
        approximation='Strict linear initial zi and lambda, retaining their mixed product.',
        matching='Identical initial and final azimuthal frequencies, initial z, and masses for body/point comparison.',
        illustrative_units='G=c=1; no astrophysical mass calibration or detector model.',
        output_hashes={path.name:digest(path) for path in directory.iterdir() if path.is_file()})
    write_json(directory/'status.json', report, exclusive=True)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    print(dict(state='complete', rows=len(rows), maximum_coefficient_error=max(row['maximum_scaled_error'] for row in solutions),
        maximum_resolution=max(row['maximum_scaled_resolution'] for row in solutions), illustrative_endpoint=endpoints[-1]), flush=True)


if __name__ == '__main__':
    main()
