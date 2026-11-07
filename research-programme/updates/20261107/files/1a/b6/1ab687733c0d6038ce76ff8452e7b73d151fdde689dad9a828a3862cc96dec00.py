from __future__ import annotations

import traceback
from constraint_common import *


def main():
    modest()
    folder=ROOT/'runs/native'
    folder.mkdir(parents=True,exist_ok=True)
    inputs=[]
    report=dict(state='running',pid=os.getpid(),completed=0,total=2)
    write_json(folder/'status.json',report)
    try:
        old=np.load(HISTORY/'runs/exact/chunk-0000.npz')['requested_scale']
        for label,source_name in [('heavy','unmatched-base.npz'),('cold','cold-base.npz')]:
            source=HISTORY/'runs/sources'/source_name
            inputs.append(source)
            params=inherited.inherited.inherited.inherited.params_for(source)
            background=camb.get_background(params)
            background.Params.Accuracy.IntTolBoost=6
            anchor_times=background.conformal_time(1/np.r_[1e-9,old]-1,tol=1e-10)
            times=np.unique(np.r_[anchor_times,np.linspace(anchor_times[0],anchor_times[-1],2001),np.geomspace(anchor_times[0],anchor_times[-1],301)])
            modes=np.array([.03,.1,1.])
            names=camb.model.evolve_names
            started=time.monotonic()
            values=background.get_time_evolution(modes,times,vars=names,lAccuracyBoost=4)
            assert np.isfinite(values).all()
            assert np.max(abs(values[:,:,names.index('mts_match_count')]))==0
            np.savez_compressed(folder/(label+'.npz'),modes=modes,names=names,values=values,conformal_time=times,
                baryon_fraction=params.ombh2/(params.ombh2+params.omch2),effective_neutrino_number=params.N_eff)
            report.update(completed=report['completed']+1,last_label=label,last_seconds=time.monotonic()-started)
            write_json(folder/'status.json',report)
            print(json.dumps(report),flush=True)
        finish(folder,dict(completed=2,models=['heavy','cold'],modes=[.03,.1,1.],matching_disabled=True,
            identical_native_accuracy=True,all_checks_passed=True),__file__,[*inputs,NATIVE/'camb/cambdll.dll',HISTORY/'runs/exact/chunk-0000.npz'])
    except BaseException as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        write_json(folder/'status.json',report)
        raise


if __name__=='__main__':
    main()
