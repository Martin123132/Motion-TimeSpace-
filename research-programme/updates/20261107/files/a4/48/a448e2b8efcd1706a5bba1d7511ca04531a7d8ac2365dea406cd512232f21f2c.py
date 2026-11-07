from withheld_source_common import *


def main():
    modest()
    folder=ROOT/'results/frozen-prediction'
    assert not (ROOT/'runs').exists()
    folder.mkdir(parents=True,exist_ok=False)
    ancestors=sealed_ancestors()
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for name,expected in parent['file_hashes'].items():
        assert digest(PARENT/name)==expected,name
    anchor_path=PARENT/'results/anchor-source/source.npz'
    anchor=dict(np.load(anchor_path))
    matched=dict(np.load(MID/'source.npz'))
    bundle=EpochBundle()
    contexts=epoch_context(bundle)
    withheld=contexts[0][0]['theta']
    background=thermal_wave.thermal.ThermalBackground('heavy')
    lower,upper=.25*background.end,.5*background.end
    weight=(bundle.coordinate-lower)/(upper-lower)
    assert abs(weight-.5)<1e-14
    quarter_theta=background.at(lower)['thermal_parameter']
    midpoint_theta=background.at(upper)['thermal_parameter']
    inputs=[anchor_path,anchor_path.parent/'status.json',MID/'source.npz',*bundle.inputs]
    for models in contexts:
        for model in models:
            inputs.extend(Path(path) for path in model['inputs'])
    for path in inputs:
        verify_reference(path,ancestors)
    assert np.array_equal(bundle.basis.mass,anchor['mass'])
    assert np.array_equal(bundle.basis.temperature,anchor['temperature'])
    keys=['control','sampled_leading','kinematic_remainder','difference','virtual','state','remainder']
    values={key:(1-weight)*anchor[key][:,:4]+weight*matched[key] for key in keys}
    assert np.array_equal(matched['remainder'],anchor['midpoint'])
    expected=(1-weight)*anchor['quarter']+weight*anchor['midpoint']
    assert np.array_equal(expected,values['remainder'])
    component_error=dual_norm((sum(values[key] for key in ['kinematic_remainder','difference','virtual','state'])-expected)[1:-1],anchor['mass'])
    scale=np.maximum(dual_norm(expected[1:-1],anchor['mass']),1e-300)
    checks=[
        dict(name='Stage102 payloads and sealed source/profile ownership',value=len(parent['file_hashes']),passed=True),
        dict(name='Prediction made before withheld production directory exists',passed=True),
        dict(name='Same pilot source anchors and 96-mode mass matrix',passed=True),
        dict(name='Log-expansion source secant weight equals one half',value=weight,passed=abs(weight-.5)<1e-14),
        dict(name='Withheld temperature is geometric mean,not arithmetic mean',value=withheld,passed=abs(withheld/math.sqrt(quarter_theta*midpoint_theta)-1)<1e-14),
        dict(name='Component prediction sums to total remainder',value=float(np.max(component_error/scale)),passed=bool(np.max(component_error/scale)<1e-12)),
        dict(name='Expected production counts frozen',passed=all(sum(1 for node in physical_nodes(withheld,part))==count for part,count in [('expensive',1008),('control',4608)]))
    ]
    np.savez(folder/'prediction.npz',**values,quarter=anchor['quarter'],midpoint=anchor['midpoint'],
        mass=anchor['mass'],temperature=anchor['temperature'],chemical=anchor['chemical'],weight=weight)
    sampled=sampled_leading(bundle,withheld)
    assert sampled.shape==(98,4) and np.isfinite(sampled).all()
    np.savez(folder/'sampled-leading.npz',withheld=sampled)
    finish(folder,dict(checks=checks,epoch_fraction=FRACTION,withheld_theta=withheld,
        quarter_theta=quarter_theta,midpoint_theta=midpoint_theta,epoch_contexts=contexts,
        predicted_before_production_utc=datetime.now(timezone.utc).isoformat(),
        source_relative_gate=.01,response_relative_gate=.01,prior_chain_entries=sum(len(packet['file_hashes']) for packet in ancestors.values()),
        source_formula='(R(.25)+R(.5))/2 at .375 in log-expansion;no fitted exponent.',
        independent_withheld_source_evaluated=False,quarter_precision_gate_closed=False,
        source_interpolation_error_bounded=False,new_parent_history=False),__file__,[*inputs,ROOT/'DERIVATION.md'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
        withheld_theta=withheld,prediction_sha256=digest(folder/'prediction.npz'))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()

