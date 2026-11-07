from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from balance import ROOT, read_json, write_json, digest, input_hashes, orbit_average, modest_process


def zero_intercept(coordinates, values):
    return float(sum(value*np.prod([-other/(coordinate-other) for other_index, other in enumerate(coordinates) if other_index != index])
                     for index, (coordinate, value) in enumerate(zip(coordinates, values))))


def main():
    modest_process()
    directory = ROOT/'results/orbits'
    directory.mkdir(parents=True, exist_ok=False)
    step = 1e-4
    parameters = [(0., 0.)]+[(multiple*step, 0.) for multiple in [-2, -1, 1, 2]]+[(0., multiple*step) for multiple in [-2, -1, 1, 2]]
    report = dict(state='running', script_sha256=digest(__file__), rows=[], extrapolations=[], coefficients=[],
                  started_at_utc=datetime.now(timezone.utc).isoformat(), interpretation='Numerical algebra controls of truncated static-tide mechanics; signed auxiliary parameters are not physical fits.')
    write_json(directory/'status.json', report)
    try:
        for label, tolerance in [('fine', 3e-13), ('coarse', 3e-11)]:
            for conservative, induced in parameters:
                family = []
                for amplitude in [.01, .02, .04]:
                    row, archive = orbit_average(conservative, induced, amplitude, tolerance)
                    filename = f'{label}-k{conservative:+.4f}-b{induced:+.4f}-amp{amplitude:.3f}.npz'
                    np.savez_compressed(directory/filename, **archive)
                    row.update(settings=label, tolerance=tolerance, archive=filename)
                    family.append(row)
                    report['rows'].append(row)
                coordinates = [row['z'] for row in family]
                values = {}
                for flux in ['energy', 'angular']:
                    coefficient = [(row[flux+'_flux_ratio']-row['circular_'+flux+'_flux_ratio'])/row['z'] for row in family]
                    values[flux+'2'] = zero_intercept(coordinates, coefficient)
                    values[flux+'2_raw'] = coefficient
                omega2 = [(row['Omega_phi']-row['circular_radius']**-2)/row['z'] for row in family]
                values['omega2'] = zero_intercept(coordinates, omega2)
                values['radial0'] = zero_intercept(coordinates, [row['Omega_r'] for row in family])
                report['extrapolations'].append(dict(settings=label, conservative=conservative, induced=induced, **values))
                write_json(directory/'status.json', report)
            selected = [row for row in report['extrapolations'] if row['settings'] == label]
            center = next(row for row in selected if row['conservative'] == 0. and row['induced'] == 0.)
            for parameter in ['conservative', 'induced']:
                lookup = {round(row[parameter]/step):row for row in selected if row['induced' if parameter == 'conservative' else 'conservative'] == 0.}
                for quantity in ['energy2', 'angular2', 'omega2', 'radial0']:
                    derivative = (lookup[-2][quantity]-8*lookup[-1][quantity]+8*lookup[1][quantity]-lookup[2][quantity])/(12*step)
                    report['coefficients'].append(dict(settings=label, parameter=parameter, quantity=quantity, derivative=derivative,
                                                      zero_value=center[quantity]))
            print(label, '27 finite-radial-action control orbits complete', flush=True)
        report.update(state='complete', finished_at_utc=datetime.now(timezone.utc).isoformat(),
                      input_hashes={**input_hashes(), str(ROOT/'results/derivation/status.json'):digest(ROOT/'results/derivation/status.json')})
        write_json(directory/'status.json', report)
        (directory/'COMPLETE').write_text(report['finished_at_utc']+'\n', encoding='utf-8')
        print(report['coefficients'], flush=True)
    except BaseException as error:
        report.update(state='failed', error=repr(error))
        write_json(directory/'status.json', report)
        raise


if __name__ == '__main__':
    main()
