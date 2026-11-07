from __future__ import annotations

import time
from velocity_common import *


def main():
    modest()
    folder=ROOT/'results/response-tables'
    folder.mkdir(parents=True,exist_ok=False)
    started=time.monotonic()
    reports=[]
    for label in ['heavy','cold','lcdm']:
        angular=AngularResponse(label)
        zero_poles=angular.poles(0.)
        for family in FAMILIES:
            poles=np.array([angular.poles(variance,family) for variance in VARIANCE_GRID])
            for cap in ['NGC','SGC']:
                packet=np.load(PARENT/'results/prepared'/(cap+'.npz'))
                table=np.array([convolved(row,packet['operator']) for row in poles])
                parent=np.load(PARENT/'results/response'/(label+'-'+cap+'.npz'))
                difference=float(np.max(abs(table[0]-parent['basis'])))
                assert difference<1e-7,difference
                np.savez_compressed(folder/(label+'-'+family+'-'+cap+'.npz'),grid=VARIANCE_GRID,basis=table,poles=poles)
                reports.append(dict(branch=label,family=family,cap=cap,zero_limit_max_difference=difference))
            print(label,family,f'{time.monotonic()-started:.1f}s',flush=True)
    finish(folder,dict(tables=reports,variance_grid_count=len(VARIANCE_GRID),single_thread=True),__file__,
        [*[PARENT/'results/prepared'/(cap+'.npz') for cap in ['NGC','SGC']],
            *[PARENT/'results/response'/(label+'-'+cap+'.npz') for label in ['heavy','cold','lcdm'] for cap in ['NGC','SGC']],
            *[SPECTRUM/'results/spectrum'/(label+'.npz') for label in ['heavy','cold','lcdm']],
            *[SPECTRUM/'runs'/label/'background.npz' for label in ['heavy','cold','lcdm']],*folder.glob('*.npz')])


if __name__=='__main__':
    main()
