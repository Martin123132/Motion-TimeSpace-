from __future__ import annotations

import argparse
from datetime import datetime, timezone
import sys
import time
from pathlib import Path

import numpy as np

from sidebands import ROOT, BRANCH, AnalyticWave, FixedPolar, polar_settings, digest, write_json, modest_process


def main():
    modest_process()
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--settings', choices=['coarse', 'fine'], required=True)
    parser.add_argument('--plan', choices=['analytic', 'finite'], required=True)
    args = parser.parse_args()
    directory = ROOT/'results'/args.label
    directory.mkdir(parents=True, exist_ok=False)
    report = {'state': 'running', 'started_at_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'arguments': vars(args), 'rows': [], 'orbits': []}
    started = time.perf_counter()

    def save(row, archive, tag):
        row['archive'] = tag+'.npz'
        np.savez_compressed(directory/row['archive'], **archive)
        report['rows'].append(row)
        report['elapsed_seconds'] = time.perf_counter()-started
        write_json(directory/'status.json', report)
        with (directory/'log.txt').open('a', encoding='utf-8') as handle:
            handle.write(tag+'\n')

    try:
        if args.plan == 'analytic':
            for separation in [5., 10., 20., 40.]:
                for sector, modes in [('polar', [(2, 0), (2, -1), (2, 1), (0, 1)]), ('odd', [(1, 0), (1, -1), (1, 1)])]:
                    engine = AnalyticWave(sector, args.settings, separation)
                    for azimuth, harmonic in modes:
                        row, archive = engine.evaluate(azimuth, harmonic)
                        save(row, archive, f'analytic_D{separation:g}_{sector}_m{azimuth}_n{harmonic}')
                print('Analytic separation', separation, 'completed', flush=True)
        else:
            for eccentricity in [.005, .01, .02, .04]:
                engine = FixedPolar(polar_settings(args.settings), eccentricity)
                report['orbits'].append(engine.orbit_report())
                for azimuth, harmonic in [(2, item) for item in range(-6, 7)]+[(0, item) for item in range(1, 7)]:
                    row, archive = engine.evaluate(azimuth, harmonic)
                    row['sector'] = 'polar'
                    save(row, archive, f'finite_e{eccentricity:g}_polar_m{azimuth}_n{harmonic}')
                print('Finite polar eccentricity', eccentricity, 'completed', flush=True)
            sys.path.insert(0, str(BRANCH/'secular-actions-20261005'))
            from run_small_e import FixedSemilatusRadiation
            from eccentric_radiation import settings as odd_settings
            engine = FixedSemilatusRadiation(odd_settings(args.settings), .005)
            for harmonic in range(-8, 9):
                row, archive = engine.evaluate(harmonic)
                row.update(sector='odd', azimuth=1)
                save(row, archive, f'finite_e0.005_odd_m1_n{harmonic}')
        report['input_hashes'] = {str(Path(module.__file__).resolve()): digest(module.__file__) for module in list(sys.modules.values())
                 if getattr(module, '__file__', None) and Path(module.__file__).suffix == '.py' and BRANCH in Path(module.__file__).resolve().parents}
        parent = BRANCH/'eccentric-polar-radiation-20261005/results/stage-integrity.json'
        report['input_hashes'][str(parent)] = digest(parent)
        report['state'] = 'complete'
        report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
        report['elapsed_seconds'] = time.perf_counter()-started
        write_json(directory/'status.json', report)
        (directory/'COMPLETE').write_text(report['finished_at_utc']+'\n', encoding='utf-8')
        print(args.label, len(report['rows']), 'complete', flush=True)
    except BaseException as error:
        report['state'], report['error'] = 'failed', repr(error)
        write_json(directory/'status.json', report)
        raise


if __name__ == '__main__':
    main()
