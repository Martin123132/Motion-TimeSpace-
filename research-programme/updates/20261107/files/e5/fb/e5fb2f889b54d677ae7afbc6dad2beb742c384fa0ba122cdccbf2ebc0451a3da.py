from stage154_anchor_common import *
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
    checks=[dict(name='Stage153 immediate payloads verified',passed=True)]
    inputs=[SOURCE152/'results/integration-source/source.npz',
        STAGE149/'results/holdout-source/source.npz',STAGE148/'results/terminal-sources/source.npz',
        STAGE149/'results/preflight/frozen-inputs.npz',STAGE148/'results/preflight/frozen-inputs.npz',
        PARENT/'FINAL-SUMMARY.json']
    arrays=read_npz(inputs[0])
    sources={'warm':read_npz(inputs[1]),'centre':read_npz(inputs[2])}
    profiles={'warm':read_npz(inputs[3]),'centre':read_npz(inputs[4])}
    reference=ast.parse((SOURCE152/'stage152_order6_common.py').read_text())
    current=ast.parse((ROOT/'stage154_anchor_common.py').read_text())
    for name in ['owned_loop','expensive_components']:
        assert ast.dump(next(node for node in reference.body if isinstance(node,ast.FunctionDef) and node.name==name))==ast.dump(next(node for node in current.body if isinstance(node,ast.FunctionDef) and node.name==name))
        checks.append(dict(name='Identical physical evaluator AST:'+name,passed=True))
    contexts={}
    for anchor,fraction in ANCHORS.items():
        bundle=EpochBundle(fraction)
        contexts[anchor]=epoch_context(bundle)[0]
        theta=contexts[anchor][0]['theta']
        old_nodes=list(integration_nodes(theta,4))
        new_nodes=list(integration_nodes(theta,5))
        assert old_nodes==list(stage150_parent.physical_nodes(theta,'expensive'))
        assert len(old_nodes)==1008 and len(new_nodes)==1260
        assert not set(map(event_signature,old_nodes))&set(map(event_signature,new_nodes))
        prefix='actual' if anchor=='warm' else 'centre'
        profile_prefix='' if anchor=='warm' else 'centre_'
        assert np.array_equal(bundle.epochs[0].values,profiles[anchor][profile_prefix+'profiles'])
        assert np.array_equal(bundle.basis.mass,arrays['mass'])
        arrays[anchor+'_source4']=sources[anchor][prefix]
        for name in ['control','sampled_leading',*COMPONENTS]:
            arrays[anchor+'_'+name]=sources[anchor][prefix+'_'+name]
        if anchor=='centre':
            assert np.array_equal(arrays['centre_source4'],arrays['centre'])
        else:
            assert np.array_equal(arrays['warm_source4'],sources['warm']['actual'])
        inputs.extend(bundle.inputs)
        for context in contexts[anchor]:
            inputs.extend(Path(path) for path in context['inputs'])
        checks.append(dict(name='Exact original profiles and order4 rule;1260new nodes:'+anchor,passed=True))
    for route in ['local','cubic']:
        for anchor in ANCHORS:
            for phase in [0.,.25,.5,.75,1.]:
                expected=float(phase==(.25 if anchor=='warm' else .5))
                assert abs(response_basis(phase,route,anchor)-expected)<1e-14
            checks.append(dict(name='Fixed-cold cardinal sensitivity:'+route+':'+anchor,passed=True))
        for model in ['heavy','cold']:
            for count in COUNTS:
                location=SOURCE152/'results/response'/f'{model}-{route}-order6-{count}'
                assert verify_packet(location)['all_checks_passed']
                inputs.extend([location/'status.json',location/'response.npz'])
            for match in [20,40]:
                inputs.append(SOURCE152/'results/comparison'/f'{model}-m{match}-{route}-order6-4096.npz')
    for path in set(inputs):
        inherited.inherited.verify_source(path,chain)
    np.savez_compressed(folder/'frozen-reference.npz',**arrays)
    finish(folder,dict(checks=checks,contexts=contexts,anchors=ANCHORS,incoming_orders=[4,5],
        reused_order4_events=2016,reused_control_events=9216,new_events=2520,
        frozen_sha256=digest(folder/'frozen-reference.npz'),curve_changed=False,
        scope='Incoming D/V/S finite-rule sensitivity,not certified continuum accuracy',
        baseline_inner_history_refined=False),__file__,[*inputs,folder/'frozen-reference.npz'])
    assert all(row['passed'] for row in checks)
    print(json.dumps(dict(preflight=True,checks=len(checks),
        temperatures={name:context[0]['theta'] for name,context in contexts.items()},new_events=2520)),flush=True)


if __name__=='__main__':
    main()
