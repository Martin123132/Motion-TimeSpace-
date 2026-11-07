from stage155_anchor_common import *
import ast


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'status.json').exists() and not (ROOT/'runs').exists()
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    for filename,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert digest(PARENT/filename)==sha
    checks=[dict(name='Stage154 complete immediate payloads verified',passed=True)]
    inputs=[PARENT/'results/anchor-sources/source.npz',PARENT/'results/anchor-sources/status.json',
        PARENT/'NUMERICAL-SUMMARY.json',PARENT/'results/preflight/status.json']
    arrays=read_npz(inputs[0])
    previous=verify_packet(PARENT/'results/preflight')
    reference=ast.parse((PARENT/'stage154_anchor_common.py').read_text())
    current=ast.parse((ROOT/'stage155_anchor_common.py').read_text())
    for name in ['owned_loop','expensive_components']:
        assert ast.dump(next(node for node in reference.body if isinstance(node,ast.FunctionDef) and node.name==name))==ast.dump(next(node for node in current.body if isinstance(node,ast.FunctionDef) and node.name==name))
        checks.append(dict(name='Identical physical evaluator AST:'+name,passed=True))
    contexts={}
    for anchor,fraction in ANCHORS.items():
        bundle=EpochBundle(fraction)
        contexts[anchor]=epoch_context(bundle)[0]
        assert contexts[anchor]==previous['contexts'][anchor]
        theta=contexts[anchor][0]['theta']
        rules={order:list(integration_nodes(theta,order)) for order in [4,5,6]}
        assert rules[4]==list(stage150_parent.physical_nodes(theta,'expensive'))
        assert [len(rules[order]) for order in [4,5,6]]==[1008,1260,1512]
        for order in [4,5]:
            assert not set(map(event_signature,rules[order]))&set(map(event_signature,rules[6]))
        assert np.array_equal(bundle.basis.mass,arrays['mass'])
        assert verify_packet(PARENT/'runs'/anchor)['nodes']==1260
        inputs.extend([PARENT/'runs'/anchor/'status.json',*bundle.inputs])
        for context in contexts[anchor]:
            inputs.extend(Path(path) for path in context['inputs'])
        checks.append(dict(name='Exact inherited context;1512 independent order6 nodes:'+anchor,passed=True))
    for route in ['local','cubic']:
        for anchor in ANCHORS:
            for phase in [0.,.25,.5,.75,1.]:
                expected=float(phase==(.25 if anchor=='warm' else .5))
                assert abs(response_basis(phase,route,anchor)-expected)<1e-14
            checks.append(dict(name='Fixed-cold cardinal sensitivity:'+route+':'+anchor,passed=True))
        for model in ['heavy','cold']:
            for count in COUNTS:
                location=PARENT/'results/response'/f'{model}-{route}-{count}'
                assert verify_packet(location)['all_checks_passed']
                inputs.extend([location/'status.json',location/'response.npz'])
            for match in [20,40]:
                inputs.append(PARENT/'results/comparison'/f'{model}-m{match}-{route}-4096.npz')
    for path in set(inputs):
        inherited.inherited.verify_source(path,chain)
    np.savez_compressed(folder/'frozen-reference.npz',**arrays)
    finish(folder,dict(checks=checks,contexts=contexts,anchors=ANCHORS,incoming_orders=[4,5,6],
        reused_order4_events=2016,reused_order5_events=2520,reused_control_events=9216,new_events=3024,
        frozen_sha256=digest(folder/'frozen-reference.npz'),curve_changed=False,
        scope='Matched incoming D/V/S finite-rule contraction and cancellation;not continuum certification',
        baseline_inner_history_refined=False),__file__,[*inputs,folder/'frozen-reference.npz'])
    assert all(row['passed'] for row in checks)
    print(json.dumps(dict(preflight=True,checks=len(checks),
        temperatures={name:context[0]['theta'] for name,context in contexts.items()},new_events=3024)),flush=True)


if __name__=='__main__':
    main()
