from colder_common import *


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    assert not (ROOT/'runs').exists()
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    for filename,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert digest(PARENT/filename)==sha,filename
    anchor_path=ANCHORS/'results/adjacent-sources/source.npz'
    warm_path=PARENT/'results/holdout-source/source.npz'
    warm_prediction_path=PARENT/'results/preflight/frozen-prediction.npz'
    start_path=parent.MID/'source.npz'
    anchors,warm,warm_prediction,start=map(read_npz,[anchor_path,warm_path,warm_prediction_path,start_path])
    arrays,checks={},[]
    for key in COMPONENTS:
        quad=-.125*start[key]+.75*anchors['centre_'+key]+.375*anchors['end_'+key]
        warm_defect=warm[key]-warm_prediction['predicted_'+key]
        arrays['local_'+key]=quad
        arrays['cubic_'+key]=quad-warm_defect
    for kind in ['local','cubic']:
        arrays['prediction_'+kind]=forecast(anchors,warm['defect'],PHASE,kind)
        test(checks,'Independent component Lagrange forecast:'+kind,
             np.max(abs(arrays['prediction_'+kind]-arrays[kind+'_remainder']))/
             np.max(abs(arrays['prediction_'+kind])),1e-12)
        assert cold_bubble(.75,kind)==1
        assert all(cold_bubble(node,kind)==0 for node in [0,.25,.5,1])
    arrays['warm_defect']=warm['defect']
    prediction_path=folder/'frozen-prediction.npz'
    np.savez_compressed(prediction_path,**arrays,mass=anchors['mass'],
                        temperature=anchors['temperature'],chemical=anchors['chemical'],
                        fraction=.6875,phase=.75,quadratic_weights=[-.125,.75,.375])
    lock_path=folder/'prediction-lock.json'
    write_json(lock_path,dict(frozen_utc=datetime.now(timezone.utc).isoformat(),
        fraction=.6875,source_gate=.01,predictions=['local','cubic'],
        error_extensions=['piecewise_quadratic','five_node_quartic'],event_nodes_started=False,
        prediction_sha256=digest(prediction_path),warm_source_sha256=digest(warm_path),
        anchor_source_sha256=digest(anchor_path),method_sha256=digest(ROOT/'DERIVATION.md'),
        common_sha256=digest(ROOT/'colder_common.py')))
    bundle=EpochBundle(.6875)
    models=epoch_context(bundle)[0]
    theta=models[0]['theta']
    background=thermal_wave.thermal.ThermalBackground('heavy')
    reference=background.at(.5*background.end)['thermal_parameter']*math.exp(-.1875*background.end)
    test(checks,'Independent exponential source temperature',abs(theta/reference-1),1e-14)
    assert np.array_equal(bundle.basis.mass,anchors['mass'])
    sampled=sampled_leading(bundle,theta)
    np.savez_compressed(folder/'frozen-inputs.npz',colder_sampled_leading=sampled,
        profiles=bundle.epochs[0].values,frequency=bundle.epochs[0].frequency,gas=np.array(bundle.gas))
    inputs=[anchor_path,warm_path,warm_prediction_path,start_path,prediction_path,lock_path,
            folder/'frozen-inputs.npz',*bundle.inputs]
    inputs.extend(Path(path) for model in models for path in model['inputs'])
    for path in inputs:
        if not path.is_relative_to(ROOT):
            inherited.inherited.verify_source(path,chain)
    checks.append(dict(name='Finite complete photon gas histories at withheld colder temperature',
                       passed=bool(sampled.shape==(98,4) and np.isfinite(sampled).all())))
    finish(folder,dict(checks=checks,epoch_contexts={'colder':models},fractions=FRACTIONS,
        column_order=COLUMN_NAMES,frozen_inputs_sha256=digest(folder/'frozen-inputs.npz'),
        prediction_sha256=digest(prediction_path),source_forecast_gate=.01,
        both_predictions_frozen_before_new_events=True,baseline_reused_not_zero=True),
        __file__,inputs)
    print(json.dumps(dict(state='complete',theta=theta,checks=len(checks))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
