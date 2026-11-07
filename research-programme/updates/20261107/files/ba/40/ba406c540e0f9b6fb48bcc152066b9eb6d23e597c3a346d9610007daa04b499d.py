from __future__ import annotations

import argparse
import time
import traceback

from native_common import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('label')
    parser.add_argument('--accuracy', type=float, default=1.5)
    parser.add_argument('--start-factor', type=float, default=1.)
    parser.add_argument('--seed-scale', type=float, default=1.)
    parser.add_argument('--int-tol-boost', type=float, default=1.)
    parser.add_argument('--background-boost', type=float, default=1.)
    parser.add_argument('--end', type=float, default=.000265)
    args = parser.parse_args()
    modest()
    folder = ROOT / 'runs' / args.label
    folder.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    try:
        table_path = ROOT / 'runs/backgrounds/heavy.npz'
        table = np.load(table_path)
        phase_of_n = interpolate.CubicSpline(table['heavy_efold'], table['phase_h'])
        n_of_phase = interpolate.PchipInterpolator(table['phase_h'], table['heavy_efold'])
        nodes = list(np.linspace(math.log(1e-7), math.log(args.end), 650))
        windows = []
        for center in [.0002, .000225, .00025]:
            center_phase = float(phase_of_n(math.log(center)))
            phases = center_phase + np.linspace(-8*math.pi, 8*math.pi, 1201)
            window = n_of_phase(phases)
            nodes.extend(window)
            windows.append(dict(center=center, phase=center_phase, minimum_a=float(np.exp(window[0])), maximum_a=float(np.exp(window[-1]))))
        nodes = np.unique(nodes)
        nodes = nodes[nodes <= math.log(args.end)]
        scales = np.exp(nodes)
        modes = np.array([.03, .1, 1., 5.])
        rows = []
        for fraction in [0., .5]:
            path = ROOT / 'runs/backgrounds' / ('heavy.npz' if fraction else 'cold.npz')
            params = params_for(path, accuracy=args.accuracy, seed_scale=args.seed_scale,
                initial_time_factor=args.start_factor)
            params.Accuracy.IntTolBoost = 1.
            params.Accuracy.BackgroundTimeStepBoost = args.background_boost
            native = camb.get_background(params)
            times = native.conformal_time(1/scales-1, tol=1e-10)
            native.Params.Accuracy.IntTolBoost = args.int_tol_boost
            print('Evolving native early hierarchy', fraction, len(times), 'times', flush=True)
            data = native.get_time_evolution(modes, times, vars=camb.model.evolve_names, lAccuracyBoost=4)
            name = 'heavy' if fraction else 'cold'
            np.savez_compressed(folder / (name + '.npz'), modes=modes, requested_scale=scales,
                conformal_time=times, values=data, names=np.array(camb.model.evolve_names),
                heavy_background_phase=phase_of_n(nodes))
            rows.append(dict(fraction=fraction, all_finite=bool(np.isfinite(data).all()), shape=list(data.shape)))
            print('Saved', name, flush=True)
        finish(folder, dict(accuracy=args.accuracy, initial_time_factor=args.start_factor, seed_scale=args.seed_scale,
            integration_tolerance_boost=args.int_tol_boost,
            tightened_tolerance_scope='Perturbation evolution only; background initialization uses IntTolBoost=1 and conformal-time queries tol=1e-10',
            background_time_step_boost=args.background_boost,
            windows=windows, rows=rows, elapsed_seconds=time.monotonic()-started,
            separate_scalar_stresses=True, all_standard_species=True, late_heavy_matching=False), __file__,
            list(folder.glob('*.npz')) + list((ROOT / 'runs/backgrounds').glob('*.npz')))
    except BaseException as error:
        write_json(folder / 'status.json', dict(state='failed', error=repr(error), traceback=traceback.format_exc()))
        raise


if __name__ == '__main__':
    main()
