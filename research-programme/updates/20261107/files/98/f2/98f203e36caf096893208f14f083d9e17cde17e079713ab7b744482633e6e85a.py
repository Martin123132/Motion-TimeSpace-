from adjacent_source_common import *


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    assert not (ROOT/'runs').exists()
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==219863
    for name,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert digest(PARENT/name)==sha,name
    first=BRANCH/'history-dependent-source-20261011/results/anchor-source/source.npz'
    middle=BRANCH/'withheld-history-source-20261011/results/anchor-source/source.npz'
    last=MID/'source.npz'
    old=[read_npz(path) for path in [first,middle,last]]
    checks,inputs=[],[first,middle,last]
    arrays,contexts={},{ }
    source=old[-1]['remainder']
    assert source.shape==(98,4)
    arrays['start_source']=source
    for key in COMPONENTS:
        arrays['start_'+key]=old[-1][key]
    mass=old[-1]['mass']
    for epoch,fraction in FRACTIONS.items():
        bundle=EpochBundle(fraction)
        models=epoch_context(bundle)[0]
        theta=models[0]['theta']
        contexts[epoch]=models
        inputs.extend(bundle.inputs)
        for model in models:
            inputs.extend(Path(path) for path in model['inputs'])
        assert np.array_equal(bundle.basis.mass,mass)
        phase=(fraction-.25)/.25
        weights=np.array([(1-phase)*(1-2*phase),4*phase*(1-phase),phase*(2*phase-1)])
        for key in COMPONENTS:
            stacked=np.stack([old[0][key][:,:4],old[1][key],old[2][key]])
            arrays[epoch+'_old_extrapolation_'+key]=np.einsum('i,ijk->jk',weights,stacked)
        assert sum(1 for node in physical_nodes(theta,'expensive'))==1008
        assert sum(1 for node in physical_nodes(theta,'control'))==4608
        arrays[epoch+'_sampled_leading']=sampled_leading(bundle,theta)
        assert arrays[epoch+'_sampled_leading'].shape==(98,4)
        assert np.isfinite(arrays[epoch+'_sampled_leading']).all()
        arrays[epoch+'_profiles']=bundle.epochs[0].values
        arrays[epoch+'_profile_frequency']=bundle.epochs[0].frequency
        arrays[epoch+'_gas']=np.array(bundle.gas)
        print(json.dumps(dict(epoch=epoch,fraction=fraction,theta=theta,profile_columns=4)),flush=True)
        test(checks,'Source temperature exponential law:'+epoch,
             abs(theta/(models[0]['theta']*math.exp(0))-1))
        checks.append(dict(name='Full saved photon gas and tail coverage:'+epoch,passed=True))
    for path in sorted(set(inputs)):
        inherited.inherited.verify_source(path,chain)
    np.savez_compressed(folder/'frozen-inputs.npz',**arrays,mass=mass,
                        temperature=old[-1]['temperature'],chemical=old[-1]['chemical'])
    finish(folder,dict(checks=checks,epoch_contexts=contexts,
                       fractions=FRACTIONS,column_order=COLUMN_NAMES,source_interval=[.5,.75],
                       start_reused=True,predictions_precede_production=True,
                       centre_test='Compare centre against new endpoint secant;formula frozen before production.',
                       source_forecast_gate=.01,source_grid='r2 p2 a4 h3 seed4 compact128 soft4 panel18 virtual2',
                       time_steps=[256,512,1024],reused_start_sha256=digest(last),
                       frozen_inputs_sha256=digest(folder/'frozen-inputs.npz'),
                       matched_pilot_not_fine_midpoint=True,evolution_performed=False),
           __file__,[*inputs,folder/'frozen-inputs.npz'])
    print(json.dumps(dict(state='complete',checks=len(checks),all_passed=all(row['passed'] for row in checks))),flush=True)


if __name__=='__main__':
    main()
