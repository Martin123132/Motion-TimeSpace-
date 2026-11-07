from stage150_colder_common import *
from repair_saved_sources import compensated_leading
import ast


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    assert not (ROOT/'runs').exists()
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    parent=chain[PARENT/'results/stage-integrity.json']
    for filename,sha in parent['file_hashes'].items():
        assert digest(PARENT/filename)==sha,filename
    assert verify_packet(PARENT/'results/readiness')['all_checks_passed']
    anchor_path=PARENT/'results/holdout-source/source.npz'
    anchors=read_npz(anchor_path)
    checks=[dict(name='Immediate Stage149 seal and payloads intact',passed=True)]
    inputs=[anchor_path,PARENT/'results/readiness/status.json']
    source_tree=ast.parse((PARENT/'stage149_holdout_common.py').read_text())
    target_tree=ast.parse((ROOT/'stage150_colder_common.py').read_text())
    for name in ['owned_loop','expensive_components']:
        original=next(node for node in source_tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
        current=next(node for node in target_tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
        assert ast.dump(original)==ast.dump(current)
        checks.append(dict(name='Unchanged physical evaluator AST:'+name,passed=True))
    bundle=EpochBundle(FRACTIONS['holdout'])
    models=epoch_context(bundle)[0]
    theta=models[0]['theta']
    background=thermal_wave.thermal.ThermalBackground('heavy')
    reference=background.at(.75*background.end)['thermal_parameter']
    test(checks,'Independent exponential temperature history',
        abs(theta/(reference*math.exp(-.1875*background.end))-1),1e-14)
    assert np.array_equal(bundle.basis.mass,anchors['mass'])
    arrays={key:anchors[key] for key in ['start','centre','end','curvature','mass','temperature','chemical']}
    arrays['warm_defect']=anchors['defect'].copy()
    arrays['prediction_local']=quadratic(anchors,PHASE)
    arrays['prediction_cubic']=arrays['prediction_local']-arrays['warm_defect']
    barycentric=-.125*anchors['start']+.75*anchors['centre']+.375*anchors['end']
    test(checks,'Independent colder-quarter interpolation identity',
        float(np.max(dual_norm((arrays['prediction_local']-barycentric)[1:-1],anchors['mass'])/
                     dual_norm(arrays['prediction_local'][1:-1],anchors['mass']))),1e-14)
    for route in ['local','cubic']:
        predicted=original_source(arrays,PHASE,route)
        assert np.array_equal(predicted,arrays['prediction_'+route])
        assert cold_bubble(PHASE,route)==1.
        assert all(cold_bubble(phase,route)==0. for phase in [0.,.25,.5,1.])
    checks.append(dict(name='Local and cubic numeric forecasts frozen; old anchors preserved',passed=True))
    leading_folder=folder/'holdout'
    leading_folder.mkdir()
    arrays['sampled_leading'],leading_metadata=compensated_leading(bundle.epochs[0],theta,leading_folder)
    arrays['raw_sampled_leading']=sampled_leading(bundle,theta)
    arrays['profiles']=bundle.epochs[0].values
    arrays['profile_frequency']=bundle.epochs[0].frequency
    arrays['gas']=np.asarray(bundle.gas)
    assert arrays['profiles'].shape==(24001,4)
    write_json(leading_folder/'leading-metadata.json',leading_metadata)
    inputs.extend([leading_folder/'leading-terms.npz',leading_folder/'leading-metadata.json',*bundle.inputs])
    for model in models:
        inputs.extend(Path(path) for path in model['inputs'])
    for part,expected in [('expensive',1008),('control',4608)]:
        assert len(list(physical_nodes(theta,part)))==expected
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                location=PARENT/'results/response'/f'{model}-{route}-{count}'
                assert verify_packet(location)['all_checks_passed']
                inputs.extend([location/'status.json',location/'response.npz'])
            for match in [20,40]:
                inputs.append(PARENT/'results/comparison'/f'{model}-m{match}-{route}-4096.npz')
    for path in set(inputs):
        if not path.is_relative_to(ROOT):
            inherited.inherited.verify_source(path,chain)
    checks.append(dict(name='Saved physical history,four profiles,baseline and fixed grid retained',passed=True))
    np.savez_compressed(folder/'frozen-inputs.npz',**arrays)
    finish(folder,dict(checks=checks,epoch_contexts={'holdout':models},fractions=FRACTIONS,
        phase=PHASE,source_interval=[.75,1.],column_order=COLUMN_NAMES,modes=96,
        frozen_inputs_sha256=digest(folder/'frozen-inputs.npz'),predictions_precede_production=True,
        primary_source_forecasts=['local','cubic'],source_forecast_gate=.01,response_steps=COUNTS,
        immediate_parent_payloads=len(parent['file_hashes']),baseline_inner_history_refined=False),
        __file__,[*inputs,folder/'frozen-inputs.npz'])
    assert all(row['passed'] for row in checks)
    print(json.dumps(dict(preflight='complete',checks=len(checks),theta=theta,
        phase=PHASE,fraction=FRACTIONS['holdout'])),flush=True)


if __name__=='__main__':
    main()
