from source_pair_common import *
from propagate_matched_feedback import solve_response
import argparse
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--upper',type=float,choices=[.02,.04],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'shape-error-{args.model}-m{int(args.upper*1000)}'
    folder.mkdir(parents=True,exist_ok=False)
    parent_folder=ROOT/'results'/f'feedback-{args.model}-m{int(args.upper*1000)}'
    physical_source=read_npz(parent_folder/'physical-source.npz')
    discrete_source=read_npz(parent_folder/'discrete-source.npz')
    physical_response=read_npz(parent_folder/'physical-response.npz')
    discrete_response=read_npz(parent_folder/'discrete-response.npz')
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    background=thermal_wave.thermal.ThermalBackground(args.model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    delta=discrete_source['source']-physical_source['source']
    modes=np.column_stack([basis.chemical,basis.temperature])
    duals=basis.mass@modes
    moments=np.einsum('ir,ntik->ntrk',modes,delta)
    coefficients=np.einsum('rs,ntsk->ntrk',linalg.inv(modes.T@duals),moments)
    removed=np.einsum('ir,ntrk->ntik',duals,coefficients)
    shape_only=delta-removed
    weak_scale=max(float(np.max(abs(delta))),1e-300)
    relative_removed=float(np.max(abs(removed))/weak_scale)
    checks=[dict(name='Difference is Compton only',passed=not np.count_nonzero(delta[:,1:])),
        check('Removed weak moment fraction',relative_removed,1e-8)]
    results={}
    reference_gas=discrete_response['gas']-physical_response['gas']
    reference_photon=discrete_response['photon_final']-physical_response['photon_final']
    for label,forcing in [('difference',delta),('shape',shape_only)]:
        packet=dict(coordinate=physical_source['coordinate'],source=forcing)
        solution,errors=solve_response(args.model,packet,2048,ladder,emission,background)
        np.savez_compressed(folder/(label+'-response.npz'),**{key:value for key,value in solution.items() if key!='photon'},photon_final=solution['photon'][-1])
        gas_reference=reference_gas if label=='difference' else results['difference']['gas']
        photon_reference=reference_photon if label=='difference' else results['difference']['photon']
        relative_gas=np.max(abs(solution['gas'][:,:3]-gas_reference[:,:3]),axis=0)/np.maximum(np.max(abs(gas_reference[:,:3]),axis=0),1e-300)
        relative_photon=np.linalg.norm(solution['photon'][-1,:,:3]-photon_reference[:,:3],axis=0)/np.maximum(np.linalg.norm(photon_reference[:,:3],axis=0),1e-300)
        for kind,values in [('gas',relative_gas),('photon',relative_photon)]:
            checks.extend(check('Difference-response:'+label+':'+kind+':'+column,value,1e-4) for column,value in zip(['baseline','join1','join2'],values))
        checks.extend(check('Response:'+label+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
        results[label]=dict(gas=solution['gas'],photon=solution['photon'][-1],comparison_gas=relative_gas.tolist(),
            comparison_photon=relative_photon.tolist(),gas_endpoint=solution['gas'][-1,:3].tolist(),response_errors=errors)
    np.savez_compressed(folder/'forcing.npz',coordinate=physical_source['coordinate'],difference=delta,shape=shape_only,removed=removed,weak_moments=moments)
    inputs=[*[parent_folder/name for name in ['physical-source.npz','discrete-source.npz','physical-response.npz','discrete-response.npz','status.json']],
        *ladder.inputs,*emission.inputs,background.parent.source,background.native_constants,ROOT/'SHAPE-ERROR-ATTRIBUTION.md']
    rows={label:{key:value for key,value in row.items() if key not in ['gas','photon']} for label,row in results.items()}
    finish(folder,dict(checks=checks,model=args.model,upper=args.upper,removed_weak_moment_relative=relative_removed,
        variants=rows,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(model=args.model,upper=args.upper,removed=relative_removed,results=rows,
        failures=[row['name'] for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
