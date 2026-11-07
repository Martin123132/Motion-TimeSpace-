from __future__ import annotations

import argparse
import time
import traceback
from matching_common import *


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('label')
    parser.add_argument('--input', default='a225-w6-d8')
    parser.add_argument('--cold', action='store_true')
    parser.add_argument('--lcdm', action='store_true')
    parser.add_argument('--raw', action='store_true')
    parser.add_argument('--bg', type=float, default=8.)
    parser.add_argument('--inttol', type=float, default=6.)
    parser.add_argument('--end', type=float, default=1.)
    args = parser.parse_args()
    folder = ROOT / 'runs' / args.label
    folder.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    try:
        source = PARENT / 'runs/backgrounds/cold.npz' if args.cold else ROOT / 'runs/matching-inputs' / (args.input+'.npz')
        params = params_for(source, background_boost=args.bg)
        if args.lcdm:
            params.DarkEnergy = camb.dark_energy.DarkEnergyFluid()
        native = camb.get_background(params)
        source_table = np.load(source)
        center = float(source_table['matching_scale']) if not args.cold else .000225
        requested = np.unique(np.concatenate([np.geomspace(1e-7, args.end, 901),
            center*np.exp(np.linspace(-.02, .02, 301)),
            [.0003, .0005, .001, .01, .1, 1/3, .5, 1.]]))
        requested = requested[requested <= args.end]
        times = native.conformal_time(1/requested-1, tol=1e-10)
        native.Params.Accuracy.IntTolBoost = args.inttol
        if args.raw:
            native.Params.DarkEnergy.matching_raw = 1.
        print('Native evolution', args.label, flush=True)
        values = native.get_time_evolution(MODES, times, vars=camb.model.evolve_names, lAccuracyBoost=4)
        names = camb.model.evolve_names
        densities = native.get_background_densities(requested, vars=['cdm', 'baryon', 'nu'])
        np.savez_compressed(folder / 'evolution.npz', values=values, names=names, modes=MODES,
            requested_scale=requested, conformal_time=times, **{'background_'+key:value for key,value in densities.items()})
        finish(folder, dict(arguments=vars(args), elapsed_seconds=time.monotonic()-started,
            finite=bool(np.isfinite(values).all()), end_scale=float(values[0,-1,names.index('a')]),
            maximum_scale_map_error=float(np.max(abs(values[0,:,names.index('a')]/requested-1))),
            matching_count=values[:,-1,names.index('mts_match_count')].tolist(),
            maximum_nonheavy_state_change=float(np.max(abs(values[:,:,names.index('mts_nonheavy_change')]))),
            state_counts=values[:,-1,names.index('mts_preserved_states')].tolist()),
            __file__, [source, *native_hashes(), folder/'evolution.npz'])
        print('Finished', args.label, time.monotonic()-started, flush=True)
    except BaseException as error:
        write_json(folder / 'status.json', dict(state='failed', error=repr(error), traceback=traceback.format_exc()))
        raise


if __name__ == '__main__':
    main()
