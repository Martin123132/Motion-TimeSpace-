from __future__ import annotations

import argparse
from pathlib import Path
from time import monotonic

import numpy as np

from transient import ROOT, body, spatial_rule, spectrum, transfer, dependencies, save, digest, modest_process


def main():
    modest_process()
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--frequencies', type=int, default=96)
    parser.add_argument('--spatial', type=int, default=24)
    parser.add_argument('--far-phase', type=float, default=40.)
    parser.add_argument('--order', type=int, default=10)
    parser.add_argument('--tolerance', type=float, default=2e-11)
    args = parser.parse_args()
    directory = ROOT/'results'/args.label
    directory.mkdir(parents=True, exist_ok=False)
    start = monotonic()
    model = body()
    detector = 200.
    interior, spatial_weights = spatial_rule(args.spatial, model['compactness'], detector)
    positions = np.sort(np.concatenate([[1., 5., detector], interior]))
    energy_indices = np.array([int(np.flatnonzero(positions == position)[0]) for position in interior])
    source_index = int(np.flatnonzero(positions == 5.)[0])
    frequencies, frequency_weights, amplitudes = spectrum(args.frequencies)
    waves, outgoing, diagnostics = [], [], []
    for index, frequency in enumerate(frequencies):
        wave, infinity, controls = transfer(frequency, positions, model, args.far_phase, args.order, args.tolerance)
        waves.append(wave)
        outgoing.append(infinity)
        diagnostics.append(dict(frequency=float(frequency), **controls))
        if index % 24 == 0:
            print(dict(label=args.label, completed=index+1, total=len(frequencies)), flush=True)
    archive = directory/'transfer.npz'
    np.savez_compressed(archive, frequencies=frequencies, frequency_weights=frequency_weights,
        amplitudes=amplitudes, positions=positions, spatial_weights=spatial_weights,
        energy_indices=energy_indices, source_index=source_index, green=np.array(waves),
        infinity=np.array(outgoing), **model)
    report = save(directory, Path(__file__), dict(arguments=vars(args), input_hashes=dependencies(),
        output_hashes={archive.name:digest(archive)}, model=model, detector=detector,
        positive_frequency_support=[.006, .030], spectral_density='(1-z^2)^8/(width*Beta(1/2,9)), width=.012',
        dimensionless_energy='E*R/N', dimensionless_time='t/R',
        source='Canonical real l=2 master shell forcing j(t/R)*delta(y-y_source), rho_source=5',
        source_is_new_physical_matter_model=False, diagnostics=diagnostics,
        maximum_controls={key:max(row[key] for row in diagnostics) for key in diagnostics[0] if key != 'frequency'},
        new_exterior_IVPs=2*len(frequencies), new_interior_or_background_solves=0,
        elapsed_seconds=monotonic()-start))
    print(dict(state=report['state'], elapsed_seconds=report['elapsed_seconds'],
               maximum_controls=report['maximum_controls']), flush=True)


if __name__ == '__main__':
    main()

