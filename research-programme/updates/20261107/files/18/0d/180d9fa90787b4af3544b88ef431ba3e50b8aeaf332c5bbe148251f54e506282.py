import ast
from late_frequency_common import *


def main():
    modest()
    folder=ROOT/'results/refinement-preflight'
    assert not (ROOT/'runs').exists()
    folder.mkdir(parents=True,exist_ok=False)
    ancestors=sealed_ancestors()
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for name,expected in parent['file_hashes'].items():
        assert digest(PARENT/name)==expected,name
    baseline_path=ANCHOR/'results/holdout-sources/source.npz'
    coarse_path=PARENT/'runs/expensive-late/source.npz'
    fine_path=ANCHOR/'runs/expensive-late/source.npz'
    control_path=ANCHOR/'runs/control-late/source.npz'
    old_comparison_path=PARENT/'results/frequency-sources/source.npz'
    baseline,coarse,fine,control,old_comparison=[dict(np.load(path)) for path in
        [baseline_path,coarse_path,fine_path,control_path,old_comparison_path]]
    assert digest(baseline_path)=='695037a1f7052d32d242457ab1b31b2a69becc544637c0ed77e0f2238eec8c3c'
    bundle=EpochBundle(.4375)
    contexts={'late':epoch_context(bundle)}
    theta=contexts['late'][0][0]['theta']
    assert theta==.0001678413900125661
    assert np.array_equal(bundle.basis.mass,baseline['mass'])
    inputs=[baseline_path,coarse_path,fine_path,control_path,old_comparison_path,*bundle.inputs]
    inputs.extend(Path(path) for context in contexts['late'] for model in context for path in model['inputs'])
    old_config=json.loads((coarse_path.parent/'configuration.json').read_text())
    assert old_config['temperature']==theta and old_config['epoch_fraction']==.4375
    for key,value in dict(radial=2,polar=2,azimuthal=4,hard_order=3,soft_angular=4,panel_order=18,seed_order=3).items():
        assert old_config[key]==value
    inputs.append(coarse_path.parent/'configuration.json')
    for key in ['difference','virtual','state']:
        assert np.array_equal(fine[key],baseline['late_'+key])
        assert np.array_equal(coarse[key],old_comparison['late_coarse_'+key])
        assert np.array_equal(fine[key]-coarse[key],old_comparison['late_delta_'+key])
    assert np.array_equal(control['control'],baseline['late_control'])
    assert np.array_equal(baseline['late_control']-baseline['late_sampled_leading'],baseline['late_kinematic_remainder'])
    electrons={}
    for order in [3,4,5]:
        current={}
        for node in population_nodes(theta,order,3,radial=2,polar=2,azimuthal=4):
            current[tuple(node['velocity'])]=node['electron_weight']
        electrons[order]=current
    assert len(electrons[5])==16 and electrons[3]==electrons[4]==electrons[5]
    new_nodes=list(physical_nodes(theta,'expensive'))
    assert len(new_nodes)==1260 and len({node['frequency'] for node in new_nodes})==35
    old_nodes={}
    for path in sorted((coarse_path.parent/'nodes').rglob('*.npz')):
        with np.load(path) as archive:
            identity=json.loads(str(archive['identity']))
            old_nodes[physical_key(identity)]=path
    assert len(old_nodes)==756
    reuse={}
    for node in new_nodes:
        parameters,weight=parameters_and_weight(theta,node)
        assert weight>0
        path=old_nodes.get(physical_key(node))
        if path is None:
            continue
        with np.load(path) as archive:
            identity=json.loads(str(archive['identity']))
            for key in ['electron_weight','hard_weight','reflection_multiplicity']:
                assert identity[key]==node[key]
            loop_path=Path(str(archive['loop_path']))
            loop=json.loads(loop_path.read_text())
            assert loop['identity']==inherited.virtual_identity(parameters)
            assert loop['finite'] and loop['scalar']==float(archive['loop_scalar'])
            for key in ['difference','virtual','state']:
                assert archive[key].shape==(98,4) and np.isfinite(archive[key]).all()
            reuse[str(node['index'])]=dict(path=str(path),sha256=digest(path),loop_path=str(loop_path),
                loop_sha256=digest(loop_path),old_weight=float(archive['weight']),new_weight=weight,
                physical_key=physical_key(node))
        inputs.extend([path,loop_path])
    old_tree=ast.parse((PARENT/'history_frequency_common.py').read_text())
    new_tree=ast.parse((ROOT/'late_frequency_common.py').read_text())
    old_functions={node.name:ast.dump(node,include_attributes=False) for node in old_tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef))}
    new_functions={node.name:ast.dump(node,include_attributes=False) for node in new_tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef))}
    unchanged=['EpochBundle','epoch_context','parameters_and_weight','expensive_components']
    assert all(old_functions[name]==new_functions[name] for name in unchanged)
    inputs.append(PARENT/'history_frequency_common.py')
    for path in dict.fromkeys(inputs):
        verify_reference(path,ancestors)
    plan_path=folder/'reuse-plan.json'
    write_json(plan_path,reuse)
    rejected=False
    try:
        list(physical_nodes(theta,'control'))
    except ValueError:
        rejected=True
    checks=[
        dict(name='Stage105 payloads unchanged before refinement',value=len(parent['file_hashes']),passed=True),
        dict(name='Baseline source and three saved components retain exact provenance',passed=True),
        dict(name='Control and sampled-leading difference reused exactly',passed=True),
        dict(name='Same actual late temperature,profiles,gas and96-mode basis',passed=True),
        dict(name='Electron/hard/inner rules unchanged;only incoming frequency order changes',passed=True),
        dict(name='35 incoming points and1260 positive weighted representatives',passed=True),
        dict(name='Exact physical event reuse and virtual identity verified',value=len(reuse),passed=True),
        dict(name='Physical source evaluation functions unchanged',functions=unchanged,passed=True),
        dict(name='All referenced inputs have sealed owners',passed=True),
        dict(name='Production route rejects control recomputation',passed=rejected)]
    finish(folder,dict(checks=checks,epoch_contexts=contexts,baseline_sha256=digest(baseline_path),
        previous_comparison_sha256=digest(old_comparison_path),reuse_plan_sha256=digest(plan_path),
        weighted_nodes=1260,reused_physical_nodes=len(reuse),new_physical_nodes=1260-len(reuse),
        source_component_sum_gate=.01,response_component_sum_gate=.01,contraction_gate=1.,
        prior_chain_entries=sum(len(packet['file_hashes']) for packet in ancestors.values()),
        central_seed4_unchanged=True,scope='Seed5 versus saved seed4 and seed3 at the one fixed late epoch.'),
        __file__,[*inputs,plan_path,ROOT/'DERIVATION.md'])
    print(json.dumps(dict(checks=len(checks),reused_nodes=len(reuse),new_nodes=1260-len(reuse),
        theta=theta,failed=[row['name'] for row in checks if not row['passed']])),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
