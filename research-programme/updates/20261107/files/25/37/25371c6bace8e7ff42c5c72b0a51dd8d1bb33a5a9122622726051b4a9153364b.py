from __future__ import annotations

from precision_common import *


def main():
    modest()
    folder=ROOT/'results/tiny-mode-precision'
    folder.mkdir(parents=True,exist_ok=False)
    source=ROOT/'runs/sources/unmatched-base.npz'
    table=np.load(source)
    sample=np.load(ROOT/'runs/exact/chunk-0000.npz')
    requested=sample['requested_scale']
    modes=np.array([1e-5,3e-5,1e-4,3e-4])
    matching=np.load(ROOT/'runs/projection/a225-w6-d8.npz')
    center=float(matching['matching_scale'])
    density=float(matching['matching_density'])
    reference=np.load(PARENT/'runs/heavy-fine/trajectory.npz')
    named={name:reference['values'][index] for index,name in enumerate(reference['names'])}
    selected=np.exp(reference['efold'])>=.00016
    scale=np.exp(reference['efold'][selected])
    named={name:value[selected] for name,value in named.items()}
    mass=float(reference['masses'][1])
    energy=named['dotphi_h']*named['dotf_h']+mass**2*named['phi_h']*named['f_h']
    pressure=named['dotphi_h']*named['dotf_h']-mass**2*named['phi_h']*named['f_h']
    names=camb.model.evolve_names
    reference_names=np.array(['a','mts_drho_h','mts_q_h','mts_dp_h','H'])
    reference_values=np.array([np.array([scale,4*wave**2*scale**2*energy,
        4*wave**3*scale*named['dotphi_h']*named['f_h'],4*wave**2*scale**2*pressure,scale*named['H']]).T for wave in modes])
    expected=projection(dict(names=reference_names,modes=modes,values=reference_values),table,center,density,6,8)['delta']
    rows=[]
    paths=[source,ROOT/'runs/projection/a225-w6-d8.npz',PARENT/'runs/heavy-fine/trajectory.npz',
        NATIVE/'fortran/camb_python.f90',NATIVE/'camb/cambdll.dll']
    for boost in [6,8,9]:
        params=inherited.inherited.params_for(source)
        native=camb.get_background(params)
        native.Params.Accuracy.IntTolBoost=boost
        times=native.conformal_time(1/requested-1,tol=1e-10)
        values=native.get_time_evolution(modes,times,vars=names,lAccuracyBoost=4)
        assert np.isfinite(values).all() and np.all(values[:,:,names.index('a')]>0)
        actual=projection(dict(names=np.array(names),modes=modes,values=values),table,center,density,6,8)['delta']
        output=folder/('boost-'+str(boost)+'.npz')
        np.savez_compressed(output,modes=modes,requested_scale=requested,names=names,values=values)
        paths.append(output)
        for wave,derived,numeric in zip(modes,expected,actual):
            rows.append(dict(boost=boost,k_Mpc_inverse=float(wave),derived_curvature=float(derived),native=float(numeric),
                relative_difference=float(numeric/derived-1)))
        print(json.dumps(rows[-len(modes):]),flush=True)
    finish(folder,dict(rows=rows,production_rows_replaced=False,
        interpretation='Direct native tolerance-control test of tiny-amplitude matching rows; leading-gradient reference has a finite-k remainder. Standard transfer columns also pass through default-real Arr in the pinned exporter, so bitwise equality is not unlimited precision.'),__file__,paths)


if __name__=='__main__':
    main()
