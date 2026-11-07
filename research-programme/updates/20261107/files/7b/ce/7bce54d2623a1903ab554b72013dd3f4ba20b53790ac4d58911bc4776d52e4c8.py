from __future__ import annotations

from datetime import datetime, timezone
import json
import time

import numpy as np
import psutil
from scipy.optimize import brentq
from scipy.special import spherical_jn

from causal_system import ROOT, BRANCH, build_model, digest, response


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/spectrum'
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    rows, inputs = [], {}
    reference = None
    with (output/'log.txt').open('x', encoding='utf-8', buffering=1) as log:
        for nominal, cells in [(0., 64), (.03, 64), (.03, 128), (.03, 256)]:
            model = build_model(cells, nominal)
            body = model['body']
            if nominal != 0 and reference is None:
                static, _ = body.solve(0., tolerance=8e-14, max_step=1/360, start=5e-6, variations=True)
                reference = {'static': static, 'waves': []}
                for frequency in [.01, .05, .2, .5, 1.]:
                    wave, _ = body.solve(frequency, tolerance=8e-14, max_step=1/360, start=5e-6)
                    reference['waves'].append(wave)
            name = f'flat-{cells}' if nominal == 0 else f'body-{cells}'
            np.savez_compressed(output/f'{name}.npz', **{key: model[key] for key in
                                ['eigenvalues', 'coupling', 'stiffness', 'inertia', 'static_profile', 'modes']},
                                norm=model['norm'], moment=model['moment'], static_impedance=model['static_impedance'],
                                unresolved_kinetic_norm=model['unresolved_kinetic_norm'], surface_term=model['surface_term'])
            row = {key: model[key] for key in ['cells', 'norm', 'moment', 'static_impedance',
                                             'unresolved_kinetic_norm', 'gram_error', 'eigen_error']}
            row.update({'name': name, 'nominal': nominal, 'radius': body.radius, 'mass': body.mass,
                        'gap_lower': 3*body.central_lapse**2, 'first_five_eigenvalues': model['eigenvalues'][:5].tolist(),
                        'positive_eigenvalues': bool(np.all(model['eigenvalues'] > 0)),
                        'responses': [response(model, frequency) for frequency in [.01, .05, .2, .5, 1.]],
                        'source_path': str(body.profile.path), 'archive_sha256': digest(output/f'{name}.npz')})
            if nominal == 0:
                row['flat_exact_first_eigenvalue'] = brentq(lambda frequency: spherical_jn(2, frequency), 5., 6.)**2
            rows.append(row)
            inputs[str(body.profile.path)] = digest(body.profile.path)
            message = {'state': 'running', 'name': name, 'first_eigenvalue': row['first_five_eigenvalues'][0],
                       'norm': row['norm'], 'moment': row['moment'], 'eigen_error': row['eigen_error']}
            log.write(json.dumps(message)+'\n')
            print(json.dumps(message), flush=True)
        for path in [ROOT/'causal_system.py', BRANCH/'dynamical-axial-20261004/axial_wave.py',
                     BRANCH/'axial-reciprocity-20261005/results/stage-integrity.json']:
            inputs[str(path)] = digest(path)
        report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
                  'script_sha256': digest(__file__), 'input_hashes': inputs, 'rows': rows,
                  'independent_ODE_reference': reference, 'new_background_solves': 0, 'fitted_spectral_parameters': 0,
                  'elapsed_seconds': time.monotonic()-started}
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
        (output/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
        log.write(json.dumps({'state': 'complete', 'elapsed_seconds': report['elapsed_seconds']})+'\n')
    print(json.dumps({'state': 'complete', 'elapsed_seconds': report['elapsed_seconds']}))


if __name__ == '__main__':
    main()
