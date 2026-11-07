from __future__ import annotations

import traceback
from precision_common import *


def main():
    modest()
    folder=ROOT/'runs/exact'
    folder.mkdir(parents=True,exist_ok=False)
    source=ROOT/'runs/sources/unmatched-base.npz'
    old_query=BRANCH/'native-two-field-transfer-20261007/runs/final-bg8-start/heavy.npz'
    requested=np.load(old_query)['requested_scale']
    requested=np.unique(np.r_[1e-6,requested[requested>=1e-6]])
    grid=inherited.modes(2)
    params=inherited.inherited.params_for(source)
    native=camb.get_background(params)
    native.Params.Accuracy.IntTolBoost=6
    times=native.conformal_time(1/requested-1,tol=1e-10)
    names=camb.model.evolve_names
    started=time.monotonic()
    report=dict(state='running',pid=os.getpid(),completed=0,total=len(grid))
    write_json(folder/'status.json',report)
    try:
        for start in range(0,len(grid),16):
            modes=grid[start:start+16]
            values=native.get_time_evolution(modes,times,vars=names,lAccuracyBoost=4)
            assert np.isfinite(values).all()
            assert np.all(values[:,:,names.index('a')]>0)
            assert np.max(abs(values[:,:,names.index('a')]/requested-1))<1e-6
            assert np.max(abs(values[:,:,names.index('mts_match_count')]))==0
            np.savez_compressed(folder/f'chunk-{start:04d}.npz',modes=modes,values=values,names=names,
                requested_scale=requested,conformal_time=times)
            report.update(completed=start+len(modes),elapsed_seconds=time.monotonic()-started)
            write_json(folder/'status.json',report)
            print(json.dumps(report),flush=True)
        finish(folder,dict(completed=len(grid),k_count=len(grid),elapsed_seconds=time.monotonic()-started,
            positive_native_scales=True,matching_count_zero=True),__file__,[source,old_query,NATIVE/'camb/cambdll.dll',*folder.glob('chunk-*.npz')])
    except BaseException as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        write_json(folder/'status.json',report)
        raise


if __name__=='__main__':
    main()
