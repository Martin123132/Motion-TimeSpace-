from __future__ import annotations

from onset_common import *


def main():
    modest()
    folder=ROOT/'results/source-precision'
    folder.mkdir(parents=True,exist_ok=False)
    grid=ROOT/'runs/heavy-fine/fluids.npz'
    model=Background('heavy',np.load(grid))
    start=math.log(2e-9)
    reference=model.solve(start,2e-11)
    initial=model.initial(start)
    initial_data=model.unpack(start,initial)
    state0=[initial_data['phi'][0]/math.sqrt(6),initial_data['phi_n'][0]/math.sqrt(6)]

    def equation(efold,state):
        data=model.unpack(efold,reference.sol(efold))
        return [state[1],-(3+data['h'])*state[1]-data['omega'][0]**2*state[0]]

    query=np.log(np.linspace(.00005,.00026,6001))
    names,values=physical(model,query,reference.sol(query))
    reference_velocity=values[names.index('dotphi_s')]
    rows=[]
    packets={}
    for label,atol in [('old-absolute-tolerance',1e-13),('component-resolved',[1e-15,1e-29])]:
        solved=integrate.solve_ivp(equation,(start,FINAL),state0,method='DOP853',rtol=3e-11,atol=atol,max_step=.04,dense_output=True)
        assert solved.success
        state=solved.sol(query)
        velocity=math.sqrt(6)*state[1]*values[names.index('H')]
        error=float(max(abs(velocity/reference_velocity-1)))
        rows.append(dict(label=label,atol=atol,nfev=solved.nfev,max_velocity_relative_error=error))
        packets[label]=velocity
    original=interpolate.CubicSpline(model.table['efold'],model.table['phidot_s'])(query)/np.exp(query)
    output=folder/'precision-control.npz'
    np.savez_compressed(output,efold=query,reference_velocity=reference_velocity,original_velocity=original,**packets)
    finish(folder,dict(rows=rows,original_source_velocity_max_relative_error=float(max(abs(original/reference_velocity-1))),
        same_mass_and_initial_amplitude=True,no_coefficients_fitted=True,
        interpretation='Controlled replay on the same resolved heavy background. Isolates failure of an absolute tolerance larger than the slow velocity; does not assert identical adaptive steps to the original full shooting solve.'),
        __file__,[grid,model.source,output,BRANCH/'radiation-and-slow-field-transfer-20261007/radiation_common.py'])
    print(json.dumps(dict(rows=rows)),flush=True)


if __name__=='__main__':
    main()
