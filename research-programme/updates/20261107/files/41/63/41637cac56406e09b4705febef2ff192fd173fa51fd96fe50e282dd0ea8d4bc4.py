from stage161_common import *
import argparse,ast


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    if args.dry_run:
        print(json.dumps(dict(panel=[8.,20.],order=7,reference_order=6,weighted_events=756,
            expected_new_events=648,expected_shared_values=108,reference_events=648,
            retained_lower_orders=[8,7],response_steps=COUNTS,outputs_written=False)))
        return
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    paths=[PARENT/filename for filename in chain[PARENT/'results/stage-integrity.json']['file_hashes']]
    data_path=SOURCE159/'results/sources/source.npz'
    allowance_path=PARENT/'results/analysis/source-allowance.npz'
    data=read_npz(data_path)
    allowance=read_npz(allowance_path)
    assert np.array_equal(data['after_order8_full'],allowance['latest_sources'])
    paths.extend([data_path,allowance_path,SOURCE159/'results/preflight/status.json'])
    reference=ast.parse((SOURCE159/'stage159_common.py').read_text())
    current=ast.parse((ROOT/'stage161_common.py').read_text())
    for name in ['owned_loop','expensive_components']:
        assert ast.dump(next(node for node in reference.body if isinstance(node,ast.FunctionDef) and node.name==name))==ast.dump(next(node for node in current.body if isinstance(node,ast.FunctionDef) and node.name==name))
    checks=[dict(name='Inherited physical evaluator and virtual loop AST unchanged',passed=True)]
    new_rows,old_rows=[],[]
    contexts={}
    for site in SITES:
        bundle=EpochBundle(FRACTIONS[site])
        contexts[site]=epoch_context(bundle)[0]
        theta=contexts[site][0]['theta']
        assert contexts[site]==verify_packet(SOURCE159/'results/preflight')['contexts'][site]
        assert np.array_equal(bundle.basis.mass,data['mass'])
        paths.extend(bundle.inputs)
        configs={}
        for order in [5,6]:
            path=bank_folder(site,order)/'configuration.json'
            paths.append(path)
            configs[order]=json.loads(path.read_text())
            assert configs[order]['theta']==theta
        lookup={event_signature(node):node for node in integration_nodes(theta,5)}
        for index,node in enumerate(band_nodes(theta,7,5)):
            previous=lookup.get(event_signature(node))
            reused_path,original=None,None
            if previous is not None:
                reused_path,original,reused=node_path(site,5,previous,configs[5],theta)
                event=read_npz(reused_path)
                assert json.loads(str(event['identity']))==original
                paths.extend([reused_path,Path(str(event['loop_path']))])
            new_rows.append(dict(site=site,band=5,index=index,theta=theta,node=node,
                reused_path=str(reused_path) if reused_path else None,original_node=original))
        for node in band_nodes(theta,6,5):
            path,original,reused=node_path(site,6,node,configs[6],theta)
            old_rows.append(dict(site=site,band=5,index=node['index'],theta=theta,node=node,
                reused_path=str(path),original_node=original))
            event=read_npz(path)
            paths.extend([path,Path(str(event['loop_path']))])
    assert len(new_rows)==756 and len(old_rows)==648
    assert sum(bool(row['reused_path']) for row in new_rows)==108
    for site in SITES:
        selected=[row for row in new_rows if row['site']==site]
        assert len(selected)==252 and sum(bool(row['reused_path']) for row in selected)==36
    checks.append(dict(name='648 new events;108 shared midpoint values correctly reweighted;648 references',passed=True))
    for route in ['local','cubic']:
        for phase in [0.,.25,.5,.75,1.]:
            for site in SITES:
                expected=float(phase=={'cold':.75,'warm':.25,'centre':.5}[site])
                assert abs(site_basis(phase,route,site)-expected)<1e-14
    checks.append(dict(name='Lower-band source and fixed response bases retained',passed=True))
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                for owner in [SOURCE155,SOURCE158,SOURCE159]:
                    location=owner/'results/response'/f'{model}-{route}-{count}'
                    assert verify_packet(location)['all_checks_passed']
                    paths.extend([location/'response.npz',location/'status.json'])
                for match in [20,40]:
                    paths.append(SOURCE159/'results/comparison'/f'{model}-{route}-{count}-m{match}.npz')
    hashes=authenticate(paths,chain)
    np.savez_compressed(folder/'frozen-reference.npz',**data)
    np.savez_compressed(folder/'frozen-allowance.npz',**allowance)
    write_json(folder/'events.json',dict(new=new_rows,old=old_rows))
    finish(folder,dict(checks=checks,contexts=contexts,prior_hashes=hashes,
        new_events=648,reused_values=108,weighted_events=756,reference_events=648,
        order=7,reference_order=6,lower_bands_changed=False,temperature_curve_changed=False,
        frozen_sha256=digest(folder/'frozen-reference.npz'),
        allowance_sha256=digest(folder/'frozen-allowance.npz'),
        manifest_sha256=digest(folder/'events.json')),__file__,
        [*paths,folder/'events.json',folder/'frozen-reference.npz',folder/'frozen-allowance.npz'])
    print(json.dumps(dict(preflight=True,checks=len(checks),prior_files=len(hashes),new_events=648,reused_values=108)),flush=True)


if __name__=='__main__':
    main()
