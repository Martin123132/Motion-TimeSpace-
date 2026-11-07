from __future__ import annotations

import traceback
import time
from onset_common import *


def main():
    modest()
    label=sys.argv[1]
    variant=sys.argv[2] if len(sys.argv)>2 else 'base'
    folder=ROOT/'runs'/(label+'-'+variant)
    folder.mkdir(parents=True,exist_ok=False)
    started=time.monotonic()
    write_json(folder/'status.json',dict(state='running',pid=os.getpid(),branch=label,variant=variant))
    try:
        source,native=native_for(label)
        grid_nodes=np.linspace(math.log(1e-9),FINAL,4001 if variant=='fine' else 2001)
        density=native.get_background_densities(np.exp(grid_nodes),vars=['cdm','baryon','photon','neutrino','nu','de'])
        grid=dict(efold=grid_nodes,**density)
        np.savez_compressed(folder/'fluids.npz',**grid)
        model=Background(label,grid)
        start=math.log(1e-9 if variant=='early' else 2e-9)
        solution=model.solve(start,2e-11 if variant=='fine' else 2e-10)
        query=np.unique(np.r_[np.linspace(math.log(1e-7),FINAL,1801),np.log(np.linspace(.00016,.000265,14001))])
        states=solution.sol(query)
        names,values=physical(model,query,states)
        native_h=native.hubble_parameter(np.exp(-query)-1)/299792.458
        h_error=float(max(abs(values[0]/native_h-1)))
        np.savez_compressed(folder/'trajectory.npz',efold=query,names=names,values=values,states=states,native_H=native_h,
            masses=model.masses,amplitudes=model.amplitudes,solver_nodes=solution.t)
        report=dict(branch=label,variant=variant,start_scale=math.exp(start),final_scale=math.exp(FINAL),
            nfev=solution.nfev,steps=len(solution.t),elapsed_seconds=time.monotonic()-started,
            finite=bool(np.isfinite(values).all()),max_H_relative_error=h_error,
            max_scaled_momentum_residual=float(max(abs(values[names.index('momentum_scaled')]))),
            initial_scaled_momentum_residual=float(model.unpack(start,model.initial(start))['momentum']),
            new_parameters_fitted=0,nonlinear_two_gradient_response=True)
        finish(folder,report,__file__,[source,NATIVE/'camb/cambdll.dll',folder/'fluids.npz',folder/'trajectory.npz'])
        print(json.dumps(report),flush=True)
    except BaseException as error:
        write_json(folder/'status.json',dict(state='failed',error=repr(error),traceback=traceback.format_exc()))
        raise


if __name__=='__main__':
    main()
