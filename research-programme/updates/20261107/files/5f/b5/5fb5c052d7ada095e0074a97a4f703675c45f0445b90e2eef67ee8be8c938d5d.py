from stage151_integration_common import *
import ast


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'status.json').exists()
    assert not (ROOT/'runs').exists()
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    parent=chain[PARENT/'results/stage-integrity.json']
    for filename,sha in parent['file_hashes'].items():
        assert digest(PARENT/filename)==sha,filename
    inputs=[PARENT/'results/holdout-source/source.npz',PARENT/'results/preflight/frozen-inputs.npz']
    data=read_npz(inputs[0])
    bundle=EpochBundle(.9375)
    contexts=epoch_context(bundle)[0]
    theta=contexts[0]['theta']
    checks=[dict(name='Stage150 seal and immediate payloads intact',passed=True)]
    assert list(integration_nodes(theta,4))==list(stage150_parent.physical_nodes(theta,'expensive'))
    checks.append(dict(name='Order4 exactly reproduces inherited nodes and weights',passed=True))
    parent_tree=ast.parse((PARENT/'stage150_colder_common.py').read_text())
    current_tree=ast.parse((ROOT/'stage151_integration_common.py').read_text())
    for name in ['owned_loop','expensive_components']:
        original=next(node for node in parent_tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
        current=next(node for node in current_tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
        assert ast.dump(original)==ast.dump(current)
        checks.append(dict(name='Unchanged evaluator AST:'+name,passed=True))
    nodes={order:list(integration_nodes(theta,order)) for order in [3,4,5]}
    assert [len(nodes[order]) for order in [3,4,5]]==[756,1008,1260]
    third={event_signature(node):node['index'] for node in nodes[3]}
    shared={str(node['index']):third[event_signature(node)] for node in nodes[5] if event_signature(node) in third}
    assert len(shared)==252
    assert not set(map(event_signature,nodes[4]))&set(map(event_signature,nodes[3]+nodes[5]))
    assert len(set(map(event_signature,nodes[3]+nodes[5])))==1764
    checks.append(dict(name='252 exact unweighted shared nodes;1764 distinct new events',passed=True))
    profiles=read_npz(PARENT/'results/preflight/frozen-inputs.npz')
    assert np.array_equal(bundle.epochs[0].values,profiles['profiles'])
    assert np.array_equal(bundle.basis.mass,data['mass'])
    for route in ['local','cubic']:
        for phase,key in [(0.,'start'),(.5,'centre'),(.75,'actual'),(1.,'end')]:
            difference=central_source(data,phase,route)-data[key]
            test(checks,'Retained central interpolation anchor:'+route+':'+key,
                max(dual_norm(difference[1:-1],data['mass'])/dual_norm(data[key][1:-1],data['mass'])),1e-12)
        for model in ['heavy','cold']:
            for count in COUNTS:
                location=PARENT/'results/response'/f'{model}-{route}-{count}'
                assert verify_packet(location)['all_checks_passed']
                inputs.extend([location/'response.npz',location/'status.json'])
            for match in [20,40]:
                inputs.append(PARENT/'results/comparison'/f'{model}-m{match}-{route}-4096.npz')
    inputs.extend(bundle.inputs)
    for context in contexts:
        inputs.extend(Path(path) for path in context['inputs'])
    for path in set(inputs):
        inherited.inherited.verify_source(path,chain)
    np.savez_compressed(folder/'frozen-reference.npz',**data)
    finish(folder,dict(checks=checks,theta=theta,contexts=contexts,fraction=.9375,
        order5_shared_order3=shared,event_counts={'3':756,'4_reused':1008,'5_weighted':1260,'5_new':1008},
        new_unique_events=1764,reused_control_nodes=4608,orders=[3,4,5],
        denominator='unchanged Stage150 order4 full finite remainder',
        frozen_reference_sha256=digest(folder/'frozen-reference.npz'),
        source_component_sum_limit=.01,contraction_required=True,
        baseline_inner_history_refined=False),__file__,[*inputs,folder/'frozen-reference.npz'])
    assert all(row['passed'] for row in checks)
    print(json.dumps(dict(preflight=True,theta=theta,checks=len(checks),new_events=1764,shared_nodes=len(shared))),flush=True)


if __name__=='__main__':
    main()
