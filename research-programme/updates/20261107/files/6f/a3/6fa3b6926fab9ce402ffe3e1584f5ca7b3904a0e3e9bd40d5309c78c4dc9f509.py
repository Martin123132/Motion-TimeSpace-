from stage158_common import *
import argparse,ast


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    if args.dry_run:
        print(json.dumps(dict(bands=[list(value) for value in BANDS.values()],new_order=7,reference_order=6,
            weighted_events=1512,expected_new_events=1296,expected_shared_values=216,
            unchanged_frequency_modes=96,response_steps=COUNTS,outputs_written=False)))
        return
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    paths=[PARENT/filename for filename in chain[PARENT/'results/stage-integrity.json']['file_hashes']]
    data_path=SOURCE155/'results/anchor-sources/source.npz'
    data=read_npz(data_path)
    paths.append(data_path)
    reference=ast.parse((SOURCE155/'stage155_anchor_common.py').read_text())
    current=ast.parse((ROOT/'stage158_common.py').read_text())
    for name in ['owned_loop','expensive_components']:
        assert ast.dump(next(node for node in reference.body if isinstance(node,ast.FunctionDef) and node.name==name))==ast.dump(next(node for node in current.body if isinstance(node,ast.FunctionDef) and node.name==name))
    checks=[dict(name='Identical inherited physical evaluator and loop AST',passed=True)]
    manifest=[]
    contexts={}
    old_rows=[]
    for site in SITES:
        bundle=EpochBundle(FRACTIONS[site])
        contexts[site]=epoch_context(bundle)[0]
        theta=contexts[site][0]['theta']
        config6=json.loads((parent157.bank_folder(site,6)/'configuration.json').read_text())
        assert theta==config6['theta']
        assert np.array_equal(bundle.basis.mass,data['mass'])
        paths.extend(bundle.inputs)
        paths.append(parent157.bank_folder(site,6)/'configuration.json')
        config5=json.loads((parent157.bank_folder(site,5)/'configuration.json').read_text())
        paths.append(parent157.bank_folder(site,5)/'configuration.json')
        lookup={event_signature(node):node for node in integration_nodes(theta,5)}
        for band in BANDS:
            for index,node in enumerate(band_nodes(theta,7,band)):
                previous=lookup.get(event_signature(node))
                reused_path,original=None,None
                if previous is not None:
                    reused_path,original,reused=parent157.node_path(site,5,previous,config5,theta)
                    event=read_npz(reused_path)
                    assert json.loads(str(event['identity']))==original
                    paths.extend([reused_path,Path(str(event['loop_path']))])
                manifest.append(dict(site=site,band=band,index=index,theta=theta,node=node,
                    reused_path=str(reused_path) if reused_path else None,original_node=original))
            for node in band_nodes(theta,6,band):
                path,original,reused=parent157.node_path(site,6,node,config6,theta)
                old_rows.append(dict(site=site,band=band,index=node['index'],theta=theta,node=node,
                    reused_path=str(path),original_node=original))
                event=read_npz(path)
                paths.extend([path,Path(str(event['loop_path']))])
    assert len(manifest)==1512 and sum(bool(row['reused_path']) for row in manifest)==216
    assert len(old_rows)==1296
    for site in SITES:
        for band in BANDS:
            selected=[row for row in manifest if row['site']==site and row['band']==band]
            assert len(selected)==252 and sum(bool(row['reused_path']) for row in selected)==36
    checks.append(dict(name='Shared order5 centres use order7 weights;other order7 nodes independent',passed=True))
    for route in ['local','cubic']:
        for phase in [0.,.25,.5,.75,1.]:
            for site in SITES:
                expected=float(phase=={'cold':.75,'warm':.25,'centre':.5}[site])
                assert abs(site_basis(phase,route,site)-expected)<1e-14
    checks.append(dict(name='Unchanged cardinal response bases at all anchors/endpoints',passed=True))
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                location=source155.ROOT/'results/response'/f'{model}-{route}-{count}'
                assert verify_packet(location)['all_checks_passed']
                paths.extend([location/'response.npz',location/'status.json'])
                for match in [20,40]:
                    paths.append(SOURCE155/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz')
    hashes=authenticate(paths,chain)
    np.savez_compressed(folder/'frozen-reference.npz',**data)
    write_json(folder/'events.json',dict(new=manifest,old=old_rows))
    finish(folder,dict(checks=checks,contexts=contexts,prior_hashes=hashes,
        new_events=1296,reused_values=216,weighted_events=1512,
        bands={str(key):value for key,value in BANDS.items()},order=7,reference_order=6,
        frozen_sha256=digest(folder/'frozen-reference.npz'),manifest_sha256=digest(folder/'events.json'),
        temperature_curve_changed=False,other_axes_changed=False),__file__,
        [*paths,folder/'events.json',folder/'frozen-reference.npz'])
    print(json.dumps(dict(preflight=True,checks=len(checks),prior_files=len(hashes),new_events=1296,reused_values=216)),flush=True)


if __name__=='__main__':
    main()

