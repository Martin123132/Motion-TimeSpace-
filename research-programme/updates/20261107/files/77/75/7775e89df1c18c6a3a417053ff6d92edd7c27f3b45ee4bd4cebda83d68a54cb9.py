from stage152_order6_common import *
import ast


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'status.json').exists() and not (ROOT/'runs').exists()
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    parent=chain[PARENT/'results/stage-integrity.json']
    for filename,sha in parent['file_hashes'].items():
        assert digest(PARENT/filename)==sha,filename
    inputs=[PARENT/'results/integration-source/source.npz',PARENT/'results/preflight/frozen-reference.npz']
    data=read_npz(inputs[0])
    bundle=EpochBundle(.9375)
    contexts=epoch_context(bundle)[0]
    theta=contexts[0]['theta']
    checks=[dict(name='Stage151 seal and immediate payloads intact',passed=True)]
    assert theta==verify_packet(PARENT/'results/preflight')['theta']
    parent_tree=ast.parse((PARENT/'stage151_integration_common.py').read_text())
    current_tree=ast.parse((ROOT/'stage152_order6_common.py').read_text())
    for name in ['owned_loop','expensive_components']:
        original=next(node for node in parent_tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
        current=next(node for node in current_tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
        assert ast.dump(original)==ast.dump(current)
        checks.append(dict(name='Unchanged physical evaluator AST:'+name,passed=True))
    old={order:list(integration_nodes(theta,order)) for order in [3,4,5]}
    nodes=list(integration_nodes(theta,6))
    assert len(nodes)==1512 and len({event_signature(node) for node in nodes})==1512
    previous={event_signature(node) for group in old.values() for node in group}
    assert not previous&{event_signature(node) for node in nodes}
    assert len([node for node in nodes if node['index']%2==0])==756
    assert len([node for node in nodes if node['index']%2==1])==756
    checks.append(dict(name='1512new exact abscissae;two disjoint756node shards',passed=True))
    assert np.array_equal(bundle.basis.mass,data['mass'])
    for route in ['local','cubic']:
        for phase,key in [(0.,'start'),(.5,'centre'),(.75,'source5'),(1.,'end')]:
            difference=central_source(data,phase,route)-data[key]
            test(checks,'Order5 central anchor replay:'+route+':'+key,
                max(dual_norm(difference[1:-1],data['mass'])/dual_norm(data[key][1:-1],data['mass'])),1e-12)
        for model in ['heavy','cold']:
            for count in COUNTS:
                location=PARENT/'results/response'/f'{model}-{route}-order5-{count}'
                assert verify_packet(location)['all_checks_passed']
                inputs.extend([location/'status.json',location/'response.npz'])
            for match in [20,40]:
                inputs.append(PARENT/'results/comparison'/f'{model}-m{match}-{route}-order5-4096.npz')
    inputs.extend(bundle.inputs)
    for context in contexts:
        inputs.extend(Path(path) for path in context['inputs'])
    for path in set(inputs):
        inherited.inherited.verify_source(path,chain)
    np.savez_compressed(folder/'frozen-reference.npz',**data)
    finish(folder,dict(checks=checks,theta=theta,contexts=contexts,fraction=.9375,
        new_unique_events=1512,parts=2,nodes_per_part=756,reused_control_nodes=4608,
        reused_orders=[3,4,5],new_order=6,
        denominator='unchanged Stage150 order4 full finite remainder and accumulated correction',
        frozen_reference_sha256=digest(folder/'frozen-reference.npz'),
        source_component_sum_limit=.01,contraction_required=True,baseline_inner_history_refined=False),
        __file__,[*inputs,folder/'frozen-reference.npz'])
    assert all(row['passed'] for row in checks)
    print(json.dumps(dict(preflight=True,theta=theta,checks=len(checks),new_events=1512)),flush=True)


if __name__=='__main__':
    main()
