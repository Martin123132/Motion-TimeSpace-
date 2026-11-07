from __future__ import annotations

from collision_common import *


def main():
    modest()
    folder=ROOT/'runs/backgrounds'
    folder.mkdir(parents=True,exist_ok=True)
    inputs=[]
    rows=[]
    for label,source_name in [('heavy','unmatched-base.npz'),('cold','cold-base.npz')]:
        path=PARENT/'runs/native'/(label+'.npz')
        inputs.append(path)
        packet=np.load(path)
        names=list(packet['names'])
        index=int(np.flatnonzero(np.isclose(packet['modes'],.1,rtol=1e-13))[0])
        raw=packet['values'][index]
        selected=raw[:,names.index('a')]>=.999999e-6
        values=raw[selected]
        times=packet['conformal_time'][selected]
        source=HISTORY/'runs/sources'/source_name
        inputs.append(source)
        params=inherited.inherited.inherited.inherited.inherited.params_for(source)
        background=camb.get_background(params)
        thermal=background.get_background_time_evolution(times,vars=['opacity','cs2b','T_b','x_e'])
        scales=np.ascontiguousarray(values[:,names.index('a')])
        densities=background.get_background_densities(scales,vars=['baryon','photon'])
        ratio=.75*densities['baryon']/densities['photon']
        assert all(np.isfinite(value).all() for value in thermal.values())
        assert np.min(thermal['opacity'])>0 and np.min(ratio)>0
        np.savez_compressed(folder/(label+'.npz'),times=times,values=values,names=names,scales=scales,
            ratio=ratio,**thermal,mode=.1,baryon_fraction=packet['baryon_fraction'],TCMB=params.TCMB)
        row=dict(model=label,samples=len(times),scale_range=scales[[0,-1]].tolist(),
            opacity_range=[float(np.min(thermal['opacity'])),float(np.max(thermal['opacity']))],
            baryon_inertia_ratio_range=[float(np.min(ratio)),float(np.max(ratio))])
        rows.append(row)
        print(json.dumps(row),flush=True)
    finish(folder,dict(all_checks_passed=True,rows=rows,source_parameters_unchanged=True,
        native_opacity_not_recalibrated=True),__file__,[*inputs,NATIVE/'camb/cambdll.dll',NATIVE/'fortran/constants.f90'])


if __name__=='__main__':
    main()
