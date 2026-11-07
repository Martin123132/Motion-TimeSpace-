from __future__ import annotations

import argparse
import time
import traceback
from spectrum_common import *


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('label')
    parser.add_argument('--refinement',type=int,default=2)
    parser.add_argument('--chunk',type=int,default=16)
    args=parser.parse_args()
    folder=ROOT/'runs'/args.label
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'COMPLETE').exists()
    started=time.monotonic()
    table=np.load(BACKGROUND)
    source=np.load(EARLY/'runs/final-bg8-start/heavy.npz')
    requested=source['requested_scale']
    phase_of_n=interpolate.CubicSpline(table['heavy_efold'],table['phase_h'])
    grid=modes(args.refinement)
    initial=dict(state='running',arguments=vars(args),k_count=len(grid),completed=0,
        grid=grid.tolist(),source_hash=digest(BACKGROUND),script_sha256=digest(__file__))
    status_path=folder/'status.json'
    if status_path.exists():
        old=json.loads(status_path.read_text())
        assert old['arguments']==vars(args) and old['source_hash']==initial['source_hash']
        assert old['script_sha256']==digest(__file__)
    write_json(status_path,initial)
    try:
        params=inherited.params_for(BACKGROUND)
        native=camb.get_background(params)
        times=native.conformal_time(1/requested-1,tol=1e-10)
        native.Params.Accuracy.IntTolBoost=6
        names=camb.model.evolve_names
        with (folder/'log.txt').open('a',encoding='utf-8') as log:
            for start in range(0,len(grid),args.chunk):
                stop=min(start+args.chunk,len(grid))
                selected=grid[start:stop]
                path=folder/f'chunk-{start:04d}.npz'
                if path.exists():
                    saved=np.load(path)
                    assert np.array_equal(saved['modes'],selected) and np.isfinite(saved['values']).all()
                else:
                    values=native.get_time_evolution(selected,times,vars=names,lAccuracyBoost=4)
                    assert np.isfinite(values).all()
                    assert np.max(abs(values[:,:,names.index('mts_match_count')]))==0
                    np.savez_compressed(path,values=values,modes=selected,names=names,
                        requested_scale=requested,conformal_time=times,background_phase=phase_of_n(np.log(requested)))
                line=f'Exact early states saved: {stop}/{len(grid)} modes; elapsed {time.monotonic()-started:.1f}s'
                print(line,flush=True)
                log.write(line+'\n'); log.flush()
                initial.update(completed=stop,elapsed_seconds=time.monotonic()-started)
                write_json(status_path,initial)
        finish(folder,dict(arguments=vars(args),k_count=len(grid),completed=len(grid),elapsed_seconds=time.monotonic()-started,
            source_hash=digest(BACKGROUND),single_thread=True,independent_sourced_modes=True),__file__,
            [BACKGROUND,EARLY/'runs/final-bg8-start/heavy.npz',*folder.glob('chunk-*.npz')])
    except BaseException as error:
        initial.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        write_json(status_path,initial)
        raise


if __name__=='__main__':
    main()
