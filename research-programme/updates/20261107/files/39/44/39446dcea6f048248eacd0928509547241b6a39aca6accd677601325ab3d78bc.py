from holdout_common import *


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    assert not (ROOT/'runs').exists()
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    for name,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert digest(PARENT/name)==sha,name
    source_path=PARENT/'results/adjacent-sources/source.npz'
    start_path=parent.MID/'source.npz'
    source,start=read_npz(source_path),read_npz(start_path)
    checks,arrays=[],{}
    weights=np.array([.375,.75,-.125])
    for key in COMPONENTS:
        stacked=np.stack([start[key],source['centre_'+key],source['end_'+key]])
        arrays['predicted_'+key]=np.einsum('i,ijk->jk',weights,stacked)
    arrays['predicted']=quadratic(source,PHASE)
    test(checks,'Independent Lagrange prediction',
         np.max(abs(arrays['predicted']-arrays['predicted_remainder']))/
         np.max(abs(arrays['predicted'])),1e-12)
    for kind in ['local','cubic']:
        assert bubble(PHASE,kind)==1
        assert all(bubble(node,kind)==0 for node in [0,.5,1])
    checks.append(dict(name='Frozen defect shapes preserve all three anchors',passed=True))
    prediction_path=folder/'frozen-prediction.npz'
    np.savez_compressed(prediction_path,**arrays,mass=source['mass'],
                        temperature=source['temperature'],chemical=source['chemical'],
                        fraction=.5625,phase=PHASE,weights=weights)
    write_json(folder/'prediction-lock.json',dict(frozen_utc=datetime.now(timezone.utc).isoformat(),
        fraction=.5625,source_gate=.01,defect_shapes=['local','cubic'],event_nodes_started=False,
        prediction_sha256=digest(prediction_path),parent_source_sha256=digest(source_path),
        method_sha256=digest(ROOT/'DERIVATION.md'),common_sha256=digest(ROOT/'holdout_common.py')))
    bundle=EpochBundle(.5625)
    models=epoch_context(bundle)[0]
    theta=models[0]['theta']
    background=thermal_wave.thermal.ThermalBackground('heavy')
    test(checks,'Independent exponential source temperature',
         abs(theta/background.at(.5625*background.end)['thermal_parameter']-1),1e-14)
    assert np.array_equal(bundle.basis.mass,source['mass'])
    sampled=sampled_leading(bundle,theta)
    np.savez_compressed(folder/'frozen-inputs.npz',holdout_sampled_leading=sampled,
                        profiles=bundle.epochs[0].values,frequency=bundle.epochs[0].frequency,
                        gas=np.array(bundle.gas))
    inputs=[source_path,start_path,prediction_path,folder/'prediction-lock.json',
            folder/'frozen-inputs.npz',*bundle.inputs]
    inputs.extend(Path(path) for model in models for path in model['inputs'])
    for path in inputs:
        if not path.is_relative_to(ROOT):
            inherited.inherited.verify_source(path,chain)
    checks.append(dict(name='Finite full photon gas history at independent temperature',
                       passed=bool(sampled.shape==(98,4) and np.isfinite(sampled).all())))
    finish(folder,dict(checks=checks,epoch_contexts={'holdout':models},fractions=FRACTIONS,
                       column_order=COLUMN_NAMES,frozen_inputs_sha256=digest(folder/'frozen-inputs.npz'),
                       prediction_sha256=digest(prediction_path),source_forecast_gate=.01,
                       baseline_reused_not_zero=True,prediction_frozen_before_new_events=True),
           __file__,inputs)
    print(json.dumps(dict(state='complete',theta=theta,checks=len(checks))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
