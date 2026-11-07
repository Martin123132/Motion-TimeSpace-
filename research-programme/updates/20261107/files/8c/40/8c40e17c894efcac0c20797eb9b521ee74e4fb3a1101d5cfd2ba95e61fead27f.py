from common import *
from extend import make_rhs,observables,save_dense
from thermal_candidate import Thermal
from scipy.integrate import solve_ivp
from types import SimpleNamespace
import numpy as np
import time


def main():
    modest()
    check_parent()
    require(read(ROOT/'validation-01.end.json')['exit_code']==1,'retained dense gate failure')
    diagnosis=read(ROOT/'dense-diagnosis/result.json')
    require(diagnosis['no_new_ode_solves'],'saved-polynomial diagnosis')
    frozen=read(ROOT/'extension/freeze.json')
    configuration=frozen['configurations']['heavy']
    parameters=configuration['tube']
    require(parameters['inverse_initial']**2>parameters['slow_coefficient'],'finite min-bound crossing')
    switch=configuration['initial_efold']+np.log(parameters['matter_coefficient']/(parameters['inverse_initial']**2-parameters['slow_coefficient']))/3
    require(configuration['initial_efold']<switch<configuration['final_efold'],'internal analytic switch')
    for row in diagnosis['reports']:
        if row['model']=='heavy' and row['maximum']>=GATE:
            first=row['efold']-.3819660112501051*row['interval_width']
            require(first<switch<first+row['interval_width'],'failed dense interval straddles derived switch')
    destination=ROOT/'split-envelope'
    destination.mkdir(exist_ok=False)
    write(destination/'freeze.json',dict(configuration=configuration,controls=frozen['controls'],target=frozen['target'],switch_efold=float(switch),
                                      sources=frozen_sources(),source_unchanged=True,tolerances_unchanged=True,new_physical_parameters=0))
    thermal=Thermal(configuration['thermal_parameters'])
    initial=np.zeros(5)
    initial[:2]=np.asarray(configuration['initial_energy_coordinates'])[0]/configuration['slow_unit']
    grid=load(ROOT/'extension/heavy/fine.npz')['efold']
    details=[]
    for label,method,tolerance in frozen['controls']:
        started=time.monotonic()
        segments=[]
        state=initial.copy()
        for first,last in ((configuration['initial_efold'],switch),(switch,configuration['final_efold'])):
            guard()
            result=solve_ivp(make_rhs(configuration,thermal),(first,last),state,method=method,rtol=tolerance,atol=tolerance/100,max_step=.05,dense_output=True)
            require(result.success,'split comparison integration')
            segments.append(result)
            state=result.y[:,-1].copy()
        nodes=np.concatenate([segments[0].sol.ts,segments[1].sol.ts[1:]])
        interpolants=segments[0].sol.interpolants+segments[1].sol.interpolants
        dense=type(segments[0].sol)(nodes,interpolants)
        result=SimpleNamespace(sol=dense,t=np.concatenate([segments[0].t,segments[1].t[1:]]),y=np.concatenate([segments[0].y,segments[1].y[:,1:]],axis=1))
        packet=observables(configuration,thermal,grid,dense(grid).T)
        np.savez_compressed(destination/(label+'.npz'),**packet)
        save_dense(destination/(label+'-dense.npz'),result,method)
        continuity=float(np.max(abs(segments[0].y[:,-1]-segments[1].y[:,0])))
        require(continuity==0,'exact restart state copy')
        details.append(dict(label=label,method=method,rtol=tolerance,atol=tolerance/100,nfev=sum(segment.nfev for segment in segments),
                            elapsed_seconds=time.monotonic()-started,continuity_error=continuity,segments=2))
        print(label,'split at',switch,'nfev',details[-1]['nfev'],flush=True)
    check_parent()
    write(destination/'result.json',dict(state='split_comparison_complete',reports=details,source_hashes=frozen_sources(),new_ode_segments=6,
                                       early_phase_replay_reused=True,cold_control_reused=True,original_failed_validation_retained=True))


if __name__=='__main__':
    main()
