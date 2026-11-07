from __future__ import annotations

import argparse
import json
from pathlib import Path

import psutil

from sequence_tools import SequenceProfile, digest, signed_spectrum


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--centers', type=float, nargs='+', required=True)
    parser.add_argument('--cells', type=int, nargs='+', default=[256, 512, 1024])
    parser.add_argument('--order', type=int, default=8)
    args = parser.parse_args()
    input_path = Path(args.input)
    source = json.loads(input_path.read_text(encoding='utf-8'))
    output = ROOT/'results'/args.label
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'running', 'arguments': vars(args), 'source_sha256': digest(input_path),
              'script_sha256': digest(Path(__file__)), 'helper_sha256': digest(ROOT/'sequence_tools.py'), 'rows': []}
    try:
        for center in args.centers:
            row = next(row for row in source['rows'] if row['control_kind'] == 'central' and abs(row['control_value']-center) < 1e-12)
            path = input_path.parent/row['archive']
            profile = SequenceProfile(path, row)
            for cells in args.cells:
                name = f'modes-center-{center:.10g}-N{cells}-G{args.order}'.replace('.', 'p')+'.npz'
                spectrum = signed_spectrum(profile, cells, args.order, output/name)
                result = {'central_target': center, 'profile_path': str(path), 'profile_sha256': digest(path),
                          'charge': row['charge'], 'adm_energy': row['adm_energy'], 'radius': row['radius'],
                          'surface_compactness': row['surface_compactness'], 'minimum_F': row['minimum_F'],
                          'spectrum': spectrum, 'archive': name}
                report['rows'].append(result)
                (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
                print(json.dumps(result), flush=True)
        report['state'] = 'complete'
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        raise
    finally:
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
