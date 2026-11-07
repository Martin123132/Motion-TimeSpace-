from __future__ import annotations

import argparse
from datetime import datetime, timezone
import time

import numpy as np

from common import ROOT, PARENT, AnalyticWave, digest, read_json, write_json, modest_process, imported_hashes


def main():
    modest_process()
    parser = argparse.ArgumentParser()
    parser.add_argument('--settings', choices=['fine', 'coarse'], required=True)
    parser.add_argument('--plan', choices=['nodes', 'gauss'], default='nodes')
    args = parser.parse_args()
    label = args.plan+'-'+args.settings
    directory = ROOT/'results'/label
    directory.mkdir(parents=True, exist_ok=False)
    parent_path = PARENT/'results'/('analytic-'+args.settings)/'status.json'
    parent = read_json(parent_path)
    separations = 7.5+2.5*np.cos(np.arange(17)*np.pi/16) if args.plan == 'nodes' else 7.5+2.5*np.polynomial.legendre.leggauss(8)[0]
    report = dict(state='running', script_sha256=digest(__file__), arguments=vars(args),
                  started_at_utc=datetime.now(timezone.utc).isoformat(), rows=[], reused=[], requested_separations=separations.tolist())
    started = time.perf_counter()
    try:
        for index, separation in enumerate(separations):
            if args.plan == 'nodes' and index in [0, 16]:
                selected = [row for row in parent['rows'] if abs(row['separation_over_radius']-separation) < 1e-10]
                assert len(selected) == 7
                report['reused'].extend([{**row, 'archive': str(parent_path.parent/row['archive']), 'source_report': str(parent_path)} for row in selected])
                continue
            for sector, modes in [('polar', [(2, 0), (2, -1), (2, 1), (0, 1)]), ('odd', [(1, 0), (1, -1), (1, 1)])]:
                engine = AnalyticWave(sector, args.settings, float(separation))
                for azimuth, harmonic in modes:
                    row, archive = engine.evaluate(azimuth, harmonic)
                    name = f'node{index:02d}_{sector}_m{azimuth}_n{harmonic}.npz'
                    np.savez_compressed(directory/name, **archive)
                    report['rows'].append({**row, 'archive': name, 'node_index': index})
                    report['elapsed_seconds'] = time.perf_counter()-started
                    write_json(directory/'status.json', report)
            with (directory/'log.txt').open('a', encoding='utf-8') as handle:
                handle.write(f'{index}: r0/R={separation:.16g} completed\n')
            print(label, index, 'completed', flush=True)
        report['input_hashes'] = imported_hashes()
        report['input_hashes'][str(parent_path)] = digest(parent_path)
        report['state'] = 'complete'
        report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
        write_json(directory/'status.json', report)
        (directory/'COMPLETE').write_text(report['finished_at_utc']+'\n', encoding='utf-8')
        print(label, len(report['rows']), 'new modes complete', flush=True)
    except BaseException as error:
        report['state'], report['error'] = 'failed', repr(error)
        write_json(directory/'status.json', report)
        raise


if __name__ == '__main__':
    main()
