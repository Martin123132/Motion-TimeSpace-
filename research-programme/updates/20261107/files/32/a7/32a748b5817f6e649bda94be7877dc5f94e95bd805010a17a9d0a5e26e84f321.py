from __future__ import annotations

import argparse
import time
import traceback
from spectrum_common import *


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('label')
    parser.add_argument('--branch',choices=['heavy','cold','lcdm'],default='heavy')
    parser.add_argument('--projection',default='a225-w6-d8')
    parser.add_argument('--bg',type=float,default=8.)
    parser.add_argument('--chunk',type=int,default=16)
    args=parser.parse_args()
    folder=ROOT/'runs'/args.label
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'COMPLETE').exists()
    source=ROOT/'runs/projection'/(args.projection+'.npz') if args.branch=='heavy' else EARLY/'runs/backgrounds/cold.npz'
    params=inherited.params_for(source,background_boost=args.bg)
    if args.branch=='lcdm':
        params.DarkEnergy=camb.dark_energy.DarkEnergyFluid()
    native=camb.get_background(params)
    requested=late_scales()
    times=native.conformal_time(1/requested-1,tol=1e-10)
    native.Params.Accuracy.IntTolBoost=6
    grid=modes(2)
    names=camb.model.evolve_names
    started=time.monotonic()
    report=dict(state='running',arguments=vars(args),source_hash=digest(source),script_sha256=digest(__file__),completed=0)
    if (folder/'status.json').exists():
        saved=json.loads((folder/'status.json').read_text())
        assert saved['arguments']==vars(args) and saved['source_hash']==report['source_hash']
        assert saved['script_sha256']==report['script_sha256']
    write_json(folder/'status.json',report)
    try:
        with (folder/'log.txt').open('a',encoding='utf-8') as log:
            for start in range(0,len(grid),args.chunk):
                stop=min(start+args.chunk,len(grid))
                selected=grid[start:stop]
                path=folder/f'chunk-{start:04d}.npz'
                if path.exists():
                    output=np.load(path)
                    assert np.array_equal(output['modes'],selected) and np.isfinite(output['values']).all()
                else:
                    values=native.get_time_evolution(selected,times,vars=names,lAccuracyBoost=4)
                    assert np.isfinite(values).all()
                    expected=1 if args.branch=='heavy' else 0
                    assert np.all(values[:,-1,names.index('mts_match_count')]==expected)
                    assert np.max(abs(values[:,:,names.index('mts_nonheavy_change')]))==0
                    np.savez_compressed(path,values=values,modes=selected,names=names,
                        requested_scale=requested,conformal_time=times)
                line=f'{args.label}: saved {stop}/{len(grid)}; elapsed {time.monotonic()-started:.1f}s'
                print(line,flush=True);log.write(line+'\n');log.flush()
                report.update(completed=stop,elapsed_seconds=time.monotonic()-started)
                write_json(folder/'status.json',report)
        densities=native.get_background_densities(requested,vars=['cdm','baryon','nu'])
        np.savez_compressed(folder/'background.npz',requested_scale=requested,**densities,
            rdrag=native.get_derived_params()['rdrag'],redshifts=TARGET_REDSHIFTS,
            DM=native.comoving_radial_distance(TARGET_REDSHIFTS),
            H_km_s_Mpc=native.hubble_parameter(TARGET_REDSHIFTS))
        finish(folder,dict(arguments=vars(args),completed=len(grid),k_count=len(grid),
            elapsed_seconds=time.monotonic()-started,source_hash=digest(source),all_finite=True),__file__,
            [source,folder/'background.npz',*folder.glob('chunk-*.npz')])
    except BaseException as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        write_json(folder/'status.json',report)
        raise


if __name__=='__main__':
    main()
