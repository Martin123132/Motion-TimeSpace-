from stage162_common import *
import argparse,ast


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    if args.dry_run:
        print(json.dumps(dict(endpoint_fractions=ENDPOINTS,orders=[4,5,6],
            reused_reference_events=2016,new_events=5544,maximum_workers=2,
            interior_orders=[6,6,6,8,7,7,6],curve_refit=False,outputs_written=False)))
        return
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    paths=[PARENT/filename for filename in chain[PARENT/'results/stage-integrity.json']['file_hashes']]
    data_path=PARENT/'results/sources/source.npz'
    data=read_npz(data_path)
    paths.append(data_path)
    checks=[]
    reference=ast.parse((PARENT/'stage161_common.py').read_text())
    current=ast.parse((ROOT/'stage162_common.py').read_text())
    for name in ['owned_loop','expensive_components']:
        assert ast.dump(next(node for node in reference.body if isinstance(node,ast.FunctionDef) and node.name==name))==ast.dump(
            next(node for node in current.body if isinstance(node,ast.FunctionDef) and node.name==name))
        checks.append(dict(name='Physical evaluator AST unchanged:'+name,passed=True))
    contexts,reference_rows={},[]
    for endpoint,fraction in ENDPOINTS.items():
        bundle=EpochBundle(fraction)
        contexts[endpoint]=epoch_context(bundle)[0]
        theta=contexts[endpoint][0]['theta']
        assert np.array_equal(bundle.basis.mass,data['mass'])
        saved=read_npz(OLD_SOURCES[endpoint])
        assert np.array_equal(endpoint_full(saved,endpoint),data[endpoint])
        paths.extend([OLD_SOURCES[endpoint],*bundle.inputs])
        for item in contexts[endpoint]:
            paths.extend(Path(path) for path in item['inputs'])
        np.savez_compressed(folder/(endpoint+'-reference.npz'),**saved)
        assert list(integration_nodes(theta,4))==list(physical_nodes(theta,'expensive'))
        for node in integration_nodes(theta,4):
            event,weight,path,loop_path=load_node162(endpoint,4,node,theta)
            paths.extend([path,loop_path])
            reference_rows.append(dict(endpoint=endpoint,index=node['index'],path=str(path),loop_path=str(loop_path)))
        signatures=set(event_signature(node) for node in integration_nodes(theta,4))
        for order in [5,6]:
            nodes=list(integration_nodes(theta,order))
            assert len(nodes)==252*order
            assert not signatures.intersection(event_signature(node) for node in nodes)
            signatures.update(event_signature(node) for node in nodes)
        checks.append(dict(name='Exact endpoint owner/history and complete saved order4:'+endpoint,passed=True))
    for route in ['local','cubic']:
        for endpoint in ENDPOINTS:
            for phase in [0.,.25,.5,.75,1.]:
                expected=float(phase==(0 if endpoint=='start' else 1))
                assert abs(endpoint_response_basis(phase,route,endpoint)-expected)<1e-14
        checks.append(dict(name='Endpoint response cardinal identities:'+route,passed=True))
    assert endpoint_basis(.75,'cubic','start')==.25
    assert endpoint_basis(.75,'cubic','end')==.25
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                for match in [20,40]:
                    paths.append(PARENT/'results/comparison'/f'{model}-{route}-{count}-m{match}.npz')
    hashes=authenticate(paths,chain)
    np.savez_compressed(folder/'frozen-reference.npz',**data)
    finish(folder,dict(checks=checks,contexts=contexts,prior_hashes=hashes,
        endpoint_fractions=ENDPOINTS,new_events=5544,reused_reference_events=len(reference_rows),
        orders=[4,5,6],interior_orders=[6,6,6,8,7,7,6],temperature_curve_changed=False,
        frozen_sha256=digest(folder/'frozen-reference.npz')),__file__,
        [*paths,folder/'frozen-reference.npz',folder/'start-reference.npz',folder/'end-reference.npz'])
    print(json.dumps(dict(preflight='complete',checks=len(checks),prior_files=len(hashes),contexts=contexts)),flush=True)


if __name__=='__main__':
    main()
