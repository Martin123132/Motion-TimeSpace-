from stage159_common import *
import argparse,ast


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    if args.dry_run:
        print(json.dumps(dict(panel=[1.,3.],order=8,reference_order=7,
            new_events=864,reused_reference_events=756,other_band_order=7,
            response_steps=COUNTS,temperature_curve_changed=False,outputs_written=False)))
        return
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    paths=[PARENT/filename for filename in chain[PARENT/'results/stage-integrity.json']['file_hashes']]
    data_path=PARENT/'results/sources/source.npz'
    data=read_npz(data_path)
    original_manifest=json.loads((PARENT/'results/preflight/events.json').read_text())
    paths.extend([data_path,PARENT/'results/preflight/events.json',PARENT/'NUMERICAL-SUMMARY.json'])
    reference=ast.parse((PARENT/'stage158_common.py').read_text())
    current=ast.parse((ROOT/'stage159_common.py').read_text())
    for name in ['owned_loop','expensive_components']:
        assert ast.dump(next(node for node in reference.body if isinstance(node,ast.FunctionDef) and node.name==name))==ast.dump(next(node for node in current.body if isinstance(node,ast.FunctionDef) and node.name==name))
    checks=[dict(name='Identical inherited physical evaluator and virtual-loop AST',passed=True)]
    new_rows,old_rows=[],[]
    contexts={}
    for site in SITES:
        bundle=EpochBundle(FRACTIONS[site])
        contexts[site]=epoch_context(bundle)[0]
        theta=contexts[site][0]['theta']
        prior=verify_packet(PARENT/'results/preflight')
        assert contexts[site]==prior['contexts'][site]
        assert np.array_equal(bundle.basis.mass,data['mass'])
        paths.extend(bundle.inputs)
        old_selected=[row for row in original_manifest['new'] if row['band']==3 and row['site']==site]
        assert len(old_selected)==252
        for old in old_selected:
            path=Path(old['reused_path']) if old['reused_path'] else parent158.event_path(old)
            row=dict(old,reused_path=str(path),original_node=old['original_node'] if old['reused_path'] else old['node'])
            old_rows.append(row)
            event=read_npz(path)
            paths.extend([path,Path(str(event['loop_path']))])
        nodes=band_nodes(theta,8,3)
        assert len(nodes)==288
        assert not set(map(event_signature,nodes)) & set(event_signature(row['node']) for row in old_selected)
        for index,node in enumerate(nodes):
            new_rows.append(dict(site=site,band=3,index=index,theta=theta,node=node,
                reused_path=None,original_node=None))
    assert len(new_rows)==864 and len(old_rows)==756
    checks.append(dict(name='864 new order8 events;756 authenticated order7 references;3–8 retained',passed=True))
    for route in ['local','cubic']:
        for phase in [0.,.25,.5,.75,1.]:
            for site in SITES:
                expected=float(phase=={'cold':.75,'warm':.25,'centre':.5}[site])
                assert abs(site_basis(phase,route,site)-expected)<1e-14
    checks.append(dict(name='Unchanged cardinal temperature-response bases',passed=True))
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                for stage in [PARENT,SOURCE155]:
                    location=stage/'results/response'/f'{model}-{route}-{count}'
                    assert verify_packet(location)['all_checks_passed']
                    paths.extend([location/'response.npz',location/'status.json'])
                for match in [20,40]:
                    paths.append(PARENT/'results/comparison'/f'{model}-{route}-{count}-m{match}-band4.npz')
    hashes=authenticate(paths,chain)
    np.savez_compressed(folder/'frozen-reference.npz',**data)
    write_json(folder/'events.json',dict(new=new_rows,old=old_rows))
    finish(folder,dict(checks=checks,contexts=contexts,prior_hashes=hashes,
        new_events=864,reused_reference_events=756,order=8,reference_order=7,
        fixed_band38_order=7,other_panel_order=6,temperature_curve_changed=False,
        frozen_sha256=digest(folder/'frozen-reference.npz'),
        manifest_sha256=digest(folder/'events.json')),__file__,
        [*paths,folder/'events.json',folder/'frozen-reference.npz'])
    print(json.dumps(dict(preflight=True,checks=len(checks),prior_files=len(hashes),new_events=864)),flush=True)


if __name__=='__main__':
    main()

