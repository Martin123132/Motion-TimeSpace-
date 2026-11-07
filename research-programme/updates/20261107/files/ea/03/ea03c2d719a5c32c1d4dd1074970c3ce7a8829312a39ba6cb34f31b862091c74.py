from __future__ import annotations

import argparse
from datetime import datetime, timezone
import time

import numpy as np

from carrier import ROOT, CarrierWave, digest, write_json, modest_process, imported_hashes


def main():
    modest_process()
    parser = argparse.ArgumentParser()
    parser.add_argument('--settings', choices=['fine', 'coarse'], required=True)
    parser.add_argument('--plan', choices=['pilot', 'nodes', 'extension'], default='pilot')
    args = parser.parse_args()
    label = args.plan+'-'+args.settings
    directory = ROOT/'results'/label
    directory.mkdir(parents=True, exist_ok=False)
    separations = [5.] if args.plan == 'pilot' else (7.5+2.5*np.cos(np.arange(9)*np.pi/8)).tolist()
    if args.plan == 'nodes':
        separations = separations[:-1]
    if args.plan == 'extension':
        separations = (7.5+2.5*np.cos(np.arange(1, 16, 2)*np.pi/16)).tolist()
    report = dict(state='running', script_sha256=digest(__file__), arguments=vars(args), rows=[],
                  started_at_utc=datetime.now(timezone.utc).isoformat(), requested_separations=separations)
    started = time.perf_counter()
    try:
        for index, separation in enumerate(separations):
            for sector in ['polar', 'odd']:
                engine = CarrierWave(sector, args.settings, separation)
                azimuth = 2 if sector == 'polar' else 1
                central_frequency = azimuth/(engine.mass*engine.semilatus**1.5)
                for shift in [0., -.002, -.001, -.0005, .0005, .001, .002]:
                    row, archive = engine.evaluate_frequency(central_frequency*(1+shift))
                    row.update(fractional_frequency_shift=shift, central_frequency=central_frequency)
                    filename = f'node{index:02d}_{sector}_shift{shift:+.4f}.npz'
                    np.savez_compressed(directory/filename, **archive)
                    report['rows'].append({**row, 'archive': filename})
                    report['elapsed_seconds'] = time.perf_counter()-started
                    write_json(directory/'status.json', report)
            print(label, 'radius', separation, 'complete', flush=True)
        report['state'] = 'complete'
        report['input_hashes'] = imported_hashes()
        report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
        write_json(directory/'status.json', report)
        (directory/'COMPLETE').write_text(report['finished_at_utc']+'\n', encoding='utf-8')
        print(label, len(report['rows']), 'wave evaluations complete', flush=True)
    except BaseException as error:
        report['state'], report['error'] = 'failed', repr(error)
        write_json(directory/'status.json', report)
        raise


if __name__ == '__main__':
    main()

