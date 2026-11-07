from __future__ import annotations

import traceback
from precision_common import *


def main():
    modest()
    folder=ROOT/'runs/sources'
    folder.mkdir(parents=True,exist_ok=False)
    configurations=([('unmatched',TABLES/'heavy.npz'),('cold',TABLES/'cold.npz')]+
        [(tag,MATCHING/'runs/matching-inputs'/(tag+'-w6-d8.npz')) for tag in ['a200','a225','a250']])
    reports=[]
    paths=[]
    started=time.monotonic()
    write_json(folder/'status.json',dict(state='running',pid=os.getpid(),completed=[]))
    try:
        for tag,source in configurations:
            model=SlowSource(source)
            for variant,rtol in [('base',3e-11),('fine',3e-12)] if tag in ['unmatched','a225','cold'] else [('base',3e-11)]:
                amplitude,pieces,expansion,history=model.shoot(rtol)
                old=model.old
                nodes=np.unique(np.r_[old['efold'],*[piece.t for piece in pieces]])
                sample=model.sample(nodes,amplitude,pieces)
                candidate={key:old[key].copy() for key in old.files if key not in ['efold','scale','phi_s','phidot_s','expansion2','heavy_logrho_mpc','heavy_w']}
                density,density_n=model.heavy(nodes)
                candidate.update(efold=nodes,scale=np.exp(nodes),**{key:value for key,value in sample.items() if key!='conditioned_velocity'})
                if model.heavy.fraction:
                    candidate.update(heavy_logrho_mpc=np.log(3*UNIT**2*density),heavy_w=-1-density_n/(3*density))
                path=folder/(tag+'-'+variant+'.npz')
                np.savez_compressed(path,**candidate)
                common=np.linspace(START,0.,4001)
                direct=model.sample(common,amplitude,pieces)
                old_expansion=np.exp(interpolate.CubicSpline(old['efold'],np.log(old['expansion2']))(common))
                velocity_old=interpolate.CubicSpline(old['efold'],old['phidot_s'])(common)
                early=(common>math.log(.00005))&(common<math.log(.00026))
                row=dict(tag=tag,variant=variant,rtol=rtol,flatness_residual=expansion-1,
                    amplitude=amplitude,old_amplitude=float(old['phi_s'][0])/math.sqrt(6),
                    amplitude_fractional_change=amplitude/(float(old['phi_s'][0])/math.sqrt(6))-1,
                    max_H_change=float(max(abs(np.sqrt(direct['expansion2']/old_expansion)-1))),
                    max_early_velocity_change=float(max(abs(velocity_old[early]/direct['phidot_s'][early]-1))),
                    nfev_final=sum(piece.nfev for piece in pieces),shooting=history,nodes=len(nodes))
                reports.append(row)
                paths.extend([source,path])
                print(json.dumps(row),flush=True)
                write_json(folder/'status.json',dict(state='running',pid=os.getpid(),completed=[(row['tag'],row['variant']) for row in reports],elapsed_seconds=time.monotonic()-started))
        finish(folder,dict(rows=reports,elapsed_seconds=time.monotonic()-started,full_history=True,
            same_calibration_equation=True,no_observations_refitted=True),__file__,sorted(set(paths))+[BRANCH/'radiation-and-slow-field-transfer-20261007/radiation_common.py'])
    except BaseException as error:
        write_json(folder/'status.json',dict(state='failed',error=repr(error),traceback=traceback.format_exc()))
        raise


if __name__=='__main__':
    main()
