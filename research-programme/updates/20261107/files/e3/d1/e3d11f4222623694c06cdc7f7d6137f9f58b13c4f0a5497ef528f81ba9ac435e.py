from __future__ import annotations

import traceback
from precision_common import *


def main():
    modest()
    label=sys.argv[1]
    configurations={'heavy':'a225-w6-d8','heavy-200':'a200-w6-d8','heavy-250':'a250-w6-d8','heavy-window4':'a225-w4-d8'}
    heavy=label!='cold'
    projection_label=configurations[label] if heavy else None
    source=ROOT/'runs/projection'/(projection_label+'.npz') if heavy else ROOT/'runs/sources/cold-base.npz'
    folder=ROOT/'runs'/label
    folder.mkdir(parents=True,exist_ok=False)
    native=camb.get_background(inherited.inherited.params_for(source))
    native.Params.Accuracy.IntTolBoost=6
    requested=inherited.late_scales()
    times=native.conformal_time(1/requested-1,tol=1e-10)
    grid=inherited.modes(2)
    names=camb.model.evolve_names
    started=time.monotonic()
    report=dict(state='running',pid=os.getpid(),branch='heavy' if heavy else 'cold',projection=projection_label,completed=0,total=len(grid))
    write_json(folder/'status.json',report)
    try:
        for start in range(0,len(grid),16):
            modes=grid[start:start+16]
            values=native.get_time_evolution(modes,times,vars=names,lAccuracyBoost=4)
            assert np.isfinite(values).all()
            assert np.all(values[:,:,names.index('a')]>0)
            assert np.max(abs(values[:,:,names.index('a')]/requested-1))<1e-6
            assert np.all(values[:,-1,names.index('mts_match_count')]==(1 if heavy else 0))
            assert np.max(abs(values[:,:,names.index('mts_nonheavy_change')]))==0
            np.savez_compressed(folder/f'chunk-{start:04d}.npz',modes=modes,values=values,names=names,
                requested_scale=requested,conformal_time=times)
            report.update(completed=start+len(modes),elapsed_seconds=time.monotonic()-started)
            write_json(folder/'status.json',report)
            print(json.dumps(report),flush=True)
        densities=native.get_background_densities(requested,vars=['cdm','baryon','nu'])
        np.savez_compressed(folder/'background.npz',requested_scale=requested,**densities,
            rdrag=native.get_derived_params()['rdrag'],redshifts=inherited.TARGET_REDSHIFTS,
            DM=native.comoving_radial_distance(inherited.TARGET_REDSHIFTS),H_km_s_Mpc=native.hubble_parameter(inherited.TARGET_REDSHIFTS))
        finish(folder,dict(branch=report['branch'],projection=projection_label,completed=len(grid),k_count=len(grid),
            elapsed_seconds=time.monotonic()-started,exactly_one_heavy_match=heavy,nonheavy_match_jump=0),__file__,
            [source,folder/'background.npz',NATIVE/'camb/cambdll.dll',*folder.glob('chunk-*.npz')])
    except BaseException as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        write_json(folder/'status.json',report)
        raise


if __name__=='__main__':
    main()
