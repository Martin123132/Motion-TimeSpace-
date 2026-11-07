from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from conservative import ROOT, AnalyticWave, static_law, read_json, write_json, digest, dependencies, modest_process


def main():
    modest_process()
    action_path = ROOT/'results/action/status.json'
    action = read_json(action_path)
    directory = ROOT/'results/radial-derivative'
    directory.mkdir(parents=True, exist_ok=False)
    report = dict(state='running', script_sha256=digest(__file__), rows=[], derivatives=[],
                  started_at_utc=datetime.now(timezone.utc).isoformat())
    write_json(directory/'status.json', report)
    try:
        for label in ['fine', 'coarse']:
            tidal_lambda = action['static_interiors'][label]['tidal_lambda']
            for center in [5., 10.]:
                sector_nodes = {}
                for sector in ['polar', 'odd']:
                    lookup = {}
                    for shift in [-.002, -.001, -.0005, .0005, .001, .002]:
                        separation = center*np.exp(shift)
                        engine = AnalyticWave(sector, label, separation)
                        row, archive = engine.evaluate(2 if sector == 'polar' else 1, 0)
                        action_value = row['retarded_action_real']
                        if sector == 'polar':
                            action_value += static_law(engine.mass, engine.semilatus, tidal_lambda)['action0']
                        lookup[shift] = action_value
                        filename = f'{label}-r{center:g}-{sector}-shift{shift:+.4f}.npz'
                        np.savez_compressed(directory/filename, **archive)
                        report['rows'].append(dict(settings=label, center=center, log_radius_shift=shift,
                                                  action0=action_value, archive=filename, **row))
                        write_json(directory/'status.json', report)
                    sector_nodes[sector] = lookup
                sector_nodes['total'] = {shift:sector_nodes['polar'][shift]+sector_nodes['odd'][shift] for shift in sector_nodes['polar']}
                for sector, lookup in sector_nodes.items():
                    semilatus = center*engine.radius/engine.mass
                    estimates = {str(step):float((lookup[-2*step]-8*lookup[-step]+8*lookup[step]-lookup[2*step])/(12*step*semilatus))
                                 for step in [.001, .0005]}
                    expected = next(row['action0_prime'] for row in action['frequency_laws'][label]
                                    if row['component'] == sector and row['separation'] == center)
                    report['derivatives'].append(dict(settings=label, component=sector, separation=center,
                        estimates=estimates, interpolated=expected,
                        step_error=abs(estimates['0.001']/estimates['0.0005']-1),
                        independent_stencil_error=abs(expected/estimates['0.0005']-1)))
                print(label, center, 'independent radial derivatives complete', flush=True)
        report.update(state='complete', finished_at_utc=datetime.now(timezone.utc).isoformat(),
                      input_hashes={str(action_path):digest(action_path), **dependencies()})
        write_json(directory/'status.json', report)
        (directory/'COMPLETE').write_text(report['finished_at_utc']+'\n', encoding='utf-8')
        print('waves', len(report['rows']), 'max derivative comparison',
              max(row['independent_stencil_error'] for row in report['derivatives']), flush=True)
    except BaseException as error:
        report.update(state='failed', error=repr(error))
        write_json(directory/'status.json', report)
        raise


if __name__ == '__main__':
    main()
