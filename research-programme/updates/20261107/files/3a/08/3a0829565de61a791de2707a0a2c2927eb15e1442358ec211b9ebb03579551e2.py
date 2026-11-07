from stage154_anchor_common import *
import argparse


def run(anchor,stop_at):
    folder=ROOT/'runs'/anchor
    if (folder/'COMPLETE').exists():
        assert verify_packet(folder)['all_checks_passed']
        return True
    proof=verify_packet(ROOT/'results/preflight')
    assert proof['all_checks_passed']
    frozen_path=ROOT/'results/preflight/frozen-reference.npz'
    assert digest(frozen_path)==proof['frozen_sha256']
    bundle=EpochBundle(ANCHORS[anchor])
    theta=epoch_context(bundle)[0][0]['theta']
    assert theta==proof['contexts'][anchor][0]['theta']
    model=FastSplit(bundle,'difference')
    nodes=list(integration_nodes(theta,5))
    config=dict(order=5,anchor=anchor,fraction=ANCHORS[anchor],theta=theta,node_count=len(nodes),modes=96,columns=COLUMN_NAMES,
        fingerprints={str(path):digest(path) for path in [Path(__file__),ROOT/'stage154_anchor_common.py',
            ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',ROOT/'results/preflight/status.json']})
    folder.mkdir(parents=True,exist_ok=True)
    if (folder/'configuration.json').exists():
        assert json.loads((folder/'configuration.json').read_text())==config
    else:
        write_json(folder/'configuration.json',config)
    totals={key:np.zeros((98,4)) for key in COMPONENTS}
    inputs=[folder/'configuration.json',ROOT/'results/preflight/status.json',frozen_path]
    started=time.monotonic()
    maximum_null=0.
    new_nodes=0
    for ordinal,node in enumerate(nodes):
        if datetime.now(timezone.utc)>=stop_at:
            write_json(folder/'progress.json',dict(state='paused_at_saved_node',completed_nodes=ordinal,total_nodes=len(nodes),pid=os.getpid()))
            return False
        path=event_path(anchor,node['index'])
        parameters,weight=parameters_and_weight(theta,node)
        if path.exists():
            saved=read_npz(path)
            assert json.loads(str(saved['identity']))==node and float(saved['weight'])==weight
        else:
            values,energy_null,scalar,loop_path=expensive_components(parameters,model)
            saved=dict(**values,event_energy_null=energy_null,loop_scalar=scalar,loop_path=str(loop_path),
                       identity=json.dumps(node,sort_keys=True),weight=weight)
            path.parent.mkdir(parents=True,exist_ok=True)
            temporary=path.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle,**saved)
            temporary.replace(path)
            new_nodes+=1
        for key in COMPONENTS:
            assert saved[key].shape==(98,4) and np.isfinite(saved[key]).all()
            totals[key]-=weight*saved[key]
        loop_path=Path(str(saved['loop_path']))
        assert loop_path.is_relative_to(ROOT/'virtual-cache')
        loop=json.loads(loop_path.read_text())
        assert loop['identity']==event_owner.inherited.virtual_identity(parameters)
        assert loop['scalar']==float(saved['loop_scalar']) and loop['finite']
        maximum_null=max(maximum_null,float(saved['event_energy_null']))
        inputs.extend([path,loop_path])
        elapsed=time.monotonic()-started
        progress=dict(state='running',order=5,anchor=anchor,completed_nodes=ordinal+1,total_nodes=len(nodes),pid=os.getpid(),
            elapsed_seconds=elapsed,new_nodes=new_nodes,updated_utc=datetime.now(timezone.utc).isoformat(),
            estimated_remaining_seconds=(len(nodes)-ordinal-1)*elapsed/max(new_nodes,1))
        write_json(folder/'progress.json',progress)
        if (ordinal+1)%max(1,len(nodes)//8)==0:
            print(json.dumps(progress),flush=True)
    np.savez(folder/'unique-source.npz',**totals)
    checks=[dict(name='Complete fixed-geometry unique event evaluations',passed=True)]
    test(checks,'Independent event photon gas exchange',maximum_null,1e-10)
    finish(folder,dict(checks=checks,order=5,anchor=anchor,nodes=len(nodes),shared_nodes=0,
        aggregate_scope='complete order5 single-temperature rule',
        elapsed_seconds=time.monotonic()-started),__file__,[*inputs,*bundle.inputs,folder/'unique-source.npz'])
    write_json(folder/'progress.json',dict(state='complete',order=5,anchor=anchor,completed_nodes=len(nodes),total_nodes=len(nodes),pid=os.getpid(),
        updated_utc=datetime.now(timezone.utc).isoformat()))
    return True


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--anchor',choices=sorted(ANCHORS),required=True)
    parser.add_argument('--stop-at',default='2026-10-18T01:45:00+00:00')
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    if args.dry_run:
        print(json.dumps(dict(order=5,anchor=args.anchor,weighted_nodes=1260,newly_evaluated_nodes=1260,outputs_written=False)))
    elif not run(args.anchor,datetime.fromisoformat(args.stop_at)):
        raise SystemExit(75)
